from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, SystemMessage
from app.core.embedding import query_resume_context, embeddings_model
from app.agents.matching import calculate_fit_score
from dotenv import load_dotenv
import os
import json

load_dotenv()
model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
llm = ChatGoogleGenerativeAI(model=model_name, temperature=0.3, google_api_key=os.getenv("GEMINI_API_KEY"))
search = TavilySearchResults(max_results=3)

class CareerPilotAgent:
    def __init__(self, user_id: str):
        self.user_id = user_id
        tools = [search]
        self.agent = create_react_agent(llm, tools)

    async def hunt_jobs(self, query: str):
        # 1. Get User Context
        try:
            cv_context = "\n".join(query_resume_context(self.user_id, query))
        except Exception:
            cv_context = ""
        
        # 2. Agent searches web
        prompt = f"""
        You are a Job Hunter Agent. The user wants: {query}
        Their CV context: {cv_context}
        Use the Tavily search tool to find real jobs. Return a JSON array of jobs with keys: role, company, location, deadline, url.
        Return ONLY the JSON array, no other text.
        """
        result = await self.agent.ainvoke({"messages": [HumanMessage(content=prompt)]})
        
        # 3. Calculate Fit Score
        try:
            raw_content = result['messages'][-1].content
            # Try to extract JSON from the response
            start = raw_content.find('[')
            end = raw_content.rfind(']') + 1
            if start != -1 and end > start:
                jobs = json.loads(raw_content[start:end])
            else:
                jobs = []
        except (json.JSONDecodeError, KeyError, IndexError):
            jobs = []

        for job in jobs:
            try:
                job_desc_vector = embeddings_model.embed_query(job.get('role', '') + " " + job.get('location', ''))
                user_vector = embeddings_model.embed_query(cv_context.split('.')[0] if cv_context else "developer")
                job['fit_score'] = calculate_fit_score(user_vector, job_desc_vector)
            except Exception:
                job['fit_score'] = 0.0
            
        return jobs

    async def chat(self, message: str, history: list):
        try:
            cv_context = "\n".join(query_resume_context(self.user_id, message))
        except Exception:
            cv_context = "No resume uploaded yet."
        
        system_msg = f"You are CareerPilot AI, a helpful career assistant. Answer grounded in the user's CV context: {cv_context}"
        messages = [SystemMessage(content=system_msg)] + history + [HumanMessage(content=message)]
        response = await llm.ainvoke(messages)
        return response.content