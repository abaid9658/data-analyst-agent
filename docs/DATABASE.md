# 🗄️ Database Schema

## AI Data Analyst Agent

**Database:** PostgreSQL 15  
**ORM:** SQLAlchemy 2.0 with Alembic migrations

---

## Tables Overview

| Table | Purpose |
|---|---|
| `users` | User accounts |
| `sessions` | Auth sessions (refresh tokens) |
| `data_sources` | Database connections |
| `datasets` | Uploaded file metadata |
| `dataset_profiles` | Statistical profiles |
| `conversations` | Chat sessions |
| `messages` | Individual messages |
| `generated_queries` | SQL query history |
| `generated_charts` | Chart spec history |
| `generated_reports` | Report metadata |
| `dashboards` | Dashboard configurations |
| `dashboard_widgets` | Widget layout |
| `audit_logs` | Security audit trail |

---

## Table Definitions

### users

```sql
CREATE TABLE users (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email       VARCHAR(255) UNIQUE NOT NULL,
    full_name   VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255),           -- NULL for OAuth users
    role        VARCHAR(50) NOT NULL DEFAULT 'analyst',  -- admin, analyst, viewer
    is_active   BOOLEAN NOT NULL DEFAULT TRUE,
    is_verified BOOLEAN NOT NULL DEFAULT FALSE,
    avatar_url  VARCHAR(500),
    
    -- OAuth
    google_id   VARCHAR(255) UNIQUE,
    github_id   VARCHAR(255) UNIQUE,
    
    -- Preferences (JSONB)
    preferences JSONB NOT NULL DEFAULT '{
        "theme": "dark",
        "default_chart_type": "auto",
        "language": "en",
        "timezone": "UTC"
    }'::jsonb,
    
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_login  TIMESTAMPTZ
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
```

---

### sessions

```sql
CREATE TABLE sessions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    refresh_token   VARCHAR(512) UNIQUE NOT NULL,
    expires_at      TIMESTAMPTZ NOT NULL,
    ip_address      INET,
    user_agent      VARCHAR(500),
    is_revoked      BOOLEAN NOT NULL DEFAULT FALSE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_sessions_refresh_token ON sessions(refresh_token);
```

---

### data_sources

```sql
CREATE TABLE data_sources (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name            VARCHAR(255) NOT NULL,
    type            VARCHAR(50) NOT NULL,    -- postgresql, mysql, sqlite, sqlserver, mongodb
    
    -- Encrypted connection details
    encrypted_config BYTEA NOT NULL,         -- Fernet encrypted JSON
    
    -- Metadata
    status          VARCHAR(50) DEFAULT 'active',  -- active, error, disabled
    last_connected  TIMESTAMPTZ,
    tables_cache    JSONB,                   -- cached schema info
    
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_data_sources_user_id ON data_sources(user_id);
```

---

### datasets

```sql
CREATE TABLE datasets (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name            VARCHAR(255) NOT NULL,
    description     TEXT,
    
    -- File info
    original_filename VARCHAR(500),
    file_type       VARCHAR(20),             -- csv, excel, json
    file_size_bytes BIGINT,
    storage_path    VARCHAR(1000),           -- MinIO/S3 path
    
    -- Schema
    schema          JSONB,                   -- column definitions
    row_count       BIGINT,
    column_count    INTEGER,
    
    -- Processing
    status          VARCHAR(50) DEFAULT 'processing',  -- processing, ready, error
    error_message   TEXT,
    
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_datasets_user_id ON datasets(user_id);
CREATE INDEX idx_datasets_status ON datasets(status);
```

---

### dataset_profiles

