import os

from beanie import init_beanie
from models.quote import Quote
from pymongo import AsyncMongoClient

MONGO_URI = os.getenv("MONGO_URI")

client: AsyncMongoClient | None = None


async def get_db():
    global client

    if client is None:
        client = AsyncMongoClient(MONGO_URI)

    return client["finfrases"]


async def init_db():
    db = await get_db()
    await init_beanie(database=db, document_models=[Quote])
