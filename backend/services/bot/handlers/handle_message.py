from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
import httpx


buttons = [
    ["Get weather forecast"],
    ["Change Language", "Set location"],
    ["Cancel"]
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    print("Bot started...")
    
    # button = KeyboardButton("Send my location", request_location=True)
    # keyboard = [[button]]
    # reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    
    reply_markup = ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True)
    
    
    user = update.effective_user
    return await update.message.reply_html(
        rf"Hi {user.mention_html()}! Welcome to the AI Farm Advisory Chatbot. How can I assist you today?",
        reply_markup=reply_markup
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echo the user message."""
    user_message = update.message.text
    
    latitude = update.message.location.latitude if update.message.location else None
    longitude = update.message.location.longitude if update.message.location else None
    print(f"Received location: lat={latitude}, lon={longitude}")
    
    # interact with /ask endpoint
    async with httpx.AsyncClient(timeout=None) as client:
        response = await client.post(
            "http://localhost:8000/ask",
            json={"question": user_message, "lang": "en"}
        )
        if response.status_code == 200:
            answer = response.json().get("answer", "Sorry, I couldn't find an answer.")
        else:
            answer = "Sorry, there was an error processing your request."
    
    return await update.message.reply_text(answer)
