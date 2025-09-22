from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from common.config import settings
from services.bot.handlers.handle_message import start, handle_message
from services.bot.handlers.language_changer import language_change_handler
from services.bot.handlers.location_changer import location_change_handler


def init_bot():
    app = ApplicationBuilder().token(settings.telegram_bot_token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(language_change_handler)
    app.add_handler(location_change_handler)
    
    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))


    print("Bot is running...")
    app.run_polling()
    print("Bot stopped.")

if __name__ == "__main__":
    init_bot()
