import asyncio
import os
from services.db.scripts.db import async_session, init_db
from services.db.scripts.schema import Document
from app.core.openai_client import embed_texts
from services.ingestion.chunk_texts import chunk_text

async def ingest_file(file_path, title=None):
    from pypdf import PdfReader
    reader = PdfReader(file_path)
    text = "\n\n".join(page.extract_text() or "" for page in reader.pages)
    print(f"\n[DEBUG] Extracted text from {file_path} (first 200 chars):\n{text[:200]}\n")
    chunks = chunk_text(text)
    print(f"[DEBUG] Number of chunks: {len(chunks)}")
    if chunks:
        print(f"[DEBUG] First chunk: {chunks[0][:100]}")
    embeddings = await embed_texts(chunks)
    print(f"[DEBUG] Number of embeddings: {len(embeddings)}")
    async with async_session() as session:
        for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
            print(f"[DEBUG] Adding chunk {i+1}/{len(chunks)} to DB")
            doc = Document(
                title=title or os.path.basename(file_path),
                content=chunk,
                doc_metadata={"source": file_path},
                embedding=emb
            )
            session.add(doc)    
        await session.commit()
        print(f"[DEBUG] Committed {len(chunks)} chunks for {file_path}")

if __name__ == "__main__":
    import sys, glob, asyncio, os

    if len(sys.argv) < 2:
        print("Usage: python -m services.ingestion.embed_and_store <folder_or_file_path>")
        sys.exit(1)
    input_path = sys.argv[1]
    if os.path.isdir(input_path):
        files = glob.glob(os.path.join(input_path, "*.pdf"))
    else:
        files = [input_path]
    print("Files found:", files)

    async def main():
        await init_db()
        for f in files:
            print("Ingesting", f)
            await ingest_file(f)

    asyncio.run(main())