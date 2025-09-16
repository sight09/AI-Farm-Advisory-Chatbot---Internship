from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chat_bot_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_bot_router)
# app.include_router(item.router)

