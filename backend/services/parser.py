"""
CV Parser Service — CareerPilot

PDF  → Gemini 2.0 Flash multimodal (handles multi-column Canva/Figma CVs)
DOCX → python-docx (pure Python, no ML, Railway-safe)

NEVER use: pypdf, pdfplumber, pdfminer, docling, unstructured
"""

import io
import os
from google import genai
from google.genai import types
from docx import Document

# Re-use the configured genai client; GOOGLE_API_KEY must be set in env
_client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY", ""))

_PDF_PROMPT = (
    "You are a CV parser. Extract the full text content from this CV/resume exactly "
    "as it appears, preserving all sections (Skills, Experience, Education, Projects, etc.). "
    "Return only the extracted plain text, nothing else."
)


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Parse a PDF CV using Gemini 2.0 Flash multimodal."""
    pdf_part = types.Part.from_bytes(data=file_bytes, mime_type="application/pdf")
    response = _client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[_PDF_PROMPT, pdf_part],
    )
    return response.text or ""


def extract_text_from_docx(file_bytes: bytes) -> str:
    """Parse a DOCX CV using python-docx."""
    doc = Document(io.BytesIO(file_bytes))
    return "\n".join(para.text for para in doc.paragraphs if para.text.strip())


def route_parser(file_bytes: bytes, filename: str) -> str:
    """Route to the correct parser based on file extension."""
    lower = filename.lower()
    if lower.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)
    elif lower.endswith(".docx"):
        return extract_text_from_docx(file_bytes)
    else:
        raise ValueError(f"Unsupported file format: {filename}")
