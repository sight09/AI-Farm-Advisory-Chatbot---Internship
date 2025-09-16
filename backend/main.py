import asyncio
from services.ingestion.embed_and_store import embed_and_store
from common.core.openai_client import single_embed
from common.models.user import User
from common.models.document import Document
from common.models.db import SessionLocal
from common.models import init_db
from common.core.openweather import get_weather


async def test_embed_and_store():
    init_db()
    db = SessionLocal()
    
    try:
        weather = await get_weather("London", units="metric", lang="en")
        print(weather)
        
    except Exception as e:
        print(f"Error during test setup: {e}")
    finally:
        db.close()
    
asyncio.run(test_embed_and_store())


# asyncio.run(embed_and_store("services/ingestion/raw/hess403.pdf", title="Hess 403 Syllabus"))



print("Starting embedding and storage process...")