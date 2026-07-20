"""
Custom exception classes for clean error handling across the application.
"""
from uuid import UUID


class AppError(Exception):
    """Base exception for all application errors."""

    status_code: int = 500
    error_code: str = "INTERNAL_ERROR"
    message: str = "An unexpected error occurred"

    def __init__(self, message: str | None = None, **kwargs):
        self.message = message or self.__class__.message
        self.details = kwargs
        super().__init__(self.message)


# ─── Auth Errors ──────────────────────────────────────────────────────────────

class InvalidCredentialsError(AppError):
    status_code = 401
    error_code = "INVALID_CREDENTIALS"
    message = "Invalid email or password"


class TokenExpiredError(AppError):
    status_code = 401
    error_code = "TOKEN_EXPIRED"
    message = "Token has expired"


class InvalidTokenError(AppError):
    status_code = 401
    error_code = "INVALID_TOKEN"
    message = "Invalid or malformed token"


class InsufficientPermissionsError(AppError):
    status_code = 403
    error_code = "FORBIDDEN"
    message = "Insufficient permissions to perform this action"


class EmailAlreadyExistsError(AppError):
    status_code = 409
    error_code = "EMAIL_EXISTS"
    message = "An account with this email already exists"


# ─── Resource Errors ─────────────────────────────────────────────────────────

class NotFoundError(AppError):
    status_code = 404
    error_code = "NOT_FOUND"
    message = "Resource not found"


class UserNotFoundError(NotFoundError):
    message = "User not found"


class DatasetNotFoundError(NotFoundError):
    message = "Dataset not found"

    def __init__(self, dataset_id: UUID | None = None):
        super().__init__(f"Dataset {dataset_id} not found" if dataset_id else None)


class ConversationNotFoundError(NotFoundError):
    message = "Conversation not found"


# ─── Upload Errors ───────────────────────────────────────────────────────────

class FileTooLargeError(AppError):
    status_code = 413
    error_code = "FILE_TOO_LARGE"
    message = "File exceeds the maximum allowed size"


class UnsupportedFileTypeError(AppError):
    status_code = 415
    error_code = "UNSUPPORTED_FILE_TYPE"
    message = "File type not supported. Use CSV, Excel, or JSON."


class FileParseError(AppError):
    status_code = 422
    error_code = "FILE_PARSE_ERROR"
    message = "Failed to parse the uploaded file"


# ─── Database Connection Errors ──────────────────────────────────────────────

class ConnectionTestFailedError(AppError):
    status_code = 422
    error_code = "CONNECTION_FAILED"
    message = "Failed to connect to the database"


# ─── Agent Errors ────────────────────────────────────────────────────────────

class AgentMaxRetriesError(AppError):
    status_code = 422
    error_code = "AGENT_MAX_RETRIES"
    message = "Agent failed to complete the task after maximum retries"


class SQLInjectionDetectedError(AppError):
    status_code = 400
    error_code = "SQL_INJECTION_DETECTED"
    message = "Potentially unsafe SQL detected. Query rejected."


class CodeExecutionError(AppError):
    status_code = 422
    error_code = "CODE_EXECUTION_ERROR"
    message = "Failed to execute the generated code"


# ─── Rate Limit ──────────────────────────────────────────────────────────────

class RateLimitExceededError(AppError):
    status_code = 429
    error_code = "RATE_LIMITED"
    message = "Too many requests. Please wait before trying again."
