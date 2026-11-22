from datetime import UTC, datetime

from loguru import logger

from api.models.subscriber import Subscriber
from api.schemas.email_event_schema import EmailEventSchema, WelcomeEmail
from api.services.quote_service import QuoteService
from api.services.rabbitmq_service import RabbitMQService


class SenderService:
    def __init__(self, rabbitmq_service: RabbitMQService) -> None:
        self.rabbitmq_service = rabbitmq_service

    async def send_welcome_email(
        self,
        subscriber: Subscriber,
    ) -> None:
        """
        Envia um e-mail de boas-vindas para o assinante recém-criado.

        Args:
            subscriber: O assinante recém-criado.
            sender_service: Instância do serviço SenderService para envio de e-mails.
        """
        payload = WelcomeEmail(
            recipient_name=subscriber.name,
            recipient_email=subscriber.email,
            unsubscribe_token=subscriber.unsubscribe_token,
        )

        await self._publish_email(
            routing_key=RabbitMQService.WELCOME_ROUTING_KEY,
            payload=payload,
        )

    async def send_diary_quote_email(
        self,
        quote_service: QuoteService,
    ) -> None:
        """
        Envia um e-mail diário com uma citação para o assinante.
        """

    async def _publish_email(
        self,
        routing_key: str,
        payload: EmailEventSchema,
    ):
        idempotency_key = self._generate_idempotency_key(payload)

        try:
            await self.rabbitmq_service.publish(
                routing_key=routing_key,
                payload=payload,
                idempotency_key=idempotency_key,
            )
        except Exception as e:  # noqa: BLE001
            logger.error(
                f"Erro ao enviar e-mail de boas-vindas para {payload.recipient_email}: {e}"
            )

    def _generate_idempotency_key(
        self,
        payload: EmailEventSchema,
    ) -> str:
        """
        Gera uma chave de idempotência única para o envio do e-mail de boas-vindas, baseada na data atual e no e-mail do assinante.
        """
        idempotency_key = (
            f"email_sent:{datetime.now(UTC).date()}:{payload.recipient_email}"
        )
        return idempotency_key
