# # services/telegram_bot/bot.py
# import os
# import logging
# from telegram import Update
# from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
# import requests

# TOKEN = os.getenv("TELEGRAM_TOKEN")
# BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000/api/ask")

# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text("Welcome to the Farm Advisory bot. Ask your question in Amharic, Afan Oromo or English.")

# async def handle_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     q = update.message.text
#     # naive: detect language or let user send /lang. We'll assume English for simple example.
#     payload = {"question": q, "lang": "en"}
#     r = requests.post(BACKEND_URL, json=payload, timeout=30)
#     if r.ok:
#         data = r.json()
#         await update.message.reply_text(data["answer"])
#     else:
#         await update.message.reply_text("Sorry, service is down.")

# if __name__ == "__main__":
#     app = ApplicationBuilder().token(TOKEN).build()
#     app.add_handler(CommandHandler("start", start))
#     app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_question))
#     print("Starting telegram bot...")
#     app.run_polling()
