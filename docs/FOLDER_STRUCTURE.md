# 📁 Folder Structure

## AI Data Analyst Agent — Complete Directory Layout

```
DataAnalystAgent/
│
├── README.md
├── CHANGELOG.md
├── .env.example
├── .gitignore
├── docker-compose.yml
├── docker-compose.prod.yml
│
├── docs/
│   ├── PRD.md
│   ├── ARCHITECTURE.md
│   ├── API_SPEC.md
│   ├── DATABASE.md
│   ├── DESIGN.md
│   ├── TECH_STACK.md
│   ├── CODING_STANDARDS.md
│   ├── FOLDER_STRUCTURE.md
│   ├── TASKS.md
│   └── RULES.md
│
├── .github/
│   └── workflows/
│       ├── ci.yml                  # Test + Lint on every PR
│       ├── deploy-staging.yml      # Deploy to staging on merge to main
│       └── deploy-prod.yml         # Deploy to prod on release tag
│
├── frontend/                       # Next.js 14 App Router
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── next.config.ts
│   ├── .eslintrc.json
│   ├── .prettierrc
│   │
│   ├── public/
│   │   ├── favicon.ico
│   │   └── assets/
│   │
│   └── src/
│       ├── app/                    # Next.js App Router
│       │   ├── layout.tsx          # Root layout (fonts, providers)
│       │   ├── page.tsx            # Landing page
│       │   ├── globals.css         # Global CSS + CSS variables
│       │   │
│       │   ├── (auth)/
│       │   │   ├── login/
│       │   │   │   └── page.tsx
│       │   │   ├── register/
│       │   │   │   └── page.tsx
│       │   │   └── callback/
│       │   │       └── page.tsx    # OAuth callback handler
│       │   │
│       │   ├── (dashboard)/
│       │   │   ├── layout.tsx      # Dashboard layout (sidebar)
│       │   │   ├── chat/
│       │   │   │   ├── page.tsx    # New chat
│       │   │   │   └── [sessionId]/
│       │   │   │       └── page.tsx
│       │   │   ├── datasets/
│       │   │   │   ├── page.tsx    # Dataset manager
│       │   │   │   └── [datasetId]/
│       │   │   │       └── page.tsx
│       │   │   ├── dashboards/
│       │   │   │   ├── page.tsx
│       │   │   │   └── [dashboardId]/
│       │   │   │       └── page.tsx
│       │   │   ├── reports/
│       │   │   │   └── page.tsx
│       │   │   ├── history/
│       │   │   │   └── page.tsx
│       │   │   └── settings/
│       │   │       └── page.tsx
│       │   │
│       │   └── admin/
│       │       ├── layout.tsx
│       │       ├── page.tsx        # Admin dashboard
│       │       ├── users/
│       │       │   └── page.tsx
│       │       └── audit-logs/
│       │           └── page.tsx
│       │
│       ├── components/
│       │   ├── ui/                 # Shadcn UI base components
│       │   │   ├── button.tsx
│       │   │   ├── input.tsx
│       │   │   ├── dialog.tsx
│       │   │   ├── badge.tsx
│       │   │   ├── card.tsx
│       │   │   ├── select.tsx
│       │   │   ├── table.tsx
│       │   │   ├── tabs.tsx
│       │   │   ├── tooltip.tsx
│       │   │   └── ...
│       │   │
│       │   ├── layout/             # App layout components
│       │   │   ├── Sidebar.tsx
│       │   │   ├── Header.tsx
│       │   │   ├── MobileNav.tsx
│       │   │   └── ThemeToggle.tsx
│       │   │
│       │   ├── chat/               # Chat interface
│       │   │   ├── ChatContainer.tsx
│       │   │   ├── ChatInput.tsx
│       │   │   ├── ChatMessage.tsx
│       │   │   ├── ChatMessageUser.tsx
│       │   │   ├── ChatMessageAssistant.tsx
│       │   │   ├── ThinkingIndicator.tsx
│       │   │   ├── StreamingText.tsx
│       │   │   ├── MessageSQLBlock.tsx
│       │   │   ├── MessageCodeBlock.tsx
│       │   │   ├── MessageInsights.tsx
│       │   │   └── WelcomeScreen.tsx
│       │   │
│       │   ├── charts/             # Chart components
│       │   │   ├── PlotlyChart.tsx
│       │   │   ├── ChartCard.tsx
│       │   │   └── ChartDownloader.tsx
│       │   │
│       │   ├── datasets/           # Dataset management
│       │   │   ├── DatasetUpload.tsx
│       │   │   ├── DatasetList.tsx
│       │   │   ├── DatasetCard.tsx
│       │   │   ├── DataPreview.tsx
│       │   │   └── SchemaViewer.tsx
│       │   │
│       │   ├── database/           # DB connection wizard
│       │   │   ├── DatabaseWizard.tsx
│       │   │   ├── ConnectionForm.tsx
│       │   │   └── ConnectionList.tsx
│       │   │
│       │   ├── dashboard/          # Dashboard builder
│       │   │   ├── DashboardGrid.tsx
│       │   │   ├── DashboardWidget.tsx
│       │   │   ├── KPIWidget.tsx
│       │   │   └── DashboardToolbar.tsx
│       │   │
│       │   ├── reports/            # Report management
│       │   │   ├── ReportCard.tsx
│       │   │   └── ReportDownloader.tsx
│       │   │
│       │   └── common/             # Shared utilities
│       │       ├── EmptyState.tsx
│       │       ├── LoadingSkeleton.tsx
│       │       ├── ErrorBoundary.tsx
│       │       ├── PageLoader.tsx
│       │       └── ConfirmDialog.tsx
│       │
│       ├── hooks/
│       │   ├── useAuth.ts
│       │   ├── useChat.ts
│       │   ├── useDatasets.ts
│       │   ├── useStreamingChat.ts
│       │   ├── useTheme.ts
│       │   └── useDebounce.ts
│       │
│       ├── services/               # API service layer
│       │   ├── api-client.ts       # Axios instance + interceptors
│       │   ├── auth.service.ts
│       │   ├── chat.service.ts
│       │   ├── dataset.service.ts
│       │   ├── database.service.ts
│       │   ├── chart.service.ts
│       │   ├── report.service.ts
│       │   └── dashboard.service.ts
│       │
│       ├── store/                  # Zustand stores
│       │   ├── auth.store.ts
│       │   ├── chat.store.ts
│       │   └── ui.store.ts
│       │
│       ├── types/                  # TypeScript types
│       │   ├── auth.types.ts
│       │   ├── chat.types.ts
│       │   ├── dataset.types.ts
│       │   ├── chart.types.ts
│       │   └── api.types.ts
│       │
│       ├── lib/                    # Utilities
│       │   ├── utils.ts
│       │   ├── formatters.ts
│       │   └── validators.ts
│       │
│       └── providers/              # React context providers
│           ├── QueryProvider.tsx
│           ├── ThemeProvider.tsx
│           └── AuthProvider.tsx
│
│
├── backend/                        # FastAPI application
│   ├── main.py                     # App entry point
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   ├── pyproject.toml
│   ├── alembic.ini
│   │
│   ├── alembic/                    # DB migrations
│   │   ├── env.py
│   │   └── versions/
│   │       └── 001_initial_schema.py
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py               # Settings (Pydantic BaseSettings)
│   │   │
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   ├── base.py             # SQLAlchemy Base, engine, session
│   │   │   └── redis.py            # Redis connection
│   │   │
│   │   ├── models/                 # SQLAlchemy ORM models
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── session.py
│   │   │   ├── data_source.py
│   │   │   ├── dataset.py
│   │   │   ├── conversation.py
│   │   │   ├── message.py
│   │   │   ├── generated_query.py
│   │   │   ├── generated_chart.py
│   │   │   ├── generated_report.py
│   │   │   ├── dashboard.py
│   │   │   └── audit_log.py
│   │   │
│   │   ├── schemas/                # Pydantic request/response schemas
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── upload.py
│   │   │   ├── database.py
│   │   │   ├── chat.py
│   │   │   ├── query.py
│   │   │   ├── chart.py
│   │   │   ├── report.py
│   │   │   ├── dashboard.py
│   │   │   └── common.py
│   │   │
│   │   ├── routes/                 # API route handlers
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── upload.py
│   │   │   ├── database.py
│   │   │   ├── chat.py
│   │   │   ├── query.py
│   │   │   ├── chart.py
│   │   │   ├── report.py
│   │   │   ├── dashboard.py
│   │   │   ├── export.py
│   │   │   ├── history.py
│   │   │   └── settings.py
│   │   │
│   │   ├── services/               # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── upload_service.py
│   │   │   ├── database_service.py
│   │   │   ├── chat_service.py
│   │   │   ├── chart_service.py
│   │   │   ├── report_service.py
│   │   │   └── dashboard_service.py
│   │   │
│   │   ├── repositories/           # Data access layer
│   │   │   ├── __init__.py
│   │   │   ├── user_repo.py
│   │   │   ├── dataset_repo.py
│   │   │   ├── conversation_repo.py
│   │   │   └── message_repo.py
│   │   │
│   │   ├── middleware/             # FastAPI middleware
│   │   │   ├── __init__.py
│   │   │   ├── auth.py             # JWT verification
│   │   │   ├── rate_limit.py
│   │   │   ├── cors.py
│   │   │   ├── logging.py
│   │   │   └── audit.py
│   │   │
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── security.py         # Password hashing, token generation
│   │       ├── encryption.py       # Fernet encryption
│   │       ├── validators.py       # Input validation helpers
│   │       ├── exceptions.py       # Custom exception classes
│   │       ├── storage.py          # MinIO/S3 operations
│   │       └── pagination.py
│   │
│   ├── agents/                     # AI Agent Orchestration
│   │   ├── __init__.py
│   │   ├── orchestrator.py         # Main LangGraph agent
│   │   ├── planner.py              # Task planning
│   │   ├── intent_classifier.py    # Intent detection
│   │   ├── memory.py               # Conversation memory
│   │   └── state.py                # LangGraph state definitions
│   │
│   ├── tools/                      # Agent tools
│   │   ├── __init__.py
│   │   ├── base_tool.py            # Abstract base tool
│   │   ├── sql_tool.py             # NL → SQL, execution
│   │   ├── python_tool.py          # Python execution sandbox
│   │   ├── visualization_tool.py   # Plotly chart generation
│   │   ├── ml_tool.py              # ML pipeline
│   │   ├── statistics_tool.py      # Statistical analysis
│   │   └── report_tool.py          # Report generation
│   │
│   ├── prompts/                    # LLM prompt templates
│   │   ├── __init__.py
│   │   ├── intent.py
│   │   ├── planner.py
│   │   ├── sql_generator.py
│   │   ├── python_generator.py
│   │   ├── chart_selector.py
│   │   ├── insights.py
│   │   └── report.py
│   │
│   └── tasks/                      # Celery background tasks
│       ├── __init__.py
│       ├── celery_app.py
│       ├── upload_tasks.py
│       ├── ml_tasks.py
│       └── report_tasks.py
│
│
├── tests/
│   ├── conftest.py
│   ├── factories/
│   │   ├── user_factory.py
│   │   └── dataset_factory.py
│   │
│   ├── unit/
│   │   ├── test_auth_service.py
│   │   ├── test_sql_tool.py
│   │   ├── test_python_tool.py
│   │   ├── test_ml_tool.py
│   │   ├── test_visualization_tool.py
│   │   └── test_upload_service.py
│   │
│   └── integration/
│       ├── test_auth_routes.py
│       ├── test_upload_routes.py
│       ├── test_chat_routes.py
│       └── test_query_routes.py
│
│
└── docker/
    ├── Dockerfile.backend
    ├── Dockerfile.frontend
    ├── Dockerfile.worker
    └── nginx/
        ├── nginx.conf
        └── ssl/
```
