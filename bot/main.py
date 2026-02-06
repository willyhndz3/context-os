import logging
from contextlib import asynccontextmanager
from http import HTTPStatus

from fastapi import FastAPI, Request, Response
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

from config import TELEGRAM_BOT_TOKEN, WEBHOOK_URL, WEBHOOK_SECRET
from handlers import handle_query, handle_capture, handle_prep, handle_start, handle_accounts

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Build PTB application (no updater -- webhook mode)
ptb = (
    Application.builder()
    .token(TELEGRAM_BOT_TOKEN)
    .updater(None)
    .read_timeout(7)
    .get_updates_read_timeout(42)
    .build()
)

# Register handlers
ptb.add_handler(CommandHandler("start", handle_start))
ptb.add_handler(CommandHandler("capture", handle_capture))
ptb.add_handler(CommandHandler("prep", handle_prep))
ptb.add_handler(CommandHandler("accounts", handle_accounts))
ptb.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_query))


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info(f"Setting webhook to {WEBHOOK_URL}")
    await ptb.bot.set_webhook(url=WEBHOOK_URL, secret_token=WEBHOOK_SECRET)
    async with ptb:
        await ptb.start()
        yield
        await ptb.stop()


app = FastAPI(lifespan=lifespan)


@app.post("/")
async def telegram_webhook(request: Request):
    if request.headers.get("X-Telegram-Bot-Api-Secret-Token") != WEBHOOK_SECRET:
        return Response(status_code=HTTPStatus.FORBIDDEN)
    data = await request.json()
    update = Update.de_json(data, ptb.bot)
    await ptb.process_update(update)
    return Response(status_code=HTTPStatus.OK)


@app.get("/health")
async def health():
    return {"status": "ok"}
