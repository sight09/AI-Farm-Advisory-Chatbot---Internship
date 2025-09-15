import os
import pathlib
from typing import Union
from pypdf import PdfReader  # type: ignore
# import docx  # python-docx
from common.config import settings


def document_reader(file_path: str) -> Union[str, None]:
    """
    Read a PDF/DOCX file and return its text content.
    """

    if not os.path.exists(file_path):
        print(f"The file '{file_path}' does not exist.")
        return None

    file_extension = pathlib.Path(file_path).suffix.lower()

    if file_extension not in settings.allowed_file_types:
        print(f"File type {file_extension} is not allowed.")
        return None

    text = ""

    with open(file_path, "rb") as f:
        if file_extension == ".pdf":
            reader = PdfReader(f)
            text = "\n\n".join(page.extract_text() or "" for page in reader.pages)

        # elif file_extension == ".docx":
        #     doc = docx.Document(f)
        #     text = " ".join(p.text for p in doc.paragraphs)

    return text.strip() if text else None
