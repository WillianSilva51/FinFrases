from http import HTTPStatus

from fastapi import APIRouter, Request, Response, Security

from api.core.limiter import limiter
from api.core.security import api_key_header, verify_api_key

api_router = APIRouter(prefix="/auth")


@api_router.get(
    path="/verify",
    status_code=HTTPStatus.NO_CONTENT,
    name="verify_api_key",
    summary="Verificar a validade da chave de API",
    description="Endpoint para verificar a validade da chave de API.",
    response_description="A chave de API é válida.",
    responses={HTTPStatus.UNAUTHORIZED: {"description": "Chave de API inválida."}},
)
@limiter.limit("10/minute;100/hour")
async def verify(
    request: Request, response: Response, api_key: str | None = Security(api_key_header)
) -> None:
    """
    Endpoint para verificar a validade da chave de API.
    """
    verify_api_key(api_key)
