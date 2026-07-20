"""
Input validation utilities
"""
import re
import uuid
from typing import Any


def is_valid_email(email: str) -> bool:
    """Check whether a string is a structurally valid email address."""
    pattern = r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def is_strong_password(password: str) -> bool:
    """Validate password strength: 8+ chars, uppercase, lowercase, digit."""
    return (
        len(password) >= 8
        and any(c.isupper() for c in password)
        and any(c.islower() for c in password)
        and any(c.isdigit() for c in password)
    )


def is_valid_uuid(value: Any) -> bool:
    """Check whether a value is a valid UUID."""
    try:
        uuid.UUID(str(value))
        return True
    except (ValueError, AttributeError):
        return False


def sanitize_filename(filename: str) -> str:
    """Strip dangerous characters from uploaded filenames."""
    # Keep alphanumeric, dot, underscore, dash
    sanitized = re.sub(r"[^\w.\-]", "_", filename)
    # Collapse multiple underscores
    sanitized = re.sub(r"_{2,}", "_", sanitized)
    return sanitized[:255]


def is_safe_sql(sql: str) -> bool:
    """Quick heuristic check for dangerous SQL keywords."""
    sql_upper = sql.upper().strip()
    dangerous = ["DROP", "DELETE", "TRUNCATE", "ALTER", "CREATE", "INSERT", "UPDATE", "GRANT", "REVOKE", "EXEC", "EXECUTE"]
    for kw in dangerous:
        if re.search(rf"\b{kw}\b", sql_upper):
            return False
    return True
