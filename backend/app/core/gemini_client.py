# app/core/gemini_client.py
import google.generativeai as genai
from app.config import settings
from app.core.gemini_client import embed_texts, generate_answer

# Configure the Gemini client with your API key
genai.configure(api_key=settings.gemini_api_key)


def embed_texts(texts):
    """
    Generate embeddings for a list of texts using the Gemini embedding model.
    """
    embeddings = []
    for text in texts:
        res = genai.embed_content(
            model=settings.embedding_model,
            content=text
        )
        embeddings.append(res["embedding"])
    return embeddings


def generate_answer(prompt: str, max_tokens: int = 512) -> str:
    """
    Generate an answer using the Gemini generative model.
    """
    model = genai.GenerativeModel(settings.gen_model)
    response = model.generate_content(
        prompt,
        generation_config={"max_output_tokens": max_tokens}
    )
    return response.text
