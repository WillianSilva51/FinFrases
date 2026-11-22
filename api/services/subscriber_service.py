from collections.abc import Callable
from datetime import UTC, datetime, timedelta

from loguru import logger

from api.core.exceptions.custom_exceptions import (
    SubscriberAlreadyExistsException,
    SubscriberNotFoundException,
    UnsubscriberAlreadyUnsubscribedException,
)
from api.models.enums import SubscriberStatus
from api.models.subscriber import Subscriber
from api.repositories.subscriber_repository import SubscriberRepository
from api.schemas.subscriber_schema import (
    CreateSubscriberRequest,
    UnsubscribeSubscriberRequest,
)
from api.services.email.send_welcome_email import SendWelcomeEmail


class SubscriberService:
    def __init__(
        self,
        repo: SubscriberRepository,
        send_welcome_email: SendWelcomeEmail,
    ) -> None:
        self.subscriber_repository = repo
        self.send_welcome_email = send_welcome_email

    async def create_subscriber(
        self,
        subscriber: CreateSubscriberRequest,
        token_generator: Callable[[int], str],
    ) -> Subscriber:
        """
        Cria um novo assinante.

        Args:
            token_generator: Uma função que gera um token de desinscrição.
            repo: Instância do repositório de assinantes.
            subscriber: Dados de entrada validados para criação do assinante.

        Returns:
            Uma instância de ``SubscriberResponse`` com os dados do novo assinante.
        """
        subscriber_exists = await self.subscriber_repository.get_subscriber_by_email(
            subscriber.email
        )

        if subscriber_exists:
            if subscriber_exists.status == SubscriberStatus.UNSUBSCRIBED:
                new_unsubscribe_token = token_generator(32)

                subscriber_exists = (
                    await self.subscriber_repository.reactivate_subscriber(
                        subscriber_exists, new_unsubscribe_token
                    )
                )

                await self._check_and_send_welcome_email(subscriber_exists)

                return subscriber_exists
            else:
                raise SubscriberAlreadyExistsException(
                    "Assinante com este e-mail já existe."
                )

        new_subscriber = await self.subscriber_repository.create_subscriber(subscriber)

        await self.send_welcome_email.execute(new_subscriber)

        return new_subscriber

    async def _check_and_send_welcome_email(
        self, subscriber_exists: Subscriber
    ) -> None:
        created_at = subscriber_exists.created_at

        if datetime.now(UTC) - created_at < timedelta(days=1):
            logger.info(
                f"Assinante com e-mail {subscriber_exists.email} reativado recentemente. E-mail de boas-vindas não será enviado novamente."
            )
            return
        else:
            await self.send_welcome_email.execute(subscriber_exists)

    async def unsubscribe_subscriber(
        self,
        unsubscriber: UnsubscribeSubscriberRequest,
    ) -> Subscriber:
        """
        Desinscreve um assinante existente.

        Args:
            repo: Instância do repositório de assinantes.
            unsubscriber: Um objeto ``UnsubscribeSubscriberRequest`` contendo o e-mail do assinante a ser desinscrito e o token de desinscrição.

        Returns:
            Uma instância de ``UnsubscribeResponse`` indicando o sucesso da operação.
        """
        subscriber = (
            await self.subscriber_repository.get_subscriber_by_unsubscribe_token(
                unsubscriber.unsubscribe_token
            )
        )

        if not subscriber:
            raise SubscriberNotFoundException(
                "Assinante com este token de desinscrição não foi encontrado."
            )

        if subscriber.status == SubscriberStatus.UNSUBSCRIBED:
            raise UnsubscriberAlreadyUnsubscribedException(
                "Assinante com este token de desinscrição já está desinscrito."
            )

        unsubscribed_subscriber = (
            await self.subscriber_repository.unsubscribe_subscriber(subscriber)
        )

        return unsubscribed_subscriber

    async def get_subscribers(
        self,
        status: SubscriberStatus,
        skip: int,
        limit: int,
    ) -> tuple[list[Subscriber], int, int]:
        """
        Obtém uma lista de assinantes com base no status fornecido.

        Args:
            repo: Instância do repositório de assinantes.
            status: O status dos assinantes a serem obtidos.
            skip: O número de registros a serem ignorados (para paginação).
            limit: O número máximo de registros a serem retornados.

        Returns:
            Uma tupla contendo a lista de assinantes e o total de assinantes encontrados.
        """
        (
            subscribers,
            total_count,
        ) = await self.subscriber_repository.get_subscribers_by_status(
            status=status, skip=skip, limit=limit
        )

        return subscribers, total_count, (total_count + limit - 1) // limit
