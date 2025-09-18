from telegram import Update
from telegram.ext import ContextTypes
import httpx


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    print("Bot started...")
    user = update.effective_user
    return await update.message.reply_html(
        rf"Hi {user.mention_html()}! Welcome to the AI Farm Advisory Chatbot. How can I assist you today?"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echo the user message."""
    user_message = update.message.text
    
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
    
    await update.message.reply_text(answer)
    
    # print(f"Received message: {user_message}")
    # await update.message.reply_text(f"You said: {user_message}")
