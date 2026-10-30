
import os
import asyncio
import logging

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.types import Update

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("BOT_TOKEN sozlanmagan")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message()
async def all_messages(message):
    await message.answer(
        "👋 AKOSHSAVEDBOT ishlayapti!\n\n"
        "🎬 Video yuklash uchun havola yuboring.\n"
        "🎵 Musiqa qidirish uchun /music buyrug'ini yuboring."
    )

async def telegram_webhook(request):
    try:
        data = await request.json()
        update = Update.model_validate(
            data,
            context={"bot": bot}
        )
        await dp.feed_update(bot, update)
        return web.json_response({"ok": True})
    except Exception:
        logging.exception("Webhook xatosi")
        return web.json_response({"ok": False}, status=500)

async def health(request):
    return web.json_response({
        "status": "online",
        "bot": "AKOSHSAVEDBOT"
    })

app = web.Application()
app.router.add_post("/api/webhook", telegram_webhook)
app.router.add_get("/api/health", health)
