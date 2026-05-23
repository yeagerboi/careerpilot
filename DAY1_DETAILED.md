# DAY 1 — Foundation Setup (Detailed AI-Executable Guide)

**CareerPilot · Codesprint 2026 · DEV1 Backend**

> This is a step-by-step guide for AI agents (Kiro/Antigravity IDE) to execute Day 1 tasks.
> Every command, every file, every configuration is specified exactly.

**Estimated Time:** 6–8 hours
**Goal:** Database live, backend initialized, all API keys configured, environment working

---

## Prerequisites Check

Before starting, verify:

- [ ] You have internet connection
- [ ] You have a GitHub account
- [ ] You have a code editor (VS Code, Cursor, or Kiro IDE)
- [ ] You have Python 3.11+ installed (`python --version`)
- [ ] You have Git installed (`git --version`)

---

## PHASE 1 — Supabase Setup (90 minutes)

### Step 1.1: Create Supabase Project (10 minutes)

1. Go to https://supabase.com
2. Click "Start your project"
3. Sign in with GitHub
4. Click "New project"
5. Fill in:
   - **Name:** `careerpilot`
   - **Database Password:** Generate strong password (SAVE THIS)
   - **Region:** Choose closest to Bangladesh (Singapore recommended)
   - **Pricing Plan:** Free
6. Click "Create new project"
7. Wait 2-3 minutes for provisioning

