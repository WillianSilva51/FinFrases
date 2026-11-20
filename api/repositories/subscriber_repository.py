from datetime import UTC, datetime

from api.models.enums import SubscriberStatus
from api.models.subscriber import Subscriber
from api.schemas.subscriber_schema import (
    CreateSubscriberRequest,
    UnsubscribeSubscriberRequest,
)


class SubscriberRepository:
    """Repositório responsável pelas operações de persistência de assinantes.

    Esta classe encapsula as operações de criação, consulta, atualização,
    exclusão e obtenção de assinantes no banco de dados, mantendo a
    camada de acesso a dados isolada da regra de negócio.
    """

    async def create_subscriber(
        self, subscriber_data: CreateSubscriberRequest
    ) -> Subscriber:
        """Cria e persiste um novo assinante no banco de dados.

        Args:
            subscriber_data: Dados de entrada validados para criação do assinante.

        Returns:
            A instância de ``Subscriber`` já inserida no banco de dados.
        """
        new_subscriber = Subscriber.model_validate(subscriber_data.model_dump())

        return await new_subscriber.insert()

    async def reativate_subscriber(
        self, subscriber: Subscriber, new_unsubscribe_token: str
    ) -> Subscriber:
        """
        Reativa um assinante previamente desinscrito, atualizando seu status para "active".

        Args:
            subscriber: A instância de ``Subscriber`` a ser reativada.

        Returns:
            A instância de ``Subscriber`` atualizada com o status "active".
        """
        return await subscriber.update(
            {
                "$set": {
                    "status": SubscriberStatus.ACTIVE,
                    "updated_at": datetime.now(UTC),
                    "unsubscribed_at": None,
                    "unsubscribe_token": new_unsubscribe_token,
                }
            }
        )

    async def get_subscriber_by_email(self, email: str) -> Subscriber | None:
        """
        Obtém um assinante pelo endereço de e-mail.

        Args:
            email: O endereço de e-mail do assinante.

        Returns:
            A instância de ``Subscriber`` encontrada, ou ``None`` se não for encontrada.
        """
        return await Subscriber.find_one({"email": email})

    async def get_subscribers_by_status(
        self, status: SubscriberStatus, limit: int, skip: int
    ) -> tuple[list[Subscriber], int]:
        """
        Obtém uma lista de assinantes com um status específico.

        Args:
            status: O status dos assinantes a serem retornados.
            limit: O número máximo de assinantes a serem retornados.
            skip: O número de assinantes a serem ignorados no início da lista.

        Returns:
            Uma tupla contendo a lista de assinantes e o total de assinantes encontrados.
        """
        params = {"status": status}

        total_count = await Subscriber.find(params).count()

        subscribers = Subscriber.find(params)

        subscribers = subscribers.skip(skip).limit(limit)

        return await subscribers.to_list(), total_count

    async def get_subscriber_by_unsubscribe_token(
        self, unsubscribe_token: str
    ) -> Subscriber | None:
        """
        Obtém um assinante pelo token de cancelamento de inscrição.

        Args:
            unsubscribe_token: O token de cancelamento de inscrição do assinante.

        Returns:
            A instância de ``Subscriber`` encontrada, ou ``None`` se não for encontrada.
        """
        return await Subscriber.find_one({"unsubscribe_token": unsubscribe_token})

    async def subscriber_exists_by_unsubscribe_token(
        self, unsubscribe_token: str
    ) -> bool:
        """
        Verifica se um assinante existe com o token de cancelamento de inscrição fornecido.

        Args:
            unsubscribe_token: O token de cancelamento de inscrição do assinante.

        Returns:
            ``True`` se o assinante existir, ``False`` caso contrário.
        """
        return (
            await Subscriber.find_one({"unsubscribe_token": unsubscribe_token}).count()
            > 0
        )

    async def unsubscribe_subscriber(
        self, unsubscriber: UnsubscribeSubscriberRequest
    ) -> Subscriber:
        """
        Realiza a exclusão suave (soft delete) de um assinante, atualizando seu status para "unsubscribed" e registrando a data de desinscrição.

        Args:
            unsubscriber: Um objeto ``UnsubscribeSubscriberRequest`` contendo o e-mail do assinante a ser desinscrito.

        Returns:
            A instância de ``Subscriber`` atualizada com o status "unsubscribed" e a data de desinscrição.
        """

        subscriber = await self.get_subscriber_by_unsubscribe_token(
            unsubscriber.unsubscribe_token
        )

        date = datetime.now(UTC)

        return await subscriber.update(
            {
                "$set": {
                    "status": SubscriberStatus.UNSUBSCRIBED,
                    "updated_at": date,
                    "unsubscribed_at": date,
                }
            }
        )

    async def update_subscriber(self, email: str, subscriber_data: dict) -> Subscriber:
        """
        Atualiza os dados de um assinante existente.

        Args:
            email: O endereço de e-mail do assinante a ser atualizado.
            subscriber_data: Um dicionário contendo os dados atualizados do assinante.

        Returns:
            A instância de ``Subscriber`` atualizada.
        """
        existing_subscriber = await self.get_subscriber_by_email(email)

        update_data = {**subscriber_data, "updated_at": datetime.now(UTC)}

        return await existing_subscriber.update({"$set": update_data})
