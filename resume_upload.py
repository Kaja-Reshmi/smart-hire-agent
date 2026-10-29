
from pathlib import Path
from io import BytesIO

from docx import Document
from pypdf import PdfReader


def extract_resume_text(filename, file_bytes):
    """Extract text from an uploaded PDF or DOCX résumé."""
    extension = Path(filename).suffix.lower()

    if extension == ".pdf":
        reader = PdfReader(BytesIO(file_bytes))
        text = "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )

    elif extension == ".docx":
        document = Document(BytesIO(file_bytes))
        text = "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )

    else:
        raise ValueError("Only PDF and DOCX files are supported.")

    if not text.strip():
        raise ValueError(
            "No readable text found. The PDF may be scanned or image-based."
        )

    return text
