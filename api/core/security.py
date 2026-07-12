import secrets

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
from loguru import logger

from .config import settings

api_key_header = APIKeyHeader(
    name="X-API-Key",
    scheme_name="API-Key",
    description="Chave de API para autenticação.",
    auto_error=False,
)
"""Esquema de autenticação por cabeçalho para a API.

Este objeto define o cabeçalho ``X-API-Key`` como fonte da credencial e
desativa o erro automático para que a validação seja realizada manualmente
na função :func:`verify_api_key`.
"""


def verify_api_key(api_key: str | None = Security(api_key_header)) -> str:
    """Valida a chave de API enviada na requisição.

        A função verifica se a credencial foi informada e compara o valor recebido
    com a chave configurada em ``settings.API_KEY`` usando comparação segura.

        Args:
            api_key: Chave de API obtida do cabeçalho ``X-API-Key``.

        Returns:
            A chave de API validada.

        Raises:
            HTTPException: Se a credencial estiver ausente ou for inválida.
    """
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
