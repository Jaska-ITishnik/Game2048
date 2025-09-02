from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.i18n import gettext as _
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.keyboard.keyboard_buttons import main_keyboard, record_keyboard, change_lang_buttons
from app.database import connection, async_session_maker
from app.game.dao import UserDAO
from app.game.schemas import TelegramIDModel, UserModel

router = Router()


async def welcome_message(message: Message, state: FSMContext, markup):
    data = await state.get_data()
    lang = data.get('locale', 'uz')
    await message.answer(text=_("""
🎮 2048 o‘yiniga xush kelibsiz! 🧩

Bu yerda siz qiziqarli boshqotirmadan bahramand bo‘lib, o‘zingizni sinab ko‘rishingiz mumkin. Sizni quyidagilar kutmoqda:

🔢 2048 o‘ynang va g‘alabaga intiling!  
🏆 O‘z joriy rekordingizni kuzating va yangi cho‘qqilarga intiling  
👥 Boshqa o‘yinchilarning rekordlarini bilib oling va eng yaxshisi bo‘lish uchun bellashing!  

Boshlashga tayyormisiz? Eng zo‘r bo‘ling va 2048 plitkasiga erishing! 🚀
    """, locale=lang), reply_markup=markup)


@router.message(CommandStart())
@connection()
async def cmd_start(message: Message, session: AsyncSession, state: FSMContext, **kwargs):
    data = await state.get_data()
    lang = data.get('locale', 'uz')
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

        await welcome_message(message, state, main_keyboard(lang))

    except Exception as e:
        await message.answer(f"{e}")
        await message.answer(
            _("Sizning sorovingizni tahlil qilishda muammo yuzaga keldi. Iltimos keyinroq urinib ko'ring"))


@router.callback_query(F.data == "show_my_record")
async def get_user_record(callback: CallbackQuery, **kwargs):
    await callback.answer()
    await callback.message.delete()
    async with async_session_maker() as session:
        try:
            record_info = await UserDAO.get_user_rank(session, telegram_id=callback.from_user.id)
            rank = record_info['rank']
            best_score = record_info['best_score']
            if rank == 1:
                text = _("""
🥇 Tabriklaymiz! Siz {best_score} ochko bilan birinchi o‘rindasiz! Siz — chempionsiz!

Darajangizni saqlab qoling va unvoningizni himoya qiling. Quyidagi tugmani bosing va
natijangizni yanada yaxshilashga harakat qiling!
                    """).format(best_score=best_score)
            elif rank == 2:
                text = _(
                    """
🥈 Ajoyib! Siz {best_score} ochko bilan ikkinchi o‘rinda turibsiz!
                    
Yana biroz harakat qilsangiz — cho‘qqi sizniki bo‘ladi! Birinchi bo‘lish uchun quyidagi tugmani bosing!
                    """).format(best_score=best_score)
            elif rank == 3:
                text = _(
                    """
🥉 Zo‘r natija! Siz {best_score} ochko bilan uchinchi o‘rindasiz!
Cho‘qqiga juda yaqin! Quyidagi tugmani bosib, o‘zingizni sinab ko‘ring va oltin o‘rinni egallang!
                    """
                ).format(best_score=best_score)
            else:
                text = _(
                    """
📊 Sizning rekordingiz: {best_score} ochko. Siz umumiy reytingda {rank}-o‘rindasiz.
                    
Har safar siz yanada kuchliroq bo‘lyapsiz! Quyidagi tugmani bosing va
o‘zingizni sinab, yanada yuqoriga ko‘tariling hamda rekordni yangilang!
                    """
                ).format(best_score=best_score)

            await callback.message.answer(text, reply_markup=record_keyboard())

        except:
            await session.rollback()
            raise


@router.callback_query(F.data == "change_language")
async def change_lang(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(_("Tillardan birini tanlang👇"), reply_markup=change_lang_buttons())


@router.callback_query(F.data.startswith("change_language_to_"))
async def change_lang_callback_func(callback: CallbackQuery, state: FSMContext):
    lang = callback.data.split('_')[-1]
    await state.set_data({'locale': lang})
    await callback.message.delete()
    await welcome_message(callback.message, state, main_keyboard(lang))
