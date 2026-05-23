# DEV 1 — Backend & Infrastructure

**CareerPilot · Codesprint 2026**

> You own: Backend (FastAPI), Database (Supabase), All APIs, Agent Logic, RAG Pipeline
> Your partner owns: Frontend (Next.js), UI Components, Deployment

---

## Your Responsibilities

**Core Systems:**

- ✅ FastAPI backend (all routes, services, business logic)
- ✅ Supabase schema (tables, indexes, stored procedures, pg_cron)
- ✅ CV parsing (PDF via Gemini, DOCX via python-docx)
- ✅ RAG pipeline (embeddings, vector storage, hybrid search)
- ✅ Fit score algorithm (weighted cosine similarity)
- ✅ LangGraph agent (job search orchestration)
- ✅ Chat service (streaming, memory, RAG context)
- ✅ Job search APIs (JSearch, Remotive, Tavily)
- ✅ Redis caching (Upstash)
- ✅ All backend endpoints

**Not Your Responsibility:**

- ❌ Frontend code (Next.js, React components, Tailwind)
- ❌ UI design or styling
- ❌ Vercel deployment (your partner handles this)

---

## Day-by-Day Tasks

### Day 1 — Foundation (6–8 hours)

**Goal:** Database live, backend initialized, all API keys working

#### Morning

- [ ] Create Supabase project at supabase.com
- [ ] Run all SQL migrations (see CareerPilot_Stack_Final.md Section 8):

  ```sql
  -- Enable pgvector
  create extension if not exists vector;

  -- Create all tables: cvs, cv_chunks, jobs, applications,
  -- chat_messages, goals, todos, nudges, progress_snapshots

  -- Create indexes (HNSW for embeddings, GIN for full-text)

  -- Create hybrid_search stored procedure
  ```

- [ ] Enable Supabase Realtime on `applications` and `nudges` tables
- [ ] Set up Supabase Auth (Email + Password provider)

#### Afternoon

- [ ] Get all API keys:
  - Groq (groq.com)
  - Google AI Studio (aistudio.google.com)
  - Voyage AI (voyageai.com)
  - Upstash Redis (upstash.com)
  - JSearch via RapidAPI
  - Tavily (tavily.com)
- [ ] Create `backend/.env` with all keys
- [ ] Initialize backend:
  ```bash
  cd backend
  python -m venv venv
  source venv/bin/activate  # Windows: venv\Scripts\activate
  pip install -r requirements.txt
  ```
- [ ] Create `backend/requirements.txt`:
  ```
  fastapi==0.115.0
  uvicorn==0.30.6
  python-multipart==0.0.9
  httpx==0.27.0
  google-generativeai==0.8.3
  voyageai==0.3.2
  python-docx==1.1.2
  supabase==2.7.4
  upstash-redis==1.1.0
  groq==0.11.0
  scikit-learn==1.5.2
  numpy==1.26.4
  python-dotenv==1.0.1
  langgraph==0.2.28
  langchain-core==0.3.15
  langchain-groq==0.2.0
  psutil==6.0.0
  ```
- [ ] Create `backend/main.py` with basic FastAPI app
- [ ] Create `backend/db/supabase.py` with Supabase client
- [ ] Test connection: `uvicorn main:app --reload`

**Deliverable:** Backend running on localhost:8000, Supabase accessible

---

### Day 2 — CV Parsing (6–8 hours)

**Goal:** Upload endpoint working, both parsers returning structured JSON

#### Morning

- [ ] Create `backend/services/parser.py`:

  ```python
  async def parse_pdf_cv(file: UploadFile) -> dict:
      # Gemini 2.0 Flash multimodal
      # Return: {"skills": str, "experience": str, "education": str, "projects": str}

  async def parse_docx_cv(file: UploadFile) -> dict:
      # python-docx + Gemini for structuring
      # Return same schema
  ```

- [ ] Create `backend/routers/cv.py`:
  ```python
  @router.post("/api/cv/upload")
  async def upload_cv(file: UploadFile):
      # Route to correct parser based on file extension
      # Save to Supabase Storage
      # Save metadata to cvs table
      # Return parsed JSON
  ```
- [ ] Test with 3 CVs: single-column PDF, multi-column PDF, DOCX

#### Afternoon

