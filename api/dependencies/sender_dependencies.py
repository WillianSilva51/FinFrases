from fastapi import Depends

from api.dependencies.rabbitmq_dependencies import get_rabbitmq_service
from api.services.rabbitmq_service import RabbitMQService
from api.services.sender_service import SenderService


def get_sender_service(
    rabbitmq_service: RabbitMQService = Depends(get_rabbitmq_service),  # noqa: B008
) -> SenderService:
    return SenderService(
        rabbitmq_service=rabbitmq_service,
    )
