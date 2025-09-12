# app/core/retrieval_service.py
import psycopg2
import json
from app.config import settings

def get_db_conn():
    return psycopg2.connect(settings.database_url)

def retrieve_top_k(query_embedding, k=None):
    k = k or settings.k_retrieval
    conn = get_db_conn()
    cur = conn.cursor()
    qvec = '[' + ','.join(map(str, query_embedding)) + ']'
    sql = """
    SELECT id, source, chunk_text, metadata, embedding <=> %s::vector AS score
    FROM documents
    ORDER BY score DESC
    LIMIT %s;
    """
    cur.execute(sql, (qvec, k))
    rows = cur.fetchall()
    conn.close()
    return [
        {"id": r[0], "source": r[1], "chunk": r[2], "metadata": json.loads(r[3] or "{}"), "score": r[4]}
        for r in rows
    ]
