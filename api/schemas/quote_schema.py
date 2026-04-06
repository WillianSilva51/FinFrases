from datetime import datetime, timezone
from typing import Annotated

from beanie import PydanticObjectId
from pydantic import BaseModel, ConfigDict, Field, field_validator

from api.models.enums import CategoryQuote


def strip_and_validate(v: str | None) -> str | None:
    if v is None:
        return v
    v = v.strip()
    if not v:
        raise ValueError("Campo não pode ser vazio")
    return v


class CreateQuoteRequest(BaseModel):
    content: Annotated[
        str, Field(min_length=10, max_length=500, description="O texto da citação")
    ]

    author: Annotated[
        str, Field(min_length=3, max_length=100, description="O autor da citação")
    ]

    tags: list[CategoryQuote] = Field(default_factory=lambda: [CategoryQuote.GERAL])

    source: Annotated[
        str | None,
        Field(
            default=None,
            min_length=10,
            max_length=150,
            description="A fonte da citação",
        ),
    ]

    verified: bool = False

    @field_validator("content", "author", "source")
    @classmethod
    def validate_fields(cls, v):
        return strip_and_validate(v)


class UpdateQuoteRequest(BaseModel):
    content: Annotated[
        str | None,
        Field(
            min_length=10,
            max_length=500,
            description="O texto da citação",
        ),
    ] = None

    author: Annotated[
        str | None,
        Field(min_length=3, max_length=100, description="O autor da citação"),
    ] = None

    tags: list[CategoryQuote] | None = Field(
        default=None, description="As categorias da citação"
    )

    source: Annotated[
        str | None,
        Field(min_length=10, max_length=150, description="A fonte da citação"),
    ] = None

    verified: bool | None = Field(
        default=None, description="Indica se a citação foi verificada ou não"
    )

    @field_validator("content", "author", "source")
    @classmethod
    def validate_fields(cls, v):
        return strip_and_validate(v)


class QuoteResponse(BaseModel):
    id: PydanticObjectId = Field(alias="_id", description="O ID da citação")
    content: str
    author: str
    tags: list[CategoryQuote]
    source: str | None
    verified: bool
    created_at: datetime
    updated_at: datetime | None
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
