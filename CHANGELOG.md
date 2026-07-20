# Changelog

All notable changes to **AI Data Analyst Agent** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

### Planned
- Voice input (Speech-to-Text)
- Text-to-Speech responses
- Slack / Microsoft Teams integration
- Scheduled email reports
- Real-time collaboration (WebSockets)
- LSTM forecasting model
- Model monitoring & data drift detection

---

## [1.0.0] — 2026-07-17

### Added

**Infrastructure**
- Full Docker + Docker Compose setup
- GitHub Actions CI/CD pipelines (test → build → deploy)
- Environment configuration with .env.example
- Alembic database migration setup

**Backend (FastAPI)**
- `/auth` — JWT login, registration, Google OAuth, GitHub OAuth
- `/upload` — CSV, Excel, JSON file upload with schema detection
- `/database` — PostgreSQL, MySQL, SQLite, SQL Server, MongoDB connection wizard
- `/chat` — Streaming AI chat endpoint with conversation memory
- `/query` — SQL generation, execution, and explanation
- `/chart` — Auto visualization generation with Plotly
- `/report` — PDF, Word, PowerPoint, Excel, Markdown report generation
- `/dashboard` — Auto dashboard builder
- `/export` — Export data and reports
- `/history` — Conversation and analysis history
- `/settings` — User preferences and configuration

**AI Agent**
- LangGraph-based multi-step agent orchestrator
- Intent classification with LLM
- Planner: breaks user request into ordered steps
- Tool calling layer with retry logic
- Memory: conversation history + dataset context

**Tools**
- SQL Tool: NL→SQL, validation, optimization, injection prevention
- Python Tool: Pandas/NumPy/SciPy auto analysis + data cleaning
- Visualization Tool: Plotly auto chart selection (10 chart types)
- ML Tool: XGBoost, LightGBM, CatBoost, Random Forest, ARIMA, Prophet
- Statistics Tool: descriptive stats, correlation, hypothesis testing, outlier detection
- Report Generator: multi-format reports with AI insights

**Frontend (Next.js)**
- App Router with TypeScript
- Tailwind CSS + Shadcn UI design system
- Dark mode with system preference detection
- Authentication: login, register, OAuth callbacks
- Chat interface with streaming responses
- Dataset upload & manager
- Database connection wizard
- Interactive Plotly charts embedded in chat
- SQL viewer with syntax highlighting
- Python code viewer
- Conversation history sidebar
- Report download manager
- Admin dashboard
- Responsive mobile layout

**Database**
- Users, Sessions, DataSources, Datasets, Conversations, Messages
- Generated SQL, Charts, Reports, Audit Logs tables
- Full indexing strategy

**Security**
- JWT + refresh token rotation
- SQL injection prevention
- Prompt injection detection
- Rate limiting (per user + per IP)
- Encrypted database credentials storage
- Audit logging for all sensitive actions
- Input validation with Pydantic

**Documentation**
- README.md
- PRD.md
- ARCHITECTURE.md
- API_SPEC.md
- DATABASE.md
- DESIGN.md
- TECH_STACK.md
- CODING_STANDARDS.md
- TASKS.md
- RULES.md
- CHANGELOG.md
- FOLDER_STRUCTURE.md

---

## Template for Future Versions

```
## [X.Y.Z] — YYYY-MM-DD

### Added
- New features

### Changed
- Modified existing features

### Fixed
- Bug fixes

### Removed
- Removed features

### Security
- Security patches
```
