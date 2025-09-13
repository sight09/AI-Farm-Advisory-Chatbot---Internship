# backend/app/core/openai_client.py
import os, asyncio
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
EMBED_MODEL = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")

CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")

async def embed_texts(texts: list[str]) -> list[list[float]]:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(model=EMBED_MODEL, input=texts)
    return [d.embedding for d in response.data]


async def chat_completion(system_prompt: str, messages: list[dict], max_tokens=512):
    def _call():
        resp = openai.ChatCompletion.create(
            model=CHAT_MODEL,
            messages=[{"role":"system", "content": system_prompt}] + messages,
            max_tokens=max_tokens,
            temperature=0.2,
        )
        return resp["choices"][0]["message"]["content"]
    return await asyncio.to_thread(_call)

# lightweight translator using the chat model (good for small text)
async def translate(text: str, target_lang: str):
    # Keep translations short; for bulk use a dedicated translator
    prompt = f"Translate the following text to {target_lang}. Keep meaning and units. Text:\n\n{text}"
    return await chat_completion("You are a translation assistant.", [{"role":"user","content":prompt}], max_tokens=512)
