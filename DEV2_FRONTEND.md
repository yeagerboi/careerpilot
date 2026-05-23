# DEV 2 — Frontend & UI

**CareerPilot · Codesprint 2026**

> You own: Frontend (Next.js), All UI Components, Styling, User Experience, Vercel Deployment
> Your partner owns: Backend (FastAPI), Database, APIs, Agent Logic

---

## Your Responsibilities

**Core Systems:**

- ✅ Next.js 14 App Router (all pages, layouts, routing)
- ✅ All UI components (shadcn/ui + custom)
- ✅ Tailwind CSS styling (responsive, polished)
- ✅ Auth UI (login, signup, protected routes)
- ✅ Job cards UI with fit score display
- ✅ Streaming chat interface
- ✅ Kanban board (drag-and-drop with dnd-kit)
- ✅ Calendar and todo list
- ✅ Progress dashboard (charts with Recharts)
- ✅ Supabase Realtime subscriptions
- ✅ Vercel deployment

**Not Your Responsibility:**

- ❌ Backend code (FastAPI, Python)
- ❌ Database schema or migrations
- ❌ API business logic
- ❌ LLM integrations
- ❌ Railway deployment (your partner handles this)

---

## Day-by-Day Tasks

### Day 1 — Wait for DEV1 (Your Day Off)

**Goal:** Let DEV1 set up database and get API keys

**What DEV1 is doing:** Supabase schema, environment setup, API keys

**What you should do:**

- [ ] Read all documentation (AGENTS.md, PRD.md, CareerPilot_Stack_Final.md)
- [ ] Install Node.js and npm (if not already installed)
- [ ] Familiarize yourself with shadcn/ui documentation
- [ ] Optional: Watch Next.js 14 App Router tutorial
- [ ] Optional: Review dnd-kit documentation

**No coding today. Prepare mentally.**

---

### Day 2 — Wait for DEV1 (Your Day Off)

**Goal:** Let DEV1 build CV parsing

**What DEV1 is doing:** CV upload endpoint, PDF/DOCX parsers

**What you should do:**

- [ ] Optional: Sketch UI wireframes on paper
- [ ] Optional: Plan component structure
- [ ] Optional: Review Tailwind CSS utilities

**No coding today. DEV1 needs to finish backend foundation first.**

---

### Day 3 — Wait for DEV1 (Your Day Off)

**Goal:** Let DEV1 build embeddings pipeline

**What DEV1 is doing:** Voyage AI embeddings, vector storage, hybrid search

**What you should do:**

- [ ] Optional: Design color scheme and typography
- [ ] Optional: Find inspiration (dribbble.com, ui.shadcn.com)

**No coding today. Backend must be ready before you start.**

---

### Day 4 — Wait for DEV1 (Your Day Off)

**Goal:** Let DEV1 build fit score and job search

**What DEV1 is doing:** Fit score algorithm, job search APIs

**What you should do:**

- [ ] Optional: Create logo or branding
- [ ] Optional: Plan responsive breakpoints

**No coding today. Almost ready to start.**

---

### Day 5 — Wait for DEV1 (Your Day Off)

**Goal:** Let DEV1 build agent and chat

**What DEV1 is doing:** LangGraph agent, streaming chat service

**What you should do:**

- [ ] Optional: Review Vercel AI SDK documentation
- [ ] Optional: Test Supabase client in a scratch project

**No coding today. Tomorrow you start.**

---

### Day 6 — Frontend Scaffold (6–8 hours)

**Goal:** Next.js app with auth, navigation, placeholder pages

#### Morning

- [ ] Get from DEV1: Supabase URL and anon key
- [ ] Create Next.js project:
  ```bash
  npx create-next-app@latest frontend --typescript --tailwind --app
  cd frontend
  ```
- [ ] Install dependencies:
  ```bash
  npm install @supabase/supabase-js @supabase/ssr
  npm install @tanstack/react-query
  npm install ai
  npm install @dnd-kit/core @dnd-kit/sortable
  npm install recharts
  npm install lucide-react
  ```
