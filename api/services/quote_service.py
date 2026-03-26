from fastapi import Depends
from models.enums import CategoryQuote
from models.quote import Quote
from repositories.quote_repository import QuoteRepository
from schemas.quote_schema import (
    CreateQuoteRequest,
)


class QuoteService:
    def __init__(self, repo: QuoteRepository = Depends()) -> None:
        self.repo = repo

    async def create_quote(self, quote: CreateQuoteRequest) -> Quote:
        new_quote = await self.repo.create(quote)

        return new_quote

    async def get_all(
        self,
        author: str | None,
        tags: list[CategoryQuote] | None,
        source: str | None,
        verified: bool,
        limit: int | None,
        skip: int,
    ) -> list[Quote]:
        filters = {}
        filters["verified"] = verified

        if author:
            filters["author"] = author
        if source:
            filters["source"] = source
        if tags:
            filters = {"$in": tags}

        quotes = await self.repo.get_all(filters, limit, skip)

        return quotes
