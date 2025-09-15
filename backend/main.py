from services.ingestion.embed_and_store import embed_and_store
from common.models.user import User
from common.models.document import Document
from common.models.db import SessionLocal
from common.models import init_db


def test_embed_and_store():
    init_db()
    db = SessionLocal()
    
    try:
        pass
    except Exception as e:
        print(f"Error during test setup: {e}")
    finally:
        db.close()
    
test_embed_and_store()

print("Starting embedding and storage process...")