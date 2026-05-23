"""
Chat Router — CareerPilot (Pillar 3: AI Assistant)

Streaming chat via Server-Sent Events (SSE).
LLM: Llama 3.3 70B via Groq (NEVER use Gemini for chat).
RAG: hybrid_search over user's cv_chunks for context injection.
Memory: last N messages fetched from chat_messages table.
"""

import os
import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from groq import Groq
from db.supabase import supabase
from services.searcher import hybrid_search

router = APIRouter(prefix="/chat", tags=["chat"])

_groq = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))
_MODEL = "llama-3.3-70b-versatile"
_MEMORY_LIMIT = 10  # last 10 messages for session memory


class ChatRequest(BaseModel):
    user_id: str
    session_id: str
    message: str


async def _get_session_history(user_id: str, session_id: str) -> list[dict]:
    """Fetch last N messages for this session from Supabase."""
    result = await supabase.table("chat_messages").select(
        "role, content"
    ).eq("user_id", user_id).eq("session_id", session_id).order(
        "created_at", desc=True
    ).limit(_MEMORY_LIMIT).execute()

    messages = result.data or []
    # Reverse to chronological order
    return list(reversed(messages))


async def _save_message(user_id: str, session_id: str, role: str, content: str) -> None:
    """Persist a chat message to Supabase."""
    await supabase.table("chat_messages").insert({
        "user_id":    user_id,
        "session_id": session_id,
        "role":       role,
        "content":    content,
    }).execute()


@router.post("/")
async def chat_endpoint(req: ChatRequest):
    """
    Streaming SSE chat endpoint.
    1. Fetch CV context via hybrid_search (RAG)
    2. Fetch session memory from chat_messages
    3. Stream response from Groq Llama 3.3 70B
    4. Persist user message and assistant reply
    """
    # 1. RAG — get CV context
    try:
        cv_chunks = await hybrid_search(
            query=req.message,
            user_id=req.user_id,
            match_count=5,
        )
        cv_context = "\n".join(c["content"] for c in cv_chunks)
    except Exception:
        cv_context = "No CV uploaded yet."

    # 2. Session memory
    history = await _get_session_history(req.user_id, req.session_id)

    # 3. Build messages for Groq
    system_prompt = (
        "You are CareerPilot AI, an expert career co-pilot. "
        "You help users find jobs, improve their CVs, write cover letters, and plan their careers. "
        "Always ground your answers in the user's actual CV context when available.\n\n"
        f"User CV context:\n{cv_context or 'No CV data available.'}"
    )

    groq_messages = [{"role": "system", "content": system_prompt}]
    for msg in history:
        groq_messages.append({"role": msg["role"], "content": msg["content"]})
    groq_messages.append({"role": "user", "content": req.message})

    # 4. Save user message before streaming
    await _save_message(req.user_id, req.session_id, "user", req.message)

    # 5. Stream from Groq — SSE generator
    async def generate():
        full_reply = []
        try:
            stream = _groq.chat.completions.create(
                model=_MODEL,
                messages=groq_messages,
                stream=True,
                temperature=0.4,
                max_tokens=1024,
            )
            for chunk in stream:
                token = chunk.choices[0].delta.content or ""
                if token:
                    full_reply.append(token)
                    yield f"data: {json.dumps({'token': token})}\n\n"

            # Save full assistant reply
            await _save_message(
                req.user_id, req.session_id, "assistant", "".join(full_reply)
            )
            yield "data: [DONE]\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