- [ ] Initialize shadcn:
  ```bash
  npx shadcn-ui@latest init
  npx shadcn-ui@latest add card button input textarea badge progress calendar
  ```

#### Afternoon

- [ ] Create Supabase clients:
  - `lib/supabase.ts` — browser client
  - `lib/supabase-server.ts` — server component client
- [ ] Create auth pages:
  - `app/(auth)/login/page.tsx`
  - `app/(auth)/signup/page.tsx`
  - Use Supabase Auth with email/password
- [ ] Create dashboard layout:
  - `app/(dashboard)/layout.tsx` — sidebar with navigation
  - Links: Jobs, CV, Chat, Tracker
  - User menu with logout
- [ ] Create placeholder pages:
  - `app/(dashboard)/jobs/page.tsx` — "Jobs coming soon"
  - `app/(dashboard)/cv/page.tsx` — "CV upload coming soon"
  - `app/(dashboard)/chat/page.tsx` — "Chat coming soon"
  - `app/(dashboard)/tracker/page.tsx` — "Tracker coming soon"
- [ ] Add protected route middleware
- [ ] Test auth flow: signup → login → dashboard → logout

**Deliverable:** Frontend scaffold with working auth, navigation, placeholder pages

---

### Day 7 — Deployment + Job Cards UI (6–8 hours)

**Goal:** Frontend deployed, job search UI working

#### Morning (2–3 hours) — DEPLOY FIRST

- [ ] Get from DEV1: Railway backend URL
- [ ] Create `frontend/.env.local`:
  ```bash
  NEXT_PUBLIC_SUPABASE_URL=
  NEXT_PUBLIC_SUPABASE_ANON_KEY=
  NEXT_PUBLIC_API_URL=https://your-app.railway.app
  ```
- [ ] Push frontend to GitHub
- [ ] Connect repo at vercel.com
- [ ] Add environment variables in Vercel dashboard
- [ ] Get Vercel URL: `https://your-app.vercel.app`
- [ ] Test deployed auth flow

**Handoff to DEV1:** Share Vercel URL

#### Afternoon (4–5 hours) — Job Cards UI

- [ ] Create `components/job-card.tsx`:
  ```tsx
  interface JobCardProps {
    title: string;
    company: string;
    location: string;
    salaryRange: string;
    deadline: string;
    fitScore: number;
    fitExplanation: string;
    onSave: () => void;
  }
  // Display all fields, fit score badge, "Save" button
  ```
- [ ] Create `components/fit-score-badge.tsx`:
  ```tsx
  interface FitScoreBadgeProps {
    score: number; // 0-100
  }
  // Circular progress, color: <40 red, 40-70 yellow, >70 green
  ```
- [ ] Update `app/(dashboard)/jobs/page.tsx`:
  ```tsx
  "use client";
  // Search bar with location filter
  // Grid of job cards
  // Loading state
  // Empty state
  // Connect to POST /api/jobs/search
  ```
- [ ] Test with real searches: "Python developer Dhaka"

**Deliverable:** 🚀 Frontend deployed, job search UI working with fit scores

---

### Day 8 — Streaming Chat UI (6–8 hours)

**Goal:** Chat interface with streaming, RAG, memory

#### Morning (3–4 hours)

- [ ] Create `app/api/chat/route.ts`:
  ```tsx
  // Proxy streaming requests to FastAPI backend
  // Handle SSE stream
  // Return as ReadableStream
  ```
- [ ] Create `components/chat-interface.tsx`:

  ```tsx
  "use client";
  import { useChat } from "ai/react";

  // Message list with user/assistant bubbles
  // Input field with send button
  // Loading indicator while streaming
  // Markdown rendering for assistant responses
  ```

- [ ] Update `app/(dashboard)/chat/page.tsx`:
  ```tsx
  // Render <ChatInterface />
  // Session switcher (dropdown)
  // "Clear history" button
  ```

#### Afternoon (3–4 hours)

