import os
import asyncio
import threading

from flask import Flask
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from waitress import serve


BOT_TOKEN = "".join(os.environ.get("BOT_TOKEN", "").split())

app = Flask(__name__)

telegram_app = Application.builder().token(BOT_TOKEN).build()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 Welcome to Video Save Bot!\n\n"
        "Send me a video."
    )


async def receive_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video = update.message.video

    await update.message.reply_text(
        "✅ Video received!\n\n"
        f"File ID:\n{video.file_id}"
    )


telegram_app.add_handler(
    CommandHandler("start", start)
)

telegram_app.add_handler(
    MessageHandler(filters.VIDEO, receive_video)
)


@app.route("/")
def home():
    return "Video Save Bot is running!"


async def run_telegram():
    print("Starting Telegram bot...")
    print("Token found:", bool(BOT_TOKEN))
    print("Token length:", len(BOT_TOKEN))

    await telegram_app.initialize()

    print("Telegram connection successful!")

    await telegram_app.start()

    print("Telegram bot started!")

    await telegram_app.updater.start_polling()

    await asyncio.Event().wait()


def start_telegram_thread():
    asyncio.run(run_telegram())


if __name__ == "__main__":
    print("Starting web server...")

    telegram_thread = threading.Thread(
        target=start_telegram_thread,
        daemon=True
    )

    telegram_thread.start()

    port = int(os.environ.get("PORT", 10000))

    print(f"Web server listening on port {port}")

    serve(
        app,
        host="0.0.0.0",
        port=port
    )
