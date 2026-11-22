from loguru import logger

from api.models.enums import SubscriberStatus
from api.repositories.subscriber_repository import SubscriberRepository
from api.schemas.email_event_schema import DailyEmail
from api.schemas.quote_schema import QuoteResponse
from api.services.quote_service import QuoteService
from api.services.rabbitmq_service import RabbitMQService
from api.services.sender_service import SenderService


class SendDailyQuoteEmails:
    def __init__(
        self,
        sender_service: SenderService,
        quote_service: QuoteService,
        subscriber_repository: SubscriberRepository,
    ) -> None:
        self.sender_service = sender_service
        self.quote_service = quote_service
        self.subscriber_repository = subscriber_repository

    async def execute(self) -> None:
        quotes = await self.quote_service.get_today_quote()

        if not quotes:
            logger.warning("Nenhuma citação encontrada para o envio diário.")
            return

        quote = QuoteResponse.model_validate(quotes[0].model_dump())

        skip = 0
        limit = 100

        while True:
            (
                subscribers,
                total_count,
            ) = await self.subscriber_repository.get_subscribers_by_status(
                status=SubscriberStatus.ACTIVE,
                skip=skip,
                limit=limit,
            )

            if not subscribers:
                break

            for subscriber in subscribers:
                payload = DailyEmail(
                    recipient_name=subscriber.name,
                    recipient_email=subscriber.email,
                    unsubscribe_token=subscriber.unsubscribe_token,
                    quote=quote,
                )

                await self.sender_service.send(
                    routing_key=RabbitMQService.DAILY_ROUTING_KEY,
                    payload=payload,
                )

            skip += len(subscribers)

            if skip >= total_count:
                break
