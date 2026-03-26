from models.quote import Quote
from schemas.quote_schema import CreateQuoteRequest


class QuoteRepository:
    async def create(self, quote_data: CreateQuoteRequest) -> Quote:
        new_quote = Quote(**quote_data.model_dump())

        return await new_quote.insert()

    async def get_all(self, params: dict, limit: int | None, skip: int) -> list[Quote]:
        quotes = Quote.find(params).limit(limit).skip(skip)

        return await quotes.to_list()