- [ ] Add error handling (file size, type validation, parsing failures)
- [ ] Add Supabase Storage integration (bucket: `cv-files`)
- [ ] Memory profiling with psutil (verify < 512 MB)
- [ ] Register route in `main.py`

**Deliverable:** `POST /api/cv/upload` working, returns parsed JSON

**Handoff to DEV2:** Share Supabase URL and anon key for frontend integration

---

### Day 3 — Embeddings & Vector Storage (6–8 hours)

**Goal:** CV chunks embedded and stored, hybrid search working

#### Morning

- [ ] Create `backend/services/embedder.py`:

  ```python
  def embed_chunks(chunks: list[str]) -> list[list[float]]:
      # Voyage AI voyage-3, input_type="document"

  def embed_query(query: str) -> list[float]:
      # Voyage AI voyage-3, input_type="query"

  # Add fallback to Gemini embeddings if Voyage fails
  ```

- [ ] Add chunking to `parser.py`:
  ```python
  def chunk_cv(parsed: dict, cv_id: str, user_id: str) -> list[dict]:
      # One chunk per section: skills, experience, education, projects
      # Return list of chunks with metadata
  ```
- [ ] Update `/api/cv/upload`:
  - Parse → chunk → embed → store in `cv_chunks` table

#### Afternoon

- [ ] Create `backend/services/searcher.py`:
  ```python
  async def search_cv_chunks(query: str, user_id: str, top_k: int) -> list[dict]:
      # Call Supabase RPC hybrid_search
  ```
- [ ] Test hybrid search with 3 different CVs
- [ ] Create test endpoint: `GET /api/cv/search?q=Python`

**Deliverable:** CV chunks stored with embeddings, hybrid search returns relevant results

---

### Day 4 — Fit Score & Job Search (8–10 hours)

**Goal:** Fit score algorithm working, job APIs integrated

#### Morning

- [ ] Create `backend/services/fit_score.py`:
  ```python
  async def compute_fit_score(job_description: str, user_id: str) -> dict:
      # 1. Embed JD
      # 2. Hybrid search per section
      # 3. Cosine similarity per section
      # 4. Weighted average (skills 40%, experience 35%, education 15%, projects 10%)
      # 5. Gemini explanation
      # Return: {"score": int, "explanation": str, "breakdown": dict}
  ```
- [ ] Test with 5 JDs (senior/junior mismatch, exact match, no overlap, partial)

#### Afternoon

- [ ] Create `backend/services/job_search.py`:
  ```python
  async def search_jsearch(query: str, location: str) -> list[dict]
  async def search_remotive(query: str) -> list[dict]
  async def search_tavily(query: str, location: str) -> list[dict]
  async def search_jobs(query: str, location: str) -> list[dict]:
      # Three-tier fallback
  ```
- [ ] Create `backend/services/cache.py`:
  ```python
  async def cached_job_search(query: str, location: str) -> list[dict]:
      # Redis cache, TTL 7200 seconds
  ```
- [ ] Create `backend/routers/jobs.py`:
  ```python
  @router.post("/api/jobs/search")
  async def search_jobs_endpoint(request: JobSearchRequest):
      # Return list of job cards with fit scores
  ```

**Deliverable:** Fit score tested, job search working from all 3 APIs

**Handoff to DEV2:** API endpoint ready for frontend integration

---

### Day 5 — LangGraph Agent & Chat (8–10 hours)

**Goal:** Agent loop working, streaming chat with memory

#### Morning

- [ ] Create `backend/services/agent.py`:

  ```python
  from langgraph.graph import StateGraph, END

  class AgentState(TypedDict):
      query: str
      user_id: str
      jobs: List[dict]
      scored_jobs: List[dict]
      iterations: int

  # Define nodes: search_node, score_node, filter_node
  # Define conditional edge: should_retry
  # Compile graph

  async def run_job_hunter_agent(query: str, user_id: str) -> dict
  ```

- [ ] Create LangChain tools (search, fit_score, cv_context, cover_letter)
- [ ] Test agent: "Find me ML internships in Dhaka"

#### Afternoon

- [ ] Create `backend/services/chat.py`:
  ```python
  async def get_chat_history(user_id: str, session_id: str) -> list[dict]
  async def save_message(user_id: str, session_id: str, role: str, content: str)
  async def stream_chat(user_id: str, session_id: str, message: str, cv_context: str):
      # Fetch history → RAG query → Groq stream → save
      # Yield tokens via AsyncGenerator
  ```