```sql
CREATE TABLE dataset_profiles (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dataset_id      UUID NOT NULL REFERENCES datasets(id) ON DELETE CASCADE,
    
    -- Profile data
    missing_values  JSONB,                   -- { column: count }
    duplicate_rows  INTEGER DEFAULT 0,
    data_types      JSONB,                   -- { column: inferred_type }
    numeric_stats   JSONB,                   -- { column: { mean, std, min, max, p25, p50, p75 } }
    categorical_stats JSONB,                 -- { column: { top_values, unique_count } }
    correlations    JSONB,                   -- correlation matrix
    outlier_indices INTEGER[],
    
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

---

### conversations

```sql
CREATE TABLE conversations (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title           VARCHAR(500),
    
    -- Context
    dataset_id      UUID REFERENCES datasets(id) ON DELETE SET NULL,
    data_source_id  UUID REFERENCES data_sources(id) ON DELETE SET NULL,
    
    -- Stats
    message_count   INTEGER DEFAULT 0,
    
    -- Settings
    is_pinned       BOOLEAN DEFAULT FALSE,
    is_archived     BOOLEAN DEFAULT FALSE,
    
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_conversations_updated_at ON conversations(updated_at DESC);
```

---

### messages

```sql
CREATE TABLE messages (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    
    role            VARCHAR(20) NOT NULL,    -- user, assistant, system
    content         TEXT NOT NULL,
    
    -- Rich metadata for assistant messages
    metadata        JSONB,                   -- { sql_query, python_code, chart_id, insights, plan_steps }
    
    -- Token usage (for cost tracking)
    prompt_tokens   INTEGER,
    completion_tokens INTEGER,
    
    -- Processing
    processing_time_ms INTEGER,
    model_used      VARCHAR(100),
    
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
```

---

### generated_queries

```sql
CREATE TABLE generated_queries (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    message_id      UUID REFERENCES messages(id) ON DELETE SET NULL,
    
    -- Query details
    natural_language TEXT NOT NULL,
    sql_query       TEXT NOT NULL,
    explanation     TEXT,
    
    -- Execution
    execution_status VARCHAR(50),            -- success, error, timeout
    execution_time_ms INTEGER,
    row_count       INTEGER,
    error_message   TEXT,
    
    -- Source
    data_source_id  UUID REFERENCES data_sources(id) ON DELETE SET NULL,
    tables_used     VARCHAR(255)[],
    
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_generated_queries_user_id ON generated_queries(user_id);
```

---

### generated_charts

```sql
CREATE TABLE generated_charts (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    message_id      UUID REFERENCES messages(id) ON DELETE SET NULL,
    
    chart_type      VARCHAR(50),             -- bar, line, scatter, pie, histogram, etc.
    title           VARCHAR(500),
    plotly_spec     JSONB NOT NULL,          -- full Plotly figure spec
    explanation     TEXT,                    -- why this chart was chosen
    
    -- Storage paths for exports
    png_path        VARCHAR(1000),
    svg_path        VARCHAR(1000),
    
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_generated_charts_user_id ON generated_charts(user_id);
```

---

### generated_reports

```sql
CREATE TABLE generated_reports (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    conversation_id UUID REFERENCES conversations(id) ON DELETE SET NULL,
    
    title           VARCHAR(500) NOT NULL,
    format          VARCHAR(20) NOT NULL,    -- pdf, docx, pptx, xlsx, markdown
    
    -- Storage
    file_path       VARCHAR(1000),
    file_size_bytes INTEGER,
    
    -- Status
    status          VARCHAR(50) DEFAULT 'generating',  -- generating, ready, error
    error_message   TEXT,
    
    -- Metadata
    sections        JSONB,                   -- which sections were included
    
    -- Expiry
    expires_at      TIMESTAMPTZ,
    
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_generated_reports_user_id ON generated_reports(user_id);
```

---

### dashboards

```sql
CREATE TABLE dashboards (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title           VARCHAR(500) NOT NULL,
    description     TEXT,
    
    -- Layout (react-grid-layout format)
    layout          JSONB,
    
    -- Sharing
    is_public       BOOLEAN DEFAULT FALSE,
    share_token     VARCHAR(255) UNIQUE,
    
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

---

### dashboard_widgets

```sql
CREATE TABLE dashboard_widgets (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dashboard_id    UUID NOT NULL REFERENCES dashboards(id) ON DELETE CASCADE,
    
    widget_type     VARCHAR(50) NOT NULL,    -- kpi, chart, table, text
    title           VARCHAR(255),
    
    -- Widget config
    config          JSONB NOT NULL,          -- type-specific config
    
    -- Position (grid)
    grid_x          INTEGER NOT NULL DEFAULT 0,
    grid_y          INTEGER NOT NULL DEFAULT 0,
    grid_w          INTEGER NOT NULL DEFAULT 4,
    grid_h          INTEGER NOT NULL DEFAULT 3,
    
    -- Data source
    chart_id        UUID REFERENCES generated_charts(id) ON DELETE SET NULL,
    query_id        UUID REFERENCES generated_queries(id) ON DELETE SET NULL,
    
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_dashboard_widgets_dashboard_id ON dashboard_widgets(dashboard_id);
```

---

### audit_logs

```sql
CREATE TABLE audit_logs (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID REFERENCES users(id) ON DELETE SET NULL,
    
    -- Event
    action          VARCHAR(100) NOT NULL,   -- login, upload, query_execute, etc.
    resource_type   VARCHAR(100),            -- dataset, query, report, etc.
    resource_id     UUID,
    
    -- Details
    details         JSONB,
    
    -- Request info
    ip_address      INET,
    user_agent      VARCHAR(500),
    request_id      VARCHAR(255),
    
    -- Status
    status          VARCHAR(20) DEFAULT 'success',  -- success, failure
    error_message   TEXT,
    
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at DESC);
```

---

## Relationships

```
users ──────────────────┬── sessions (1:N)
                        ├── data_sources (1:N)
                        ├── datasets (1:N)
                        ├── conversations (1:N)
                        ├── generated_queries (1:N)
                        ├── generated_charts (1:N)
                        ├── generated_reports (1:N)
                        ├── dashboards (1:N)
                        └── audit_logs (1:N)

conversations ──────────┬── messages (1:N)
                        ├── datasets (N:1)
                        └── data_sources (N:1)

messages ───────────────┬── generated_queries (1:N)
                        └── generated_charts (1:N)

dashboards ─────────────── dashboard_widgets (1:N)

dashboard_widgets ──────┬── generated_charts (N:1)
                        └── generated_queries (N:1)
```

---

## Indexes Strategy

All foreign keys are indexed. Additional indexes:

- `users.email` — login lookups
- `users.google_id`, `users.github_id` — OAuth lookups
- `sessions.refresh_token` — token validation
- `conversations.updated_at DESC` — recent conversations list
- `messages.created_at` — chronological message fetching
- `audit_logs.created_at DESC` — recent audit log queries
