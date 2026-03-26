from models.enums import CategoryQuote
from repositories.quote_repository import QuoteRepository
from schemas.quote_schema import (
    CreateQuoteRequest,
    QuoteResponse,
    to_response,
)

quote_repo = QuoteRepository()


async def create_quote(quote: CreateQuoteRequest) -> QuoteResponse:
    new_quote = await quote_repo.create(quote)

    return to_response(new_quote)


async def get_all(
    author: str | None, tags: list[CategoryQuote] | None, source: str | None
) -> list[QuoteResponse]:
    filters = {
        k: v
        for k, v in {"author": author, "tags": tags, "source": source}.items()
        if v is not None
    }
    quotes = await quote_repo.get_all(filters)
    quotes_response = [to_response(quote) for quote in quotes]

    return quotes_response
