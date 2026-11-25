from fastapi import Depends

from api.core.cache import get_redis
from api.dependencies.quote_dependencies import get_quote_service
from api.dependencies.rabbitmq_dependencies import get_rabbitmq_service
from api.dependencies.repositories.repositories_dependencies import (
    get_quote_repository,
    get_subscriber_repository,
)
from api.dependencies.sender_dependencies import get_sender_service
from api.repositories.subscriber_repository import SubscriberRepository
from api.services.email.send_daily_emails import SendDailyQuoteEmails
from api.services.email.send_welcome_email import SendWelcomeEmail
from api.services.quote_service import QuoteService
from api.services.sender_service import SenderService


def get_send_welcome_email(
    sender_service: SenderService = Depends(get_sender_service),  # noqa: B008
) -> SendWelcomeEmail:
    return SendWelcomeEmail(
        sender_service=sender_service,
    )


def get_daily_quote_email(
    sender_service: SenderService = Depends(get_sender_service),  # noqa: B008
    quote_service: QuoteService = Depends(get_quote_service),  # noqa: B008
    subscriber_repository: SubscriberRepository = Depends(get_subscriber_repository),  # noqa: B008
) -> SendDailyQuoteEmails:
    return SendDailyQuoteEmails(
        sender_service=sender_service,
        quote_service=quote_service,
        subscriber_repository=subscriber_repository,
    )


def create_daily_quote_email() -> SendDailyQuoteEmails:
    sender_service = SenderService(
        rabbitmq_service=get_rabbitmq_service(),
        redis_cache=get_redis(),
    )

    quote_service = get_quote_service(quote_repo=get_quote_repository())

    subscriber_repository = get_subscriber_repository()

    return SendDailyQuoteEmails(
        sender_service=sender_service,
        quote_service=quote_service,
        subscriber_repository=subscriber_repository,
    )
