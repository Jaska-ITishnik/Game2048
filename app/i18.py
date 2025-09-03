import contextvars
import gettext
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOCALES_DIR = BASE_DIR / "locales"

# Context variable to store current language
current_lang = contextvars.ContextVar("current_lang", default="uz")


def set_locale(lang: str):
    """Set current language (uz/ru)"""
    current_lang.set(lang)


def get_translation(lang: str = None):
    """Return gettext translation object"""
    lang = lang or current_lang.get()
    return gettext.translation(
        "messages",
        localedir=str(LOCALES_DIR),
        languages=[lang],
        fallback=True,
    )


def _(text: str) -> str:
    """Universal translation function"""
    return get_translation().gettext(text)