- [ ] Create `backend/routers/chat.py`:
  ```python
  @router.post("/api/chat")
  async def chat_endpoint(request: ChatRequest):
      # SSE streaming
      async def generate():
          async for token in chat_service.stream(...):
              yield f"data: {token}\n\n"
      return StreamingResponse(generate(), media_type="text/event-stream")
  ```
- [ ] Test streaming with follow-up questions

**Deliverable:** Agent working, streaming chat with memory and RAG

**Handoff to DEV2:** Chat endpoint ready for frontend streaming integration

---

### Day 6 — REST (Your Day Off)

**Goal:** Let DEV2 build frontend scaffold while you rest or review code

- [ ] Optional: Review Days 1-5 code
- [ ] Optional: Write docstrings
- [ ] Optional: Add logging
- [ ] Optional: Start thinking about Day 9-10 tracker endpoints

**No new features today. DEV2 is building the UI.**

---

### Day 7 — Backend Deployment (2–3 hours)

**Goal:** Backend deployed to Railway

#### Morning

- [ ] Create `backend/Dockerfile`:
  ```dockerfile
  FROM python:3.11-slim
  WORKDIR /app
  COPY requirements.txt .
  RUN pip install --no-cache-dir -r requirements.txt
  COPY . .
  CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
  ```
- [ ] Push backend to GitHub
- [ ] Connect repo at railway.app
- [ ] Add all environment variables in Railway dashboard
- [ ] Get Railway URL: `https://your-app.railway.app`
- [ ] Test deployed endpoints with curl

**Deliverable:** Backend live at Railway URL

**Handoff to DEV2:** Share Railway URL for `NEXT_PUBLIC_API_URL`

#### Afternoon

- [ ] Help DEV2 with any frontend integration issues
- [ ] Monitor Railway logs for errors
- [ ] Fix any deployment issues

---

### Day 8 — REST (Your Day Off)

**Goal:** Let DEV2 build streaming chat UI

- [ ] Optional: Monitor backend logs
- [ ] Optional: Optimize slow endpoints
- [ ] Optional: Add request validation

**No new features today. DEV2 is building chat UI.**

---

### Day 9 — Tracker Endpoints (3–4 hours)

**Goal:** All tracker CRUD endpoints working

#### Morning/Afternoon

- [ ] Create `backend/routers/tracker.py`:

  ```python
  @router.get("/api/applications")
  async def get_applications(user_id: str)

  @router.post("/api/applications")
  async def create_application(request: ApplicationCreate)

  @router.patch("/api/applications/{id}")
  async def update_application(id: str, request: ApplicationUpdate)

  @router.delete("/api/applications/{id}")
  async def delete_application(id: str)

  @router.get("/api/goals")
  async def get_goals(user_id: str)

  @router.post("/api/goals")
  async def create_goal(request: GoalCreate)

  @router.get("/api/todos")
  async def get_todos(user_id: str, date: Optional[str])

  @router.post("/api/todos")
  async def create_todo(request: TodoCreate)

  @router.patch("/api/todos/{id}")
  async def toggle_todo(id: str)
  ```

- [ ] Test all endpoints with Postman or curl

**Deliverable:** All tracker endpoints working

**Handoff to DEV2:** Endpoints ready for Kanban/Calendar integration

---

### Day 10 — Dashboard & AI Nudges (4–5 hours)

**Goal:** Dashboard stats endpoint, pg_cron nudges

#### Morning

- [ ] Create `backend/routers/dashboard.py`:
  ```python
  @router.get("/api/dashboard/stats")
  async def get_dashboard_stats(user_id: str):
      # Query progress_snapshots table
      # Return: applications_sent, skills_added, roadmap_pct, streak_days
  ```
- [ ] Test dashboard endpoint

#### Afternoon

- [ ] Set up AI nudges in Supabase:
  ```sql
  -- Enable pg_cron in Supabase dashboard
  select cron.schedule(
    'weekly-nudge',
    '0 9 * * 1',  -- Every Monday 9 AM UTC
    $$
    insert into nudges (user_id, message, job_ids)
    select u.id, 'You have not applied...', array(...)
    from auth.users u
    where not exists (select 1 from applications ...);
    $$
  );
  ```
