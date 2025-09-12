from fastapi import APIRouter
from pydantic import BaseModel
from app.core.gemini_client import embed_texts, generate_answer
from app.core.retrieval_service import retrieve_top_k

router = APIRouter()

class AskRequest(BaseModel):
    question: str
    lang: str = "auto"  # optional

class AskResponse(BaseModel):
    answer: str
    sources: list

@router.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    # 1) Translate to English using Gemini (if needed)
    translation_prompt = f"Translate to English only (no extra text):\n\n{req.question}"
    english_question = generate_answer(translation_prompt)

    # 2) Embed the question
    q_emb = embed_texts([english_question])[0]

    # 3) Retrieve relevant chunks
    hits = retrieve_top_k(q_emb, k=5)
    context = "\n\n---\n\n".join(h["chunk"] for h in hits)

    # 4) Build prompt for answer
    system = (
        "You are an agricultural assistant. Use ONLY the provided context to answer the question in clear simple English. "
        "If answer not in context, be honest and say you don't know."
    )
    prompt = system + "\n\nCONTEXT:\n" + context + "\n\nQUESTION:\n" + english_question + "\n\nAnswer succinctly:"

    # 5) Generate answer with Gemini
    ans = generate_answer(prompt)
    return {"answer": ans, "sources": [h["id"] for h in hits]}