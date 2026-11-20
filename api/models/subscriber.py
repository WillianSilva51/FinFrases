from datetime import UTC, datetime
from secrets import token_urlsafe
from typing import Annotated

from beanie import Document, Indexed
from pydantic import EmailStr, Field

from api.models.enums import SubscriberStatus


class Subscriber(Document):
    name: Annotated[str, Field(max_length=100)]
    email: Annotated[EmailStr, Indexed(unique=True, name="uq_subscriber_email")]
    status: Annotated[SubscriberStatus, Indexed(name="idx_status_subscriber")] = Field(
        default=SubscriberStatus.ACTIVE
    )
    unsubscribe_token: Annotated[
        str,
        Indexed(unique=True, name="uq_subscriber_unsubscribe_token"),
    ] = Field(default_factory=token_urlsafe)
    created_at: Annotated[datetime, Field(default_factory=lambda: datetime.now(UTC))]
    updated_at: datetime | None = None
    unsubscribed_at: Annotated[
        datetime | None,
        Indexed(expireAfterSeconds=2592000, name="idx_unsubscribed_at_ttl"),
    ] = None

    class Settings:
        name = "subscribers"
