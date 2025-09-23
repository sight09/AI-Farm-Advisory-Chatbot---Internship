# tests/test_bot.py
import unittest
from unittest.mock import MagicMock
from telegram import Update, Bot
from telegram.ext import CallbackContext
from services.bot.handlers.handle_message import start, handle_message

class TestBotHandlers(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_update = MagicMock(spec=Update)
        self.mock_context = MagicMock(spec=CallbackContext)
        
        self.mock_update.message.reply_text = MagicMock()
        self.mock_update.message.reply_html = MagicMock()

    def test_start(self):
        self.mock_update.message.text = "/start"
        self.mock_update.effective_user.id = 12345
        start(self.mock_update, self.mock_context)
        
        # print all available attributes of mock_update.message
        # print(dir(self.mock_update.message.reply_html))
        # print(self.mock_update.message.reply_html.return_value)
        # self.mock_update.message.reply_text.assert_called_once_with("Hi ! Welcome to the AI Farm Advisory Chatbot. How can I assist you today?")

    # def test_handle_message(self):
    #     self.mock_update.message.text = "Hello"
    #     handle_message(self.mock_update, self.mock_context)
    #     self.mock_update.message.reply_text.assert_called_once_with("You said: Hello")
