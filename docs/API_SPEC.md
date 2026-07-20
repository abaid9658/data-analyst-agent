# 🔌 API Specification

## AI Data Analyst Agent — REST API v1

**Base URL:** `https://api.dataanalystagent.com/api/v1`  
**Auth:** Bearer token (JWT) in `Authorization` header  
**Content-Type:** `application/json`

---

## Authentication

### POST /auth/register

Register a new user.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "full_name": "John Doe"
}
```

**Response 201:**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "analyst",
  "created_at": "2026-07-17T10:00:00Z"
}
```

---

### POST /auth/login

Login with email and password.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response 200:**
```json
{
  "access_token": "eyJhbGci...",
  "refresh_token": "eyJhbGci...",
  "token_type": "bearer",
  "expires_in": 900,
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "full_name": "John Doe",
    "role": "analyst"
  }
}
```

---

### POST /auth/refresh

Refresh access token.

**Request:**
```json
{
  "refresh_token": "eyJhbGci..."
}
```

**Response 200:**
```json
{
  "access_token": "eyJhbGci...",
  "expires_in": 900
}
```

---

### POST /auth/logout

Revoke refresh token.

**Response 200:**
```json
{ "message": "Logged out successfully" }
```

---

### GET /auth/google

Redirect to Google OAuth. (Redirects to Google)

### GET /auth/google/callback

Handle Google OAuth callback. Returns tokens.

### GET /auth/github

Redirect to GitHub OAuth.

### GET /auth/github/callback

Handle GitHub OAuth callback. Returns tokens.

---

## Upload

### POST /upload/file

Upload a CSV, Excel, or JSON file.

**Request:** `multipart/form-data`
- `file` — the data file
- `name` (optional) — friendly name
- `description` (optional)

**Response 202:**
```json
{
  "dataset_id": "uuid",
  "name": "sales_data.csv",
  "status": "processing",
  "task_id": "celery-task-uuid",
  "message": "File uploaded. Processing in background."
}
```

---

### GET /upload/status/{task_id}

Check upload processing status.

**Response 200:**
```json
{
  "task_id": "celery-task-uuid",
  "status": "completed",
  "dataset_id": "uuid",
  "schema": {
    "columns": [
      { "name": "date", "type": "datetime", "nullable": false },
      { "name": "revenue", "type": "float", "nullable": false },
      { "name": "region", "type": "string", "nullable": true }
    ],
    "row_count": 12453,
    "file_size_mb": 2.4
  },
  "profile": {
    "missing_values": { "region": 23 },
    "duplicates": 0,
    "numeric_summary": {
      "revenue": {
        "mean": 45230.5, "std": 12300.2,
        "min": 100.0, "max": 250000.0,
        "p25": 22000.0, "p50": 40000.0, "p75": 65000.0
      }
    }
  }
}
```

---

### GET /upload/datasets

List all uploaded datasets for current user.

**Response 200:**
```json
{
  "datasets": [
    {
      "id": "uuid",
      "name": "sales_data.csv",
      "row_count": 12453,
      "column_count": 8,
      "file_size_mb": 2.4,
      "created_at": "2026-07-17T10:00:00Z",
      "status": "ready"
    }
  ],
  "total": 5
}
```

---

### DELETE /upload/datasets/{dataset_id}

Delete a dataset.

**Response 200:**
```json
{ "message": "Dataset deleted successfully" }
```

---

## Database Connections

### POST /database/connect

Test and save a database connection.

**Request:**
```json
{
  "name": "Production DB",
  "type": "postgresql",
  "host": "db.example.com",
  "port": 5432,
  "database": "analytics",
  "username": "readonly_user",
  "password": "secret",
  "ssl": true
}
```

**Response 201:**
```json
{
  "connection_id": "uuid",
  "name": "Production DB",
  "type": "postgresql",
  "status": "connected",
  "tables": ["orders", "customers", "products"],
  "schema_preview": {
    "orders": {
      "columns": ["id", "customer_id", "total", "created_at"],
      "row_count": 1234567
    }
  }
}
```

