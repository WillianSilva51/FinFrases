from enum import Enum


class CategoryQuote(str, Enum):
    GERAL = "geral"
    INVESTIMENTOS = "investimentos"
    POUPANCA = "poupanca"
    PSICOLOGIA = "psicologia"
    DIVIDENDOS = "dividendos"
    EDUCACAO = "educacao"
    EMPREENDEDORISMO = "empreendedorismo"
    ACAO = "acao"
    FIIS = "fiis"

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            for category in cls:
                if category.value.lower() == value.lower():
                    return category

        return cls.GERAL
