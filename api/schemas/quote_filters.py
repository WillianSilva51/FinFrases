from dataclasses import dataclass
from typing import Annotated

from beanie import SortDirection
from fastapi import Query

from api.models.enums import CategoryQuote, QuoteOrderBy, SortOrder


@dataclass
class QuoteFilters:
    """Classe para encapsular os parâmetros de consulta para a busca de citações.

    Attributes:
        verified (bool): Indica se apenas citações verificadas devem ser retornadas.
        author (str | None): Filtro pelo autor da citação.
        source (str | None): Filtro pela fonte da citação.
        tags (list[str] | None): Filtro por tags associadas à citação.
        exclude_tags (list[str] | None): Filtro para excluir citações com determinadas tags.
        search (str | None): Filtro de pesquisa textual para buscar citações que contenham a string fornecida.
    """

    verified: bool | None = None
    author: str | None = None
    source: str | None = None
    tags: Annotated[
        list[CategoryQuote] | None,
        Query(description="Filtro por tags associadas à citação"),
    ] = None
    exclude_tags: Annotated[
        list[CategoryQuote] | None,
        Query(description="Filtro para excluir citações com determinadas tags"),
    ] = None
    search: str | None = None

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
            "verified": self.verified,
            "author": self.author,
            "source": self.source,
            "tags": tags_filter or None,
            "$text": {"$search": self.search} if self.search else None,
        }

        return {
            **{
                key: value
                for key, value in optional_filters.items()
                if value is not None
            },
        }


@dataclass
class QuoteSort:
    """Classe que representa a ordenação de citações."""

    sort_by: Annotated[
        list[QuoteOrderBy] | None,
        Query(description="O campo pelo qual a ordenação será feita"),
    ] = None
    order: Annotated[
        list[SortOrder] | None,
        Query(description="A ordem da ordenação"),
    ] = None

    def to_sort_list(self) -> list[tuple[str, SortDirection]] | None:
        """Converte a ordenação de citações para uma lista de tuplas.

        Returns:
            Uma lista de tuplas contendo o campo e a direção da ordenação.
        """
        if self.sort_by is not None and self.order is None:
            return [(field.value, SortDirection.ASCENDING) for field in self.sort_by]

        if self.order is None or self.sort_by is None:
            return None

        return [
            (
                field.value,
                SortDirection.ASCENDING
                if direction == SortOrder.ASCENDING
                else SortDirection.DESCENDING,
            )
            for field, direction in zip(self.sort_by, self.order)
        ]
