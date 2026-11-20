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

    async def create(self, subscriber_data: CreateSubscriberRequest) -> Subscriber:
        """Cria e persiste um novo assinante no banco de dados.

        Args:
            subscriber_data: Dados de entrada validados para criação do assinante.

        Returns:
            A instância de ``Subscriber`` já inserida no banco de dados.
        """
        new_subscriber = Subscriber.model_validate(subscriber_data.model_dump())

        return await new_subscriber.insert()

    async def get_subscriber_by_email(self, email: str):
        """
        Obtém um assinante pelo endereço de e-mail.

        Args:
            email: O endereço de e-mail do assinante.

        Returns:
            A instância de ``Subscriber`` encontrada, ou ``None`` se não for encontrada.
        """
        return await Subscriber.find_one({"email": email})

    async def get_subscriber_with_status(
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

    async def soft_delete(
        self, unsubscriber: UnsubscribeSubscriberRequest
    ) -> Subscriber:
        """
        Realiza a exclusão suave (soft delete) de um assinante, atualizando seu status para "unsubscribed" e registrando a data de desinscrição.

        Args:
            unsubscriber: Um objeto ``UnsubscribeSubscriberRequest`` contendo o e-mail do assinante a ser desinscrito.

        Returns:
            A instância de ``Subscriber`` atualizada com o status "unsubscribed" e a data de desinscrição.
        """

        subcriber = await self.get_subscriber_by_email(str(unsubscriber.email))

        date = datetime.now(UTC)

        assert subcriber is not None
        return await subcriber.update(
            {
                "$set": {
                    "status": SubscriberStatus.UNSUBCRIBED,
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

        assert existing_subscriber is not None
        return await existing_subscriber.update({"$set": update_data})
