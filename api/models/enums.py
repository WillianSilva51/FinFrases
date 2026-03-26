from enum import Enum


class CategoryQuote(str, Enum):
    GERAL = "GERAL"
    INVESTIMENTOS = "INVESTIMENTOS"
    POUPANCA = "POUPANCA"
    PSICOLOGIA = "PSICOLOGIA"
    DIVIDENDOS = "DIVIDENDOS"
    EDUCACAO = "EDUCACAO"
    EMPREENDEDORISMO = "EMPREENDEDORISMO"
    ACAO = "ACAO"
    FIIS = "FIIS"

    @classmethod
    def _missing_(cls, value):
        return cls.GERAL
