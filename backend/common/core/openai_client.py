# backend/app/core/openai_client.py
import os
import asyncio
from openai import OpenAI # type: ignore
from common.config import settings

openai_client = OpenAI(api_key=settings.openai_api_key)


async def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Generate embeddings for a list of texts using the OpenAI embedding model.
    """
    response = openai_client.embeddings.create(
        model=settings.embedding_model,
        input=texts
    )

    embeddings = [data_point.embedding for data_point in response.data]
    return embeddings


async def single_embed(text: str) -> list[float]:
    """
    Generate embedding for a given text.
    """
    response = openai_client.embeddings.create(
        model=settings.embedding_model,
        input=text
    )
    return response.data[0].embedding


async def chat_completion(system_prompt: str, messages: list[dict], max_tokens=512):
    """
    Generate a chat completion using the OpenAI chat model.
    """
    def _call():
        response = openai_client.ChatCompletion.create(
            model=settings.gen_model,
            messages=[{"role":"system", "content": system_prompt}] + messages,
            max_tokens=max_tokens,
            temperature=0.2,
        )
        return response["choices"][0]["message"]["content"]
    return await asyncio.to_thread(_call)


async def translate(text: str, target_lang: str):
    """
    lightweight translator using the chat model (good for small text)
    """
    # Keep translations short; for bulk use a dedicated translator
    prompt = f"Translate the following text to {target_lang}. Keep meaning and units. Text:\n\n{text}"
    return await chat_completion("You are a translation assistant.", [{"role":"user","content":prompt}], max_tokens=512)
