from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters, CommandHandler
import re
from common.config import settings
from common.models.db import get_db
from common.models.user import User
from .handle_message import buttons

# location change handler
LOCATION_CHANGE = range(1)
CITY_NAME_PATTERN = r"^[A-Za-z\s]+$"

async def change_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Change the location of the user.
    """
    await update.message.reply_text("Please enter a city:", reply_markup=ReplyKeyboardMarkup([["Back"]], one_time_keyboard=True, resize_keyboard=True))
    return LOCATION_CHANGE

async def set_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Set the selected location.
    """
    reply_markup = ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True)
    
    if update.message.text == "Back":
        await update.message.reply_text("Location change canceled.", reply_markup=reply_markup)
        return ConversationHandler.END
    
    
    with next(get_db()) as db:
        user = db.query(User).filter_by(telegram_id=str(update.effective_user.id)).first()

        if not user:
            return await update.message.reply_text("User not found. Please start the bot first.")
        
        if not update.message or not update.message.text:
            return await update.message.reply_text("Invalid selection. Please try again.")
        
        city_name = update.message.text.strip().title()
        
        if not re.match(CITY_NAME_PATTERN, city_name):
            await update.message.reply_text(f"City name '{city_name}' is invalid! Please enter a valid city name.")
            return ConversationHandler.END

        if user.location == city_name:
            await update.message.reply_text(f"Location is already set to {city_name}.", reply_markup=reply_markup)
            return ConversationHandler.END

        # save the selected location
        user.location = city_name
        db.commit()
        

        await update.message.reply_text(f"Location changed to {city_name}.", reply_markup=reply_markup)

    return ConversationHandler.END

async def cancel_location_change(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Cancel the location change process.
    """
    reply_markup = ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text("Location change canceled.", reply_markup=reply_markup)
    return ConversationHandler.END

location_change_handler = ConversationHandler(
    entry_points=[
        CommandHandler('change_location', change_location),
        MessageHandler(filters.Regex('^Set location$'), change_location)
    ],
    states={
        LOCATION_CHANGE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, set_location)
        ]
    },
    fallbacks=[
        CommandHandler('cancel', cancel_location_change),
        MessageHandler(filters.Regex('^Cancel$'), cancel_location_change)
    ],
    allow_reentry=True
)
