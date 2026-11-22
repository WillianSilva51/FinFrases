from typing import Annotated

from pydantic import BaseModel, EmailStr, Field

from api.schemas.quote_schema import QuoteResponse


class EmailEventSchema(BaseModel):
    recipient_name: Annotated[
        str | None,
        Field(
            title="Nome do destinatário",
            description="O nome do destinatário",
            examples=["João"],
            max_length=50,
        ),
    ] = None
    recipient_email: Annotated[
        EmailStr,
        Field(
            title="E-mail do destinatário",
            description="O e-mail do destinatário",
            examples=["joao@example.com"],
        ),
    ]
    unsubscribe_token: Annotated[
        str,
        Field(
            title="Token de cancelamento de inscrição",
            description="O token de cancelamento de inscrição do assinante",
            min_length=16,
            max_length=128,
            examples=["1234567890abcdef"],
        ),
    ]


class WelcomeEmail(EmailEventSchema):
    pass


class DailyEmail(EmailEventSchema):
    quote: Annotated[
        QuoteResponse,
        Field(
            title="Citação do dia",
            description="A citação do dia a ser enviada no e-mail",
        ),
    ]
