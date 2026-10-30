
import os
import json
import asyncio
import logging
from http.server import BaseHTTPRequestHandler

from aiogram import Bot, Dispatcher
from aiogram.types import Update

logging.basicConfig(level=logging.INFO)

dp = Dispatcher()

@dp.message()
async def start_handler(message):
    await message.answer(
        "👋 Assalomu alaykum!\n\n"
        "AKOSHSAVEDBOT ishga tushdi! 🚀\n\n"
        "🎬 TikTok, Instagram va YouTube\n"
        "🎵 Musiqa qidirish\n"
        "⭐ Sevimlilar"
    )

async def process_update(data):
    token = os.environ["BOT_TOKEN"]
    bot = Bot(token=token)

    try:
        update = Update.model_validate(
            data,
            context={"bot": bot}
        )
        await dp.feed_update(bot, update)
    finally:
        await bot.session.close()


class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        secret = os.environ.get("WEBHOOK_SECRET", "")
        received = self.headers.get(
            "X-Telegram-Bot-Api-Secret-Token", ""
        )

        if not secret or received != secret:
            self.send_response(403)
            self.end_headers()
            return

        try:
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length))

            asyncio.run(process_update(data))

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"ok":true}')

        except Exception:
            logging.exception("Webhook error")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b'{"ok":false}')

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"AKOSHSAVEDBOT ONLINE")
