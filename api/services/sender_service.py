from datetime import UTC, datetime

from loguru import logger

from api.schemas.email_event_schema import EmailEventSchema
from api.services.rabbitmq_service import RabbitMQService


class SenderService:
    def __init__(
        self,
        rabbitmq_service: RabbitMQService,
    ) -> None:
        self.rabbitmq_service = rabbitmq_service

    async def send(
        self,
        routing_key: str,
        payload: EmailEventSchema,
    ) -> None:
        idempotency_key = self._generate_idempotency_key(
            routing_key,
            payload,
        )

        try:
            await self.rabbitmq_service.publish(
                routing_key=routing_key,
                payload=payload,
                idempotency_key=idempotency_key,
            )
        except Exception:
            logger.exception(f"Erro ao publicar evento para {payload.recipient_email}")
            raise

    def _generate_idempotency_key(
        self,
        routing_key: str,
        payload: EmailEventSchema,
    ) -> str:
        return f"{routing_key}:{datetime.now(UTC).date()}:{payload.recipient_email}"
