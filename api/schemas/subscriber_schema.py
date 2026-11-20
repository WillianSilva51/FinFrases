from typing import Annotated

from pydantic import BaseModel, EmailStr, Field


class CreateSubscriberRequest(BaseModel):
    name: Annotated[
        str,
        Field(
            title="Nome",
            description="O nome do assinante",
            examples=["João da Silva"],
            max_length=100,
        ),
    ]
    email: Annotated[
        EmailStr,
        Field(
            title="E-mail",
            description="O e-mail do assinante",
            examples=["joao@example.com"],
        ),
    ]


class UpdateSubscriberRequest(CreateSubscriberRequest):
    pass


class UnsubscribeSubscriberRequest(BaseModel):
    unsubscribe_token: Annotated[
        str,
        Field(
            title="Token de cancelamento de inscrição",
            description="O token de cancelamento de inscrição do assinante",
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
    token: Annotated[
        str,
        Field(
            title="Token de cancelamento de inscrição",
            description="O token de cancelamento de inscrição do assinante",
            examples=["1234567890abcdef"],
        ),
    ]
