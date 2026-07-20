# 📏 Coding Standards

## AI Data Analyst Agent

---

## 1. General Rules

1. **TypeScript everywhere** — No JavaScript files. No `any` type.
2. **Async/Await** — No raw `.then()` chains. All async code uses `async/await`.
3. **Error handling** — Every async function has try/catch. Never let errors go silent.
4. **No hardcoded values** — All config via environment variables.
5. **No fake/mock data in production code** — Use proper test factories in tests.
6. **Validation everywhere** — Every input validated at the API layer (Pydantic) and frontend (Zod).
7. **Never skip tests for new features.**
8. **Always update documentation when behavior changes.**

---

## 2. Python Standards (Backend)

### Style & Formatting

```python
# Tool: Ruff + Black
# Line length: 88 characters
# Python version: 3.11+

# ✅ Good
async def get_user_by_email(email: str) -> User | None:
    """Fetch a user by their email address."""
    result = await db.execute(
        select(User).where(User.email == email)
    )
    return result.scalar_one_or_none()

# ❌ Bad
def get_user(e):
    return db.query(User).filter(User.email == e).first()
```

### Type Annotations

```python
# ✅ Required — all function signatures typed
from typing import Optional, List
from uuid import UUID

async def create_dataset(
    user_id: UUID,
    name: str,
    file_path: str,
    schema: dict[str, str],
) -> Dataset:
    ...

# ❌ Never use Any unless absolutely unavoidable
from typing import Any  # Avoid
```

### Error Handling

```python
# ✅ Good — specific exceptions, logged
from app.utils.exceptions import DatasetNotFoundError

async def get_dataset(dataset_id: UUID) -> Dataset:
    dataset = await dataset_repo.get_by_id(dataset_id)
    if dataset is None:
        raise DatasetNotFoundError(dataset_id=dataset_id)
    return dataset

# ❌ Bad — bare except, no logging
try:
    data = get_data()
except:
    pass
```

### Pydantic Models

```python
# ✅ Good
from pydantic import BaseModel, Field, EmailStr
from uuid import UUID

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    full_name: str = Field(..., min_length=1, max_length=255)

    model_config = ConfigDict(str_strip_whitespace=True)
```

### Repository Pattern

```python
# ✅ All DB access through repository classes
class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: UUID) -> User | None:
        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def create(self, user_data: UserCreate) -> User:
        user = User(**user_data.model_dump())
        self.session.add(user)
        await self.session.flush()
        return user
```

### Service Layer

```python
# ✅ Business logic in services, not routes
class AuthService:
    def __init__(self, user_repo: UserRepository, ...):
        self.user_repo = user_repo

    async def register(self, data: UserCreate) -> AuthResponse:
        # Check email uniqueness
        existing = await self.user_repo.get_by_email(data.email)
        if existing:
            raise EmailAlreadyExistsError()
        
        # Hash password
        hashed = hash_password(data.password)
        
        # Create user
        user = await self.user_repo.create(
            UserCreate(password=hashed, **data.model_dump(exclude={'password'}))
        )
        
        # Generate tokens
        return self._create_auth_response(user)
```

---

## 3. TypeScript Standards (Frontend)

### Types & Interfaces

```typescript
// ✅ Always define types — never use any
interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  metadata?: MessageMetadata;
  createdAt: Date;
}

// ✅ Enums for fixed sets
enum ChartType {
  Bar = 'bar',
  Line = 'line',
  Scatter = 'scatter',
  Pie = 'pie',
}

// ❌ Never
const data: any = await fetchData();
```

### React Components

```typescript
// ✅ Typed props, named exports, JSDoc for complex props
interface ChatMessageProps {
  message: Message;
  /** Whether to show the avatar */
  showAvatar?: boolean;
  onCopy?: (content: string) => void;
}

export const ChatMessage: React.FC<ChatMessageProps> = ({
  message,
  showAvatar = true,
  onCopy,
}) => {
  // ...
};
```

### API Service Layer

