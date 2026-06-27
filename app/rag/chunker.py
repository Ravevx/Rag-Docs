import pdfplumber
import pymupdf
from typing import List
import io


def extract_text_from_pdf(file_bytes: bytes) -> str:
    text = ""
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception:
        pass

    if not text.strip():
        try:
            doc = pymupdf.open(stream=file_bytes, filetype="pdf")
            for page in doc:
                text += page.get_text() + "\n"
        except Exception:
            pass

    return text


def extract_text_from_markdown(file_bytes: bytes) -> str:
    return file_bytes.decode("utf-8", errors="ignore")


def chunk_text(text: str, chunk_size: int = 150, overlap: int = 50) -> List[str]:
    words = text.split()

    if not words:
        return []

    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap

    return [c for c in chunks if len(c.strip()) > 20]