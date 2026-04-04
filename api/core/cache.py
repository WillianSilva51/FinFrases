from functools import wraps
from json import dumps, loads
from typing import Callable

from loguru import logger
from redis import ConnectionError
from redis.asyncio import Redis


class RedisCache:
    def __init__(self) -> None:
        try:
            self.client = Redis()
        except ConnectionError as e:
            logger.error(e)

    def ping(self):
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
            if isinstance(keys, (list, tuple, set)):
                return await self.client.delete(*keys)
            else:
                return await self.client.delete(keys)
        except ConnectionError as e:
            logger.error(e)

    def _normalize_cache_value(self, value):
        if isinstance(value, (str, int, float, bool, type(None))):
            return value

        if isinstance(value, (list, tuple)):
            return [self._normalize_cache_value(v) for v in value]

        if isinstance(value, dict):
            return {k: self._normalize_cache_value(v) for k, v in value.items()}

        return str(value)

    def _is_cacheable(self, value):
        return isinstance(value, (str, int, float, bool, type(None), list, dict))

    def cacheable(self, expire: Callable[[], int] | int = 3600):
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                clean_kwargs = {
                    k: self._normalize_cache_value(v)
                    for k, v in kwargs.items()
                    if self._is_cacheable(v)
                }

                cache_key = f"{func.__name__}:{dumps(clean_kwargs, sort_keys=True)}"

                cache_data = await self.get(cache_key)

                if cache_data:
                    logger.info(f"Cache encontrado para a chave: {cache_key}")

                    return loads(cache_data.decode("utf-8"))

                result = await func(*args, **kwargs)

                if result is not None:
                    if isinstance(result, list):
                        serializable_result = [
                            self._normalize_cache_value(model.model_dump(mode="json"))
                            for model in result
                        ]
                    elif hasattr(result, "model_dump"):
                        serializable_result = self._normalize_cache_value(
                            result.model_dump(mode="json")
                        )
                    else:
                        serializable_result = self._normalize_cache_value(result)

                    logger.info(f"Armazenando no cache para a chave: {cache_key}")

                    await self.set(
                        key=cache_key,
                        value=dumps(serializable_result),
                        expire=expire() if callable(expire) else expire,
                    )

                return result

            return wrapper

        return decorator
