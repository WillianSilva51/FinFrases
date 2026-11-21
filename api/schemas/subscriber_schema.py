from typing import Annotated

from pydantic import BaseModel, EmailStr, Field

from api.models.enums import SubscriberStatus


class CreateSubscriberRequest(BaseModel):
    email: Annotated[
        EmailStr,
        Field(
            title="E-mail",
            description="O e-mail do assinante",
            examples=["joao@example.com"],
        ),
    ]


class UnsubscribeSubscriberRequest(BaseModel):
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


class SubscriberResponse(BaseModel):
    email: Annotated[
        EmailStr,
        Field(
            title="E-mail",
            description="O e-mail do assinante",
            examples=["joao@example.com"],
        ),
    ]
    status: Annotated[
        SubscriberStatus,
        Field(
            title="Status do assinante",
            description="O status atual do assinante",
            examples=[SubscriberStatus.ACTIVE.value],
        ),
    ] = SubscriberStatus.ACTIVE


class UnsubscribeResponse(BaseModel):
    message: Annotated[
        str,
        Field(
            title="Mensagem de sucesso",
            description="Mensagem indicando que o assinante foi removido com sucesso",
            examples=["Assinante removido com sucesso."],
        ),
    ]
    status: Annotated[
        SubscriberStatus,
        Field(
            title="Status da operação",
            description="Status indicando que a operação foi bem-sucedida",
            examples=[SubscriberStatus.UNSUBSCRIBED.value],
        ),
    ] = SubscriberStatus.UNSUBSCRIBED
    masked_email: Annotated[
        str | None,
        Field(
            title="E-mail mascarado",
            description="O e-mail do assinante com parte do endereço mascarada",
            examples=["j***@example.com"],
        ),
    ]
