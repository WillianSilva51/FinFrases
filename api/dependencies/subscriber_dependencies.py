from fastapi import Depends

from api.dependencies.email_dependencies import get_send_welcome_email
from api.dependencies.repositories.repositories_dependencies import (
    get_subscriber_repository,
)
from api.repositories.subscriber_repository import SubscriberRepository
from api.services.email.send_welcome_email import SendWelcomeEmail
from api.services.subscriber_service import SubscriberService


def get_subscriber_service(
    subscriber_repo: SubscriberRepository = Depends(get_subscriber_repository),  # noqa: B008
    send_welcome_email: SendWelcomeEmail = Depends(get_send_welcome_email),  # noqa: B008
) -> SubscriberService:
    """
    Retorna uma instância do serviço de assinantes.

    Args:
        subscriber_repo (SubscriberRepository): Instância do repositório de assinantes.
        send_welcome_email (SendWelcomeEmail): Instância do serviço de envio de e-mails de boas-vindas.

    Returns:
        SubscriberService: Uma instância do serviço de assinantes.
    """

    return SubscriberService(
        repo=subscriber_repo,
        send_welcome_email=send_welcome_email,
    )
