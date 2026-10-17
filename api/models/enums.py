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


class SortOrder(str, Enum):
    ASCENDING = "asc"
    DESCENDING = "desc"

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            for order in cls:
                if order.value.lower() == value.lower():
                    return order

        return cls.ASCENDING


class QuoteOrderBy(str, Enum):
    CONTENT = "content"
    AUTHOR = "author"
    TAGS = "tags"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            for order_by in cls:
                if order_by.value.lower() == value.lower():
                    return order_by

        return cls.CREATED_AT
