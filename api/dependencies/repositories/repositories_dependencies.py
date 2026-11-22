from api.repositories.quote_repository import QuoteRepository
from api.repositories.subscriber_repository import SubscriberRepository


def get_quote_repository() -> QuoteRepository:
    """
    Retorna uma instância do repositório de citações.

    Returns:
        QuoteRepository: Instância do repositório de citações.
    """
    return QuoteRepository()


def get_subscriber_repository() -> SubscriberRepository:
    """
    Retorna uma instância do repositório de assinantes.

    Returns:
        SubscriberRepository: Uma instância do repositório de assinantes.
    """
    return SubscriberRepository()
