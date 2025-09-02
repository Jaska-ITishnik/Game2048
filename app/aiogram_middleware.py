from aiogram import BaseMiddleware
from aiogram.types import Message

from app.i18 import set_locale


class I18nMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if isinstance(event, Message):
            lang = event.from_user.language_code or "uz"
            set_locale(lang if lang in ["uz", "ru"] else "uz")
        return await handler(event, data)
