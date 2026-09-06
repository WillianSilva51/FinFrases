from collections.abc import Sequence
from typing import TypeVar

from fastapi import Query
from pydantic import BaseModel

T = TypeVar("T")


class Params(BaseModel):
    page: int = Query(default=1, ge=1, description="Page number")
    size: int = Query(default=50, ge=1, le=100, description="Page size")

    def get_limit(self) -> int:
        return self.size

    def get_offset(self) -> int:
        return self.size * (self.page - 1)


class PaginatedResponse[T](BaseModel):
    items: Sequence[T]
    total: int
    page: int
    size: int
    pages: int
