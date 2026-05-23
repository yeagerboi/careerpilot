"""
CV Router — CareerPilot (Pillar 2: CV Intelligence)

Handles:
  POST /cv/upload  — parse, chunk, embed and store a CV
  GET  /cv/{user_id} — fetch CV metadata for a user
"""

import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from db.supabase import supabase
from services.parser import route_parser
from services.embedder import embed_documents

router = APIRouter(prefix="/cv", tags=["cv"])

# CV section keywords used for naive section classification
_SECTION_KEYWORDS: dict[str, list[str]] = {
    "skills":     ["skill", "technology", "tech stack", "tools", "language", "framework", "proficiency"],
    "experience": ["experience", "work", "employment", "job", "role", "position", "intern"],
    "education":  ["education", "degree", "university", "college", "school", "cgpa", "gpa", "academic"],
    "projects":   ["project", "built", "developed", "created", "portfolio", "github"],
}


def _classify_section(chunk: str) -> str:
    """Classify a text chunk into one of the four allowed section labels."""
    lower = chunk.lower()
    scores: dict[str, int] = {
        sec: sum(kw in lower for kw in kws)
        for sec, kws in _SECTION_KEYWORDS.items()
    }
    best = max(scores, key=lambda s: scores[s])
    # Default to experience if no keyword matches
    return best if scores[best] > 0 else "experience"


def _chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """Split text into overlapping chunks."""
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


class CVMeta(BaseModel):
    user_id: str
    file_name: str


@router.post("/upload")
async def upload_cv(user_id: str, file: UploadFile = File(...)):
    """
    Upload, parse, chunk, embed and store a CV.
    Stores metadata in `cvs` table and chunks in `cv_chunks` table.
    """
    filename = file.filename or "unknown"
    if not (filename.lower().endswith(".pdf") or filename.lower().endswith(".docx")):
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported.")

    file_bytes = await file.read()

    # 1. Parse CV text
    try:
        text = route_parser(file_bytes, filename)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"CV parsing failed: {e}")

    if not text.strip():
        raise HTTPException(status_code=422, detail="Could not extract text from CV.")

    # 2. Insert CV metadata into `cvs` table
    cv_id = str(uuid.uuid4())
    cv_meta_result = await supabase.table("cvs").insert({
        "id":        cv_id,
        "user_id":   user_id,
        "file_name": filename,
    }).execute()

    if not cv_meta_result.data:
        raise HTTPException(status_code=500, detail="Failed to save CV metadata.")

    # 3. Chunk text
    chunks = _chunk_text(text)

    # 4. Embed all chunks with Voyage AI
    try:
        embeddings = embed_documents(chunks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding failed: {e}")

    # 5. Classify each chunk into a section and insert into `cv_chunks`
    rows = [
        {
            "user_id":   user_id,
            "cv_id":     cv_id,
            "section":   _classify_section(chunk),
            "content":   chunk,
            "embedding": embedding,
        }
        for chunk, embedding in zip(chunks, embeddings)
    ]

    await supabase.table("cv_chunks").insert(rows).execute()

    return {
        "status":  "success",
        "cv_id":   cv_id,
        "chunks":  len(chunks),
    }


@router.get("/{user_id}")
async def get_cv(user_id: str):
    """Fetch CV metadata for a user."""
    result = await supabase.table("cvs").select(
        "id, user_id, file_name, parsed_at"
    ).eq("user_id", user_id).order("parsed_at", desc=True).execute()

    return {"cvs": result.data or []}
