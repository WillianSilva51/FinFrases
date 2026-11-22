from fastapi import Depends

from api.dependencies.repositories.repositories_dependencies import get_quote_repository
from api.repositories.quote_repository import QuoteRepository
from api.services.quote_service import QuoteService


def get_quote_service(
    quote_repo: QuoteRepository = Depends(get_quote_repository),  # noqa: B008
) -> QuoteService:
    """
    Retorna uma instância do serviço de citações.

    Args:
        quote_repo (QuoteRepository): Instância do repositório de citações.

    Returns:
        QuoteService: Instância do serviço de citações.
    """
    return QuoteService(repo=quote_repo)
