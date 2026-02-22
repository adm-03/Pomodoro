import pytest
from app.repository.user import UserRepository
from app.service.auth import AuthService
from app.settings import Settings

@pytest.fixture
def mock_auth_service(yandex_client, google_client, fake_user_repository):
    return AuthService(user_repository=fake_user_repository,
                        settings=Settings(),
                        google_client=google_client,
                        yandex_client=yandex_client
                            )

@pytest.fixture
def auth_service(google_client, yandex_client, db_session):
    return AuthService(
        user_repository=UserRepository(db_session=db_session),
        settings=Settings(),
        google_client=google_client,
        yandex_client=yandex_client
    )