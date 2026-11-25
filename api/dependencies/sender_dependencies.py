from fastapi import Depends

from api.core.cache import RedisCache, get_redis
from api.dependencies.rabbitmq_dependencies import get_rabbitmq_service
from api.services.rabbitmq_service import RabbitMQService
from api.services.sender_service import SenderService


def get_sender_service(
    rabbitmq_service: RabbitMQService = Depends(get_rabbitmq_service),  # noqa: B008
    redis_cache: RedisCache = Depends(get_redis),  # noqa: B008
) -> SenderService:
    return SenderService(
        rabbitmq_service=rabbitmq_service,
        redis_cache=redis_cache,
    )
