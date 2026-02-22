import pytest
import pytest_asyncio
from jose import jwt 
from app.models.user import UserProfile
from app.schema.user import UserLoginSchema
from app.service.auth import AuthService
from app.settings import Settings
import datetime as dt
from freezegun import freeze_time

def test_get_google_redirect_url__success(mock_auth_service: AuthService, settings: Settings):
    settings_google_redirect_url = settings.google_redirect_url

    mock_auth_service_google_refirect_url = mock_auth_service.get_google_redirect_url()

    assert settings_google_redirect_url == mock_auth_service_google_refirect_url

def test_get_yandex_redirect_url__success(mock_auth_service: AuthService, settings: Settings):
    settings_yandex_redirect_url = settings.yandex_redirect_url

    mock_auth_service_yandex_refirect_url = mock_auth_service.get_yandex_redirect_url()

    assert settings_yandex_redirect_url == mock_auth_service_yandex_refirect_url

@freeze_time("2026-02-15 12:00:00")
def test_geerate_access_token__success(mock_auth_service: AuthService, settings: Settings):
    user_id = str(1)

    access_token = mock_auth_service.generate_access_token(user_id=user_id)
    decode_access_token = jwt.decode(token=access_token,
                                    key=settings.JWT_SECRET_KEY,
                                    algorithms=[settings.JWT_ENCODE_ALGORITHM])
    decoded_user_id = decode_access_token["user_id"]
    decoded_token_expire = dt.datetime.fromtimestamp(decode_access_token["exp"], tz=dt.timezone.utc)


    assert dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=7) == decoded_token_expire
    assert user_id == decoded_user_id

def test_get_user_id_from_access_token__success(mock_auth_service: AuthService, settings: Settings):
    user_id = str(1)
    expires_date_unix = dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=30)

    token = jwt.encode(
            {'user_id': user_id, 'exp': expires_date_unix},
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ENCODE_ALGORITHM
            )
    
    assert user_id == mock_auth_service.get_user_id_from_access_token(access_token=token)
    
async def test_google_auth__success(mock_auth_service: AuthService):
    code = "fake_code"

    user = await mock_auth_service.google_auth(code=code)
    decoded_user_id = mock_auth_service.get_user_id_from_access_token(user.access_token)

    assert user.user_id == decoded_user_id
    assert isinstance(user, UserLoginSchema)

async def test_yandex_auth__success(mock_auth_service: AuthService):
    code = "fake_code"

    user = await mock_auth_service.yandex_auth(code=code)
    decoded_user_id = mock_auth_service.get_user_id_from_access_token(user.access_token)

    assert user.user_id == decoded_user_id
    assert isinstance(user, UserLoginSchema)
    