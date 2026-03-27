from models.enums import CategoryQuote
from models.quote import Quote
from repositories.quote_repository import QuoteRepository
from schemas.quote_schema import (
    CreateQuoteRequest,
)
from loguru import logger


class QuoteService:
    async def create_quote(
        self, quote: CreateQuoteRequest, repo: QuoteRepository
    ) -> Quote:
        logger.info(f"Criando nova citação: {quote}")

        new_quote = await repo.create(quote)

        return new_quote

    async def get_all(
        self,
        author: str | None,
        tags: list[CategoryQuote] | None,
        source: str | None,
        verified: bool,
        limit: int,
        skip: int,
        repo: QuoteRepository,
    ) -> tuple[list[Quote], int]:
        filters = {}
        filters["verified"] = verified

        if author:
            filters["author"] = author
        if source:
            filters["source"] = source
        if tags:
            filters = {"$in": tags}

        logger.info(
            f"Obtendo citações com filtros: {filters}, limit: {limit}, skip: {skip}"
        )

        quotes = await repo.get_all(filters, limit, skip)

        return quotes

    async def get_random_quote(self, size: int, repo: QuoteRepository) -> list[Quote]:
        logger.info(f"Obtendo {size} citações aleatórias.")

        return await repo.get_random_quote(size=size)

    async def get_today_quote(self, repo: QuoteRepository) -> list[Quote]:
        logger.info("Obtendo a citação do dia.")
        return await self.get_random_quote(size=1, repo=repo)