---

### POST /database/test

Test a connection without saving.

**Request:** (same as /database/connect)

**Response 200:**
```json
{
  "status": "success",
  "latency_ms": 45,
  "tables_count": 12
}
```

---

### GET /database/connections

List saved connections.

**Response 200:**
```json
{
  "connections": [
    {
      "id": "uuid",
      "name": "Production DB",
      "type": "postgresql",
      "status": "healthy",
      "last_used": "2026-07-17T09:30:00Z"
    }
  ]
}
```

---

### DELETE /database/connections/{connection_id}

Delete a connection.

**Response 200:**
```json
{ "message": "Connection deleted" }
```

---

## Chat

### POST /chat/message

Send a message to the AI agent. Returns Server-Sent Events stream.

**Request:**
```json
{
  "message": "Show me monthly revenue trend for last year",
  "session_id": "uuid",
  "dataset_id": "uuid",
  "stream": true
}
```

**Response:** `text/event-stream`

```
data: {"type": "thinking", "content": "Analyzing your request..."}

data: {"type": "plan", "content": {"steps": ["Load dataset", "Aggregate by month", "Generate chart", "Provide insights"]}}

data: {"type": "sql", "content": "SELECT DATE_TRUNC('month', date) as month, SUM(revenue) as total_revenue FROM sales GROUP BY 1 ORDER BY 1"}

data: {"type": "code", "content": "import pandas as pd\ndf = pd.read_csv(...)..."}

data: {"type": "text", "content": "Revenue has grown 23% year-over-year..."}

data: {"type": "chart", "content": {"type": "line", "plotly_spec": {...}}}

data: {"type": "insights", "content": ["Peak month: December ($2.3M)", "Q4 outperforms Q1 by 45%"]}

data: {"type": "done", "message_id": "uuid"}
```

---

### GET /chat/sessions

List all chat sessions.

**Response 200:**
```json
{
  "sessions": [
    {
      "id": "uuid",
      "title": "Sales Analysis Q4",
      "message_count": 12,
      "dataset_id": "uuid",
      "created_at": "2026-07-17T08:00:00Z",
      "updated_at": "2026-07-17T09:45:00Z"
    }
  ]
}
```

---

### GET /chat/sessions/{session_id}/messages

Get full conversation history.

**Response 200:**
```json
{
  "session_id": "uuid",
  "messages": [
    {
      "id": "uuid",
      "role": "user",
      "content": "Show monthly revenue",
      "created_at": "2026-07-17T08:05:00Z"
    },
    {
      "id": "uuid",
      "role": "assistant",
      "content": "Here is your monthly revenue analysis...",
      "metadata": {
        "sql_query": "SELECT...",
        "chart_spec": {...},
        "insights": [...]
      },
      "created_at": "2026-07-17T08:05:15Z"
    }
  ]
}
```

---

### DELETE /chat/sessions/{session_id}

Delete a conversation.

**Response 200:**
```json
{ "message": "Session deleted" }
```

---

## Query (SQL)

### POST /query/generate

Generate SQL from natural language.

**Request:**
```json
{
  "question": "Total revenue by region last quarter",
  "connection_id": "uuid",
  "table_context": ["orders", "regions"]
}
```

**Response 200:**
```json
{
  "sql": "SELECT r.name as region, SUM(o.total) as revenue FROM orders o JOIN regions r ON o.region_id = r.id WHERE o.created_at >= '2026-04-01' AND o.created_at < '2026-07-01' GROUP BY r.name ORDER BY revenue DESC",
  "explanation": "This query joins the orders and regions tables, filters for Q2 2026, groups by region name, and sorts by total revenue descending.",
  "estimated_rows": 12,
  "tables_used": ["orders", "regions"]
}
```

---

### POST /query/execute

Execute a SQL query.

**Request:**
```json
{
  "sql": "SELECT region, SUM(revenue) FROM orders GROUP BY region",
  "connection_id": "uuid",
  "limit": 1000
}
```

