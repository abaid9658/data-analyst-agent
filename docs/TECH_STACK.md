# 🛠️ Technology Stack

## AI Data Analyst Agent

---

## Frontend

| Technology | Version | Purpose |
|---|---|---|
| **Next.js** | 14 (App Router) | React framework, SSR, file-based routing |
| **React** | 18 | UI library |
| **TypeScript** | 5.x | Type safety |
| **Tailwind CSS** | 3.x | Utility-first CSS |
| **Shadcn UI** | Latest | Component library (built on Radix UI) |
| **Framer Motion** | 11 | Animations and transitions |
| **Zustand** | 4 | Global state management |
| **React Query (TanStack)** | 5 | Server state, caching, fetching |
| **Plotly.js** | 2.x | Interactive charts |
| **Monaco Editor** | Latest | SQL/Python code viewer with syntax highlighting |
| **React Dropzone** | Latest | File upload drag-and-drop |
| **React Hook Form** | 7 | Form handling |
| **Zod** | 3 | Schema validation (frontend) |
| **Axios** | 1.x | HTTP client |
| **date-fns** | 3 | Date manipulation |
| **Lucide React** | Latest | Icon system |

---

## Backend

| Technology | Version | Purpose |
|---|---|---|
| **FastAPI** | 0.111+ | High-performance async API framework |
| **Python** | 3.11+ | Backend language |
| **Uvicorn** | Latest | ASGI server |
| **SQLAlchemy** | 2.0 | ORM (async support) |
| **Alembic** | Latest | Database migrations |
| **Pydantic** | 2.x | Data validation, schemas |
| **Celery** | 5.x | Background job processing |
| **Redis** | 7 | Cache, message broker, sessions |
| **httpx** | Latest | Async HTTP client |
| **python-jose** | Latest | JWT handling |
| **passlib** | Latest | Password hashing (bcrypt) |
| **cryptography** | Latest | Fernet encryption for DB credentials |
| **slowapi** | Latest | Rate limiting middleware |
| **python-multipart** | Latest | File upload handling |

---

## AI / Agent

| Technology | Version | Purpose |
|---|---|---|
| **LangChain** | 0.2+ | LLM abstraction, chains |
| **LangGraph** | 0.1+ | Agent state machine / orchestration |
| **OpenAI** | 1.x | GPT-4o LLM (primary) |
| **Anthropic** | Latest | Claude (fallback) |
| **Google GenerativeAI** | Latest | Gemini (alternative) |
| **tiktoken** | Latest | Token counting |

---

## Data Science / ML

| Library | Purpose |
|---|---|
| **Pandas** | Data manipulation and analysis |
| **NumPy** | Numerical computing |
| **SciPy** | Scientific computing, statistics |
| **Statsmodels** | Statistical models, time series |
| **Scikit-learn** | ML preprocessing, models, evaluation |
| **XGBoost** | Gradient boosting (regression/classification) |
| **LightGBM** | Fast gradient boosting |
| **CatBoost** | Gradient boosting (categorical features) |
| **Prophet** | Facebook's time series forecasting |
| **Plotly** | Interactive visualization |
| **chardet** | Character encoding detection |
| **openpyxl** | Excel reading/writing |
| **RestrictedPython** | Safe Python code execution sandbox |

---

## Report Generation

| Library | Purpose |
|---|---|
| **ReportLab** | PDF generation |
| **python-docx** | Word (.docx) generation |
| **python-pptx** | PowerPoint (.pptx) generation |
| **openpyxl** | Excel (.xlsx) generation |
| **Jinja2** | HTML templates for reports |
| **WeasyPrint** | HTML → PDF (alternative) |

---

## Database

| Technology | Purpose |
|---|---|
| **PostgreSQL 15** | Primary application database |
| **Redis 7** | Cache, sessions, task queue broker |
| **MinIO** | Object storage (file uploads) — S3 compatible |

**Supported User Databases (connection targets):**
- PostgreSQL, MySQL, SQLite, SQL Server (via pyodbc), MongoDB (via pymongo)

---

## Authentication & Security

| Technology | Purpose |
|---|---|
| **PyJWT** | JWT token creation/validation |
| **python-jose** | JOSE standard JWT |
| **bcrypt** | Password hashing |
| **Fernet (cryptography)** | Symmetric encryption for DB credentials |
| **Google Auth** | Google OAuth 2.0 |
| **GitHub OAuth** | GitHub OAuth 2.0 |
| **slowapi** | Rate limiting |

---

## DevOps & Infrastructure

| Technology | Purpose |
|---|---|
| **Docker** | Containerization |
| **Docker Compose** | Local multi-service orchestration |
| **Nginx** | Reverse proxy, SSL termination |
| **GitHub Actions** | CI/CD pipelines |
| **Render / Railway** | Cloud deployment (simple) |
| **AWS ECS / Azure ACI / GCP Cloud Run** | Cloud deployment (production) |
| **Vercel** | Frontend deployment |

---

## Testing

| Technology | Purpose |
|---|---|
| **pytest** | Backend unit & integration tests |
| **pytest-asyncio** | Async test support |
| **httpx** | FastAPI test client (async) |
| **factory_boy** | Test data factories |
| **Jest** | Frontend unit tests |
| **React Testing Library** | Frontend component tests |
| **Playwright** | End-to-end tests |

---

## Code Quality

| Technology | Purpose |
|---|---|
| **Ruff** | Python linting & formatting (fast) |
| **Black** | Python code formatter |
| **mypy** | Python static type checking |
| **ESLint** | JavaScript/TypeScript linting |
| **Prettier** | JavaScript/TypeScript formatting |
| **pre-commit** | Git hooks for quality gates |

---

## Environment Variables Required

```bash
# LLM
OPENAI_API_KEY=
ANTHROPIC_API_KEY=            # Optional fallback
GOOGLE_AI_API_KEY=            # Optional fallback

# Database
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/dataanalyst
REDIS_URL=redis://localhost:6379/0

# Auth
JWT_SECRET_KEY=
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# OAuth
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GITHUB_CLIENT_ID=
GITHUB_CLIENT_SECRET=
FRONTEND_URL=http://localhost:3000

# Storage
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=
MINIO_SECRET_KEY=
MINIO_BUCKET=dataanalyst

# Encryption
ENCRYPTION_KEY=               # Fernet key for DB credentials

# Security
ALLOWED_ORIGINS=http://localhost:3000
RATE_LIMIT_PER_MINUTE=60

# Celery
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2
```
