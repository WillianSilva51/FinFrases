from models.quote import Quote
from schemas.quote_schema import CreateQuoteRequest


class QuoteRepository:
    async def create(self, quote_data: CreateQuoteRequest) -> Quote:
        new_quote = Quote(**quote_data.model_dump())

        return await new_quote.insert()

    async def get_all(
        self, params: dict, limit: int, skip: int
    ) -> tuple[list[Quote], int]:
        total_count = await Quote.find(params).count()

        quotes = Quote.find(params).limit(limit).skip(skip)

        return await quotes.to_list(), total_count

    async def get_random_quote(self, size: int) -> list[Quote]:
        agregation = [
            {"$match": {"verified": True}},
            {"$sample": {"size": size}},
        ]
        result = await Quote.aggregate(agregation).to_list()

        return [Quote.model_validate(doc) for doc in result]
