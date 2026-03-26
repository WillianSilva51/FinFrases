from datetime import datetime
from typing import Annotated

from models.enums import CategoryQuote
from pydantic import BaseModel, Field


class CreateQuoteRequest(BaseModel):
    content: Annotated[
        str, Field(min_length=30, max_length=500, description="O texto da citação")
    ]

    author: Annotated[str, Field(min_length=3, max_length=100)]

    tags: list[CategoryQuote] = Field(default_factory=lambda: [CategoryQuote.GERAL])

    source: Annotated[str | None, Field(min_length=10, max_length=150)] = None

    verified: bool = False


class QuoteResponse(BaseModel):
    content: str
    author: str
    tags: list[CategoryQuote]
    source: str | None
    verified: bool
    created_at: datetime