**Response 200:**
```json
{
  "columns": ["region", "sum_revenue"],
  "rows": [
    ["North America", 1234567.89],
    ["Europe", 987654.32]
  ],
  "row_count": 5,
  "execution_time_ms": 234
}
```

---

## Chart

### POST /chart/generate

Generate a chart from data.

**Request:**
```json
{
  "dataset_id": "uuid",
  "chart_type": "auto",
  "x_column": "month",
  "y_column": "revenue",
  "title": "Monthly Revenue 2026",
  "color_column": "region"
}
```

**Response 200:**
```json
{
  "chart_id": "uuid",
  "chart_type": "line",
  "plotly_spec": {
    "data": [...],
    "layout": {...},
    "config": {...}
  },
  "explanation": "Line chart chosen because x-axis is temporal and y-axis is continuous.",
  "download_urls": {
    "png": "/chart/uuid/download?format=png",
    "svg": "/chart/uuid/download?format=svg",
    "pdf": "/chart/uuid/download?format=pdf"
  }
}
```

---

## Report

### POST /report/generate

Generate a report.

**Request:**
```json
{
  "session_id": "uuid",
  "format": "pdf",
  "title": "Q2 2026 Sales Analysis",
  "include_sections": ["summary", "charts", "insights", "recommendations"]
}
```

**Response 202:**
```json
{
  "report_id": "uuid",
  "status": "generating",
  "task_id": "celery-task-uuid"
}
```

---

### GET /report/{report_id}

Get report status and download URL.

**Response 200:**
```json
{
  "report_id": "uuid",
  "status": "ready",
  "format": "pdf",
  "title": "Q2 2026 Sales Analysis",
  "download_url": "/report/uuid/download",
  "created_at": "2026-07-17T10:30:00Z",
  "expires_at": "2026-07-24T10:30:00Z"
}
```

---

## Dashboard

### POST /dashboard/auto-generate

Auto-generate a dashboard from a session.

**Request:**
```json
{
  "session_id": "uuid",
  "title": "Sales Dashboard"
}
```

**Response 201:**
```json
{
  "dashboard_id": "uuid",
  "title": "Sales Dashboard",
  "widgets": [
    { "id": "w1", "type": "kpi", "title": "Total Revenue", "value": "$2.3M" },
    { "id": "w2", "type": "chart", "chart_id": "uuid" },
    { "id": "w3", "type": "table", "data": [...] }
  ],
  "layout": [...]
}
```

---

## History

### GET /history

Get analysis history.

**Query Params:** `page`, `limit`, `search`

**Response 200:**
```json
{
  "items": [
    {
      "id": "uuid",
      "type": "query",
      "question": "Show monthly revenue",
      "dataset_name": "sales_data.csv",
      "created_at": "2026-07-17T09:00:00Z"
    }
  ],
  "total": 45,
  "page": 1,
  "limit": 20
}
```

---

## Settings

### GET /settings/profile

Get user profile.

**Response 200:**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "analyst",
  "preferences": {
    "theme": "dark",
    "default_chart_type": "auto",
    "language": "en"
  }
}
```

---

### PUT /settings/profile

Update user profile.

**Request:**
```json
{
  "full_name": "John Doe",
  "preferences": {
    "theme": "dark"
  }
}
```

---

## Error Responses

All errors follow this format:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email is required",
    "details": {
      "field": "email",
      "constraint": "required"
    }
  },
  "request_id": "uuid",
  "timestamp": "2026-07-17T10:00:00Z"
}
```

**Error Codes:**

| HTTP | Code | Description |
|---|---|---|
| 400 | VALIDATION_ERROR | Invalid request body |
| 401 | UNAUTHORIZED | Missing or invalid token |
| 403 | FORBIDDEN | Insufficient permissions |
| 404 | NOT_FOUND | Resource not found |
| 409 | CONFLICT | Resource already exists |
| 422 | UNPROCESSABLE | Semantic validation error |
| 429 | RATE_LIMITED | Too many requests |
| 500 | INTERNAL_ERROR | Server error |
| 503 | SERVICE_UNAVAILABLE | LLM/DB temporarily unavailable |
