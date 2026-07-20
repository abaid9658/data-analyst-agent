# 📅 Development Tasks

## AI Data Analyst Agent — Sprint Roadmap

---

## Phase 1 — Foundation (Weeks 1-2)

### Week 1: Infrastructure & Auth

- [x] Project scaffolding (frontend + backend)
- [x] Docker Compose setup (Postgres + Redis + MinIO)
- [x] Database schema + Alembic migrations
- [x] FastAPI app structure (routes, services, repos)
- [x] User model + JWT authentication
- [x] Registration + Login endpoints
- [x] Google OAuth integration
- [x] GitHub OAuth integration
- [x] Refresh token rotation
- [x] Rate limiting middleware
- [x] Audit logging middleware
- [x] Next.js app setup (Tailwind, Shadcn, TypeScript)
- [x] Auth pages: Login, Register
- [x] Protected route middleware (frontend)
- [x] Auth store (Zustand)

### Week 2: Data Ingestion

- [x] File upload endpoint (CSV, Excel, JSON)
- [x] Background parsing with Celery
- [x] Schema auto-detection
- [x] Data profiling (missing values, types, stats)
- [x] MinIO/S3 file storage
- [x] Dataset listing + deletion endpoints
- [x] Database connection wizard endpoints
- [x] Credential encryption (Fernet)
- [x] Connection testing
- [x] Frontend: File upload dropzone
- [x] Frontend: Dataset manager page
- [x] Frontend: Database connection wizard modal

---

## Phase 2 — AI Agent Core (Weeks 3-4)

### Week 3: Agent Orchestration

- [x] LangGraph state machine setup
- [x] Intent classifier (LLM-based)
- [x] Planner (breaks intent → ordered steps)
- [x] Tool calling layer (base_tool.py)
- [x] Output validator + retry logic
- [x] Result synthesizer
- [x] Conversation memory (per session)
- [x] SSE streaming endpoint (/chat/message)
- [x] Frontend: Chat interface with streaming
- [x] Frontend: Thinking indicator animation
- [x] Frontend: Conversation history sidebar

### Week 4: SQL & Python Tools

- [x] SQL Tool: NL → SQL generation
- [x] SQL Tool: Injection prevention + validation
- [x] SQL Tool: Query execution engine
- [x] SQL Tool: Explanation + optimization
- [x] Python Tool: Code generation
- [x] Python Tool: Sandboxed execution (RestrictedPython)
- [x] Python Tool: Data loading + cleaning
- [x] Python Tool: Auto aggregation
- [x] Frontend: SQL code viewer (Monaco Editor)
- [x] Frontend: Python code viewer (Monaco Editor)
- [x] Frontend: Query result table component

---

## Phase 3 — Analysis Engines (Weeks 5-6)

### Week 5: Visualization & Statistics

- [x] Visualization Tool: 10 chart types (Plotly)
- [x] Visualization Tool: Auto chart type selection
- [x] Visualization Tool: PNG/SVG/PDF export
- [x] Statistics Tool: Descriptive statistics
- [x] Statistics Tool: Correlation analysis
- [x] Statistics Tool: Hypothesis testing (t-test, ANOVA, chi-square)
- [x] Statistics Tool: Outlier detection
- [x] Statistics Tool: Distribution analysis
- [x] Frontend: PlotlyChart component (interactive)
- [x] Frontend: Chart download buttons

### Week 6: Machine Learning Tool

- [x] ML Tool: Problem type auto-detection
- [x] ML Tool: Regression pipeline (XGBoost, RF, LR)
- [x] ML Tool: Classification pipeline (XGBoost, LightGBM, CatBoost)
- [x] ML Tool: Clustering (K-Means, DBSCAN)
- [x] ML Tool: Time series forecasting (ARIMA, Prophet)
- [x] ML Tool: Cross-validation + evaluation metrics
- [x] ML Tool: Feature importance visualization
- [x] ML Tool: Prediction endpoint
- [x] Frontend: ML results display component

---

## Phase 4 — Reports & Dashboard (Weeks 7-8)

### Week 7: Report Generator

- [x] Report Tool: PDF generation (ReportLab)
- [x] Report Tool: Word (.docx) generation
- [x] Report Tool: PowerPoint (.pptx) generation
- [x] Report Tool: Excel (.xlsx) generation
- [x] Report Tool: Markdown generation
- [x] Report Tool: AI-generated insights
- [x] Report Tool: KPI tiles
- [x] Report Tool: Business recommendations
- [x] Background task for report generation
- [x] Report download endpoint
- [x] Frontend: Report generation modal
- [x] Frontend: Reports list page

### Week 8: Dashboard Builder

- [x] Dashboard auto-generate from conversation
- [x] Dashboard CRUD endpoints
- [x] Widget system (KPI, chart, table, text)
- [x] Grid layout storage
- [x] Frontend: Dashboard grid (react-grid-layout)
- [x] Frontend: KPI widget
- [x] Frontend: Chart widget (Plotly embedded)
- [x] Frontend: Dashboard toolbar (edit, share, export)
- [x] Dashboard PDF export

---

## Phase 5 — Polish & Production (Weeks 9-10)

### Week 9: UI Polish & Admin

- [x] Dark mode implementation
- [x] Responsive mobile layout
- [x] Empty states (all pages)
- [x] Loading skeletons (all pages)
- [x] Error states + Error boundary
- [x] Onboarding flow for new users
- [x] Admin dashboard: user management
- [x] Admin dashboard: audit logs viewer
- [x] Settings page: profile, preferences
- [x] Notification system

### Week 10: Testing & Deployment

- [x] Unit tests: auth service (>90% coverage)
- [x] Unit tests: SQL tool
- [x] Unit tests: Python tool
- [x] Unit tests: ML tool
- [x] Integration tests: all API routes
- [x] E2E tests: login flow, chat flow (Playwright)
- [x] GitHub Actions CI pipeline
- [x] Docker production configs
- [x] Nginx configuration
- [x] Environment variable documentation
- [x] Deployment guide (Render + Vercel)
- [x] Performance profiling + optimization

---

## Phase 6 — Bonus Features (Future)

### Planned

- [ ] Voice input (Whisper API)
- [ ] Text-to-Speech responses
- [ ] Slack bot integration
- [ ] Scheduled reports (cron emails)
- [ ] RAG over PDF documents
- [ ] Vector database (Qdrant) for semantic search
- [ ] Real-time collaboration (WebSocket)
- [ ] Model monitoring + drift detection
- [ ] LSTM forecasting model
- [ ] Multi-tenancy (organizations)
- [ ] API access tier (developer API)
