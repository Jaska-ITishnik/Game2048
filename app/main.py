import logging
from contextlib import asynccontextmanager

from aiogram.types import Update
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request

from app.bot.create_bot import dp, start_bot, bot, stop_bot
from app.config import settings
from app.bot.handlers.router import router as bot_router
from app.game.router import router as game_router

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting bot setup...")
    dp.include_router(bot_router)
    await start_bot()
    webhook_url = settings.get_webhook_url()
    await bot.set_webhook(
        url=webhook_url,
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True
    )
    logging.info(f"Webhook set to {webhook_url}")
    yield
    logging.info("Shutting down bot...")
    await bot.delete_webhook()
    await stop_bot()
    logging.info("Webhook deleted")


app = FastAPI(lifespan=lifespan)

app.mount('/static', StaticFiles(directory='app/static'), 'static')
app.include_router(game_router)


@app.post("/webhook")
async def webhook(request: Request) -> None:
    logging.info("Received webhook request")
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)
    logging.info("Update processed")
