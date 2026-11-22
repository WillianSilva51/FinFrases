from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, Mock

import pytest

from api.core.exceptions.custom_exceptions import (
    SubscriberAlreadyExistsException,
    SubscriberNotFoundException,
    UnsubscriberAlreadyUnsubscribedException,
)
from api.models.enums import SubscriberStatus
from api.models.subscriber import Subscriber
from api.repositories.subscriber_repository import SubscriberRepository
from api.schemas.subscriber_schema import (
    CreateSubscriberRequest,
    UnsubscribeSubscriberRequest,
)
from api.services.email.send_welcome_email import SendWelcomeEmail
from api.services.subscriber_service import SubscriberService


@pytest.fixture
def service(
    mock_repo: AsyncMock,
    mock_send_welcome_email: AsyncMock,
) -> SubscriberService:
    return SubscriberService(mock_repo, mock_send_welcome_email)


@pytest.fixture
def mock_send_welcome_email() -> AsyncMock:
    return AsyncMock(spec=SendWelcomeEmail)


@pytest.fixture
def mock_repo() -> AsyncMock:
    return AsyncMock(spec=SubscriberRepository)


@pytest.fixture
def mock_token_generator() -> Mock:
    return Mock(spec=Callable[[int], str])


@pytest.fixture
def valid_subscriber_request() -> CreateSubscriberRequest:
    return CreateSubscriberRequest(
        email="joao@example.com",
    )


@pytest.fixture
def subscriber(valid_subscriber_request) -> Subscriber:
    return Subscriber.model_construct(
        email=valid_subscriber_request.email,
        status=SubscriberStatus.ACTIVE,
    )


class TestCreateSubscriber:
    @pytest.mark.asyncio
    async def test_create_subscriber_success(
        self,
        service: SubscriberService,
        mock_repo: AsyncMock,
        mock_send_welcome_email: AsyncMock,
        mock_token_generator: Mock,
        subscriber: Subscriber,
        valid_subscriber_request: CreateSubscriberRequest,
    ):
        mock_repo.get_subscriber_by_email.return_value = None

        mock_repo.create_subscriber.return_value = subscriber

        mock_send_welcome_email.execute.return_value = None

        response = await service.create_subscriber(
            valid_subscriber_request, mock_token_generator
        )

        mock_repo.get_subscriber_by_email.assert_called_once_with(
            valid_subscriber_request.email
        )
        mock_repo.create_subscriber.assert_called_once_with(valid_subscriber_request)
        mock_send_welcome_email.execute.assert_called_once_with(subscriber)

        assert response.email == subscriber.email
        assert response.status == subscriber.status
        assert response.unsubscribe_token == subscriber.unsubscribe_token

    @pytest.mark.asyncio
    async def test_create_subscriber_already_exists(
        self,
        service: SubscriberService,
        mock_repo: AsyncMock,
        mock_token_generator: Mock,
        subscriber: Subscriber,
        valid_subscriber_request: CreateSubscriberRequest,
    ):
        mock_repo.get_subscriber_by_email.return_value = subscriber

        with pytest.raises(SubscriberAlreadyExistsException) as exc_info:
            await service.create_subscriber(
                valid_subscriber_request,
                mock_token_generator,
            )

        assert str(exc_info.value) == "Assinante com este e-mail já existe."

        mock_repo.get_subscriber_by_email.assert_called_once_with(
            valid_subscriber_request.email
        )

        mock_repo.create_subscriber.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_create_subscriber_reactivate(
        self,
        service: SubscriberService,
        mock_send_welcome_email: AsyncMock,
        mock_repo: AsyncMock,
        mock_token_generator: Mock,
        subscriber: Subscriber,
        valid_subscriber_request: CreateSubscriberRequest,
    ):
        subscriber.status = SubscriberStatus.UNSUBSCRIBED
        subscriber.created_at = datetime.now(UTC) - timedelta(days=2)

        mock_repo.get_subscriber_by_email.return_value = subscriber

        new_unsubscribe_token = "new_token_with_32_characters_length"
        mock_token_generator.return_value = new_unsubscribe_token

        reactivated_subscriber = Subscriber.model_construct(
            name=subscriber.name,
            email=subscriber.email,
            status=SubscriberStatus.ACTIVE,
            unsubscribe_token=new_unsubscribe_token,
            created_at=subscriber.created_at,
        )

        mock_repo.reactivate_subscriber.return_value = reactivated_subscriber

        mock_send_welcome_email.execute.return_value = None

        response = await service.create_subscriber(
            valid_subscriber_request,
            mock_token_generator,
        )

        mock_token_generator.assert_called_once_with(32)
        mock_repo.get_subscriber_by_email.assert_called_once_with(
            valid_subscriber_request.email
        )
        mock_repo.reactivate_subscriber.assert_called_once_with(
            subscriber, new_unsubscribe_token
        )
        mock_send_welcome_email.execute.assert_called_once_with(reactivated_subscriber)
        mock_repo.create_subscriber.assert_not_awaited()

        assert response.email == subscriber.email
        assert response.status == SubscriberStatus.ACTIVE
        assert response.unsubscribe_token == new_unsubscribe_token
        assert response.unsubscribed_at is None

    @pytest.mark.asyncio
    async def test_create_subscriber_reactivate_without_welcome_email(
        self,
        service: SubscriberService,
        mock_send_welcome_email: AsyncMock,
        mock_repo: AsyncMock,
        mock_token_generator: Mock,
        subscriber: Subscriber,
        valid_subscriber_request: CreateSubscriberRequest,
    ):
        subscriber.status = SubscriberStatus.UNSUBSCRIBED
        subscriber.created_at = datetime.now(UTC) - timedelta(hours=12)

        mock_repo.get_subscriber_by_email.return_value = subscriber

        new_unsubscribe_token = "new_token_with_32_characters_length"
        mock_token_generator.return_value = new_unsubscribe_token

        reactivated_subscriber = Subscriber.model_construct(
            name=subscriber.name,
            email=subscriber.email,
            status=SubscriberStatus.ACTIVE,
            unsubscribe_token=new_unsubscribe_token,
            created_at=subscriber.created_at,
        )

        mock_repo.reactivate_subscriber.return_value = reactivated_subscriber

        # Simulate that the welcome email is not sent
        mock_send_welcome_email.execute.return_value = None

        await service.create_subscriber(
            valid_subscriber_request,
            mock_token_generator,
        )

        mock_token_generator.assert_called_once_with(32)
        mock_repo.get_subscriber_by_email.assert_called_once_with(
            valid_subscriber_request.email
        )
        mock_repo.reactivate_subscriber.assert_called_once_with(
            subscriber, new_unsubscribe_token
        )
        mock_send_welcome_email.execute.assert_not_called()


