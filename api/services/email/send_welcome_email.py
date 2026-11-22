from api.models.subscriber import Subscriber
from api.schemas.email_event_schema import WelcomeEmail
from api.services.rabbitmq_service import RabbitMQService
from api.services.sender_service import SenderService


class SendWelcomeEmail:
    def __init__(
        self,
        sender_service: SenderService,
    ) -> None:
        self.sender_service = sender_service

    async def execute(self, subscriber: Subscriber) -> None:
        payload = WelcomeEmail(
            recipient_name=subscriber.name,
            recipient_email=subscriber.email,
            unsubscribe_token=subscriber.unsubscribe_token,
        )

        await self.sender_service.send(
            routing_key=RabbitMQService.WELCOME_ROUTING_KEY,
            payload=payload,
        )
