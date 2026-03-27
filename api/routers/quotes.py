from http import HTTPStatus

from fastapi import APIRouter, Depends, Query
from models.enums import CategoryQuote
from schemas.quote_schema import CreateQuoteRequest, QuoteResponse
from services.quote_service import QuoteService
from models.quote import Quote

api_router = APIRouter(prefix="/v1/quotes", tags=["frases"])


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
    new_quote: CreateQuoteRequest, service: QuoteService = Depends()
) -> Quote:
    return await service.create_quote(new_quote)


@api_router.get(
    path="/",
    response_model=list[QuoteResponse],
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
        description="Número máximo de citações a serem retornadas.",
    ),
    skip: int = Query(
        default=0, description="Número de citações a serem ignoradas para paginação."
    ),
    service: QuoteService = Depends(),
) -> list[Quote]:
    return await service.get_all(
        author=author,
        tags=tags,
        source=source,
        verified=verified,
        limit=limit,
        skip=skip,
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
async def get_random_quote(
    size: int = Query(
        default=1, description="Número de citações aleatórias a serem retornadas."
    ),
    service: QuoteService = Depends(),
) -> list[Quote]:
    return await service.get_random_quote(size=size)
