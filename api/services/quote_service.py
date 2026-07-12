from datetime import datetime, timezone

from loguru import logger

from api.core.exceptions.custom_exceptions import (
    DomainValidationException,
    QuoteNotFoundException,
)
from api.models.enums import CategoryQuote
from api.models.quote import Quote
from api.repositories.quote_repository import QuoteRepository
from api.schemas.quote_schema import CreateQuoteRequest, UpdateQuoteRequest


class QuoteService:
    """Serviço responsável pelas regras de negócio relacionadas às citações.

    Centraliza operações de criação, consulta, atualização e remoção de
    citações, aplicando validações de domínio antes de delegar a persistência
    ao repositório.
    """

    async def create_quote(
        self, quote: CreateQuoteRequest, repo: QuoteRepository
    ) -> Quote:
        """Cria uma nova citação após validar duplicidade.

        Args:
            quote: Dados da citação a ser criada.
            repo: Repositório responsável pelo acesso aos dados.

        Returns:
            A citação recém-criada.

        Raises:
            DomainValidationException: Se já existir uma citação com o mesmo
                conteúdo e autor.
        """
        logger.info(f"Criando nova citação: {quote}")

        if (
            await repo.get_quote_by_content_and_author(quote.content, quote.author)
            is not None
        ):
            raise DomainValidationException(
                f"A frase '{quote.content}' do autor '{quote.author}' já existe"
            )

        new_quote = await repo.create(quote)

        return new_quote

    async def get_all(
        self,
        author: str | None,
        tags: list[CategoryQuote] | None,
        source: str | None,
        verified: bool,
        limit: int,
        skip: int,
        repo: QuoteRepository,
    ) -> tuple[list[Quote], int, int]:
        """Retorna citações paginadas com base nos filtros informados.

        Args:
            author: Nome do autor para filtragem, quando informado.
            tags: Lista de categorias para filtragem, quando informada.
            source: Fonte da citação para filtragem, quando informada.
            verified: Define se a consulta deve retornar apenas citações
                verificadas.
            limit: Quantidade máxima de itens por página.
            skip: Quantidade de itens a serem ignorados na paginação.
            repo: Repositório responsável pelo acesso aos dados.

        Returns:
            Uma tupla contendo a lista de citações, o total de registros e o
            total de páginas calculado.
        """
        filters = {}
        filters["verified"] = verified

        if author:
            filters["author"] = author
        if source:
            filters["source"] = source
        if tags:
            filters["tags"] = {"$in": tags}

        logger.info(
            f"Obtendo citações com filtros: {filters}, limit: {limit}, skip: {skip}"
        )

        quotes = await repo.get_all(filters, limit, skip)

        quotes, total_counts = quotes

        return quotes, total_counts, (total_counts + limit - 1) // limit

    async def get_quote_by_id(self, id: str, repo: QuoteRepository) -> Quote:
        """Busca uma citação pelo identificador.

        Args:
            id: Identificador da citação.
            repo: Repositório responsável pelo acesso aos dados.

        Returns:
            A citação encontrada.

        Raises:
            QuoteNotFoundException: Se nenhuma citação for encontrada.
        """
        logger.info(f"Obtendo citação com id: {id}")

        quote = await repo.get_quote_by_id(id)

        if quote is None:
            raise QuoteNotFoundException(f"Citação com id '{id}' não encontrada")
        return quote

    async def get_random_quote(self, size: int, repo: QuoteRepository) -> list[Quote]:
        """Retorna uma lista de citações aleatórias.

        Args:
            size: Quantidade de citações aleatórias desejadas.
            repo: Repositório responsável pelo acesso aos dados.

        Returns:
            Lista de citações aleatórias.
        """
        logger.info(f"Obtendo {size} citações aleatórias.")

        return await repo.get_random_quote(size=size)

    async def get_today_quote(self, repo: QuoteRepository) -> list[Quote]:
        """Retorna a citação do dia.

        A implementação atual obtém uma citação aleatória com tamanho 1 e
        valida se algum resultado foi retornado.

        Args:
            repo: Repositório responsável pelo acesso aos dados.

        Returns:
            Lista contendo uma única citação.

        Raises:
            QuoteNotFoundException: Se nenhuma citação for encontrada.
        """
        logger.info("Obtendo a citação do dia.")
        quote = await self.get_random_quote(size=1, repo=repo)

        if not quote:
            raise QuoteNotFoundException("Nenhuma citação verificada encontrada")

        return quote

    async def update_quote_by_id(
        self, id: str, quote_data: UpdateQuoteRequest, repo: QuoteRepository
    ) -> Quote:
        """Atualiza uma citação existente pelo identificador.

        Antes da atualização, valida se a citação existe e evita duplicidade
        quando conteúdo e autor forem informados simultaneamente.

        Args:
            id: Identificador da citação a ser atualizada.
            quote_data: Dados parciais ou completos para atualização.
            repo: Repositório responsável pelo acesso aos dados.

        Returns:
            A citação atualizada.

        Raises:
            QuoteNotFoundException: Se a citação não existir.
            DomainValidationException: Se já existir outra citação com o mesmo
                conteúdo e autor.
        """
        logger.info(f"Atualizando citação com id: {id}, dados: {quote_data}")

        await self.get_quote_by_id(id, repo)

        if quote_data.author and quote_data.content:
            existing_quote = await repo.get_quote_by_content_and_author(
                quote_data.content, quote_data.author
            )
            if existing_quote and existing_quote.id != id:
                raise DomainValidationException(
                    f"A frase '{quote_data.content}' do autor '{quote_data.author}' já existe"
                )

        quote_data_dict = quote_data.model_dump(exclude_unset=True)
        quote_data_dict["updated_at"] = datetime.now(timezone.utc)

        return await repo.update_quote(id, quote_data_dict)

    async def delete_quote_by_id(self, id: str, repo: QuoteRepository) -> None:
        """Remove uma citação existente pelo identificador.

        Antes da remoção, valida se a citação existe.

        Args:
            id: Identificador da citação a ser removida.
            repo: Repositório responsável pelo acesso aos dados.

        Raises:
            QuoteNotFoundException: Se a citação não existir.
        """
        logger.info(f"Deletando citação com id: {id}")

        await self.get_quote_by_id(id, repo)

        await repo.delete_quote_by_id(id)
