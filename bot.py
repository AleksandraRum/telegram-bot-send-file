import os
import asyncio

from flask import Flask, request
from telegram import Update

from hypercorn.asyncio import serve
from hypercorn.config import Config
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

# async def setup():
#     await application.initialize()
#     webhook_url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/webhook/{WEBHOOK_SECRET}"
#     await application.bot.set_webhook(webhook_url)
#     print(f"Webhook set to: {webhook_url}")


async def main():
    await application.initialize()
    webhook_url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/webhook/{WEBHOOK_SECRET}"
    await application.bot.set_webhook(webhook_url)
    print(f"✅ Webhook установлен: {webhook_url}")

    from hypercorn.asyncio import serve
    from hypercorn.config import Config
    config = Config()
    config.bind = [f"0.0.0.0:{os.environ.get('PORT', '10000')}"]
    await serve(app, config)

if __name__ == "__main__":
    asyncio.run(main())