**Save these values (you'll need them):**

- Project URL: `https://xxxxx.supabase.co`
- Anon key: `eyJhbGc...` (from Settings → API)
- Service role key: `eyJhbGc...` (from Settings → API)

---

### Step 1.2: Enable pgvector Extension (5 minutes)

1. In Supabase dashboard, go to **Database → Extensions**
2. Search for `vector`
3. Enable `vector` extension
4. Verify: Green checkmark appears

---

### Step 1.3: Run SQL Migrations (30 minutes)

1. In Supabase dashboard, go to **SQL Editor**
2. Click "New query"
3. Copy and paste this SQL (execute in order):

**Migration 1: Enable pgvector**

```sql
-- Enable pgvector extension
create extension if not exists vector;
```

Click "Run" (bottom right)

**Migration 2: Create cvs table**

```sql
-- CV metadata table
create table cvs (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users(id) on delete cascade,
  file_name text not null,
  file_url text,
  parsed_at timestamptz,
  created_at timestamptz default now()
);

-- Index for fast user lookups
create index cvs_user_id_idx on cvs(user_id);
```

Click "Run"

**Migration 3: Create cv_chunks table**

```sql
-- CV chunks with embeddings
create table cv_chunks (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users(id) on delete cascade,
  cv_id uuid references cvs(id) on delete cascade,
  section text not null check (section in ('skills', 'experience', 'education', 'projects')),
  content text not null,
  embedding vector(1024),
  fts tsvector generated always as (to_tsvector('english', content)) stored,
  created_at timestamptz default now()
);

-- HNSW index for fast vector similarity search
create index cv_chunks_embedding_idx on cv_chunks
  using hnsw (embedding vector_cosine_ops);

-- GIN index for full-text search
create index cv_chunks_fts_idx on cv_chunks using gin(fts);

-- Index for user lookups
create index cv_chunks_user_id_idx on cv_chunks(user_id);
```

Click "Run"

**Migration 4: Create jobs table**

```sql
-- Cached job search results
create table jobs (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users(id) on delete cascade,
  external_id text,
  title text not null,
  company text not null,
  location text,
  salary_range text,
  deadline text,
  description text,
  source text not null,
  fit_score int check (fit_score >= 0 and fit_score <= 100),
  fit_explanation text,
  cached_at timestamptz default now()
);

create index jobs_user_id_idx on jobs(user_id);
create index jobs_fit_score_idx on jobs(fit_score desc);
```

Click "Run"

**Migration 5: Create applications table**

```sql
-- Application tracker (Kanban)
create table applications (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users(id) on delete cascade,
  job_id uuid references jobs(id) on delete cascade,
  status text not null check (status in ('saved', 'applied', 'interviewing', 'offer', 'rejected')),
  applied_at timestamptz,
  notes text,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

create index applications_user_id_idx on applications(user_id);
create index applications_status_idx on applications(status);
```

Click "Run"

**Migration 6: Create chat_messages table**

```sql
-- Chat memory for conversational context
create table chat_messages (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users(id) on delete cascade,
  session_id uuid not null,
  role text not null check (role in ('user', 'assistant')),
  content text not null,
  created_at timestamptz default now()
);

create index chat_messages_session_idx on chat_messages(session_id, created_at);
create index chat_messages_user_id_idx on chat_messages(user_id);
```

Click "Run"

**Migration 7: Create goals and todos tables**

```sql
-- Goals
create table goals (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users(id) on delete cascade,
  title text not null,
  target_date date,
  completed boolean default false,
  created_at timestamptz default now()
);

-- To-dos linked to goals
create table todos (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users(id) on delete cascade,
  goal_id uuid references goals(id) on delete set null,
  title text not null,
  due_date date,
  completed boolean default false,
  created_at timestamptz default now()
);

create index goals_user_id_idx on goals(user_id);
create index todos_user_id_idx on todos(user_id);
create index todos_due_date_idx on todos(due_date);
```

Click "Run"

**Migration 8: Create nudges table**

```sql
-- AI proactive reminders
create table nudges (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users(id) on delete cascade,
  message text not null,
  job_ids uuid[],
  seen boolean default false,
  created_at timestamptz default now()
);

create index nudges_user_id_idx on nudges(user_id);
create index nudges_seen_idx on nudges(seen) where seen = false;
```

Click "Run"

**Migration 9: Create progress_snapshots table**

```sql
-- Weekly progress tracking
create table progress_snapshots (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users(id) on delete cascade,
  week_start date not null,
  applications_sent int default 0,
  skills_added int default 0,
  roadmap_pct int default 0 check (roadmap_pct >= 0 and roadmap_pct <= 100),
  streak_days int default 0,
  created_at timestamptz default now()
);

create index progress_snapshots_user_id_idx on progress_snapshots(user_id);
create unique index progress_snapshots_user_week_idx on progress_snapshots(user_id, week_start);
```

Click "Run"

**Migration 10: Create hybrid_search stored procedure**

```sql
-- Hybrid search: dense (vector) + sparse (BM25) + RRF merge
create or replace function hybrid_search(
  query_embedding vector(1024),
  query_text text,
  match_count int,
  p_user_id uuid
)
returns table (id uuid, content text, section text, score float)
language sql
as $$
  with semantic as (
    select
      cv_chunks.id,
      cv_chunks.content,
      cv_chunks.section,
      row_number() over (order by cv_chunks.embedding <=> query_embedding) as rank
    from cv_chunks
    where cv_chunks.user_id = p_user_id
    order by cv_chunks.embedding <=> query_embedding
    limit 20
  ),
  keyword as (
    select
      cv_chunks.id,
      cv_chunks.content,
      cv_chunks.section,
      row_number() over (
        order by ts_rank(cv_chunks.fts, plainto_tsquery('english', query_text)) desc
      ) as rank
    from cv_chunks
    where cv_chunks.user_id = p_user_id
      and cv_chunks.fts @@ plainto_tsquery('english', query_text)
    limit 20
  ),
  rrf as (
    select
      coalesce(s.id, k.id) as id,
      coalesce(s.content, k.content) as content,
      coalesce(s.section, k.section) as section,
      coalesce(1.0 / (60 + s.rank), 0.0) + coalesce(1.0 / (60 + k.rank), 0.0) as score
    from semantic s
    full outer join keyword k on s.id = k.id
  )
  select rrf.id, rrf.content, rrf.section, rrf.score
  from rrf
  order by rrf.score desc
  limit match_count;
$$;
```

Click "Run"

**Verify all tables created:**

```sql
-- Check all tables exist
select table_name
from information_schema.tables
where table_schema = 'public'
order by table_name;
```

Click "Run"

Expected output: 9 tables (applications, chat_messages, cv_chunks, cvs, goals, jobs, nudges, progress_snapshots, todos)

---

### Step 1.4: Enable Supabase Realtime (10 minutes)

1. Go to **Database → Replication**
2. Find `applications` table → Toggle ON
3. Find `nudges` table → Toggle ON
4. Verify: Both show green "Enabled"

---

### Step 1.5: Configure Supabase Auth (10 minutes)

1. Go to **Authentication → Providers**
2. Find "Email" provider
3. Toggle ON "Enable Email provider"
4. **Confirm email:** Toggle OFF (for development)
5. Click "Save"

---

### Step 1.6: Create Storage Bucket (10 minutes)

1. Go to **Storage**
2. Click "New bucket"
3. Name: `cv-files`
4. Public: OFF (private)
5. Click "Create bucket"
6. Click on `cv-files` bucket
7. Go to "Policies" tab
8. Click "New policy"
9. Template: "Allow authenticated users to upload"
10. Click "Review" → "Save policy"

---

## PHASE 2 — API Keys Collection (60 minutes)

### Step 2.1: Groq API Key (5 minutes)

1. Go to https://console.groq.com
2. Sign in with Google/GitHub
3. Go to "API Keys"
4. Click "Create API Key"
5. Name: `careerpilot`
6. Copy key: `gsk_...`
7. **SAVE THIS KEY**

---

### Step 2.2: Google AI Studio API Key (5 minutes)

1. Go to https://aistudio.google.com/app/apikey
2. Sign in with Google
3. Click "Create API Key"
4. Select "Create API key in new project"
5. Copy key: `AIza...`
6. **SAVE THIS KEY**

---

### Step 2.3: Voyage AI API Key (10 minutes)

1. Go to https://www.voyageai.com
2. Click "Get Started"
3. Sign up with email
4. Verify email
5. Go to Dashboard → API Keys
6. Click "Create new key"
7. Name: `careerpilot`
8. Copy key: `pa-...`
9. **SAVE THIS KEY**

---

### Step 2.4: Upstash Redis (10 minutes)

1. Go to https://console.upstash.com
2. Sign in with GitHub
3. Click "Create Database"
4. Name: `careerpilot-cache`
5. Type: Regional
6. Region: Choose closest to your location
7. Click "Create"
8. Go to "REST API" tab
9. Copy:
   - `UPSTASH_REDIS_REST_URL`: `https://...`
   - `UPSTASH_REDIS_REST_TOKEN`: `...`
10. **SAVE BOTH**

---

### Step 2.5: JSearch API Key (15 minutes)

1. Go to https://rapidapi.com
2. Sign up with email
3. Search for "JSearch"
4. Go to https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch
5. Click "Subscribe to Test"
6. Select "Basic" plan (FREE)
7. Click "Subscribe"
8. Go to "Endpoints" tab
9. Copy `X-RapidAPI-Key` from code snippet
10. **SAVE THIS KEY**

---

### Step 2.6: Tavily API Key (10 minutes)

1. Go to https://tavily.com
2. Click "Get API Key"
3. Sign up with email
4. Verify email
5. Go to Dashboard
6. Copy API key: `tvly-...`
7. **SAVE THIS KEY**

---

## PHASE 3 — Backend Initialization (90 minutes)

### Step 3.1: Create GitHub Repository (10 minutes)

**Option A: Monorepo (Recommended)**

```bash
# Create local directory
mkdir careerpilot
cd careerpilot

# Initialize git
git init
git branch -M main

# Create .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Environment variables
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Database
*.db
*.sqlite

# Node (for frontend)
node_modules/
.next/
out/
dist/
EOF

# Create README
cat > README.md << 'EOF'
# CareerPilot

Your agentic career co-pilot. Built for Codesprint 2026.

## Setup

See individual README files in `/backend` and `/frontend` directories.
EOF

# Initial commit
git add .
git commit -m "Initial commit"

# Create GitHub repo (via GitHub CLI or web)
# If you have gh CLI:
gh repo create careerpilot --public --source=. --remote=origin --push

# If no gh CLI, create repo on github.com and:
# git remote add origin https://github.com/YOUR_USERNAME/careerpilot.git
# git push -u origin main
```

---

### Step 3.2: Create Backend Directory Structure (5 minutes)

```bash
# Create backend structure
mkdir -p backend/{routers,services,db,scripts}
cd backend

# Create __init__.py files
touch routers/__init__.py
touch services/__init__.py
touch db/__init__.py
touch scripts/__init__.py
```

---

### Step 3.3: Create requirements.txt (5 minutes)

```bash
cat > requirements.txt << 'EOF'
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
pydantic==2.9.0
pydantic-settings==2.5.2
EOF
```

---

### Step 3.4: Create .env File (10 minutes)

```bash
cat > .env << 'EOF'
# LLM APIs
GROQ_API_KEY=your_groq_key_here
GOOGLE_API_KEY=your_google_key_here

# Embeddings
VOYAGE_API_KEY=your_voyage_key_here

# Database
SUPABASE_URL=your_supabase_url_here
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key_here

# Cache
UPSTASH_REDIS_REST_URL=your_upstash_url_here
UPSTASH_REDIS_REST_TOKEN=your_upstash_token_here

# Job Search APIs
JSEARCH_API_KEY=your_jsearch_key_here
TAVILY_API_KEY=your_tavily_key_here
EOF

# Now replace placeholders with actual keys
# Use your text editor to replace all "your_*_here" with actual values
```

**IMPORTANT:** Replace ALL placeholders with actual API keys you collected in Phase 2.

---

### Step 3.5: Create Python Virtual Environment (10 minutes)

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
# source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

**Wait 5-10 minutes for installation to complete.**

---

### Step 3.6: Create Supabase Client (10 minutes)

```bash
# Create db/supabase.py
cat > db/supabase.py << 'EOF'
"""
Supabase client initialization.
Import this client in all services - never create a new client.
"""
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    raise ValueError("Missing Supabase credentials in .env file")

# Service role client - full access, use only in backend
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
EOF
```

---

### Step 3.7: Create Main FastAPI App (15 minutes)

```bash
cat > main.py << 'EOF'
"""
CareerPilot Backend API
FastAPI application with CORS and health check.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="CareerPilot API",
    description="Agentic career co-pilot backend",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local Next.js dev
        "https://*.vercel.app",   # Vercel deployments
        os.getenv("FRONTEND_URL", "")  # Production frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "CareerPilot API is running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "database": "connected",  # TODO: Add actual DB check
        "services": {
            "groq": bool(os.getenv("GROQ_API_KEY")),
            "gemini": bool(os.getenv("GOOGLE_API_KEY")),
            "voyage": bool(os.getenv("VOYAGE_API_KEY")),
            "supabase": bool(os.getenv("SUPABASE_URL")),
            "redis": bool(os.getenv("UPSTASH_REDIS_REST_URL")),
        }
    }

# TODO: Import and include routers here as they're built
# from routers import cv, jobs, chat, tracker, dashboard
# app.include_router(cv.router, prefix="/api/cv", tags=["cv"])
# app.include_router(jobs.router, prefix="/api/jobs", tags=["jobs"])
# app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
# app.include_router(tracker.router, prefix="/api/tracker", tags=["tracker"])
# app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
EOF
```

---

### Step 3.8: Test Backend Startup (10 minutes)

```bash
# Start the server
uvicorn main:app --reload

# You should see:
# INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
# INFO:     Started reloader process
# INFO:     Started server process
# INFO:     Waiting for application startup.
# INFO:     Application startup complete.
```

**Open browser and test:**

- http://localhost:8000 → Should show `{"status": "ok", ...}`
- http://localhost:8000/health → Should show all services as `true`

**If health check shows any `false` values:**

- Check your `.env` file
- Verify all API keys are correct
- Restart the server

Press `CTRL+C` to stop the server.

---

### Step 3.9: Create .env.example (5 minutes)

```bash
cat > .env.example << 'EOF'
# LLM APIs
GROQ_API_KEY=
GOOGLE_API_KEY=

# Embeddings
VOYAGE_API_KEY=

# Database
SUPABASE_URL=
SUPABASE_SERVICE_ROLE_KEY=

# Cache
UPSTASH_REDIS_REST_URL=
UPSTASH_REDIS_REST_TOKEN=

# Job Search APIs
JSEARCH_API_KEY=
TAVILY_API_KEY=
EOF
```

---

### Step 3.10: Commit Day 1 Work (10 minutes)

```bash
# Add all files
git add .

# Commit
git commit -m "Day 1: Database schema, API keys, backend initialization

- Created Supabase schema with all tables
- Enabled pgvector and Realtime
- Collected all API keys
- Initialized FastAPI backend
- Created virtual environment
- Tested health check endpoint"

# Push to GitHub
git push origin main
```

---

## PHASE 4 — Handoff to DEV2 (15 minutes)

### Step 4.1: Share Credentials with DEV2

Create a file `HANDOFF_DEV2.md` (DO NOT COMMIT THIS):

```bash
cat > HANDOFF_DEV2.md << 'EOF'
# DEV2 Credentials (Day 1 Handoff)

## Supabase
- **URL:** [your_supabase_url]
- **Anon Key:** [your_supabase_anon_key]

## Test User (create this tomorrow)
- Email: demo@careerpilot.com
- Password: Demo123!

## Backend Status
- ✅ Database schema created
- ✅ All tables and indexes ready
- ✅ Realtime enabled on applications and nudges
- ✅ Auth configured (email/password)
- ✅ Storage bucket created (cv-files)
- ✅ Backend running on localhost:8000

## Next Steps for DEV2
- Wait until Day 6 to start frontend
- Read all documentation (AGENTS.md, PRD.md, DEV2_FRONTEND.md)
- Prepare mentally for Days 6-10

EOF
```

Send this file to DEV2 via secure channel (Slack DM, encrypted email, etc.)

---

## Day 1 Checklist

- [ ] Supabase project created
- [ ] pgvector extension enabled
- [ ] All 9 tables created
- [ ] All indexes created
- [ ] hybrid_search stored procedure created
- [ ] Realtime enabled on applications and nudges
- [ ] Auth configured (email/password)
- [ ] Storage bucket created (cv-files)
- [ ] All 7 API keys collected
- [ ] GitHub repository created
- [ ] Backend directory structure created
- [ ] requirements.txt created
- [ ] .env file created with all keys
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Supabase client created (db/supabase.py)
- [ ] FastAPI app created (main.py)
- [ ] Health check endpoint tested
- [ ] .env.example created
- [ ] Work committed and pushed to GitHub
- [ ] Credentials shared with DEV2

---

## Troubleshooting

### Issue: "Module not found" errors

**Solution:** Make sure virtual environment is activated:

```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### Issue: Supabase connection fails

**Solution:** Check `.env` file:

- SUPABASE_URL should start with `https://`
- SUPABASE_SERVICE_ROLE_KEY should start with `eyJ`
- No quotes around values
- No spaces around `=`

### Issue: Health check shows false for services

**Solution:** Verify API keys in `.env`:

- Each key should be on its own line
- No extra spaces
- No quotes
- Restart server after fixing

### Issue: pip install fails

**Solution:**

```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Try installing one by one to find problematic package
pip install fastapi
pip install uvicorn
# ... etc
```

---

## Success Criteria

By end of Day 1, you should have:

- ✅ Database fully configured with all tables
- ✅ All API keys working
- ✅ Backend running on localhost:8000
- ✅ Health check returning all `true` values
- ✅ Code committed to GitHub
- ✅ DEV2 has Supabase credentials

**If all checkboxes are checked, Day 1 is COMPLETE. Rest well. Tomorrow you build CV parsing.**

---

_DAY 1 Complete · CareerPilot · Codesprint 2026_
_Next: DAY 2 — CV Parsing Pipeline_