class TestUnsubscribeSubscriber:
    @pytest.fixture
    def unsubscriber(self) -> UnsubscribeSubscriberRequest:
        return UnsubscribeSubscriberRequest(unsubscribe_token="valid_token_1234567890")

    @pytest.mark.asyncio
    async def test_unsubscribe_subscriber_success(
        self,
        service: SubscriberService,
        mock_repo: AsyncMock,
        subscriber: Subscriber,
        unsubscriber: UnsubscribeSubscriberRequest,
    ):
        subscriber.unsubscribe_token = unsubscriber.unsubscribe_token
        mock_repo.get_subscriber_by_unsubscribe_token.return_value = subscriber

        date_now = datetime.now(UTC)

        unsubscribed_subscriber = Subscriber.model_construct(
            name=subscriber.name,
            email=subscriber.email,
            status=SubscriberStatus.UNSUBSCRIBED,
            updated_at=date_now,
            unsubscribed_at=date_now,
            unsubscribe_token=subscriber.unsubscribe_token,
        )
        mock_repo.unsubscribe_subscriber.return_value = unsubscribed_subscriber

        response = await service.unsubscribe_subscriber(
            unsubscriber,
        )

        mock_repo.get_subscriber_by_unsubscribe_token.assert_called_once_with(
            unsubscriber.unsubscribe_token
        )
        mock_repo.unsubscribe_subscriber.assert_called_once_with(subscriber)

        assert response.status == SubscriberStatus.UNSUBSCRIBED
        assert response.unsubscribed_at is not None
        assert response.updated_at == date_now
        assert response.unsubscribed_at == date_now
        assert response.unsubscribe_token == subscriber.unsubscribe_token

    @pytest.mark.asyncio
    async def test_unsubscribe_subscriber_not_found(
        self,
        service: SubscriberService,
        mock_repo: AsyncMock,
        unsubscriber: UnsubscribeSubscriberRequest,
    ):
        mock_repo.get_subscriber_by_unsubscribe_token.return_value = None

        with pytest.raises(SubscriberNotFoundException) as exc_info:
            await service.unsubscribe_subscriber(
                unsubscriber,
            )

        assert (
            str(exc_info.value)
            == "Assinante com este token de desinscrição não foi encontrado."
        )

        mock_repo.get_subscriber_by_unsubscribe_token.assert_called_once_with(
            unsubscriber.unsubscribe_token
        )

        mock_repo.unsubscribe_subscriber.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_unsubscribe_subscriber_already_unsubscribed(
        self,
        service: SubscriberService,
        mock_repo: AsyncMock,
        subscriber: Subscriber,
        unsubscriber: UnsubscribeSubscriberRequest,
    ):
        subscriber.unsubscribe_token = unsubscriber.unsubscribe_token
        subscriber.status = SubscriberStatus.UNSUBSCRIBED
        mock_repo.get_subscriber_by_unsubscribe_token.return_value = subscriber

        with pytest.raises(UnsubscriberAlreadyUnsubscribedException) as exc_info:
            await service.unsubscribe_subscriber(
                unsubscriber,
            )

        assert (
            str(exc_info.value)
            == "Assinante com este token de desinscrição já está desinscrito."
        )

        mock_repo.get_subscriber_by_unsubscribe_token.assert_called_once_with(
            unsubscriber.unsubscribe_token
        )

        mock_repo.unsubscribe_subscriber.assert_not_awaited()


