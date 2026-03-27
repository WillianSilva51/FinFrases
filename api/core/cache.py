from redis.asyncio import Redis
from redis import ConnectionError
from functools import wraps
import logging
from json import loads, dumps


logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)

logger = logging.getLogger("Redis")


class RedisCache:
    def __init__(self, redis_url: str) -> None:
        try:
            self.client = Redis.from_url(redis_url, decode_responses=True)
            self.client.ping()
        except ConnectionError as e:
            logger.error(e)

    def set(self, key: str, value, expire: int):
        try:
            return self.client.set(name=key, value=value, ex=expire, get=True)
        except ConnectionError as e:
            logger.error(e)

    async def get(self, key: str):
        try:
            return self.client.get(name=key)
        except ConnectionError as e:
            logger.error(e)

    async def delete(self, keys):
        try:
            self.client.delete(keys)
        except ConnectionError as e:
            logger.error(e)

    def cacheable(self, expire: int = 3600):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                cache_key = f"{func.__name__}:{args}:{kwargs}"

                cache_data = self.get(cache_key)

                if cache_data:
                    return loads(cache_data)

                result = func(*args, **kwargs)

                if result:
                    self.set(key=cache_key, value=dumps(result), expire=expire)

                return result

            return wrapper

        return decorator
