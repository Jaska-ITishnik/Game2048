from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.config import settings


def main_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(text="🎮 Старт игры 2048", web_app=WebAppInfo(url=settings.BASE_SITE)),
        InlineKeyboardButton(text="🏆 Лидеры 2048", web_app=WebAppInfo(url=f"{settings.BASE_SITE}/records")),
        InlineKeyboardButton(text="📈 Мой рекорд", callback_data="show_my_record")
    ]
    kb.add(*buttons)
    kb.adjust(1)
    return kb.as_markup()


def record_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(text="🎮 Старт игры 2048", web_app=WebAppInfo(url=settings.BASE_SITE)),
        InlineKeyboardButton(text="🏆 Рекоды других", web_app=WebAppInfo(url=f"{settings.BASE_SITE}/records")),
        InlineKeyboardButton(text="🔄 Обновить мой рекорд", callback_data="show_my_record")
    ]
    kb.add(*buttons)
    kb.adjust(1)
    return kb.as_markup()
