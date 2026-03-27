import logging
from functools import wraps
from json import dumps, loads

from redis import ConnectionError
from redis.asyncio import Redis

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)

logger = logging.getLogger("Redis")


class RedisCache:
    def __init__(self) -> None:
        try:
            self.client = Redis()
        except ConnectionError as e:
            logger.error(e)

    async def ping(self):
        try:
            return self.client.ping()
        except ConnectionError as e:
            logger.error(f"Erro de conexão com o Redis: {e}")

    async def set(self, key: str, value, expire: int):
        try:
            return await self.client.set(name=key, value=value, ex=expire, get=True)
        except ConnectionError as e:
            logger.error(e)

    async def get(self, key: str):
        try:
            return await self.client.get(name=key)
        except ConnectionError as e:
            logger.error(e)

    async def delete(self, keys):
        try:
            await self.client.delete(keys)
        except ConnectionError as e:
            logger.error(e)

    def cacheable(self, expire: int = 3600):
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                clean_kwargs = {
                    k: v
                    for k, v in kwargs.items()
                    if isinstance(v, (str, int, float, bool, type(None)))
                }

                cache_key = f"{func.__name__}:{dumps(clean_kwargs, sort_keys=True)}"

                cache_data = await self.get(cache_key)

                if cache_data:
                    return loads(cache_data.decode("utf-8"))

                result = await func(*args, **kwargs)

                if result:
                    serilizable_result = [
                        model.model_dump(mode="json") for model in result
                    ]

                    await self.set(
                        key=cache_key,
                        value=dumps(serilizable_result),
                        expire=expire,
                    )

                return result

            return wrapper

        return decorator
