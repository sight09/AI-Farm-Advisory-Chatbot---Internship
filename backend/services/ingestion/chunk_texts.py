# services/ingestion/chunk_texts.py
def chunk_text(text: str, chunk_size=800, overlap=100):
    chunks = []
    start = 0
    L = len(text)
    while start < L:
        end = min(L, start + chunk_size)
        chunks.append(text[start:end])
        start = max(start + chunk_size - overlap, end)
    return chunks
