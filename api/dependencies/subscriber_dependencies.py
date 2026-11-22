from fastapi import Depends

from api.dependencies.email_dependencies import get_rabbitmq_service
from api.repositories.subscriber_repository import SubscriberRepository
from api.services.rabbitmq_service import RabbitMQService
from api.services.sender_service import SenderService
from api.services.subscriber_service import SubscriberService


def get_subscriber_repository() -> SubscriberRepository:
    """
    Retorna uma instância do repositório de assinantes.

    Returns:
        SubscriberRepository: Uma instância do repositório de assinantes.
    """
    return SubscriberRepository()


def get_sender_service(
    rabbitmq_service: RabbitMQService = Depends(get_rabbitmq_service),  # noqa: B008
) -> SenderService:
    """
    Retorna uma instância do serviço de envio.

    Args:
        rabbitmq_service (RabbitMQService): Instância do serviço RabbitMQ.

    Returns:
        SenderService: Uma instância do serviço de envio.
    """

    return SenderService(rabbitmq_service=rabbitmq_service)


def get_subscriber_service(
    subscriber_repo: SubscriberRepository = Depends(get_subscriber_repository),  # noqa: B008
    sender_service: SenderService = Depends(get_sender_service),  # noqa: B008
) -> SubscriberService:
    """
    Retorna uma instância do serviço de assinantes.

    Args:
        subscriber_repo (SubscriberRepository): Instância do repositório de assinantes.
        sender_service (SenderService): Instância do serviço de envio.

    Returns:
        SubscriberService: Uma instância do serviço de assinantes.
    """

    return SubscriberService(repo=subscriber_repo, sender_service=sender_service)
