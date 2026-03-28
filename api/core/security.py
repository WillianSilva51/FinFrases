import secrets

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from .config import settings
from loguru import logger

api_key_header = APIKeyHeader(
    name="X-API-Key",
    scheme_name="API-Key",
    description="Chave de API para autenticação.",
    auto_error=False,
)


def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    if not api_key:
        logger.warning("Chave de API ausente.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais ausentes.",
            headers={"WWW-Authenticate": "API-Key"},
        )

    if not secrets.compare_digest(api_key, settings.API_KEY):
        logger.warning("Chave de API inválida.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas.",
            headers={"WWW-Authenticate": "API-Key"},
        )
    return api_key
