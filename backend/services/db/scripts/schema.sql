CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS documents (
  id SERIAL PRIMARY KEY,
  source TEXT,
  metadata JSONB,
  content TEXT,
  chunk_text TEXT,
  embedding vector(3072),  -- use 3072 if using gemini-embedding-001
  created_at TIMESTAMP DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_documents_embedding ON documents USING ivfflat (embedding vector_l2_ops) WITH (lists = 100);
