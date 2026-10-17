from datetime import UTC, datetime

from beanie import Document
from pydantic import Field
from pymongo import IndexModel

from .enums import CategoryQuote


class Quote(Document):
    content: str
    author: str
    tags: list[CategoryQuote]
    source: str | None
    verified: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime | None = None

    class Settings:
        name = "quotes"
        indexes = [  # noqa: RUF012,
            "author",
            "tags",
            "verified",
            "source",
            IndexModel(
                [("content", "text"), ("author", "text"), ("source", "text")],
                weights={"content": 10, "author": 5, "source": 3},
            ),
        ]
