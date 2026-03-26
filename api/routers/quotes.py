from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from schemas.quote_schema import CreateQuoteRequest, QuoteResponse
from services.quote_service import create_quote

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
