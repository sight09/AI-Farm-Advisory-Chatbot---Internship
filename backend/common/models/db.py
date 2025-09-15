from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from common.config import settings

DATABASE_URL = settings.database_url

print(f"Using database URL: {DATABASE_URL}")

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

