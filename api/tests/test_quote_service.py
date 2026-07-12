"""Testes unitários para o serviço de citações.

Este módulo valida os principais fluxos de criação, leitura, atualização,
remoção e consulta aleatória de citações.
"""

from unittest.mock import AsyncMock

import pytest

from api.core.exceptions.custom_exceptions import (
    DomainValidationException,
    QuoteNotFoundException,
)
from api.models.enums import CategoryQuote
from api.models.quote import Quote
from api.repositories.quote_repository import QuoteRepository
from api.schemas.quote_schema import CreateQuoteRequest, UpdateQuoteRequest
from api.services.quote_service import QuoteService


@pytest.fixture
def service() -> QuoteService:
    """Cria uma instância do serviço de citações para os testes."""
    return QuoteService()


@pytest.fixture
def mock_repo() -> AsyncMock:
    """Cria um mock assíncrono do repositório de citações."""
    return AsyncMock(spec=QuoteRepository)


@pytest.fixture
def valid_request_data() -> CreateQuoteRequest:
    """Retorna um payload válido para criação de citação."""
    return CreateQuoteRequest(
        content="Investir é sobre ter paciência.",
        author="Warren Buffett",
        tags=[CategoryQuote.INVESTIMENTOS, CategoryQuote.EDUCACAO],
        source="Book of Finances",
        verified=True,
    )


@pytest.fixture
def quote(valid_request_data):
    """Constrói uma citação mock a partir dos dados válidos."""
    return Quote.model_construct(
        content=valid_request_data.content,
        author=valid_request_data.author,
        tags=valid_request_data.tags,
        source=valid_request_data.source,
        verified=valid_request_data.verified,
    )


class TestCreateQuote:
    """Testes do método de criação de citações."""

    @pytest.mark.asyncio
    async def test_create_quote_success(
        self, service, mock_repo, valid_request_data, quote
    ):
        """Verifica a criação de citação quando não há conflito."""

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
        """Verifica a validação quando a citação já existe."""
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
    """Testes do método de listagem de citações."""

    @pytest.mark.asyncio
    async def test_get_all_success(self, service, mock_repo, quote):
        """Verifica a listagem com filtro e paginação."""
        other_quote = Quote.model_construct(
            content="Outra frase.",
            author="Outro Autor",
            tags=[CategoryQuote.INVESTIMENTOS],
            source="Outra Fonte",
            verified=True,
        )

        mock_repo.get_all.return_value = ([quote, other_quote], 2)

        result, total, pages = await service.get_all(
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
        assert pages == 1

        mock_repo.get_all.assert_awaited_once_with({"verified": True}, 10, 0)


class TestGetTodayQuote:
    """Testes do método de citação do dia."""

    @pytest.mark.asyncio
    async def test_get_today_quote_success(self, service, mock_repo, quote):
        """Verifica o retorno de uma citação verificada."""
        mock_repo.get_random_quote.return_value = [quote]

        result = await service.get_today_quote(repo=mock_repo)

        assert result == [quote]

        mock_repo.get_random_quote.assert_awaited_once_with(size=1)

    @pytest.mark.asyncio
    async def test_get_today_quote_empty(self, service, mock_repo):
        """Verifica a exceção quando não existe citação verificada."""
        mock_repo.get_random_quote.return_value = []

        expected_message = "Nenhuma citação verificada encontrada"

        with pytest.raises(QuoteNotFoundException) as exc_info:
            await service.get_today_quote(repo=mock_repo)

        assert str(exc_info.value) == expected_message

        mock_repo.get_random_quote.assert_awaited_once_with(size=1)


class TestGetRandomQuote:
    """Testes do método de busca aleatória de citações."""

    @pytest.mark.asyncio
    async def test_get_random_quote_success(self, service, mock_repo, quote):
        """Verifica o retorno de citações aleatórias."""
        mock_repo.get_random_quote.return_value = [quote]

        result = await service.get_random_quote(size=1, repo=mock_repo)

        assert result == [quote]

        mock_repo.get_random_quote.assert_awaited_once_with(size=1)

    @pytest.mark.asyncio
    async def test_get_random_quote_empty(self, service, mock_repo):
        """Verifica o retorno vazio quando não há resultados."""
        mock_repo.get_random_quote.return_value = []

        result = await service.get_random_quote(size=1, repo=mock_repo)

        assert result == []

        mock_repo.get_random_quote.assert_awaited_once_with(size=1)


class TestDeleteQuoteById:
    """Testes do método de exclusão de citações por ID."""

    @pytest.mark.asyncio
    async def test_delete_quote_by_id_success(self, service, mock_repo, quote):
        """Verifica a exclusão quando a citação existe."""
        quote_id = "64b8f0c2e1d2f5a1b2c3d4e"
        mock_repo.get_quote_by_id.return_value = quote

        await service.delete_quote_by_id(id=quote_id, repo=mock_repo)

        mock_repo.get_quote_by_id.assert_awaited_once_with(quote_id)
        mock_repo.delete_quote_by_id.assert_awaited_once_with(quote_id)

    @pytest.mark.asyncio
    async def test_delete_quote_by_id_not_found(self, service, mock_repo):
        """Verifica a exceção quando a citação não é encontrada."""
        quote_id = "64b8f0c2e1d2f5a1b2c3d4e"
        expected_message = f"Citação com id '{quote_id}' não encontrada"

        mock_repo.get_quote_by_id.return_value = None

        with pytest.raises(QuoteNotFoundException) as exc_info:
            await service.delete_quote_by_id(id=quote_id, repo=mock_repo)

        assert str(exc_info.value) == expected_message

        mock_repo.get_quote_by_id.assert_awaited_once_with(quote_id)
        mock_repo.delete_quote_by_id.assert_not_awaited()


class TestGetQuoteById:
    """Testes do método de consulta de citação por ID."""

    @pytest.mark.asyncio
    async def test_get_quote_by_id_success(self, service, mock_repo, quote):
        """Verifica o retorno de uma citação existente."""
        quote_id = "64b8f0c2e1d2f5a1b2c3d4e"
        mock_repo.get_quote_by_id.return_value = quote

        result = await service.get_quote_by_id(id=quote_id, repo=mock_repo)

        assert result == quote

        mock_repo.get_quote_by_id.assert_awaited_once_with(quote_id)

    @pytest.mark.asyncio
    async def test_get_quote_by_id_not_found(self, service, mock_repo):
        """Verifica a exceção quando o ID não existe."""
        quote_id = "64b8f0c2e1d2f5a1b2c3d4e"
        expected_message = f"Citação com id '{quote_id}' não encontrada"

        mock_repo.get_quote_by_id.return_value = None

        with pytest.raises(QuoteNotFoundException) as exc_info:
            await service.get_quote_by_id(id=quote_id, repo=mock_repo)

        assert str(exc_info.value) == expected_message

        mock_repo.get_quote_by_id.assert_awaited_once_with(quote_id)


class TestUpdateQuoteById:
    """Testes do método de atualização de citações por ID."""

    @pytest.fixture
    def update_request_data(self) -> UpdateQuoteRequest:
        """Retorna um payload válido para atualização de citação."""
        return UpdateQuoteRequest(
            content="O preço é o que você paga. O valor é o que você leva.",
            author="Warren Buffett",
            tags=[CategoryQuote.INVESTIMENTOS],
        )

    @pytest.mark.asyncio
    async def test_update_quote_by_id_success(
        self, service, mock_repo, quote, update_request_data
    ):
        """Verifica a atualização quando não há conflito de dados."""
        quote_id = "64b8f0c2e1d2f5a1b2c3d4e"

        quote.id = quote_id

        mock_repo.get_quote_by_id.return_value = quote

        mock_repo.get_quote_by_content_and_author.return_value = None

        updated_quote = Quote.model_construct(
            id=quote_id,
            content=update_request_data.content,
            author=update_request_data.author,
            tags=update_request_data.tags,
            source=quote.source,
            verified=quote.verified,
        )
        mock_repo.update_quote.return_value = updated_quote

        result = await service.update_quote_by_id(
            id=quote_id, quote_data=update_request_data, repo=mock_repo
        )

        assert result.id == quote_id
        assert result.content == update_request_data.content
        assert result.author == update_request_data.author
        assert result.tags == update_request_data.tags

        mock_repo.get_quote_by_id.assert_awaited_once_with(quote_id)
        mock_repo.get_quote_by_content_and_author.assert_awaited_once_with(
            update_request_data.content, update_request_data.author
        )

        mock_repo.update_quote.assert_awaited_once()
        called_args = mock_repo.update_quote.await_args[0]
        assert called_args[0] == quote_id
        assert "updated_at" in called_args[1]
        assert called_args[1]["content"] == update_request_data.content

    @pytest.mark.asyncio
    async def test_update_quote_by_id_not_found(
        self, service, mock_repo, update_request_data
    ):
        """Verifica a exceção quando a citação não existe."""
        quote_id = "invalid_id_123"
        expected_message = f"Citação com id '{quote_id}' não encontrada"

        mock_repo.get_quote_by_id.return_value = None

        with pytest.raises(QuoteNotFoundException) as exc_info:
            await service.update_quote_by_id(
                id=quote_id, quote_data=update_request_data, repo=mock_repo
            )

        assert str(exc_info.value) == expected_message

        mock_repo.get_quote_by_id.assert_awaited_once_with(quote_id)
        mock_repo.get_quote_by_content_and_author.assert_not_awaited()
        mock_repo.update_quote.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_update_quote_by_id_conflict_with_another_quote(
        self, service, mock_repo, quote, update_request_data
    ):
        """Verifica o conflito com outra citação já existente."""
        quote_id = "64b8f0c2e1d2f5a1b2c3d4e"
        another_quote_id = "9999f0c2e1d2f5a1b2c3d4e"

        quote.id = quote_id
        expected_message = f"A frase '{update_request_data.content}' do autor '{update_request_data.author}' já existe"

        mock_repo.get_quote_by_id.return_value = quote

        conflicting_quote = Quote.model_construct(
            id=another_quote_id,
            content=update_request_data.content,
            author=update_request_data.author,
        )
        mock_repo.get_quote_by_content_and_author.return_value = conflicting_quote

        with pytest.raises(DomainValidationException) as exc_info:
            await service.update_quote_by_id(
                id=quote_id, quote_data=update_request_data, repo=mock_repo
            )

        assert str(exc_info.value) == expected_message

        mock_repo.get_quote_by_id.assert_awaited_once_with(quote_id)
        mock_repo.get_quote_by_content_and_author.assert_awaited_once_with(
            update_request_data.content, update_request_data.author
        )
        mock_repo.update_quote.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_update_quote_by_id_same_quote_identity(
        self, service, mock_repo, quote, update_request_data
    ):
        """Verifica a atualização quando a própria citação é retornada."""
        quote_id = "64b8f0c2e1d2f5a1b2c3d4e"
        quote.id = quote_id

        mock_repo.get_quote_by_id.return_value = quote

        mock_repo.get_quote_by_content_and_author.return_value = quote

        mock_repo.update_quote.return_value = quote

        await service.update_quote_by_id(
            id=quote_id, quote_data=update_request_data, repo=mock_repo
        )

        mock_repo.update_quote.assert_awaited_once()
