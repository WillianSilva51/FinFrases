from unittest.mock import AsyncMock

import pytest
from api.models.enums import CategoryQuote
from api.models.quote import Quote
from api.repositories.quote_repository import QuoteRepository
from api.schemas.quote_schema import CreateQuoteRequest
from api.services.quote_service import QuoteService
from api.core.exceptions.custom_exceptions import (
    DomainValidationException,
)


@pytest.fixture
def service() -> QuoteService:
    return QuoteService()


@pytest.fixture
def mock_repo() -> AsyncMock:
    return AsyncMock(spec=QuoteRepository)


@pytest.fixture
def valid_request_data() -> CreateQuoteRequest:
    return CreateQuoteRequest(
        content="Investir é sobre ter paciência.",
        author="Warren Buffett",
        tags=[CategoryQuote.INVESTIMENTOS, CategoryQuote.EDUCACAO],
        source="Book of Finances",
        verified=True,
    )


@pytest.fixture
def quote(valid_request_data):
    return Quote.model_construct(
        content=valid_request_data.content,
        author=valid_request_data.author,
        tags=valid_request_data.tags,
        source=valid_request_data.source,
        verified=valid_request_data.verified,
    )


class TestCreateQuote:
    @pytest.mark.asyncio
    async def test_create_quote_success(
        self, service, mock_repo, valid_request_data, quote
    ):

        mock_repo.get_quote_by_content_and_author.return_value = None
        mock_repo.create.return_value = quote

        result = await service.create_quote(quote=valid_request_data, repo=mock_repo)

        assert result.content == valid_request_data.content
        assert result.author == valid_request_data.author
        assert result.tags == valid_request_data.tags
        assert result.source == valid_request_data.source
        assert result.verified == valid_request_data.verified

        mock_repo.get_quote_by_content_and_author.assert_awaited_once_with(
            valid_request_data.content, valid_request_data.author
        )
        mock_repo.create.assert_awaited_once_with(valid_request_data)

    @pytest.mark.asyncio
    async def test_create_quote_failure(self, service, mock_repo, valid_request_data):
        expected_message = f"A frase '{valid_request_data.content}' do autor '{valid_request_data.author}' já existe"

        mock_repo.get_quote_by_content_and_author.return_value = Quote.model_construct(
            content=valid_request_data.content,
            author=valid_request_data.author,
            tags=valid_request_data.tags,
            source=valid_request_data.source,
            verified=valid_request_data.verified,
        )

        with pytest.raises(DomainValidationException) as exc_info:
            await service.create_quote(quote=valid_request_data, repo=mock_repo)

        assert str(exc_info.value) == expected_message

        mock_repo.get_quote_by_content_and_author.assert_awaited_once_with(
            valid_request_data.content, valid_request_data.author
        )
        mock_repo.create.assert_not_awaited()


class TestGetAllQuotes:
    @pytest.mark.asyncio
    async def test_get_all_success(self, service, mock_repo):
        pass
