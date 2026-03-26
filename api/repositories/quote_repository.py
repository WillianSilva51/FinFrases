from models.quote import Quote
from schemas.quote_schema import CreateQuoteRequest
from schemas.quote_schema import to_model, to_response


class QuoteRepository:
    async def create(self, quote_data: CreateQuoteRequest) -> Quote:
        new_quote = await to_model(quote_data)
        await new_quote.save()

        return new_quote
