import secrets

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from .config import settings
from loguru import logger

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)


def verify_api_key(api_key: str = Security(api_key_header)):
    if not secrets.compare_digest(api_key, settings.API_KEY):
        logger.warning(f"Chave de API inválida ou ausente. Chave recebida: {api_key}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas ou ausentes.",
        )
    return api_key
