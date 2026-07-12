"""Módulo de configuração e gerenciamento de conexão com banco de dados MongoDB.

Este módulo é responsável por inicializar e gerenciar a conexão com o banco de dados
MongoDB utilizando o cliente assíncrono do PyMongo e o Beanie para mapeamento de objetos.
"""

from beanie import init_beanie
from pymongo import AsyncMongoClient

from api.core.config import settings
from api.models.quote import Quote

client: AsyncMongoClient | None = None


async def get_db():
    """Obtém a instância do banco de dados MongoDB.

    Estabelece uma conexão com o MongoDB na primeira chamada e retorna
    uma referência ao banco de dados 'finfrases'. Nas chamadas subsequentes,
    reutiliza a conexão já estabelecida.

    Returns:
        Database: Uma instância do banco de dados MongoDB 'finfrases'.

    Raises:
        ConnectionFailure: Se não conseguir conectar ao servidor MongoDB.
    """
    global client

    if client is None:
        client = AsyncMongoClient(settings.MONGO_URI)

    return client["finfrases"]


async def init_db():
    """Inicializa o banco de dados com os modelos de documentos.

    Realiza a conexão com o banco de dados e registra os modelos de documentos
    com o Beanie, permitindo o mapeamento objeto-documento para as entidades
    definidas.

    Returns:
        None

    Raises:
        ConnectionFailure: Se não conseguir conectar ao servidor MongoDB.
        OperationalError: Se houver erros durante a inicialização do Beanie.
    """
    db = await get_db()
    await init_beanie(database=db, document_models=[Quote])
