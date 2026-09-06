from beanie import PydanticObjectId

from api.core.cache import RedisCache
from api.models.quote import Quote
from api.schemas.quote_schema import CreateQuoteRequest

cache = RedisCache()


class QuoteRepository:
    """Repositório responsável pelas operações de persistência de citações.

    Esta classe encapsula as operações de criação, consulta, atualização,
    exclusão e obtenção de citações aleatórias no banco de dados, mantendo a
    camada de acesso a dados isolada da regra de negócio.
    """

    async def create(self, quote_data: CreateQuoteRequest) -> Quote:
        """Cria e persiste uma nova citação no banco de dados.

        Args:
            quote_data: Dados de entrada validados para criação da citação.

        Returns:
            A instância de ``Quote`` já inserida no banco de dados.
        """
        new_quote = Quote.model_validate(quote_data.model_dump())

        return await new_quote.insert()

    async def get_all(
        self, params: dict, limit: int, skip: int
    ) -> tuple[list[Quote], int]:
        """Retorna uma lista paginada de citações e a quantidade total.

        Args:
            params: Filtros aplicados à consulta.
            limit: Quantidade máxima de registros retornados.
            skip: Quantidade de registros ignorados para paginação.

        Returns:
            Uma tupla contendo a lista de citações encontradas e o total de
            registros que atendem aos filtros informados.
        """
        total_count = await Quote.find(params).count()

        quotes = Quote.find(params).limit(limit).skip(skip)

        return await quotes.to_list(), total_count

    async def get_random_quote(self, size: int) -> list[Quote]:
        """Retorna uma lista de citações verificadas selecionadas aleatoriamente.

        Args:
            size: Quantidade de citações aleatórias desejadas.

        Returns:
            Uma lista de citações convertidas para o modelo ``Quote``.
        """
        agregation = [
            {"$match": {"verified": True}},
            {"$sample": {"size": size}},
        ]
        result = await Quote.aggregate(agregation).to_list()

        return [Quote.model_validate(doc) for doc in result]

    async def get_quote_by_content_and_author(
        self, content: str, author: str
    ) -> Quote | None:
        """Busca uma citação pelo conteúdo e autor.

        Args:
            content: Texto da citação.
            author: Nome do autor da citação.

        Returns:
            A citação encontrada ou ``None`` caso não exista correspondência.
        """
        return await Quote.find_one({"content": content, "author": author})

    async def get_quote_by_id(self, id: str) -> Quote | None:
        """Busca uma citação pelo identificador único.

        Args:
            id: Identificador da citação no formato de string.

        Returns:
            A citação correspondente ao identificador ou ``None`` se não for
            encontrada.
        """
        return await Quote.get(PydanticObjectId(id))

    async def update_quote(self, id: str, quote_data: dict) -> Quote:
        """Atualiza uma citação existente e invalida o cache relacionado.

        Args:
            id: Identificador da citação a ser atualizada.
            quote_data: Dados que serão aplicados na atualização.

        Returns:
            A citação atualizada.
        """
        quote = await Quote.get(PydanticObjectId(id))

        update_query = {"$set": quote_data}
        quote = await quote.update(update_query)

        await cache.delete(id)

        return quote

    async def delete_quote_by_id(self, id: str) -> None:
        """Remove uma citação pelo identificador.

        Args:
            id: Identificador da citação a ser removida.

        Returns:
            ``None``.
        """
        await Quote.find_one({"_id": PydanticObjectId(id)}).delete()
