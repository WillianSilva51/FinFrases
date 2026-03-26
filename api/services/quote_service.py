from schemas.quote_schema import (
    CreateQuoteRequest,
    QuoteResponse,
    to_response,
)
from repositories.quote_repository import QuoteRepository

quote_repo = QuoteRepository()


async def create_quote(quote: CreateQuoteRequest) -> QuoteResponse:
    new_quote = await quote_repo.create(quote)

    return await to_response(new_quote)
