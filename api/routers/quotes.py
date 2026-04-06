from http import HTTPStatus

from fastapi import APIRouter, Depends, Query

from api.core.cache import RedisCache
from api.core.security import verify_api_key
from api.models.enums import CategoryQuote
from api.repositories.quote_repository import QuoteRepository
from api.schemas.pagination import PaginatedResponse
from api.schemas.quote_schema import (
    CreateQuoteRequest,
    UpdateQuoteRequest,
    QuoteResponse,
)
from api.services.quote_service import QuoteService
from api.utils.utils import expiration_midnight

api_router = APIRouter(prefix="/v1/quotes", tags=["frases"])
cache = RedisCache()


@api_router.post(
    path="/",
    response_model=QuoteResponse,
    status_code=HTTPStatus.CREATED,
    name="create_quote",
    summary="Criar uma nova citação",
    description="Cria uma nova citação com base nos dados fornecidos.",
    response_description="A citação criada com sucesso.",
)
async def post_quote(
    new_quote: CreateQuoteRequest,
    service: QuoteService = Depends(),
    repo: QuoteRepository = Depends(),
    _: str = Depends(verify_api_key),
) -> QuoteResponse:
    quote = await service.create_quote(quote=new_quote, repo=repo)

    return QuoteResponse.model_validate(quote.model_dump())


@api_router.get(
    path="/",
    response_model=PaginatedResponse[QuoteResponse],
    status_code=HTTPStatus.OK,
    name="get_all_quotes",
    summary="Obter todas as citações",
    description="Retorna uma lista de todas as citações disponíveis.",
    response_description="Lista de citações.",
)
async def get_all_quotes(
    author: str | None = Query(
        default=None, description="Autor para filtrar as citações."
    ),
    tags: list[CategoryQuote] | None = Query(
        default=None, description="Lista de categorias para filtrar as citações."
    ),
    source: str | None = Query(
        default=None, description="Fonte para filtrar as citações."
    ),
    verified: bool = Query(
        default=True, description="Filtrar apenas citações verificadas."
    ),
    limit: int = Query(
        default=0,
        ge=0,
        le=100,
        description="Número máximo de citações a serem retornadas.",
    ),
    skip: int = Query(
        default=0,
        ge=0,
        le=1000,
        description="Número de citações a serem ignoradas para paginação.",
    ),
    service: QuoteService = Depends(),
    repo: QuoteRepository = Depends(),
) -> PaginatedResponse[QuoteResponse]:
    quotes, total_counts = await service.get_all(
        author=author,
        tags=tags,
        source=source,
        verified=verified,
        limit=limit,
        skip=skip,
        repo=repo,
    )

    quotes = [QuoteResponse.model_validate(quote.model_dump()) for quote in quotes]

    return PaginatedResponse(items=quotes, total=total_counts, limit=limit, skip=skip)


@api_router.get(
    path="/random",
    response_model=list[QuoteResponse],
    status_code=HTTPStatus.OK,
    name="get_random_quote",
    summary="Obter citações aleatórias",
    description="Retorna uma lista de citações aleatórias verificadas.",
    response_description="Lista de citações aleatórias.",
)
async def get_random_quote(
    size: int = Query(
        default=1,
        ge=1,
        le=100,
        description="Número de citações aleatórias a serem retornadas.",
    ),
    service: QuoteService = Depends(),
    repo: QuoteRepository = Depends(),
) -> list[QuoteResponse]:
    quotes = await service.get_random_quote(size=size, repo=repo)

    return [QuoteResponse.model_validate(quote.model_dump()) for quote in quotes]


@api_router.get(
    path="/today",
    response_model=list[QuoteResponse],
    status_code=HTTPStatus.OK,
    name="get_today_quote",
    summary="Obter a citação do dia",
    description="Retorna uma citação aleatória verificada para o dia.",
    response_description="Citação do dia.",
)
@cache.cacheable(expire=expiration_midnight)
async def get_today_quote(
    service: QuoteService = Depends(), repo: QuoteRepository = Depends()
) -> list[QuoteResponse]:
    quotes = await service.get_today_quote(repo=repo)
    return [QuoteResponse.model_validate(quote.model_dump()) for quote in quotes]


@api_router.get(
    path="/{id}",
    response_model=QuoteResponse,
    status_code=HTTPStatus.OK,
    name="get_quote_by_id",
    summary="Obter uma citação por ID",
    description="Retorna uma citação específica com base no ID fornecido.",
    response_description="Citação encontrada com sucesso.",
)
@cache.cacheable(expire=3600)
async def get_quote_by_id(
    id: str,
    service: QuoteService = Depends(),
    repo: QuoteRepository = Depends(),
) -> QuoteResponse:
    quote = await service.get_quote_by_id(id=id, repo=repo)
    return QuoteResponse.model_validate(quote.model_dump())


@api_router.put(
    path="/{id}",
    response_model=QuoteResponse,
    status_code=HTTPStatus.OK,
    name="update_quote",
    summary="Atualizar uma citação por ID",
    description="Atualiza uma citação existente com base no ID fornecido e nos dados atualizados.",
    response_description="Citação atualizada com sucesso.",
)
async def update_quote(
    id: str,
    quote_data: UpdateQuoteRequest,
    service: QuoteService = Depends(),
    repo: QuoteRepository = Depends(),
    _: str = Depends(verify_api_key),
) -> QuoteResponse:
    quote = await service.update_quote_by_id(id=id, quote_data=quote_data, repo=repo)

    return QuoteResponse.model_validate(quote.model_dump())


@api_router.delete(
    path="/{id}",
    status_code=HTTPStatus.NO_CONTENT,
    name="delete_quote",
    summary="Deletar uma citação por ID",
    description="Deleta uma citação existente com base no ID fornecido.",
    response_description="Citação deletada com sucesso.",
)
async def delete_quote(
    id: str,
    service: QuoteService = Depends(),
    repo: QuoteRepository = Depends(),
    _: str = Depends(verify_api_key),
) -> None:
    await service.delete_quote_by_id(id=id, repo=repo)
