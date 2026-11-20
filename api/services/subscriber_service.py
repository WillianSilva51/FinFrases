from secrets import token_urlsafe

from api.core.exceptions.custom_exceptions import (
    SubscriberAlreadyExistsException,
    SubscriberNotFoundException,
    UnsubcriberAlreadyUnsubscribedException,
    UnsubscribeTokenInvalidException,
)
from api.models.enums import SubscriberStatus
from api.models.subscriber import Subscriber
from api.repositories.subscriber_repository import SubscriberRepository
from api.schemas.subscriber_schema import (
    CreateSubscriberRequest,
    SubscriberResponse,
    UnsubscribeResponse,
    UnsubscribeSubscriberRequest,
    UpdateSubscriberRequest,
)
from api.utils.utils import mask_email


class SubscriberService:
    async def create_subscriber(
        self,
        subscriber: CreateSubscriberRequest,
        repo: SubscriberRepository,
    ) -> SubscriberResponse:
        """
        Cria um novo assinante.

        Args:
            repo: Instância do repositório de assinantes.
            subscriber: Dados de entrada validados para criação do assinante.

        Returns:
            Uma instância de ``SubscriberResponse`` com os dados do novo assinante.
        """
        subscriber_exists = await repo.get_subscriber_by_email(subscriber.email)

        if subscriber_exists:
            if subscriber_exists.status == SubscriberStatus.UNSUBSCRIBED:
                new_unsubscribe_token = token_urlsafe(32)

                subscriber_exists = await repo.reativate_subscriber(
                    subscriber_exists, new_unsubscribe_token
                )

                return self._create_subscriber_response(subscriber_exists)
            else:
                raise SubscriberAlreadyExistsException(
                    "Assinante com este e-mail já existe."
                )

        new_subscriber = await repo.create_subscriber(subscriber)

        return self._create_subscriber_response(new_subscriber)

    async def unsubscribe_subscriber(
        self,
        unsubscriber: UnsubscribeSubscriberRequest,
        repo: SubscriberRepository,
    ) -> UnsubscribeResponse:
        """
        Desinscreve um assinante existente.

        Args:
            repo: Instância do repositório de assinantes.
            unsubscriber: Um objeto ``UnsubscribeSubscriberRequest`` contendo o e-mail do assinante a ser desinscrito e o token de desinscrição.

        Returns:
            Uma instância de ``UnsubscribeResponse`` indicando o sucesso da operação.
        """
        subscriber = await repo.get_subscriber_by_unsubscribe_token(
            unsubscriber.unsubscribe_token
        )

        if not subscriber:
            raise UnsubscribeTokenInvalidException("Token de desinscrição inválido.")

        if subscriber.status == SubscriberStatus.UNSUBSCRIBED:
            raise UnsubcriberAlreadyUnsubscribedException(
                "Assinante com este token de desinscrição já está desinscrito."
            )

        unsubscribed_subscriber = await repo.unsubscribe_subscriber(unsubscriber)

        return UnsubscribeResponse.model_validate(
            {
                "message": "Sua inscrição foi cancelada com sucesso. Você não receberá mais e-mails diários.",
                "status": unsubscribed_subscriber.status,
                "masked_email": mask_email(str(unsubscribed_subscriber.email)),
            }
        )

    async def update_subscriber_name(
        self,
        update_subscriber: UpdateSubscriberRequest,
        repo: SubscriberRepository,
    ) -> SubscriberResponse:
        """
        Atualiza o nome de um assinante existente.

        Args:
            repo: Instância do repositório de assinantes.
            update_subscriber: Um objeto ``UpdateSubscriberRequest`` contendo o e-mail e o novo nome do assinante.

        Returns:
            Uma instância de ``SubscriberResponse`` com os dados atualizados.
        """
        subscriber = await repo.get_subscriber_by_email(update_subscriber.email)

        if not subscriber:
            raise SubscriberNotFoundException(
                "Assinante com este e-mail não foi encontrado."
            )

        updated_subscriber = await repo.update_subscriber(
            update_subscriber.email, {"name": update_subscriber.name}
        )

        return self._create_subscriber_response(updated_subscriber)

    async def get_subscribers(
        self,
        status: SubscriberStatus,
        skip: int,
        limit: int,
        repo: SubscriberRepository,
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
            self._create_subscriber_response(subscriber) for subscriber in subscribers
        ]

        return subscriber_responses, total_count, (total_count + limit - 1) // limit

    def _create_subscriber_response(self, subscriber: Subscriber) -> SubscriberResponse:
        """
        Cria uma instância de ``SubscriberResponse`` a partir de um objeto ``Subscriber``.
        """
        return SubscriberResponse.model_validate(
            subscriber.model_dump(include={"name", "email", "unsubscribe_token"})
        )