```typescript
// ✅ Centralized API calls with proper typing
import { apiClient } from '@/lib/api-client';
import type { ApiResponse, Message, SendMessageRequest } from '@/types';

export const chatService = {
  sendMessage: async (request: SendMessageRequest): Promise<ApiResponse<Message>> => {
    const { data } = await apiClient.post<ApiResponse<Message>>('/chat/message', request);
    return data;
  },
};
```

### Custom Hooks

```typescript
// ✅ Abstract data fetching into hooks
export const useConversation = (sessionId: string) => {
  return useQuery({
    queryKey: ['conversation', sessionId],
    queryFn: () => chatService.getMessages(sessionId),
    staleTime: 1000 * 60, // 1 minute
  });
};
```

### Zod Validation

```typescript
// ✅ Validate all forms and API inputs
import { z } from 'zod';

export const loginSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});

export type LoginFormData = z.infer<typeof loginSchema>;
```

---

## 4. API Design Rules

- **RESTful naming:** Resources are nouns, not verbs (`/datasets` not `/getDatasets`)
- **HTTP methods:** GET (read), POST (create), PUT (full update), PATCH (partial), DELETE
- **Versioning:** All routes prefixed with `/api/v1/`
- **Pagination:** All list endpoints support `page` & `limit` query params
- **Response envelope:** Consistent response structure (see API_SPEC.md)
- **Error codes:** Always return structured error objects (never bare strings)
- **Idempotency:** POST requests should be idempotent where possible

---

## 5. Security Rules

- **Never log sensitive data** (passwords, tokens, credentials)
- **Never store plaintext credentials** — always encrypt
- **Sanitize all SQL** — use parameterized queries, never string interpolation
- **Validate all file uploads** — check MIME type, extension, and content
- **Rate limit all endpoints** — stricter limits for auth endpoints
- **Use HTTPS everywhere** — never send sensitive data over HTTP
- **Rotate tokens** — refresh token rotation on every use
- **Audit log** — all sensitive operations (login, data access, deletion)

---

## 6. Git Workflow

### Branch Naming

```
feature/DAA-123-add-sql-generation
bugfix/DAA-456-fix-chart-export
hotfix/DAA-789-patch-auth-bypass
chore/DAA-012-update-dependencies
docs/DAA-345-update-api-spec
```

### Commit Messages (Conventional Commits)

```
feat: add SQL explanation feature
fix: resolve chart export PDF cropping
docs: update API_SPEC for /chart endpoint
chore: upgrade plotly to v2.30
refactor: extract chart service from agent
test: add integration tests for ML tool
perf: cache dataset schema in Redis
security: patch SQL injection in query executor
```

### PR Requirements

- ✅ Tests pass (CI must be green)
- ✅ Lint passes
- ✅ Types pass (mypy / TypeScript)
- ✅ At least 1 reviewer approval
- ✅ Documentation updated if behavior changed
- ✅ CHANGELOG entry added

---

## 7. Testing Standards

### Backend

```python
# ✅ Each feature has unit tests
@pytest.mark.asyncio
async def test_register_user_success(client: AsyncClient, db_session):
    response = await client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "password": "SecurePass123!",
        "full_name": "Test User",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "password" not in data

# ✅ Test factories for data creation
from tests.factories import UserFactory

async def test_get_dataset(client, user_factory):
    user = await user_factory.create()
    # ...
```

### Coverage Targets

| Layer | Minimum Coverage |
|---|---|
| Routes | 90% |
| Services | 85% |
| Tools (Agent) | 80% |
| Utils | 95% |
| Frontend Components | 70% |

---

## 8. Documentation Rules

- Every public function/class has a docstring
- API endpoints have inline docs (FastAPI's `summary` and `description`)
- All environment variables documented in `.env.example`
- README updated when setup process changes
- CHANGELOG entry for every user-facing change
- Never delete documentation — mark deprecated instead

---

## 9. Performance Rules

- Database queries: always use `LIMIT` on unbounded queries
- Async all the way: never use synchronous DB calls in async context
- Cache expensive operations (schema detection, ML training)
- Background tasks for slow operations (file parsing, ML, reports)
- Streaming responses for LLM output
- Lazy loading for large data tables (server-side pagination)
- Index all foreign keys and common filter columns
