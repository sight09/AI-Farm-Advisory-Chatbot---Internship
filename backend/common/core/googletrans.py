# backend/app/core/googletrans.py
from typing import Optional
from googletrans import Translator

async def translate(text: str, src_lang: str = 'auto', dest_lang: str = 'en') -> Optional[str]:
    """
    Translate text to the target language using googletrans.
    """
    try:
        async with Translator() as translator:
            result = await translator.translate(text, src=src_lang, dest=dest_lang)
            return result.text
    except Exception as e:
        print(f"Translation error: {e}")
        return None
    return None


async def detect_language(text: str) -> Optional[str]:
    """
    Detect the language of the given text using googletrans.
    """
    try:
        async with Translator() as translator:
            result = await translator.detect(text)
            return result.lang
    except Exception as e:
        print(f"Language detection error: {e}")
        return None
    return None
    