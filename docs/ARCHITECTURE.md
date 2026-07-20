# 🏗️ System Architecture

## AI Data Analyst Agent

---

## 1. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                           USER BROWSER                              │
│              Next.js 14 + TypeScript + Tailwind + Shadcn UI         │
└─────────────────────────────┬───────────────────────────────────────┘
                              │  HTTPS / WebSocket (SSE)
┌─────────────────────────────▼───────────────────────────────────────┐
│                         API GATEWAY                                  │
│                    FastAPI (Python 3.11)                             │
│          Nginx reverse proxy · SSL termination · CORS               │
└──────┬───────────────────────────────────────────────────┬──────────┘
       │                                                   │
┌──────▼──────┐                                    ┌───────▼──────────┐
│   Auth      │                                    │   File Storage   │
│  Service    │                                    │  MinIO / S3      │
│  JWT + OAuth│                                    │  (uploads)       │
└──────┬──────┘                                    └──────────────────┘
       │
┌──────▼──────────────────────────────────────────────────────────────┐
│                      AGENT ORCHESTRATOR                             │
│                    LangGraph State Machine                           │
│                                                                     │
│  ┌──────────┐  ┌──────────┐  ┌───────────┐  ┌────────────────────┐│
│  │  Intent  │  │  Planner │  │  Executor │  │  Result Synthesizer││
│  │  Classifier│ │  (Steps) │  │  (Tools)  │  │  + Memory Update  ││
│  └──────────┘  └──────────┘  └───────────┘  └────────────────────┘│
└─────────────────────────────┬───────────────────────────────────────┘
                              │ Tool Calls
┌─────────────────────────────▼───────────────────────────────────────┐
│                         TOOL LAYER                                   │
│                                                                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│  │SQL Tool  │ │Python    │ │Viz Tool  │ │ML Tool   │ │Stats Tool│ │
│  │NL→SQL    │ │Analysis  │ │Plotly    │ │XGBoost   │ │Hypothesis│ │
│  │Execution │ │Pandas    │ │Charts    │ │Prophet   │ │Testing   │ │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ │
│  ┌──────────┐ ┌──────────┐                                         │
│  │Report    │ │Dashboard │                                         │
│  │Generator │ │Builder   │                                         │
│  └──────────┘ └──────────┘                                         │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────────┐
│                          LLM LAYER                                   │
│           OpenAI GPT-4o / Anthropic Claude / Google Gemini          │
│                  (configurable via environment)                      │
└─────────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────────┐
│                        DATA LAYER                                    │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────────────────┐ │
│  │  PostgreSQL  │  │    Redis     │  │   User-Connected DBs      │ │
│  │  (App Data)  │  │  (Cache +    │  │  PG · MySQL · SQLite      │ │
│  │  Users       │  │   Sessions)  │  │  SQL Server · MongoDB     │ │
│  │  Datasets    │  └──────────────┘  └───────────────────────────┘ │
│  │  Reports     │                                                   │
│  │  History     │                                                   │
│  └──────────────┘                                                   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. Agent Orchestration (LangGraph)

```
User Message
      │
      ▼
┌─────────────────┐
│ Intent Classifier│  → Classifies: SQL/Python/ML/Viz/Stats/Report/Multi
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Planner      │  → Breaks into ordered steps
│                 │    e.g., [load_data, clean, aggregate, visualize, explain]
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────────────────────────────┐
│  Tool Executor  │────▶│ Tool 1: Python (load + clean data)      │
│  (Sequential or │     │ Tool 2: SQL (aggregate by month)        │
│   Parallel)     │     │ Tool 3: Viz (line chart revenue/month)  │
└────────┬────────┘     │ Tool 4: Stats (trend significance)      │
         │              └─────────────────────────────────────────┘
         ▼
┌─────────────────┐
│Output Validator │  → Checks each tool output for errors
│& Retry Logic    │  → Retries with modified prompt if failed (max 3x)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Result Synth.   │  → Combines all tool outputs into coherent response
│ + Memory Update │  → Updates conversation memory
└────────┬────────┘
         │
         ▼
   Streaming Response to Frontend
```

---

## 3. Frontend ↔ Backend Flow

### Chat Flow (Streaming)

```
User Types Message
        │
        ▼
ChatInput Component
        │ POST /chat/message (with session_id, dataset_id, message)
        ▼
FastAPI /chat endpoint
        │
        ▼
Agent Orchestrator (async generator)
        │ yields tokens/chunks
        ▼
Server-Sent Events (SSE)
        │
        ▼
Frontend EventSource listener
        │ Appends tokens to UI in real-time
        ▼
ChatMessage Component (streaming render)
        │ Parses final structured response:
        │  - text_response
        │  - sql_query
        │  - python_code
        │  - chart_spec (Plotly JSON)
        │  - table_data
        │  - insights []
        ▼
Renders: Text + Code Viewer + Chart + Table + Insights
```

