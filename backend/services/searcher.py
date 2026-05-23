"""
Hybrid Search Service — CareerPilot

Always call the hybrid_search stored procedure via Supabase RPC.
NEVER write raw SQL for search.
"""

from db.supabase import supabase
from services.embedder import embed_query


async def hybrid_search(
    query: str,
    user_id: str,
    match_count: int = 5,
) -> list[dict]:
    """
    Run hybrid search (dense + BM25 + RRF) over cv_chunks for a given user.

    Returns a list of matching chunk dicts with at least: content, section, similarity.
    """
    query_embedding = embed_query(query)

    result = await supabase.rpc(
        "hybrid_search",
        {
            "query_embedding": query_embedding,
            "query_text": query,
            "match_count": match_count,
            "p_user_id": user_id,
        },
    ).execute()

    return result.data or []


async def search_by_section(
    query: str,
    user_id: str,
    section: str,
    match_count: int = 3,
) -> list[dict]:
    """
    Run hybrid search filtered to a specific CV section.
    section must be one of: skills | experience | education | projects
    """
    query_embedding = embed_query(query)

    result = await supabase.rpc(
        "hybrid_search",
        {
            "query_embedding": query_embedding,
            "query_text": query,
            "match_count": match_count,
            "p_user_id": user_id,
            "p_section": section,
        },
    ).execute()

    return result.data or []
