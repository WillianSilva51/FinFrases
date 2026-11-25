from datetime import UTC, datetime

from loguru import logger

from api.core.cache import RedisCache
from api.schemas.email_event_schema import EmailEventSchema
from api.services.rabbitmq_service import RabbitMQService


class SenderService:
    def __init__(
        self, rabbitmq_service: RabbitMQService, redis_cache: RedisCache
    ) -> None:
        self.rabbitmq_service = rabbitmq_service
        self.redis_cache = redis_cache

    async def send(
        self,
        routing_key: str,
        payload: EmailEventSchema,
    ) -> None:
        idempotency_key = self._generate_idempotency_key(
            routing_key,
            payload,
        )

        acquired = await self.redis_cache.get(idempotency_key)

        if acquired:
            logger.warning(
                f"Evento já processado ou publicado para {payload.recipient_email}. Pulando envio."
            )
            return

        await self.redis_cache.set(
            key=idempotency_key, value="Processing", expire=300, nx=True
        )

        try:
            await self.rabbitmq_service.publish(
                routing_key=routing_key,
                payload=payload,
                idempotency_key=idempotency_key,
            )

            await self.redis_cache.set(
                key=idempotency_key,
                value="Published",
                expire=86400,
            )

            logger.info(f"Evento publicado com sucesso para {payload.recipient_email}")
        except Exception:
            logger.exception(f"Erro ao publicar evento para {payload.recipient_email}")
            raise

    def _generate_idempotency_key(
        self,
        routing_key: str,
        payload: EmailEventSchema,
    ) -> str:
        return f"{routing_key}:{datetime.now(UTC).date()}:{payload.recipient_email}"