- [ ] Test all benchmark queries:
  - "Am I ready for this data engineer role?"
  - "What skills am I missing for a Google internship?"
  - "Build me a 3-month roadmap to become job-ready"
  - "Draft a cover letter for this job posting"
  - Follow-up: "Make it more concise"
- [ ] Verify streaming works (tokens appear progressively)
- [ ] Add copy button for cover letters
- [ ] Add markdown rendering (code blocks, lists, bold)

**Deliverable:** Streaming chat working with RAG and memory

---

### Day 9 — Kanban Board (6–8 hours)

**Goal:** Drag-and-drop application tracker with Realtime

#### Morning (3–4 hours)

- [ ] Create `components/kanban-board.tsx`:

  ```tsx
  "use client";
  import { DndContext, DragEndEvent } from "@dnd-kit/core";
  import { SortableContext } from "@dnd-kit/sortable";

  // Five columns: Saved, Applied, Interviewing, Offer, Rejected
  // Each card: job title, company, applied date, fit score badge
  // Drag and drop between columns
  ```

- [ ] Create `components/kanban-card.tsx`:
  ```tsx
  interface KanbanCardProps {
    id: string;
    title: string;
    company: string;
    appliedAt: string;
    fitScore: number;
  }
  // Draggable card with all fields
  ```

#### Afternoon (3–4 hours)

- [ ] Add Supabase Realtime subscription:
  ```tsx
  useEffect(() => {
    const channel = supabase
      .channel("applications-changes")
      .on(
        "postgres_changes",
        { event: "*", schema: "public", table: "applications" },
        (payload) => {
          /* update local state */
        },
      )
      .subscribe();
    return () => {
      supabase.removeChannel(channel);
    };
  }, []);
  ```
- [ ] Connect to backend:
  - `GET /api/applications` — fetch all
  - `PATCH /api/applications/:id` — update status on drag
- [ ] Add "Add to Tracker" button on job cards
- [ ] Update `app/(dashboard)/tracker/page.tsx`:
  - Render `<KanbanBoard />`
- [ ] Test: drag card → verify Realtime updates in another tab

**Deliverable:** Kanban board with drag-and-drop and Realtime updates

---

### Day 10 — Calendar, Todos, Dashboard (8–10 hours)

**Goal:** Complete Pillar 4

#### Morning (4–5 hours)

- [ ] Create `components/calendar-view.tsx`:
  ```tsx
  import { Calendar } from "@/components/ui/calendar";
  // Show todos and deadlines on calendar dates
  // Click date → show todos for that day
  ```
- [ ] Create `components/todo-list.tsx`:
  ```tsx
  // List of todos with checkboxes
  // Add new todo button
  // Link todos to goals
  ```
- [ ] Connect to backend:
  - `GET /api/goals`
  - `POST /api/goals`
  - `GET /api/todos`
  - `POST /api/todos`
  - `PATCH /api/todos/:id`
- [ ] Update `app/(dashboard)/tracker/page.tsx`:
  - Add tabs: Kanban | Calendar | Goals
  - Render calendar and todo list

#### Afternoon (4–5 hours)

- [ ] Create `components/progress-dashboard.tsx`:

  ```tsx
  import { BarChart, DonutChart } from "recharts";

  // Metric cards: applications sent, skills added, roadmap %, streak
  // Bar chart: applications per week (last 4 weeks)
  // Donut chart: Kanban status breakdown
  ```

- [ ] Connect to backend:
  - `GET /api/dashboard/stats`
- [ ] Add nudge banner component:
  ```tsx
  // Subscribe to nudges table via Realtime
  // Show banner at top when new nudge arrives
  // "Dismiss" button marks nudge as seen
  ```
- [ ] Add to dashboard layout

**Deliverable:** Calendar, todos, progress dashboard, AI nudges all working

---

### Day 11 — Polish & Bug Fixes (6–8 hours)

**Goal:** UI polished, all bugs fixed, mobile responsive

#### Morning (3–4 hours)

- [ ] Bug hunt:
  - Test all flows end-to-end
  - Check error handling
  - Add loading states where missing
  - Add error boundaries
  - Fix any broken links or 404s
