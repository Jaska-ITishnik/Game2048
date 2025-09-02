from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from app.config import settings

bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


async def on_startup(dp: Dispatcher, bot: Bot):
    try:
        for admin_id in settings.ADMINS:
            await bot.send_message(admin_id, 'Bot ishga tushdi🥳.')
    except Exception:
        pass
    await bot.set_my_commands(
        [
            BotCommand(command='start', description='🛫Botni ishga tushirish')
        ]
    )


async def on_shutdown(dp: Dispatcher, bot: Bot):
    try:
        for admin_id in settings.ADMIN_IDS:
            await bot.send_message(admin_id, "Bot to'xtab qoldi😔")
    except Exception:
        pass
    await bot.delete_my_commands()
