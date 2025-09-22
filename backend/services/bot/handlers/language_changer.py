from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters, CommandHandler
from common.config import settings
from common.models.db import get_db
from common.models.user import User
from .handle_message import buttons

# language change handler
LANGUAGES_CHANGE = range(1)

async def change_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Change the language of the bot.
    """
    available_languages = settings.supported_languages
    language_buttons = [[lang] for lang in available_languages.values()] + [["Back"]]
    reply_markup = ReplyKeyboardMarkup(language_buttons, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text("Please select a language:", reply_markup=reply_markup)
    return LANGUAGES_CHANGE

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Set the selected language.
    """
    reply_markup = ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True)
    
    if update.message.text == "Back":
        await update.message.reply_text("Language change canceled.", reply_markup=reply_markup)
        return ConversationHandler.END
    
    with next(get_db()) as db:
        user = db.query(User).filter_by(telegram_id=str(update.effective_user.id)).first()

        if not user:
            return await update.message.reply_text("User not found. Please start the bot first.")
        
        if not update.message or not update.message.text:
            return await update.message.reply_text("Invalid selection. Please try again.")
        
        if update.message.text not in settings.supported_languages.values():
            return await update.message.reply_text("Selected language is not supported. Please try again.")

        if settings.supported_languages[user.language] == update.message.text:
            await update.message.reply_text(f"Language is already set to {update.message.text}.", reply_markup=reply_markup)
            return ConversationHandler.END
        
        # save the selected language key
        user.language = [key for key, value in settings.supported_languages.items() if value == update.message.text][0]
        db.commit()
        

        await update.message.reply_text(f"Language changed to {update.message.text}.", reply_markup=reply_markup)

    return ConversationHandler.END

async def cancel_language_change(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Cancel the language change process.
    """
    reply_markup = ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True)
    
    await update.message.reply_text("Language change canceled.", reply_markup=reply_markup)
    return ConversationHandler.END

language_change_handler = ConversationHandler(
    entry_points=[
        CommandHandler('change_language', change_language),
        MessageHandler(filters.Regex('^Change Language$'), change_language)
    ],
    states={
        LANGUAGES_CHANGE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, set_language)
        ]
    },
    fallbacks=[
        CommandHandler('cancel', cancel_language_change),
        MessageHandler(filters.Regex('^Cancel$'), cancel_language_change)
    ],
    allow_reentry=True
)
