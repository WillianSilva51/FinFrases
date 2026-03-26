from models.quote import Quote
from schemas.quote_schema import CreateQuoteRequest, to_model


class QuoteRepository:
    async def create(self, quote_data: CreateQuoteRequest) -> Quote:
        new_quote = to_model(quote_data)
        await new_quote.save()

        return new_quote

    async def get_all(self, params: dict, limit: int | None) -> list[Quote]:
        quotes = Quote.find_many(params, limit=limit)

        return await quotes.to_list()
