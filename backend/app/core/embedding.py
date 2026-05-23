from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.database import supabase
from app.core.parser import chunk_text, extract_text_from_pdf, extract_text_from_docx
import os

os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY", "")

embeddings_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

def process_and_store_resume(user_id: str, file_bytes: bytes, filename: str):
    if filename.endswith('.pdf'):
        text = extract_text_from_pdf(file_bytes)
    elif filename.endswith('.docx'):
        text = extract_text_from_docx(file_bytes)
    else:
        raise ValueError("Unsupported file format")

    chunks = chunk_text(text)
    
    # Generate embeddings
    vectors = embeddings_model.embed_documents(chunks)
    
    # Store in Supabase pgvector
    data_to_insert = [
        {"user_id": user_id, "content": chunk, "embedding": vector}
        for chunk, vector in zip(chunks, vectors)
    ]
    
    # Assuming a table 'resume_chunks' exists with columns: user_id, content, embedding
    supabase.table("resume_chunks").insert(data_to_insert).execute()
    return {"status": "success", "chunks": len(chunks)}

def query_resume_context(user_id: str, query: str, top_k: int = 3) -> list[str]:
    query_vector = embeddings_model.embed_query(query)
    
    # RPC call to a Supabase match function (assumes you created the function in Supabase SQL)
    response = supabase.rpc('match_resume_chunks', {
        'query_embedding': query_vector,
        'match_user_id': user_id,
        'match_count': top_k
    }).execute()
    
    return [item['content'] for item in response.data]