from datetime import datetime, timezone
from typing import Annotated

from beanie import Document, Indexed
from pydantic import Field

from .enums import CategoryQuote


class Quote(Document):
    content: str
    author: Annotated[str, Indexed()]
    tags: list[CategoryQuote]
    source: str | None
    verified: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "quotes"