class TestGetSubscribers:
    @pytest.fixture
    def list_subscribers(self) -> tuple[list[Subscriber], int]:
        return [
            Subscriber.model_construct(name="João", email="joao@example.com"),
            Subscriber.model_construct(name="Maria", email="maria@example.com"),
            Subscriber.model_construct(name="Pedro", email="pedro@example.com"),
        ], 3

    @pytest.mark.asyncio
    async def test_get_subscribers_success(
        self,
        service: SubscriberService,
        mock_repo: AsyncMock,
        list_subscribers: tuple[list[Subscriber], int],
    ):
        status = SubscriberStatus.ACTIVE
        skip = 0
        limit = 10

        mock_repo.get_subscribers_by_status.return_value = list_subscribers

        response, total_count, pages = await service.get_subscribers(
            status,
            skip,
            limit,
        )

        mock_repo.get_subscribers_by_status.assert_called_once_with(
            status=status, skip=skip, limit=limit
        )

        assert len(response) == 3
        assert total_count == 3
        assert pages == 1
        for sub in response:
            assert isinstance(sub, Subscriber)
            assert sub.name in [s.name for s in list_subscribers[0]]
            assert sub.email in [s.email for s in list_subscribers[0]]
            assert sub.status in [s.status for s in list_subscribers[0]]
            assert sub.status == status

    @pytest.mark.asyncio
    async def test_get_subscribers_empty(
        self,
        service: SubscriberService,
        mock_repo: AsyncMock,
    ):
        status = SubscriberStatus.UNSUBSCRIBED
        skip = 0
        limit = 10

        mock_repo.get_subscribers_by_status.return_value = ([], 0)

        response, total_count, pages = await service.get_subscribers(
            status,
            skip,
            limit,
        )

        mock_repo.get_subscribers_by_status.assert_called_once_with(
            status=status, skip=skip, limit=limit
        )

        assert len(response) == 0
        assert total_count == 0
        assert pages == 0

    @pytest.mark.asyncio
    async def test_get_subscribers_pagination(
        self,
        service: SubscriberService,
        mock_repo: AsyncMock,
        list_subscribers: tuple[list[Subscriber], int],
    ):
        status = SubscriberStatus.ACTIVE
        skip = 0
        limit = 2

        mock_repo.get_subscribers_by_status.return_value = list_subscribers

        response, total_count, pages = await service.get_subscribers(
            status,
            skip,
            limit,
        )

        mock_repo.get_subscribers_by_status.assert_called_once_with(
            status=status, skip=skip, limit=limit
        )

        assert len(response) == 3
        assert total_count == 3
        assert pages == 2
