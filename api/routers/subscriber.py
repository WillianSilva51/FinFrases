from http import HTTPStatus

from fastapi import APIRouter, Depends, Request, Response

from api.core.limiter import limiter
from api.repositories.subscriber_repository import SubscriberRepository
from api.schemas.subscriber_schema import (
    CreateSubscriberRequest,
    SubscriberResponse,
    UnsubscribeSubscriberRequest,
    UpdateSubscriberRequest,
)
from api.services.subscriber_service import SubscriberService

api_router = APIRouter(prefix="/v1/subscribers")


@api_router.post(
    path="/",
    response_model=SubscriberResponse,
    status_code=HTTPStatus.CREATED,
    name="Criar Assinante",
    summary="Cria um novo assinante",
    description="Cria um novo assinante com base nos dados fornecidos.",
    response_description="O assinante criado com sucesso.",
)
@limiter.limit("5/minute")
async def create_subscriber(
    request: Request,
    response: Response,
    new_subscriber: CreateSubscriberRequest,
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
        new_subscriber, subscriber_repository
    )

    return SubscriberResponse.model_validate(subscriber.model_dump())


@api_router.post(
    path="/unsubscribe",
    response_model=SubscriberResponse,
    status_code=HTTPStatus.OK,
    name="Desinscrever Assinante",
    summary="Desinscreve um assinante existente",
    description="Desinscreve um assinante existente com base nos dados fornecidos.",
    response_description="O assinante desinscrito com sucesso.",
)
@limiter.limit("5/minute")
async def unsubscribe_subscriber(
    request: Request,
    response: Response,
    unsubscriber: UnsubscribeSubscriberRequest,
    subscriber_service: SubscriberService = Depends(SubscriberService),  # noqa: B008
    subscriber_repository: SubscriberRepository = Depends(SubscriberRepository),  # noqa: B008
) -> SubscriberResponse:
    """
    Endpoint para desinscrever um assinante existente.

    Este endpoint permite desinscrever um assinante existente no sistema. O assinante será removido da base de dados ou terá seu status atualizado para "desinscrito".

    Returns:
        JSONResponse: Retorna uma resposta JSON contendo os detalhes do assinante desinscrito.
    """
    subscriber = await subscriber_service.unsubscribe_subscriber(
        unsubscriber, subscriber_repository
    )

    return SubscriberResponse.model_validate(subscriber.model_dump())


@api_router.put(
    path="/",
    response_model=SubscriberResponse,
    status_code=HTTPStatus.OK,
    name="Atualizar Nome do Assinante",
    summary="Atualiza o nome de um assinante existente",
    description="Atualiza o nome de um assinante existente com base nos dados fornecidos.",
    response_description="O nome do assinante atualizado com sucesso.",
)
@limiter.limit("5/minute")
async def update_subscriber_name(
    request: Request,
    response: Response,
    update_subscriber: UpdateSubscriberRequest,
    subscriber_service: SubscriberService = Depends(SubscriberService),  # noqa: B008
    subscriber_repository: SubscriberRepository = Depends(SubscriberRepository),  # noqa: B008
) -> SubscriberResponse:
    """
    Endpoint para atualizar o nome de um assinante existente.

    Este endpoint permite atualizar o nome de um assinante existente no sistema. O assinante será identificado pelo e-mail fornecido e seu nome será atualizado com o novo valor.

    Returns:
        JSONResponse: Retorna uma resposta JSON contendo os detalhes do assinante atualizado.
    """
    subscriber = await subscriber_service.update_subscriber_name(
        update_subscriber, subscriber_repository
    )

    return SubscriberResponse.model_validate(subscriber.model_dump())
