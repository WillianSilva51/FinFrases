from datetime import UTC, datetime
from uuid import uuid4

from aio_pika import DeliveryMode, ExchangeType, Message
from aio_pika.abc import AbstractRobustChannel, AbstractRobustExchange

from api.core.rabbitmq import rabbitmq_connection
from api.schemas.email_event_schema import EmailEventSchema


class RabbitMQService:
    MAIN_EXCHANGE = "finfrases.email.exchange"
    DLX_EXCHANGE = "finfrases.dlx.exchange"

    WELCOME_QUEUE = "emails.welcome.queue"
    DAILY_QUEUE = "emails.daily.queue"
    RETRY_QUEUE = "emails.retry.queue"
    DEAD_LETTER_QUEUE = "emails.dead_letter.queue"

    WELCOME_ROUTING_KEY = "email.welcome"
    DAILY_ROUTING_KEY = "email.daily"
    DEAD_LETTER_ROUTING_KEY = "email.dead_letter"

    async def declare_topology(self) -> None:
        async with rabbitmq_connection.connection.channel() as channel:
            main_exchange, dlx_exchage = await self._declare_exchanges(channel)

            await self._declare_dead_letter_queue(channel, dlx_exchage)

            await self._declare_retry_queue(channel, dlx_exchage)

            await self._declare_main_queues(channel, main_exchange)

    async def publish(
        self,
        routing_key: str,
        payload: EmailEventSchema,
        idempotency_key: str | None = None,
    ) -> None:
        async with rabbitmq_connection.connection.channel() as channel:
            exchange = await channel.get_exchange(self.MAIN_EXCHANGE)

            message = Message(
                body=payload.model_dump_json().encode("utf-8"),
                content_type="application/json",
                delivery_mode=DeliveryMode.PERSISTENT,
                message_id=idempotency_key or str(uuid4()),
                timestamp=datetime.now(UTC),
            )

            await exchange.publish(message=message, routing_key=routing_key)

    async def _declare_main_queues(
        self, channel: AbstractRobustChannel, main_exchange: AbstractRobustExchange
    ):
        daily_queue = await channel.declare_queue(
            name=self.DAILY_QUEUE,
            durable=True,
            arguments={"x-dead-letter-exchange": self.DLX_EXCHANGE},
        )
        await daily_queue.bind(
            exchange=main_exchange, routing_key=self.DAILY_ROUTING_KEY
        )

        welcome_queue = await channel.declare_queue(
            name=self.WELCOME_QUEUE, durable=True
        )
        await welcome_queue.bind(
            exchange=main_exchange,
            routing_key=self.WELCOME_ROUTING_KEY,
            arguments={"x-dead-letter-exchange": self.DLX_EXCHANGE},
        )

    async def _declare_retry_queue(
        self, channel: AbstractRobustChannel, dlx_exchage: AbstractRobustExchange
    ):
        retry_queue = await channel.declare_queue(
            name=self.RETRY_QUEUE,
            durable=True,
            arguments={
                "x-message-ttl": 30_000,
                "x-dead-letter-exchange": self.MAIN_EXCHANGE,
            },
        )
        await retry_queue.bind(
            exchange=dlx_exchage, routing_key=self.WELCOME_ROUTING_KEY
        )
        await retry_queue.bind(exchange=dlx_exchage, routing_key=self.DAILY_ROUTING_KEY)

    async def _declare_dead_letter_queue(
        self, channel: AbstractRobustChannel, dlx_exchage: AbstractRobustExchange
    ):
        dead_l_queue = await channel.declare_queue(
            name=self.DEAD_LETTER_QUEUE,
            durable=True,
        )
        await dead_l_queue.bind(
            exchange=dlx_exchage, routing_key=self.DEAD_LETTER_ROUTING_KEY
        )

    async def _declare_exchanges(self, channel: AbstractRobustChannel) -> tuple:
        main_exchange = await channel.declare_exchange(
            name=self.MAIN_EXCHANGE, type=ExchangeType.DIRECT, durable=True
        )
        dlx_exchange = await channel.declare_exchange(
            name=self.DLX_EXCHANGE, type=ExchangeType.DIRECT, durable=True
        )

        return main_exchange, dlx_exchange


rabbitmq_service = RabbitMQService()


def get_rabbitmq_service() -> RabbitMQService:
    return rabbitmq_service


async def declare_rabbitmq_topology() -> None:
    await rabbitmq_service.declare_topology()