- [ ] Polish UI:
  - Consistent spacing (use Tailwind spacing scale)
  - Typography hierarchy (text-sm, text-base, text-lg, text-xl)
  - Color consistency (use Tailwind color palette)
  - Add empty states with helpful messages
  - Add success toasts (use shadcn toast component)

#### Afternoon (3–4 hours)

- [ ] Mobile responsive:
  - Test on phone or use Chrome DevTools
  - Fix layout issues (use Tailwind responsive classes: sm:, md:, lg:)
  - Ensure touch targets are large enough (min 44x44px)
  - Test Kanban drag-and-drop on mobile
- [ ] Performance:
  - Add React Query caching for job search
  - Optimize images (if any)
  - Check Lighthouse score (aim for >80)
- [ ] Accessibility:
  - Add aria-labels where needed
  - Ensure keyboard navigation works
  - Check color contrast (use WebAIM contrast checker)

**Deliverable:** Fully polished UI, all bugs fixed, mobile responsive

---

### Day 12 — Support DEV1 (2–3 hours)

**Goal:** Help with evaluation suite, test frontend

- [ ] Test all 5 evaluation test cases from frontend
- [ ] Take screenshots for eval.md
- [ ] Report any backend issues to DEV1
- [ ] Optional: Add loading skeletons
- [ ] Optional: Add animations (Tailwind transitions)

**Mostly DEV1's day. You're on standby.**

---

### Day 13 — README & Architecture Diagram (4–6 hours)

**Goal:** Complete documentation

#### Morning (2–3 hours)

- [ ] Update README.md:

  ````markdown
  # CareerPilot

  Your agentic career co-pilot. Hunts jobs, scores fit, drafts applications.

  ## Features

  - Job Hunter Agent with AI-powered fit scoring
  - RAG-powered CV intelligence
  - Personal AI Assistant with streaming chat
  - Productivity tracker with Kanban, calendar, todos

  ## Tech Stack

  - Frontend: Next.js 14, Tailwind CSS, shadcn/ui
  - Backend: FastAPI, Python 3.11
  - Database: Supabase (PostgreSQL + pgvector)
  - LLMs: Groq, Gemini 2.0 Flash
  - Embeddings: Voyage AI

  ## Setup

  ### Frontend

  ```bash
  cd frontend
  npm install
  cp .env.local.example .env.local  # add your keys
  npm run dev
  ```
  ````

  ### Backend

  ```bash
  cd backend
  python -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  cp .env.example .env  # add your keys
  uvicorn main:app --reload
  ```

  ## Live Demo
  - Frontend: https://your-app.vercel.app
  - Backend: https://your-app.railway.app
  - Demo video: [YouTube link]

  ## Environment Variables

  [List all required variables]

  ```

  ```

#### Afternoon (2–3 hours)

- [ ] Create architecture diagram:
  - Use draw.io or Excalidraw
  - Show: User → Next.js → FastAPI → Supabase/Voyage/Groq/Gemini
  - Show data flow: CV upload → parsing → embedding → vector DB
  - Export as PNG or SVG
  - Add to README
- [ ] Create `.env.local.example` and `.env.example` files
- [ ] Review all documentation for accuracy

**Deliverable:** Complete README with setup instructions and architecture diagram

---

### Day 14 — Demo Video & Final Testing (6–8 hours)

**Goal:** Record demo, final polish, submit

#### Morning (3–4 hours) — Record Demo

- [ ] Script the demo (see CareerPilot_Stack_Final.md Section 18):
  - 0:00–0:30: CV Upload
  - 0:30–1:15: Job Search
  - 1:15–2:00: Fit Score
  - 2:00–2:45: AI Assistant
  - 2:45–3:30: Cover Letter
  - 3:30–4:15: Tracker
  - 4:15–5:00: Dashboard
- [ ] Use test user: `demo@careerpilot.com` / `Demo123!`
- [ ] Record with OBS Studio or Loom
- [ ] Record twice, use better take
- [ ] Edit: add title card, trim dead air
- [ ] Upload to YouTube (unlisted) or Google Drive

