from beanie import init_beanie
from pymongo import AsyncMongoClient

from api.core.config import settings
from api.models.quote import Quote

client: AsyncMongoClient | None = None


async def get_db():
    global client

    if client is None:
        client = AsyncMongoClient(settings.MONGO_URI)

    return client["finfrases"]


async def init_db():
    db = await get_db()
    await init_beanie(database=db, document_models=[Quote])
