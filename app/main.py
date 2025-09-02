import logging
from contextlib import asynccontextmanager
from pathlib import Path

from aiogram.types import Update
from aiogram.utils.i18n import I18n, FSMI18nMiddleware
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request

from app.bot.create_bot import dp, on_startup, bot, on_shutdown
from app.bot.handlers.router import router as bot_router
from app.config import settings
from app.game.router import router as game_router, templates
from app.i18 import set_locale, get_translation

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
BASE_DIR = Path(__file__).resolve().parent.parent
LOCALES_DIR = BASE_DIR / "locales"


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting bot setup...")
    i18n = I18n(path=LOCALES_DIR)
    dp.update.outer_middleware.register(FSMI18nMiddleware(i18n))
    # dp.message.middleware(I18nMiddleware())
    dp.include_router(bot_router)
    await on_startup(dp, bot)
    webhook_url = settings.get_webhook_url()
    await bot.set_webhook(
        url=webhook_url,
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True
    )
    logging.info(f"Webhook set to {webhook_url}")
    yield
    await on_shutdown(dp, bot)
    logging.info("Shutting down bot...")
    await bot.delete_webhook()
    logging.info("Webhook deleted")


app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def detect_lang_middleware(request: Request, call_next):
    # lang = request.query_params.get("lang") or request.headers.get("Accept-Language", "uz")[:2]
    lang = "ru"
    set_locale(lang if lang in ["uz", "ru"] else "uz")

    translations = get_translation()
    templates.env.globals.update({
        "_": translations.gettext,
        "gettext": translations.gettext,
        "ngettext": translations.ngettext,
    })

    response = await call_next(request)
    return response


app.mount('/static', StaticFiles(directory='app/static'), 'static')
app.include_router(game_router)


@app.post("/webhook")
async def webhook(request: Request) -> None:
    logging.info("Received webhook request")
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)
    logging.info("Update processed")
