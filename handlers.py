from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from telegram.ext import ContextTypes
import os
from config import CHANNEL_USERNAME, PDF_FILE_PATH


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args

    if "checklist" in args:
        keyboard = [
            [InlineKeyboardButton("📥 Получить чек-лист", callback_data="get_checklist")]
        ]
        await update.message.reply_text(
            "Нажмите кнопку ниже, чтобы получить чек-лист (после проверки подписки):",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.message.reply_text("Используйте кнопку из канала для получения чек-листа.")


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "get_checklist":
        user_id = query.from_user.id

        try:
            member = await context.bot.get_chat_member(chat_id=f"@{CHANNEL_USERNAME}", user_id=user_id)
            status = member.status
        except Exception:
            await context.bot.send_message(chat_id=query.message.chat.id, text="⚠️ Ошибка при проверке подписки.")
            return

        if status in ["member", "administrator", "creator"]:
            with open(PDF_FILE_PATH, "rb") as pdf:
                await context.bot.send_document(chat_id=query.message.chat.id, document=InputFile(pdf), caption="✅ Вот ваш чек-лист!")
        else:
            keyboard = [
                [InlineKeyboardButton("🔗 Подписаться", url=f"https://t.me/{CHANNEL_USERNAME}")],
                [InlineKeyboardButton("🔄 Проверить снова", callback_data="get_checklist")]
            ]
            await context.bot.send_message(
                chat_id=query.message.chat.id,
                text=f"Подпишитесь на канал @{CHANNEL_USERNAME} и нажмите 'Проверить снова':",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )