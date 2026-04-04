from unittest.mock import AsyncMock

import pytest
from api.models.enums import CategoryQuote
from api.models.quote import Quote
from api.repositories.quote_repository import QuoteRepository
from api.schemas.quote_schema import CreateQuoteRequest
from api.services.quote_service import QuoteService
from api.core.exceptions.custom_exceptions import (
    DomainValidationException,
    ResourceNotFoundException,
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
    async def test_get_all_success(self, service, mock_repo, quote):
        other_quote = Quote.model_construct(
            content="Outra frase.",
            author="Outro Autor",
            tags=[CategoryQuote.INVESTIMENTOS],
            source="Outra Fonte",
            verified=True,
        )

        mock_repo.get_all.return_value = ([quote, other_quote], 2)

        result, total = await service.get_all(
            author=None,
            tags=None,
            source=None,
            verified=True,
            limit=10,
            skip=0,
            repo=mock_repo,
        )

        assert result == [quote, other_quote]
        assert total == 2

        mock_repo.get_all.assert_awaited_once_with({"verified": True}, 10, 0)


class TestGetTodayQuote:
    @pytest.mark.asyncio
    async def test_get_today_quote_success(self, service, mock_repo, quote):
        mock_repo.get_random_quote.return_value = [quote]

        result = await service.get_today_quote(repo=mock_repo)

        assert result == [quote]

        mock_repo.get_random_quote.assert_awaited_once_with(size=1)

    @pytest.mark.asyncio
    async def test_get_today_quote_empty(self, service, mock_repo):
        mock_repo.get_random_quote.return_value = []

        expected_message = "Nenhuma citação verificada encontrada"

        with pytest.raises(ResourceNotFoundException) as exc_info:
            await service.get_today_quote(repo=mock_repo)

        assert str(exc_info.value) == expected_message

        mock_repo.get_random_quote.assert_awaited_once_with(size=1)


class TestGetRandomQuote:
    @pytest.mark.asyncio
    async def test_get_random_quote_success(self, service, mock_repo, quote):
        mock_repo.get_random_quote.return_value = [quote]

        result = await service.get_random_quote(size=1, repo=mock_repo)

        assert result == [quote]

        mock_repo.get_random_quote.assert_awaited_once_with(size=1)

    @pytest.mark.asyncio
    async def test_get_random_quote_empty(self, service, mock_repo):
        mock_repo.get_random_quote.return_value = []

        result = await service.get_random_quote(size=1, repo=mock_repo)

        assert result == []

        mock_repo.get_random_quote.assert_awaited_once_with(size=1)


class TestDeleteQuoteById:
    @pytest.mark.asyncio
    async def test_delete_quote_by_id_success(self, service, mock_repo, quote):
        quote_id = "64b8f0c2e1d2f5a1b2c3d4e"
        mock_repo.get_quote_by_id.return_value = quote

        await service.delete_quote_by_id(id=quote_id, repo=mock_repo)

        mock_repo.get_quote_by_id.assert_awaited_once_with(quote_id)
        mock_repo.delete_quote_by_id.assert_awaited_once_with(quote_id)

    @pytest.mark.asyncio
    async def test_delete_quote_by_id_not_found(self, service, mock_repo):
        quote_id = "64b8f0c2e1d2f5a1b2c3d4e"
        expected_message = f"Citação com id '{quote_id}' não encontrada"

        mock_repo.get_quote_by_id.return_value = None

        with pytest.raises(ResourceNotFoundException) as exc_info:
            await service.delete_quote_by_id(id=quote_id, repo=mock_repo)

        assert str(exc_info.value) == expected_message

        mock_repo.get_quote_by_id.assert_awaited_once_with(quote_id)
        mock_repo.delete_quote_by_id.assert_not_awaited()


class TestGetQuoteById:
    @pytest.mark.asyncio
    async def test_get_quote_by_id_success(self, service, mock_repo, quote):
        quote_id = "64b8f0c2e1d2f5a1b2c3d4e"
        mock_repo.get_quote_by_id.return_value = quote

        result = await service.get_quote_by_id(id=quote_id, repo=mock_repo)

        assert result == quote

        mock_repo.get_quote_by_id.assert_awaited_once_with(quote_id)

    @pytest.mark.asyncio
    async def test_get_quote_by_id_not_found(self, service, mock_repo):
        quote_id = "64b8f0c2e1d2f5a1b2c3d4e"
        expected_message = f"Citação com id '{quote_id}' não encontrada"

        mock_repo.get_quote_by_id.return_value = None

        with pytest.raises(ResourceNotFoundException) as exc_info:
            await service.get_quote_by_id(id=quote_id, repo=mock_repo)

        assert str(exc_info.value) == expected_message

        mock_repo.get_quote_by_id.assert_awaited_once_with(quote_id)


class TestUpdateQuoteById:
    pass
