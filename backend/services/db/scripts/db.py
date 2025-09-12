# filepath: backend/services/db/scripts/db.py
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../../../.env'))
# ...existing code...
import psycopg
from pgvector.psycopg import register_vector

conn = psycopg.connect(os.environ["DATABASE_URL"])
register_vector(conn)
print("Connected to PostgreSQL with pgvector!")