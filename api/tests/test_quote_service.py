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


@pytest.fixture
def valid_request_data():
    return CreateQuoteRequest(
        content="Investir é sobre ter paciência.",
        author="Warren Buffett",
        tags=[CategoryQuote.INVESTIMENTOS, CategoryQuote.EDUCACAO],
        source="Book of Finances",
        verified=True,
    )


class TestCreateQuote:
    @pytest.mark.asyncio
    async def test_create_quote_sucess(self, service, mock_repo, valid_request_data):
        quote = Quote.model_construct(
            content=valid_request_data.content,
            author=valid_request_data.author,
            tags=valid_request_data.tags,
            source=valid_request_data.source,
            verified=valid_request_data.verified,
        )

        mock_repo.create.return_value = quote

        result = await service.create_quote(quote=valid_request_data, repo=mock_repo)

        assert result.content == valid_request_data.content
        assert result.author == valid_request_data.author
        assert result.tags == valid_request_data.tags
        assert result.source == valid_request_data.source
        assert result.verified == valid_request_data.verified

        mock_repo.create.assert_called_once_with(valid_request_data)
