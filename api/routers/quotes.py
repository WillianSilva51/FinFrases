from http import HTTPStatus

from fastapi import APIRouter, Query
from models.enums import CategoryQuote
from schemas.quote_schema import CreateQuoteRequest, QuoteResponse
from services.quote_service import create_quote, get_all

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
async def post_quote(new_quote: CreateQuoteRequest) -> QuoteResponse:
    return await create_quote(new_quote)


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
    limit: int | None = Query(
        default=None, description="Número máximo de citações a serem retornadas."
    ),
) -> list[QuoteResponse]:
    return await get_all(author, tags, source, limit)