### File Upload Flow

```
User Drags CSV File
        │
        ▼
FileUpload Component → Shows progress bar
        │ POST /upload/file (multipart/form-data)
        ▼
Backend: Validates file type + size
        │
        ▼
Background Task: Parse file → Schema detection → Data profiling
        │ Stores in MinIO/S3, metadata in PostgreSQL
        ▼
WebSocket event: "upload_complete" with dataset_id + schema
        │
        ▼
Frontend: Dataset appears in sidebar → Preview modal opens
```

### Database Connection Flow

```
User Opens DB Wizard
        │ POST /database/test (credentials)
        ▼
Backend: Attempts connection (5s timeout)
        │
        ▼ SUCCESS
Encrypt credentials (Fernet) → Store in DB
        │
        ▼
Connection available in chat session selector
```

---

## 4. Authentication Flow

```
User → Login Page
        │
        ├─── Email/Password ───▶ POST /auth/login
        │                              │
        │                       Validate credentials
        │                              │
        │                       Return: access_token (15min) + refresh_token (7d)
        │
        ├─── Google OAuth ────▶ GET /auth/google
        │                              │
        │                       Google OAuth 2.0 flow
        │                              │
        │                       Callback: /auth/google/callback
        │                              │
        │                       Upsert user → Return tokens
        │
        └─── GitHub OAuth ────▶ GET /auth/github
                                       (same pattern)

Token Storage: HttpOnly cookies (access + refresh)
Token Refresh: Automatic via /auth/refresh before expiry
Logout: /auth/logout → Revoke refresh token in Redis
```

---

## 5. Data Flow Architecture

```
Upload / Connect
      │
      ▼
DataSource Registry (PostgreSQL)
      │
      ▼
Dataset Profile Cache (Redis)
      │
      ▼
Agent Memory (per session)
      │ Provides: schema, sample rows, column types, stats
      ▼
LLM Context Window (injected as system context)
      │
      ▼
Tool Execution (with dataset access)
```

---

## 6. Security Architecture

```
Request Pipeline:
  IP → Rate Limiter (Redis) → Auth Middleware → Role Check → Handler

SQL Security:
  User SQL intent → LLM generates parameterized SQL
  → SQL Validator (forbids DROP, DELETE without WHERE, etc.)
  → Execute on sandboxed read-only connection (for user DBs)

Python Security:
  Generated code → AST analysis (no os, subprocess, import dangerous)
  → Execute in restricted environment (RestrictedPython)
  → Timeout: 60 seconds max

Prompt Security:
  User input → Prompt injection scanner
  → Sanitize before LLM call
  → System prompt enforces safe behavior
```

---

## 7. Deployment Architecture

```
Production:

┌─────────────────────────────────────────────────────────┐
│                    Cloud Provider (AWS / GCP / Azure)    │
│                                                         │
│  ┌────────────┐     ┌────────────────────────────────┐  │
│  │  Vercel /  │     │          Docker Swarm           │  │
│  │  Cloudflare│     │          / Kubernetes           │  │
│  │  (Frontend)│     │                                 │  │
│  └────────────┘     │  ┌────────┐  ┌──────────────┐  │  │
│                     │  │FastAPI │  │  Celery       │  │  │
│                     │  │ (x3   │  │  Workers (x5) │  │  │
│                     │  │ pods) │  │  (ML tasks)   │  │  │
│                     │  └────────┘  └──────────────┘  │  │
│                     │                                 │  │
│                     │  ┌────────┐  ┌──────────────┐  │  │
│                     │  │Postgres│  │   Redis      │  │  │
│                     │  │(RDS)   │  │  (ElastiCache│  │  │
│                     │  └────────┘  └──────────────┘  │  │
│                     └────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## 8. Caching Strategy

| Layer | Technology | TTL | What's Cached |
|---|---|---|---|
| Query Results | Redis | 5 min | Repeated SQL queries |
| Dataset Schema | Redis | 1 hour | Column types, stats |
| LLM Responses | Redis | 10 min | Identical prompts |
| Chart Specs | Redis | 1 hour | Generated Plotly JSON |
| User Sessions | Redis | 24 hours | Auth + preferences |

---

## 9. Background Jobs (Celery)

| Job | Trigger | Queue |
|---|---|---|
| File parsing + profiling | After upload | `uploads` |
| ML model training | User requests prediction | `ml` |
| Report generation | User requests report | `reports` |
| Scheduled reports | Cron | `scheduled` |
| Data drift monitoring | Hourly cron | `monitoring` |
