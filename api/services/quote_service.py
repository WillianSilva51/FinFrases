from datetime import datetime, timezone

from loguru import logger

from api.core.exceptions.custom_exceptions import (
    DomainValidationException,
    ResourceNotFoundException,
)
from api.models.enums import CategoryQuote
from api.models.quote import Quote
from api.repositories.quote_repository import QuoteRepository
from api.schemas.quote_schema import CreateQuoteRequest, UpdateQuoteRequest


class QuoteService:
    async def create_quote(
        self, quote: CreateQuoteRequest, repo: QuoteRepository
    ) -> Quote:
        logger.info(f"Criando nova citação: {quote}")

        if (
            await repo.get_quote_by_content_and_author(quote.content, quote.author)
            is not None
        ):
            raise DomainValidationException(
                f"A frase '{quote.content}' do autor '{quote.author}' já existe"
            )

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
            filters["tags"] = {"$in": tags}

        logger.info(
            f"Obtendo citações com filtros: {filters}, limit: {limit}, skip: {skip}"
        )

        quotes = await repo.get_all(filters, limit, skip)

        return quotes

    async def get_quote_by_id(self, id: str, repo: QuoteRepository) -> Quote:
        logger.info(f"Obtendo citação com id: {id}")

        quote = await repo.get_quote_by_id(id)

        if quote is None:
            raise ResourceNotFoundException(f"Citação com id '{id}' não encontrada")
        return quote

    async def get_random_quote(self, size: int, repo: QuoteRepository) -> list[Quote]:
        logger.info(f"Obtendo {size} citações aleatórias.")

        return await repo.get_random_quote(size=size)

    async def get_today_quote(self, repo: QuoteRepository) -> list[Quote]:
        logger.info("Obtendo a citação do dia.")
        quote = await self.get_random_quote(size=1, repo=repo)

        if not quote:
            raise ResourceNotFoundException("Nenhuma citação verificada encontrada")

        return quote

    async def update_quote_by_id(
        self, id: str, quote_data: UpdateQuoteRequest, repo: QuoteRepository
    ) -> Quote:
        logger.info(f"Atualizando citação com id: {id}, dados: {quote_data}")

        await self.get_quote_by_id(id, repo)

        if quote_data.author and quote_data.content:
            existing_quote = await repo.get_quote_by_content_and_author(
                quote_data.content, quote_data.author
            )
            if existing_quote and existing_quote.id != id:
                raise DomainValidationException(
                    f"A frase '{quote_data.content}' do autor '{quote_data.author}' já existe"
                )

        quote_data_dict = quote_data.model_dump(exclude_unset=True)
        quote_data_dict["updated_at"] = datetime.now(timezone.utc)

        return await repo.update_quote(id, quote_data_dict)

    async def delete_quote_by_id(self, id: str, repo: QuoteRepository) -> None:
        logger.info(f"Deletando citação com id: {id}")

        await self.get_quote_by_id(id, repo)

        await repo.delete_quote_by_id(id)
