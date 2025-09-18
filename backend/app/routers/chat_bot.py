from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from common.models.db import get_db
from common.models.document import Document
from common.config import settings
from common.core.openai_client import translate, single_embed, chat_completion
from common.core.openweather import get_weather

router = APIRouter()

class AskRequest(BaseModel):
    question: str = Field(..., min_length=10, max_length=200, example="What is the best fertilizer for tomatoes?")
    lang: str = Field("auto", pattern="^(auto|en|am|om|so)$")  # optional
    location: str = Field(None, example="Addis Ababa")  # optional

class AskResponse(BaseModel):
    answer: str
    sources: list
    
lang_map = {
    "auto": "English",
    "en": "English",
    "am": "Amharic",
    "om": "Affan Oromo",
    "so": "Somali"
}

@router.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest, db: Session = Depends(get_db)):
    """
        Handle user questions and return answers.
        - request: AskRequest
        - db: Database session
    """
     
    english_question = request.question
    if request.lang != "en":
        english_question = await translate(request.question, "en")


    # Embed the question
    query_embedding = await single_embed(english_question)
        
    
    # Retrieve relevant chunks from the database
    result = db.query(Document).order_by(Document.embedding.cosine_distance(query_embedding)).limit(settings.k_retrieval).all()

    context = "\n\n".join([doc.content for doc in result])
    if not context.strip():
        return AskResponse(answer="I'm sorry, I don't have enough information to answer that question.", sources=[])


    weather_data = None
    if request.location:
        weather_data = await get_weather(request.location)
        context += f"\n\nWeather information for {request.location}:\n{weather_data}"

    # Build prompt for answering
    system = (
        "You are an agricultural assistant. Use ONLY the provided context to answer the question in clear simple English. "
        "If answer not in context, be honest and say you don't know."
        "If the user ask for the weather, provide a concise weather report using the provided data, without any additional commentary."
        f"Answer must be in {lang_map[request.lang]} language only don't include any other language."
    )
    
    prompt = f"""Use the following context to answer the

    question: {english_question}

    Context:
    {context}
    Weather Data:
    {weather_data if weather_data else 'No weather data provided.'}
    """

    answer = await chat_completion(system, [{"role":"user","content":prompt}], max_tokens=512)
    
    # print("Question:", request.question)
    # print("Context:", context)
    # print("Weather info:", weather_data)
    # print("Answer:", answer)

    sources = ["source1", "source2"]
    return AskResponse(answer=answer, sources=sources)

