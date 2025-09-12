from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.chatbot import router as chatbot_router
app = FastAPI()
app.include_router(chatbot_router)
app.include_router(health_router)