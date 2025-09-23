# tests/test_googletrans.py
import unittest
from common.core.googletrans import translate, detect_language

class TestGoogleTrans(unittest.IsolatedAsyncioTestCase):
    
    async def test_translate(self):
        text = "Hello, how are you?"
        translated_text = await translate(text, src_lang='en', dest_lang='am')
        self.assertIsInstance(translated_text, str)
        self.assertNotEqual(translated_text, text)
        self.assertIn("ሰላም", translated_text)  # Basic check for Amharic translation

    async def test_detect_language(self):
        text = "ሰላም ለሁላችሁ"
        detected_lang = await detect_language(text)
        self.assertIsInstance(detected_lang, str)
        self.assertEqual(detected_lang, 'am')  # Amharic language code
