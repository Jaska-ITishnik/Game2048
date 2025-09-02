from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.config import settings


def change_lang_buttons():
    ikb = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(text=_("🇺🇿UZ"), callback_data="change_language_to_uz"),
        InlineKeyboardButton(text=_("🇷🇺RU"), callback_data="change_language_to_ru")
    ]
    ikb.add(*buttons)
    return ikb.as_markup()


def main_keyboard(lang: str = None) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(text=_("🎮 2048 o'yinni boshlash", locale=lang), web_app=WebAppInfo(url=settings.BASE_SITE)),
        InlineKeyboardButton(text=_("🏆 Yetakchilar 2048", locale=lang), web_app=WebAppInfo(url=f"{settings.BASE_SITE}/records")),
        InlineKeyboardButton(text=_("📈 Mening rekordim", locale=lang), callback_data="show_my_record"),
        InlineKeyboardButton(text=_("🇺🇿 ♻️ 🇷🇺 Tilni almashtirish", locale=lang), callback_data="change_language")
    ]
    kb.add(*buttons)
    kb.adjust(1)
    return kb.as_markup()


def record_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(text=_("🎮 2048 o'yinni boshlash"), web_app=WebAppInfo(url=settings.BASE_SITE)),
        InlineKeyboardButton(text=_("🏆 Boshqalarni rekordi"), web_app=WebAppInfo(url=f"{settings.BASE_SITE}/records")),
        InlineKeyboardButton(text=_("🔄 Rekordni yangilash"), callback_data="show_my_record")
    ]
    kb.add(*buttons)
    kb.adjust(1)
    return kb.as_markup()
