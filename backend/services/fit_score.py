"""
Fit Score Service — CareerPilot

Algorithm (from AGENTS.md):
  Section weights: skills 40%, experience 35%, education 15%, projects 10%
  1. Embed the job description
  2. Hybrid search for top-k CV chunks per section
  3. Compute cosine similarity between JD embedding and each chunk
  4. Weighted average across sections
  5. Multiply by 100 → integer 0–100
  6. Pass score + evidence to Gemini for one-sentence explanation

NEVER ask the LLM to guess a score.
"""

import os
import numpy as np
from google import genai
from services.embedder import embed_query, embed_documents
from services.searcher import search_by_section

_client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY", ""))

SECTION_WEIGHTS: dict[str, float] = {
    "skills":     0.40,
    "experience": 0.35,
    "education":  0.15,
    "projects":   0.10,
}


def _cosine(a: list[float], b: list[float]) -> float:
    va = np.array(a, dtype=float)
    vb = np.array(b, dtype=float)
    denom = np.linalg.norm(va) * np.linalg.norm(vb)
    if denom == 0:
        return 0.0
    return float(np.dot(va, vb) / denom)


async def compute_fit_score(
    job_description: str,
    user_id: str,
) -> dict:
    """
    Compute a programmatic fit score (0–100) for a user's CV against a job description.

    Returns:
        {
            "score": int,           # 0–100
            "explanation": str,     # one-sentence from Gemini
            "section_scores": dict  # per-section cosine scores
        }
    """
    jd_embedding = embed_query(job_description)

    section_scores: dict[str, float] = {}
    evidence_snippets: list[str] = []

    for section in SECTION_WEIGHTS:
        chunks = await search_by_section(
            query=job_description,
            user_id=user_id,
            section=section,
            match_count=3,
        )
        if not chunks:
            section_scores[section] = 0.0
            continue

        chunk_texts = [c["content"] for c in chunks]
        chunk_embeddings = embed_documents(chunk_texts)

        sims = [_cosine(jd_embedding, emb) for emb in chunk_embeddings]
        section_scores[section] = float(np.mean(sims))

        # Collect best snippet for Gemini explanation
        best_idx = int(np.argmax(sims))
        evidence_snippets.append(f"[{section}] {chunk_texts[best_idx][:200]}")

    # Weighted average
    weighted_score = sum(
        section_scores.get(sec, 0.0) * weight
        for sec, weight in SECTION_WEIGHTS.items()
    )
    score_int = min(100, max(0, round(weighted_score * 100)))

    # Gemini one-sentence explanation
    evidence_text = "\n".join(evidence_snippets) if evidence_snippets else "No CV data available."
    explanation_prompt = (
        f"Job description excerpt: {job_description[:500]}\n\n"
        f"Candidate CV evidence:\n{evidence_text}\n\n"
        f"The candidate's fit score is {score_int}/100. "
        "In exactly ONE sentence, explain why this score makes sense, "
        "highlighting the strongest match or biggest gap."
    )
    gemini_response = _client.models.generate_content(
        model="gemini-2.0-flash",
        contents=explanation_prompt,
    )
    explanation = (gemini_response.text or "").strip()

    return {
        "score": score_int,
        "explanation": explanation,
        "section_scores": {k: round(v * 100, 1) for k, v in section_scores.items()},
    }
