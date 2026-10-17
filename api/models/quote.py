from datetime import UTC, datetime
from typing import Annotated

from beanie import Document, Indexed
from pydantic import Field
from pymongo import IndexModel

from .enums import CategoryQuote


class Quote(Document):
    content: str
    author: Annotated[str, Indexed()]
    tags: list[CategoryQuote]
    source: str | None
    verified: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime | None = None

    class Settings:
        name = "quotes"
        indexes = [  # noqa: RUF012
            "author",
            "tags",
            "verified",
            IndexModel(
                [("content", "text"), ("author", "text")],
            ),
        ]
