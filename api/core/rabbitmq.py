from aio_pika import connect_robust
from aio_pika.abc import AbstractRobustConnection

from api.core.config import settings


class RabbitMQConnection:
    """Gerencia a conexão com o RabbitMQ.

    Esta classe é responsável por estabelecer e gerenciar a conexão com o servidor
    RabbitMQ utilizando a biblioteca aio-pika. Ela fornece métodos para conectar
    e desconectar do servidor, garantindo que a conexão seja robusta e confiável.
    """

    def __init__(self) -> None:
        self._connection: AbstractRobustConnection | None = None

    async def connect(self) -> None:
        """Estabelece uma conexão robusta com o servidor RabbitMQ.

        Utiliza a URI de configuração para conectar ao servidor RabbitMQ de forma
        assíncrona, garantindo que a conexão seja mantida mesmo em caso de falhas
        temporárias.

        Returns:
            None

        Raises:
            ConnectionError: Se não conseguir conectar ao servidor RabbitMQ.
        """
        if self._connection is None or self._connection.is_closed:
            self._connection = await connect_robust(url=settings.RABBITMQ_URI)

    async def disconnect(self) -> None:
        """Fecha a conexão com o servidor RabbitMQ.

        Se a conexão estiver aberta, este método fecha a conexão de forma assíncrona,
        liberando os recursos associados.

        Returns:
            None
        """
        if self._connection and not self._connection.is_closed:
            await self._connection.close()

    @property
    def connection(self) -> AbstractRobustConnection:
        """Retorna a instância da conexão com o RabbitMQ.

        Returns:
            AbstractRobustConnection: A instância da conexão.
        """
        if self._connection is None or self._connection.is_closed:
            raise ConnectionError("Conexão com RabbitMQ não estabelecida.")

        return self._connection


rabbitmq_connection = RabbitMQConnection()


def get_rabbitmq_connection() -> RabbitMQConnection:
    """Retorna a instância do gerenciador de conexão com RabbitMQ.

    Returns:
        RabbitMQConnection: A instância do gerenciador de conexão.
    """
    return rabbitmq_connection


async def init_rabbitmq() -> None:
    """Inicializa a conexão com o RabbitMQ."""
    await rabbitmq_connection.connect()


async def close_rabbitmq() -> None:
    """Fecha a conexão com o RabbitMQ."""
    await rabbitmq_connection.disconnect()
