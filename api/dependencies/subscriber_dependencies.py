from fastapi import Depends

from api.dependencies.email_dependencies import get_rabbitmq_service
from api.repositories.subscriber_repository import SubscriberRepository
from api.services.rabbitmq_service import RabbitMQService
from api.services.sender_service import SenderService
from api.services.subscriber_service import SubscriberService


def get_subscriber_repository() -> SubscriberRepository:
    return SubscriberRepository()


def get_sender_service(
    rabbitmq_service: RabbitMQService = Depends(get_rabbitmq_service),  # noqa: B008
) -> SenderService:
    return SenderService(rabbitmq_service=rabbitmq_service)


def get_subscriber_service(
    repo: SubscriberRepository = Depends(get_subscriber_repository),  # noqa: B008
    sender_service: SenderService = Depends(get_sender_service),  # noqa: B008
) -> SubscriberService:
    return SubscriberService(repo=repo, sender_service=sender_service)
