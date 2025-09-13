# services/database/database.py
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import text
from .schema import Base
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
print("Using DATABASE_URL:", DATABASE_URL)
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable is not set")
engine = create_async_engine(DATABASE_URL, echo=False, future=True)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def init_db():
    async with engine.begin() as conn:
        # ensure pgvector extension is enabled
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        # create tables
        await conn.run_sync(Base.metadata.create_all)
