import os
import asyncio

from flask import Flask, request
from telegram import Update

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
)

from config import BOT_TOKEN, WEBHOOK_SECRET
from handlers import start, button_callback


app = Flask(__name__)

application = ApplicationBuilder().token(BOT_TOKEN).build()

application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(button_callback))


@app.post(f"/webhook/{WEBHOOK_SECRET}")
async def handle_webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.process_update(update)
    return "ok", 200

async def setup():
    await application.initialize()
    webhook_url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/webhook/{WEBHOOK_SECRET}"
    await application.bot.set_webhook(webhook_url)
    print(f"Webhook set to: {webhook_url}")


def main():
    # webhook_url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/webhook/{WEBHOOK_SECRET}"
    # asyncio.run(application.initialize())
    # asyncio.run(application.bot.set_webhook(webhook_url))
    # print(f"Webhook set to: {webhook_url}")
    
    asyncio.run(setup())
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()