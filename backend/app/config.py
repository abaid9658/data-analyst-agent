"""
Application Configuration — Pydantic BaseSettings
✅ Gemini LLM + Local HuggingFace Embeddings (no OpenAI required)
"""
from functools import lru_cache
from typing import Literal

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Application ──────────────────────────────────────────────────────────
    APP_NAME: str = "AI Data Analyst Agent"
    APP_ENV: Literal["development", "staging", "production"] = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000

    # ── CORS ─────────────────────────────────────────────────────────────────
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_origins(cls, v: str | list) -> list[str]:
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    # ── Database ─────────────────────────────────────────────────────────────
    DATABASE_URL: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "dataanalyst"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = ""

    # ── Redis ────────────────────────────────────────────────────────────────
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

    # ── JWT Auth ─────────────────────────────────────────────────────────────
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ── Google OAuth ─────────────────────────────────────────────────────────
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/api/v1/auth/google/callback"

    # ── GitHub OAuth ─────────────────────────────────────────────────────────
    GITHUB_CLIENT_ID: str = ""
    GITHUB_CLIENT_SECRET: str = ""
    GITHUB_REDIRECT_URI: str = "http://localhost:8000/api/v1/auth/github/callback"

    FRONTEND_URL: str = "http://localhost:3000"

    # ── LLM ──────────────────────────────────────────────────────────────────
    # ✅ Default provider is Google Gemini (free tier)
    LLM_PROVIDER: Literal["openai", "anthropic", "google"] = "google"

    # Google Gemini (primary — free)
    GOOGLE_AI_API_KEY: str = ""
    GOOGLE_AI_MODEL: str = "gemini-2.5-flash"

    # OpenAI (optional fallback — paid)
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o"

    # Anthropic (optional fallback — paid)
    ANTHROPIC_API_KEY: str = ""
    ANTHROPIC_MODEL: str = "claude-3-5-sonnet-20241022"

    # ── Object Storage ───────────────────────────────────────────────────────
    STORAGE_PROVIDER: Literal["minio", "s3"] = "minio"
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_SECURE: bool = False
    MINIO_BUCKET: str = "dataanalyst"
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "us-east-1"
    S3_BUCKET: str = "dataanalyst"

    # ── Security ─────────────────────────────────────────────────────────────
    ENCRYPTION_KEY: str = ""
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_AUTH_PER_MINUTE: int = 10
    MAX_FILE_SIZE_MB: int = 500

    # ── Qdrant Vector Database ───────────────────────────────────────────────
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_COLLECTION_NAME: str = "pdf_documents"

    # ── Embeddings — LOCAL HuggingFace (FREE, No API key needed) ─────────────
    # ✅ sentence-transformers/all-MiniLM-L6-v2 → dimension=384
    # ✅ BAAI/bge-small-en-v1.5               → dimension=384
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_DIMENSION: int = 384           # Must match the chosen model
    EMBEDDING_DEVICE: str = "cpu"           # "cpu" | "cuda"
    EMBEDDING_CHUNK_SIZE: int = 800         # Characters per text chunk
    EMBEDDING_CHUNK_OVERLAP: int = 150      # Overlap between chunks
    PDF_MAX_FILE_SIZE_MB: int = 50          # Max PDF size in MB

    @property
    def max_file_size_bytes(self) -> int:
        return self.MAX_FILE_SIZE_MB * 1024 * 1024

    def get_llm(self, temperature: float = 0):
        """
        Return the configured LLM instance based on LLM_PROVIDER.
        ✅ Defaults to Gemini — no OpenAI key needed.
        """
        if self.LLM_PROVIDER == "google":
            from langchain_google_genai import ChatGoogleGenerativeAI
            return ChatGoogleGenerativeAI(
                model=self.GOOGLE_AI_MODEL,
                google_api_key=self.GOOGLE_AI_API_KEY,
                temperature=temperature,
            )
        elif self.LLM_PROVIDER == "anthropic":
            from langchain_anthropic import ChatAnthropic
            return ChatAnthropic(
                model=self.ANTHROPIC_MODEL,
                anthropic_api_key=self.ANTHROPIC_API_KEY,
                temperature=temperature,
            )
        else:  # openai fallback
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(
                model=self.OPENAI_MODEL,
                openai_api_key=self.OPENAI_API_KEY,
                temperature=temperature,
            )


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]


settings: Settings = get_settings()
