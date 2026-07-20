"""
Pagination utilities for consistent API list responses
"""
import math
from typing import TypeVar, Generic, Sequence
from pydantic import BaseModel

T = TypeVar("T")


class PageParams(BaseModel):
    """Query parameters for pagination."""
    page: int = 1
    limit: int = 20

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.limit


class PageResponse(BaseModel, Generic[T]):
    """Standard paginated list response envelope."""
    items: Sequence[T]
    total: int
    page: int
    limit: int
    pages: int

    @classmethod
    def create(cls, items: Sequence[T], total: int, params: PageParams) -> "PageResponse[T]":
        pages = math.ceil(total / params.limit) if params.limit > 0 else 0
        return cls(
            items=items,
            total=total,
            page=params.page,
            limit=params.limit,
            pages=pages,
        )
