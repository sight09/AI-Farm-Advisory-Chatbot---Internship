# tests/test_routers_chat_bot.py
import unittest
from fastapi.testclient import TestClient
from app.main import app

class TestChatBotRouter(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_chat_bot_response(self):
        response = self.client.post("/ask", json={"question": "Hello there!"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        print(data)
        self.assertIn("answer", data)
        self.assertIn("sources", data)
        self.assertIsInstance(data["sources"], list)
        self.assertIsInstance(data["answer"], str)
        self.assertNotEqual(data["answer"], "")
    
    def test_chat_bot_invalid_question(self):
        response = self.client.post("/ask", json={"question": "H"})
        self.assertEqual(response.status_code, 422)  # Unprocessable Entity for validation error
    
    def test_chat_bot_with_location(self):
        response = self.client.post("/ask", json={
            "question": "What's the weather like?",
            "location": "Addis Ababa"
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        print(data)
        self.assertIn("answer", data)
        self.assertIn("sources", data)
        self.assertIsInstance(data["sources"], list)
        self.assertIsInstance(data["answer"], str)
        self.assertNotEqual(data["answer"], "")
    
    def test_chat_bot_with_coordinates(self):
        response = self.client.post("/ask", json={
            "question": "What's the weather like?",
            "latitude": 9.03,
            "longitude": 38.74
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        print(data)
        self.assertIn("answer", data)
        self.assertIn("sources", data)
        self.assertIsInstance(data["sources"], list)
        self.assertIsInstance(data["answer"], str)
        self.assertNotEqual(data["answer"], "")
    
    def test_chat_bot_non_english_question(self):
        response = self.client.post("/ask", json={
            "question": "ሰላም እንዴት ነህ?",  # "Hello, how are you?" in Amharic
            "lang": "am"
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        print(data)
        self.assertIn("answer", data)
        self.assertIn("sources", data)
        self.assertIsInstance(data["sources"], list)
        self.assertIsInstance(data["answer"], str)
        self.assertNotEqual(data["answer"], "")