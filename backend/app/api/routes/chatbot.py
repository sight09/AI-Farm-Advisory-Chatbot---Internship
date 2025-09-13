from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy import select

from services.db.scripts.db import async_session
from services.db.scripts.schema import Document
from app.core.openai_client import embed_texts, chat_completion, translate
router = APIRouter()


# ---- Request & Response Models ----
class AskRequest(BaseModel):
    question: str
    lang: Optional[str] = "en"   # "en", "am" (Amharic), "om" (Afan Oromo)


class SourceDoc(BaseModel):
    id: int
    title: Optional[str]
    snippet: str
    metadata: Optional[dict]


class AskResponse(BaseModel):
    answer: str
    sources: List[SourceDoc] = []


# ---- Endpoint ----
@router.post("/ask", response_model=AskResponse)
async def ask(req: AskRequest):
    """
    Handles farmer questions:
    - Translates to English (if needed)
    - Embeds the query
    - Searches pgvector for relevant docs
    - Feeds context + question to OpenAI
    - Translates back to original language (if not English)
    """

    # 1) Translate to English if needed
    original_lang = req.lang or "en"
    if original_lang != "en":
        q_en = await translate(req.question, "English")
    else:
        q_en = req.question

    # 2) Embed query
    q_emb = (await embed_texts([q_en]))[0]

    # 3) Vector search in pgvector (top 5)
    async with async_session() as session:
        stmt = (
            select(Document)
            .order_by(Document.embedding.cosine_distance(q_emb))
            .limit(5)
        )
        res = await session.execute(stmt)
        docs = res.scalars().all()

    # 4) Build context
    context = "\n\n---\n\n".join(
        f"Source({d.id}): {d.content[:1000]}" for d in docs
    )

    system_prompt = (
        "You are an agricultural advisor for smallholder farmers. "
        "Answer concisely, practically, and with actionable steps."
    )

    messages = [
        {
            "role": "user",
            "content": f"Question: {q_en}\n\nContext:\n{context}\n\n"
                       "Answer in English with practical advice."
        }
    ]

    # 5) Call OpenAI
    answer_en = await chat_completion(system_prompt, messages, max_tokens=512)

    # 6) Translate back if needed
    if original_lang != "en":
        target_lang = {"am": "Amharic", "om": "Afan Oromo"}.get(original_lang, "English")
        answer_out = await translate(answer_en, target_lang)
    else:
        answer_out = answer_en

    # 7) Return structured response
    return AskResponse(
        answer=answer_out,
        sources=[
            SourceDoc(
                id=d.id,
                title=d.title,
                snippet=(d.content[:300] + "..."),
                metadata=d.metadata,
            )
            for d in docs
        ],
    )
