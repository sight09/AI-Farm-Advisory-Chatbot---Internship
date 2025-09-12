# services/ingestion/chunk_texts.py
import re
from pathlib import Path
from typing import List

def load_text_from_pdf(path: Path) -> str:
    from pypdf import PdfReader
    r = PdfReader(str(path))
    return "\n\n".join(page.extract_text() or "" for page in r.pages)

def chunk_text(text: str, max_chars=2000, overlap=200) -> List[str]:
    # simple chunker by paragraphs -> ensure ≤ max_chars using sliding window
    paras = [p.strip() for p in re.split(r'\n{2,}', text) if p.strip()]
    chunks = []
    cur = ""
    for p in paras:
        if len(cur) + len(p) + 2 <= max_chars:
            cur = (cur + "\n\n" + p).strip()
        else:
            if cur:
                chunks.append(cur)
            # if paragraph itself bigger than max_chars, hard-split:
            while len(p) > max_chars:
                chunks.append(p[:max_chars])
                p = p[max_chars - overlap:]
            cur = p
    if cur:
        chunks.append(cur)
    return chunks
