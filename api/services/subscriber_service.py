from api.core.exceptions.custom_exceptions import (
    SubscriberAlreadyExistsException,
    SubscriberNotFoundException,
)
from api.models.enums import SubscriberStatus
from api.repositories.subscriber_repository import SubscriberRepository
from api.schemas.subscriber_schema import (
    CreateSubscriberRequest,
    SubscriberResponse,
    UnsubscribeSubscriberRequest,
    UpdateSubscriberRequest,
)


class SubscriberService:
    async def create_subscriber(
        self, repo: SubscriberRepository, subscriber: CreateSubscriberRequest
    ) -> SubscriberResponse:
        """
        Cria um novo assinante.

        Args:
            repo: Instância do repositório de assinantes.
            subscriber: Dados de entrada validados para criação do assinante.

        Returns:
            A instância de ``Subscriber`` criada.
        """
        subscriber_exists = await repo.get_subscriber_by_email(subscriber.email)

        if subscriber_exists:
            if subscriber_exists.status == SubscriberStatus.UNSUBSCRIBED:
                subscriber_exists = await repo.reativate_subscriber(subscriber_exists)

                return SubscriberResponse.model_validate(subscriber_exists.model_dump())
            else:
                raise SubscriberAlreadyExistsException(
                    "Assinante com este e-mail já existe."
                )

        new_subscriber = await repo.create(subscriber)

        return SubscriberResponse.model_validate(new_subscriber.model_dump())

    async def unsubscribe_subscriber(
        self, repo: SubscriberRepository, unsubscriber: UnsubscribeSubscriberRequest
    ) -> SubscriberResponse:
        """
        Desinscreve um assinante existente.

        Args:
            repo: Instância do repositório de assinantes.
            unsubscriber: Um objeto ``UnsubscribeSubscriberRequest`` contendo o e-mail do assinante a ser desinscrito e o token de desinscrição.

        Returns:
            A instância de ``Subscriber`` desinscrita.
        """
        subscriber = await repo.get_subscriber_by_email(unsubscriber.email)

        if not subscriber:
            raise SubscriberNotFoundException(
                "Assinante com este e-mail não foi encontrado."
            )

        if subscriber.unsubscribe_token != unsubscriber.unsubscribe_token:
            raise SubscriberNotFoundException(
                "Token de desinscrição inválido para este assinante."
            )

        unsubscribed_subscriber = await repo.unsubscribe_subscriber(unsubscriber)

        return SubscriberResponse.model_validate(unsubscribed_subscriber.model_dump())

    async def update_subscriber_name(
        self, repo: SubscriberRepository, update_subscriber: UpdateSubscriberRequest
    ) -> SubscriberResponse:
        """
        Atualiza o nome de um assinante existente.

        Args:
            repo: Instância do repositório de assinantes.
            email: O e-mail do assinante a ser atualizado.
            new_name: O novo nome para o assinante.

        Returns:
            A instância de ``Subscriber`` atualizada.
        """
        subscriber = await repo.get_subscriber_by_email(update_subscriber.email)

        if not subscriber:
            raise SubscriberNotFoundException(
                "Assinante com este e-mail não foi encontrado."
            )

        updated_subscriber = await repo.update_subscriber(
            **update_subscriber.model_dump()
        )

        return SubscriberResponse.model_validate(updated_subscriber.model_dump())

    async def get_subscribers(
        self,
        repo: SubscriberRepository,
        status: SubscriberStatus,
        skip: int,
        limit: int,
    ) -> tuple[list[SubscriberResponse], int, int]:
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
        subscribers, total_count = await repo.get_subscribers_by_status(
            status=status, skip=skip, limit=limit
        )

        subscriber_responses = [
            SubscriberResponse.model_validate(subscriber.model_dump())
            for subscriber in subscribers
        ]

        return subscriber_responses, total_count, (total_count + limit - 1) // limit
