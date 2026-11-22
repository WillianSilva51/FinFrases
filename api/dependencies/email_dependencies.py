from api.core.rabbitmq import get_rabbitmq_connection
from api.services.rabbitmq_service import RabbitMQService

rabbitmq_service: RabbitMQService = RabbitMQService(get_rabbitmq_connection())


def get_rabbitmq_service() -> RabbitMQService:
    return rabbitmq_service


async def declare_rabbitmq_topology() -> None:
    await rabbitmq_service.declare_topology()
