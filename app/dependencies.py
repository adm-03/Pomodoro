from fastapi import Depends, HTTPException, Request, Security, security
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from app.client import GoogleClient
from app.client.yandex import YandexClient
from app.exception import TokenExpired, TokenNotCorrect
from app.repository import *  # noqa: F403
from app.infrastructure.database import get_db_session
from app.infrastructure.cache import get_redis_connection
from app.service import TaskService, UserService, AuthService
from app.settings import Settings


def get_task_repository(
    db_session: AsyncSession = Depends(get_db_session),
) -> TaskRepository:
    return TaskRepository(db_session)


def get_cache_repository() -> CacheTask:
    redis_connection = get_redis_connection()
    return CacheTask(redis_connection)


def get_task_service(
    task_repository: TaskRepository = Depends(get_task_repository),
    task_cache: CacheTask = Depends(get_cache_repository),
) -> TaskService:
    return TaskService(task_repository=task_repository, task_cache=task_cache)


def get_user_repository(
    db_session: AsyncSession = Depends(get_db_session),
) -> UserRepository:
    return UserRepository(db_session=db_session)

async def get_async_client() -> httpx.AsyncClient:
    async with httpx.AsyncClient() as client:
        yield client


def get_google_client(async_client: httpx.AsyncClient = Depends(get_async_client)) -> GoogleClient:
    return GoogleClient(settings=Settings(), async_client=async_client)

def get_yandex_client(async_client: httpx.AsyncClient = Depends(get_async_client)) -> GoogleClient:
    return YandexClient(settings=Settings(), async_client=async_client)



def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
    google_client: GoogleClient = Depends(get_google_client),
    yandex_client: YandexClient = Depends(get_yandex_client)
) -> AuthService:
    return AuthService(user_repository=user_repository, settings=Settings(), google_client=google_client, yandex_client=yandex_client)


def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
    auth_service: AuthService = Depends(get_auth_service),
) -> UserService:
    return UserService(user_repository=user_repository, auth_service=auth_service)


reusable_oauth2 = security.HTTPBearer()


def get_request_user_id(
    auth_service: AuthService = Depends(get_auth_service),
    token: security.http.HTTPAuthorizationCredentials = Security(reusable_oauth2),
) -> int:
    try:
        user_id = auth_service.get_user_id_from_access_token(token.credentials)
    except TokenExpired as e:
        raise HTTPException(status_code=401, detail=e.detail)
    except TokenNotCorrect as e:
        raise HTTPException(status_code=401, detail=e.detail)
    return user_id
