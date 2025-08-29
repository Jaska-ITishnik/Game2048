from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.config import settings

bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


async def start_bot():
    try:
        for admin_id in settings.ADMINS:
            await bot.send_message(admin_id, 'Bot ishga tushdi🥳.')
    except Exception:
        pass


async def stop_bot():
    try:
        for admin_id in settings.ADMIN_IDS:
            await bot.send_message(admin_id, "Bot to'xtab qoldi😔")
    except Exception:
        pass
