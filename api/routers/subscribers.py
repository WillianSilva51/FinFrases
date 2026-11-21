from collections.abc import Callable
from http import HTTPStatus

from fastapi import APIRouter, Depends, Request, Response

from api.core.limiter import limiter
from api.models.subscriber import Subscriber
from api.repositories.subscriber_repository import SubscriberRepository
from api.schemas.subscriber_schema import (
    CreateSubscriberRequest,
    SubscriberResponse,
    UnsubscribeResponse,
    UnsubscribeSubscriberRequest,
)
from api.services.subscriber_service import SubscriberService
from api.utils.utils import get_token_generator, mask_email

api_router = APIRouter(prefix="/v1/subscribers")


def _create_subscriber_response(subscriber: Subscriber) -> SubscriberResponse:
    """
    Cria uma instância de ``SubscriberResponse`` a partir de um objeto ``Subscriber``.
    """
    return SubscriberResponse.model_validate(
        subscriber.model_dump(include={"email", "status"})
    )


@api_router.post(
    path="/",
    response_model=SubscriberResponse,
    status_code=HTTPStatus.CREATED,
    name="Criar Assinante",
    summary="Cria um novo assinante",
    description="Cria um novo assinante com base nos dados fornecidos.",
    response_description="O assinante criado com sucesso.",
)
@limiter.limit("3/minute;10/hour")
async def create_subscriber(
    request: Request,
    response: Response,
    new_subscriber: CreateSubscriberRequest,
    token_generator: Callable[[int], str] = Depends(get_token_generator),  # noqa: B008
    subscriber_service: SubscriberService = Depends(SubscriberService),  # noqa: B008
    subscriber_repository: SubscriberRepository = Depends(SubscriberRepository),  # noqa: B008
) -> SubscriberResponse:
    """
    Endpoint para criar um novo assinante.

    Este endpoint permite criar um novo assinante no sistema. O assinante será adicionado à base de dados com o status "ativo".

    Returns:
        JSONResponse: Retorna uma resposta JSON contendo os detalhes do assinante criado.
    """
    subscriber = await subscriber_service.create_subscriber(
        new_subscriber, token_generator, subscriber_repository
    )

    return _create_subscriber_response(subscriber)


@api_router.post(
    path="/unsubscribe",
    response_model=UnsubscribeResponse,
    status_code=HTTPStatus.OK,
    name="Desinscrever Assinante",
    summary="Desinscreve um assinante existente",
    description="Desinscreve um assinante existente com base nos dados fornecidos.",
    response_description="O assinante desinscrito com sucesso.",
)
@limiter.limit("10/minute")
async def unsubscribe_subscriber(
    request: Request,
    response: Response,
    unsubscriber: UnsubscribeSubscriberRequest,
    subscriber_service: SubscriberService = Depends(SubscriberService),  # noqa: B008
    subscriber_repository: SubscriberRepository = Depends(SubscriberRepository),  # noqa: B008
) -> UnsubscribeResponse:
    """
    Endpoint para desinscrever um assinante existente.

    Este endpoint permite desinscrever um assinante existente no sistema. O assinante será removido da base de dados ou terá seu status atualizado para "desinscrito".

    Returns:
        JSONResponse: Retorna uma resposta JSON contendo os detalhes do assinante desinscrito.
    """
    unsubscribed_subscriber = await subscriber_service.unsubscribe_subscriber(
        unsubscriber, subscriber_repository
    )

    return UnsubscribeResponse.model_validate(
        {
            "message": "Sua inscrição foi cancelada com sucesso. Você não receberá mais e-mails diários.",
            "status": unsubscribed_subscriber.status,
            "masked_email": mask_email(str(unsubscribed_subscriber.email)),
        }
    )