- [ ] Test nudge insertion manually

**Deliverable:** Dashboard endpoint working, pg_cron configured

---

### Day 11 — Seed Data & Bug Fixes (3–4 hours)

**Goal:** Database seeded, backend bugs fixed

#### Morning

- [ ] Create `backend/scripts/seed.py`:
  ```python
  # 3 sample CVs (upload via API)
  # 20 sample jobs (insert into jobs table)
  # 5 applications (different statuses)
  # 3 goals with todos
  # 1 progress snapshot (realistic stats)
  # 10 chat messages
  ```
- [ ] Run seed script on deployed database
- [ ] Create test user: `demo@careerpilot.com` / `Demo123!`

#### Afternoon

- [ ] Bug hunt: test all endpoints end-to-end
- [ ] Fix error handling
- [ ] Add request validation (Pydantic models)
- [ ] Check Railway logs for errors

**Deliverable:** Fully seeded database, all backend bugs fixed

---

### Day 12–14 — Support & Documentation (2–3 hours/day)

**Goal:** Help DEV2 with integration, write docs

- [ ] Day 12: Help with any frontend integration issues
- [ ] Day 13: Write API documentation (endpoints, request/response schemas)
- [ ] Day 13: Update README with backend setup instructions
- [ ] Day 14: Monitor backend during demo video recording
- [ ] Day 14: Final backend testing

---

## Your Tech Stack (Memorize This)

### LLMs

- **Streaming chat:** Groq Llama 3.3 70B (`from groq import Groq`)
- **Reasoning/parsing:** Gemini 2.0 Flash (`from google import genai`)

### Parsers

- **PDF:** Gemini multimodal (`types.Part.from_bytes`)
- **DOCX:** python-docx (`from docx import Document`)

### Embeddings

- **Primary:** Voyage AI voyage-3 (`import voyageai`)
- **Fallback:** Gemini embeddings

### Database

- **Supabase:** PostgreSQL + pgvector + Auth + Realtime
- **Client:** `from supabase import create_client`

### Cache

- **Upstash Redis:** `from upstash_redis import Redis`

### Job APIs

1. **JSearch** (RapidAPI) — primary
2. **Remotive** — fallback
3. **Tavily** — local BD fallback

### Agent

- **LangGraph:** `from langgraph.graph import StateGraph`

---

## Environment Variables (backend/.env)

```bash
GROQ_API_KEY=
GOOGLE_API_KEY=
VOYAGE_API_KEY=
SUPABASE_URL=
SUPABASE_SERVICE_ROLE_KEY=
UPSTASH_REDIS_REST_URL=
UPSTASH_REDIS_REST_TOKEN=
JSEARCH_API_KEY=
TAVILY_API_KEY=
```

---

## Forbidden (Never Use These)

```
❌ import openai
❌ from anthropic import Anthropic
❌ import docling
❌ import pypdf
❌ from langchain import ...  (use LangGraph directly)
❌ Hardcoded API keys
❌ Synchronous code (always async def)
❌ Raw dicts in routes (use Pydantic models)
```

---

## Communication with DEV2

### What to share:

- ✅ Supabase URL and anon key (Day 1)
- ✅ Railway backend URL (Day 7)
- ✅ API endpoint schemas (as you build them)
- ✅ Test user credentials (Day 11)

### What to ask for:

- ✅ Frontend deployment URL (Day 7)
- ✅ UI feedback on API response formats
- ✅ Error messages from frontend console

### Daily sync (5 minutes):

- Morning: "Today I'm building X"
- Evening: "X is done, endpoint is Y, here's how to use it"

---

## Success Metrics

By Day 14, you should have:

- [x] All backend endpoints working
- [x] Backend deployed to Railway
- [x] Database fully seeded
- [x] All APIs integrated (Groq, Gemini, Voyage, JSearch, Remotive, Tavily)
- [x] LangGraph agent working
- [x] Streaming chat with memory
- [x] Fit score algorithm tested
- [x] Zero backend errors during demo

**If you have all of these, you've done your job perfectly.**

---

_DEV1 Backend Guide · CareerPilot · Codesprint 2026_
_Related: AGENTS.md · CareerPilot_Stack_Final.md · TIMELINE.md_
