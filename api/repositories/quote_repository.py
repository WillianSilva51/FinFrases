from beanie import PydanticObjectId

from api.models.quote import Quote
from api.schemas.quote_schema import CreateQuoteRequest


class QuoteRepository:
    async def create(self, quote_data: CreateQuoteRequest) -> Quote:
        new_quote = Quote.model_validate(quote_data.model_dump())

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

    async def get_quote_by_content_and_author(
        self, content: str, author: str
    ) -> Quote | None:
        return await Quote.find_one({"content": content, "author": author})

    async def get_quote_by_id(self, id: str) -> Quote | None:
        return await Quote.get(PydanticObjectId(id))

    async def update_quote(self, id: str, quote_data: dict) -> Quote:
        quote = await Quote.get(PydanticObjectId(id))

        update_query = {"$set": quote_data}
        quote = await quote.update(update_query)

        return quote

    async def delete_quote_by_id(self, id: str) -> None:
        await Quote.find_one({"_id": PydanticObjectId(id)}).delete()
