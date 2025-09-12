import os, json
from pathlib import Path
import google.generativeai as genai
import psycopg2
from services.ingestion.chunk_texts import load_text_from_pdf, chunk_text
from dotenv import load_dotenv
load_dotenv()
# ...existing code...

GENAI_KEY = os.getenv("GEMINI_API_KEY")
EMBED_MODEL = os.getenv("EMBEDDING_MODEL", "gemini-embedding-001")

genai.configure(api_key=GENAI_KEY)
genai.configure(api_key=os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"))

def embed_texts(texts: list[str]):
    embeddings = []
    for text in texts:
        res = genai.embed_content(model=EMBED_MODEL, content=text)
        embeddings.append(res["embedding"])
    return embeddings
    # batch call
    res = genai.embed_content(model=EMBED_MODEL, content=texts[0])
    # res.embeddings usually contains the list of embeddings in order - inspect in your environment
    return [e for e in res.embeddings]   # inspect structure (res.embeddings[i].embedding or similar)

def store_chunks(db_conn, chunks, metadata):
    cur = db_conn.cursor()
    for chunk in chunks:
        emb = embed_texts([chunk])[0]  # adapt to response shape
        # convert embedding list to Postgres string representation
        emb_str = "[" + ",".join(map(str, emb)) + "]"
        cur.execute(
            "INSERT INTO documents (source, metadata, content, chunk_text, embedding) VALUES (%s,%s,%s,%s,%s)",
            (metadata["source"], json.dumps(metadata), metadata.get("content",""), chunk, emb_str)
        )
    db_conn.commit()

if __name__ == "__main__":
    # conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    conn = psycopg2.connect("postgresql://dev:devpassword@localhost:5432/embeddings_db")
    p = Path("services/ingestion/raw/example.pdf")
    text = load_text_from_pdf(p)
    chunks = chunk_text(text)
    store_chunks(conn, chunks, {"source": p.name, "filename": str(p)})