#### Afternoon (3–4 hours) — Final Polish & Submit

- [ ] Final UI polish:
  - Fix any visual glitches
  - Ensure all buttons work
  - Check all links
- [ ] Final testing:
  - Test on deployed version (not localhost)
  - Test on different browsers (Chrome, Firefox, Safari)
  - Test on mobile
- [ ] Submit:
  - GitHub repo URL
  - Live deployment URL (Vercel)
  - Demo video URL
  - Any other required forms

**Deliverable:** 🎉 Complete submission with demo video

---

## Your Tech Stack (Memorize This)

### Framework

- **Next.js 14 App Router** (never Pages Router)
- **TypeScript** (no `any` types)

### Styling

- **Tailwind CSS** (no custom CSS files)
- **shadcn/ui** (never MUI, Chakra, Ant Design)

### Components

- **Drag-and-drop:** dnd-kit (never react-beautiful-dnd)
- **Charts:** Recharts
- **Icons:** lucide-react

### Data Fetching

- **Client-side:** TanStack Query (`@tanstack/react-query`)
- **Server Components:** Native fetch
- **Streaming:** Vercel AI SDK (`useChat` hook)

### Database Client

- **Supabase:** `@supabase/supabase-js` and `@supabase/ssr`

---

## Environment Variables (frontend/.env.local)

```bash
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
NEXT_PUBLIC_API_URL=https://your-app.railway.app
```

---

## Forbidden (Never Use These)

```
❌ Pages Router (app/ directory only)
❌ getServerSideProps (use Server Components)
❌ Custom CSS files (Tailwind only)
❌ MUI, Chakra, Ant Design (shadcn/ui only)
❌ react-beautiful-dnd (dnd-kit only)
❌ any type (use proper TypeScript types)
❌ Hardcoded API URLs (use env variables)
❌ console.log in production (use proper logging)
```

---

## Communication with DEV1

### What to get from DEV1:

- ✅ Supabase URL and anon key (Day 6)
- ✅ Railway backend URL (Day 7)
- ✅ API endpoint schemas (as they're built)
- ✅ Test user credentials (Day 11)

### What to share with DEV1:

- ✅ Vercel frontend URL (Day 7)
- ✅ UI feedback on API response formats
- ✅ Error messages from browser console
- ✅ Any integration issues

### Daily sync (5 minutes):

- Morning: "Today I'm building X"
- Evening: "X is done, here's a screenshot"

---

## Component Structure

```
frontend/
├── app/
│   ├── (auth)/
│   │   ├── login/page.tsx
│   │   └── signup/page.tsx
│   ├── (dashboard)/
│   │   ├── layout.tsx
│   │   ├── jobs/page.tsx
│   │   ├── cv/page.tsx
│   │   ├── chat/page.tsx
│   │   └── tracker/page.tsx
│   ├── api/
│   │   └── chat/route.ts
│   └── page.tsx
├── components/
│   ├── ui/                    ← shadcn (auto-generated)
│   ├── job-card.tsx
│   ├── fit-score-badge.tsx
│   ├── kanban-board.tsx
│   ├── kanban-card.tsx
│   ├── cv-upload.tsx
│   ├── chat-interface.tsx
│   ├── calendar-view.tsx
│   ├── todo-list.tsx
│   └── progress-dashboard.tsx
├── lib/
│   ├── supabase.ts
│   ├── supabase-server.ts
│   └── utils.ts
└── types/
    └── index.ts
```

---

## Success Metrics

By Day 14, you should have:

- [x] All UI components working
- [x] Frontend deployed to Vercel
- [x] Responsive design (mobile + desktop)
- [x] Streaming chat with smooth UX
- [x] Kanban with drag-and-drop
- [x] Realtime updates working
- [x] Polished, professional UI
- [x] Zero frontend errors during demo

**If you have all of these, you've done your job perfectly.**

---

_DEV2 Frontend Guide · CareerPilot · Codesprint 2026_
_Related: AGENTS.md · CareerPilot_Stack_Final.md · TIMELINE.md_
