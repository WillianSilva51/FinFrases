from dataclasses import dataclass
from datetime import UTC, datetime
from re import escape
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


@dataclass
class QueryParams:
    """Classe para encapsular os parâmetros de consulta para a busca de citações.

    Attributes:
        verified (bool): Indica se apenas citações verificadas devem ser retornadas.
        author (str | None): Filtro pelo autor da citação.
        source (str | None): Filtro pela fonte da citação.
        tags (list[str] | None): Filtro por tags associadas à citação.
        exclude_tags (list[str] | None): Filtro para excluir citações com determinadas tags.
        q (str | None): Termo de pesquisa para busca textual nas citações.
    """

    verified: bool = True
    author: str | None = None
    source: str | None = None
    tags: list[CategoryQuote] | None = None
    exclude_tags: list[CategoryQuote] | None = None
    q: str | None = None

    def to_dict(self) -> dict:
        tags_filter = {
            op: values
            for op, values in (
                ("$in", self.tags),
                ("$nin", self.exclude_tags),
            )
            if values
        }

        optional_filters = {
            "author": self.author,
            "source": self.source,
            "tags": tags_filter or None,
            "$or": [
                {
                    "content": {
                        "$regex": escape(self.q.strip()),
                        "$options": "i",
                    }
                },
                {
                    "author": {
                        "$regex": escape(self.q.strip()),
                        "$options": "i",
                    }
                },
            ]
            if self.q and self.q.strip()
            else None,
        }

        return {
            "verified": self.verified,
            **{
                key: value
                for key, value in optional_filters.items()
                if value is not None
            },
        }
