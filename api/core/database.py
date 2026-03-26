from beanie import init_beanie
from models.quote import Quote
from pymongo import AsyncMongoClient

from core.config import settings

client: AsyncMongoClient | None = None


async def get_db():
    global client

    if client is None:
        client = AsyncMongoClient(settings.MONGO_URI)

    return client["finfrases"]


async def init_db():
    db = await get_db()
    await init_beanie(database=db, document_models=[Quote])
