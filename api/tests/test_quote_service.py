from unittest.mock import AsyncMock

import pytest
from models.enums import CategoryQuote
from models.quote import Quote
from repositories.quote_repository import QuoteRepository
from schemas.quote_schema import CreateQuoteRequest
from services.quote_service import QuoteService


@pytest.fixture
def service():
    return QuoteService()


@pytest.fixture
def mock_repo():
    return AsyncMock(spec=QuoteRepository)


@pytest.mark.asyncio
async def test_create_quote_sucess(service, mock_repo):
    request_data = CreateQuoteRequest(
        content="Investir é sobre ter paciência.",
        author="Warren Buffett",
        tags=[CategoryQuote.INVESTIMENTOS, CategoryQuote.EDUCACAO],
        source="Book of Finances",
        verified=True,
    )

    quote = Quote.model_construct(
        content=request_data.content,
        author=request_data.author,
        tags=request_data.tags,
        source=request_data.source,
        verified=request_data.verified,
    )

    mock_repo.create.return_value = quote

    result = await service.create_quote(quote=request_data, repo=mock_repo)

    assert result.content == request_data.content
    assert result.author == request_data.author
    assert result.tags == request_data.tags
    assert result.source == request_data.source
    assert result.verified == request_data.verified

    mock_repo.create.assert_called_once_with(request_data)
