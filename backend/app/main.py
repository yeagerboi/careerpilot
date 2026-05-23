from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.core.embedding import process_and_store_resume
from app.agents.graph import CareerPilotAgent
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    user_id: str
    message: str
    history: List[dict] = []

class JobRequest(BaseModel):
    user_id: str
    query: str

@app.post("/upload-resume")
async def upload_resume(user_id: str, file: UploadFile = File(...)):
    try:
        contents = await file.read()
        result = process_and_store_resume(user_id, contents, file.filename)
        return result
    except Exception as e:
        return {"status": "error", "detail": str(e)}

@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        agent = CareerPilotAgent(req.user_id)
        from langchain_core.messages import HumanMessage, AIMessage
        history_mapped = [HumanMessage(content=h['content']) if h['role']=='user' else AIMessage(content=h['content']) for h in req.history]
        response = await agent.chat(req.message, history_mapped)
        return {"response": response}
    except Exception as e:
        return {"response": f"Sorry, I encountered an error: {str(e)}"}

@app.post("/hunt-jobs")
async def hunt_jobs(req: JobRequest):
    try:
        agent = CareerPilotAgent(req.user_id)
        jobs = await agent.hunt_jobs(req.query)
        return {"jobs": jobs}
    except Exception as e:
        return {"jobs": [], "error": str(e)}