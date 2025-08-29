from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.keyboard.keyboard_buttons import main_keyboard, record_keyboard
from app.database import connection
from app.game.dao import UserDAO
from app.game.schemas import TelegramIDModel, UserModel

router = Router()


@router.message(CommandStart())
@connection()
async def cmd_start(message: Message, session: AsyncSession, **kwargs):
    welcome_text = (
        """
 🎮 2048 o‘yiniga xush kelibsiz! 🧩
 
 Bu yerda siz qiziqarli boshqotirmadan bahramand bo‘lib, o‘zingizni sinab ko‘rishingiz mumkin. Sizni quyidagilar kutmoqda:
 
 🔢 2048 o‘ynang va g‘alabaga intiling!  
 🏆 O‘z joriy rekordingizni kuzating va yangi cho‘qqilarga intiling  
 👥 Boshqa o‘yinchilarning rekordlarini bilib oling va eng yaxshisi bo‘lish uchun bellashing!  
 
 Boshlashga tayyormisiz? Eng zo‘r bo‘ling va 2048 plitkasiga erishing! 🚀
        """
    )

    try:
        user_id = message.from_user.id
        user_info = await UserDAO.find_one_or_none(session=session, filters=TelegramIDModel(telegram_id=user_id))

        if not user_info:
            values = UserModel(
                telegram_id=user_id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
                best_score=0
            )
            await UserDAO.add(session=session, values=values)

        await message.answer(welcome_text, reply_markup=main_keyboard())

    except Exception as e:
        await message.answer("Произошла ошибка при обработке вашего запроса. Пожалуйста, попробуйте снова позже.")


@router.callback_query(F.data == "show_my_record")
@connection
async def get_user_record(callback: CallbackQuery, session: AsyncSession, **kwargs):
    await callback.answer()
    await callback.message.delete()
    record_info = await UserDAO.get_user_rank(session, telegram_id=callback.from_user.id)
    rank = record_info['rank']
    best_score = record_info['best_score']
    if rank == 1:
        text = (
            f"🥇 Tabriklaymiz! Siz {best_score} ochko bilan birinchi o‘rindasiz! Siz — chempionsiz!\n\n"
            "Darajangizni saqlab qoling va unvoningizni himoya qiling. Quyidagi tugmani bosing va "
            "natijangizni yanada yaxshilashga harakat qiling!"
        )
    elif rank == 2:
        text = (
            f"🥈 Ajoyib! Siz {best_score} ochko bilan ikkinchi o‘rinda turibsiz!\n\n"
            "Yana biroz harakat qilsangiz — cho‘qqi sizniki bo‘ladi! Birinchi bo‘lish uchun quyidagi tugmani bosing!"
        )
    elif rank == 3:
        text = (
            f"🥉 Zo‘r natija! Siz {best_score} ochko bilan uchinchi o‘rindasiz!\n\n"
            "Cho‘qqiga juda yaqin! Quyidagi tugmani bosib, o‘zingizni sinab ko‘ring va oltin o‘rinni egallang!"
        )
    else:
        text = (
            f"📊 Sizning rekordingiz: {best_score} ochko. Siz umumiy reytingda {rank}-o‘rindasiz.\n\n"
            "Har safar siz yanada kuchliroq bo‘lyapsiz! Quyidagi tugmani bosing va "
            "o‘zingizni sinab, yanada yuqoriga ko‘tariling hamda rekordni yangilang!"
        )

    await callback.message.answer(text, reply_markup=record_keyboard())
