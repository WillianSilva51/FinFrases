from http import HTTPStatus

from fastapi import APIRouter, Depends, Query, Request, Response

from api.core.limiter import limiter
from api.core.security import verify_api_key
from api.repositories.quote_repository import QuoteRepository
from api.schemas.pagination import PaginatedResponse, Params
from api.schemas.quote_filters import QuoteFilters, QuoteSort
from api.schemas.quote_schema import (
    CreateQuoteRequest,
    QuoteResponse,
    UpdateQuoteRequest,
)
from api.services.quote_service import QuoteService

api_router = APIRouter(prefix="/v1/quotes")


@api_router.post(
    path="/",
    response_model=QuoteResponse,
    status_code=HTTPStatus.CREATED,
    name="create_quote",
    summary="Criar uma nova citação",
    description="Cria uma nova citação com base nos dados fornecidos.",
    response_description="A citação criada com sucesso.",
)
@limiter.limit("20/minute")
async def post_quote(
    request: Request,
    response: Response,
    new_quote: CreateQuoteRequest,
    service: QuoteService = Depends(QuoteService),  # noqa: B008
    repo: QuoteRepository = Depends(QuoteRepository),  # noqa: B008
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
@limiter.limit("40/minute")
async def get_all_quotes(
    request: Request,
    response: Response,
    quote_filters: QuoteFilters = Depends(QuoteFilters),  # noqa: B008
    quote_sort: QuoteSort = Depends(QuoteSort),  # noqa: B008
    params: Params = Depends(Params),  # noqa: B008
    service: QuoteService = Depends(QuoteService),  # noqa: B008
    repo: QuoteRepository = Depends(QuoteRepository),  # noqa: B008
) -> PaginatedResponse[QuoteResponse]:
    quotes, total_counts, pages = await service.get_all(
        quote_filters=quote_filters,
        quote_sort=quote_sort,
        limit=params.get_limit(),
        skip=params.get_offset(),
        repo=repo,
    )

    quotes = [QuoteResponse.model_validate(quote.model_dump()) for quote in quotes]

    return PaginatedResponse(
        items=quotes,
        total=total_counts,
        page=params.page,
        size=params.size,
        pages=pages,
    )


@api_router.get(
    path="/random",
    response_model=list[QuoteResponse],
    status_code=HTTPStatus.OK,
    name="get_random_quote",
    summary="Obter citações aleatórias",
    description="Retorna uma lista de citações aleatórias verificadas.",
    response_description="Lista de citações aleatórias.",
)
@limiter.limit("40/minute")
async def get_random_quote(
    request: Request,
    response: Response,
    size: int = Query(
        default=1,
        ge=1,
        le=100,
        description="Número de citações aleatórias a serem retornadas.",
    ),
    service: QuoteService = Depends(QuoteService),  # noqa: B008
    repo: QuoteRepository = Depends(QuoteRepository),  # noqa: B008
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
@limiter.limit("30/minute")
async def get_today_quote(
    request: Request,
    response: Response,
    service: QuoteService = Depends(QuoteService),  # noqa: B008
    repo: QuoteRepository = Depends(QuoteRepository),  # noqa: B008
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
@limiter.limit("30/minute")
async def get_quote_by_id(
    id: str,
    request: Request,
    response: Response,
    service: QuoteService = Depends(QuoteService),  # noqa: B008
    repo: QuoteRepository = Depends(QuoteRepository),  # noqa: B008
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
@limiter.limit("20/minute")
async def update_quote(
    id: str,
    quote_data: UpdateQuoteRequest,
    request: Request,
    response: Response,
    service: QuoteService = Depends(QuoteService),  # noqa: B008
    repo: QuoteRepository = Depends(QuoteRepository),  # noqa: B008
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
@limiter.limit("20/minute")
async def delete_quote(
    id: str,
    request: Request,
    response: Response,
    service: QuoteService = Depends(QuoteService),  # noqa: B008
    repo: QuoteRepository = Depends(QuoteRepository),  # noqa: B008
    _: str = Depends(verify_api_key),
) -> None:
    await service.delete_quote_by_id(id=id, repo=repo)
