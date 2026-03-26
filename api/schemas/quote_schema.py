from datetime import datetime
from typing import Annotated

from beanie import PydanticObjectId
from models.enums import CategoryQuote
from models.quote import Quote
from pydantic import BaseModel, Field


class CreateQuoteRequest(BaseModel):
    content: Annotated[
        str, Field(min_length=10, max_length=500, description="O texto da citação")
    ]

    author: Annotated[str, Field(min_length=3, max_length=100)]

    tags: list[CategoryQuote] = Field(default_factory=lambda: [CategoryQuote.GERAL])

    source: Annotated[str | None, Field(min_length=10, max_length=150)] = None

    verified: bool = False


class QuoteResponse(BaseModel):
    id: PydanticObjectId
    content: str
    author: str
    tags: list[CategoryQuote]
    source: str | None
    verified: bool
    created_at: datetime


def to_response(model: Quote) -> QuoteResponse:
    return QuoteResponse.model_validate(model.model_dump())


def to_model(request: CreateQuoteRequest) -> Quote:
    return Quote(**request.model_dump())
