import asyncio
from fastapi import FastAPI
from app.api.routes.chatbot import router as chatbot_router
from services.db.scripts.db import init_db

app = FastAPI(title="AI Farm Advisory")

# Include chatbot routes under /api
app.include_router(chatbot_router, prefix="/api")

# Health check route
@app.get("/health")
async def health():
    return {"status": "ok"}

# Initialize the database on startup
@app.on_event("startup")
async def startup_event():
    await init_db()