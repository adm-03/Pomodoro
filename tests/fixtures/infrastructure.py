import asyncio
import sys
from sqlalchemy import delete
import pytest

from app.models.user import UserProfile
from app.settings import Settings

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.infrastructure.database.database import Base

@pytest.fixture
def settings():
    return Settings()

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())



# 1. Создаем engine только как фикстуру (НЕ глобально!)
@pytest.fixture(scope="session")
async def engine():
    # На Windows NullPool часто помогает избежать ошибок закрытия цикла
    from sqlalchemy.pool import NullPool
    
    engine = create_async_engine(
        url='postgresql+asyncpg://postgres:password@localhost:5433/pomodoro-test',
        echo=True,
        poolclass=NullPool
    )
    yield engine
    await engine.dispose()
    
@pytest.fixture(scope="session")
async def init_db(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def db_session(engine, init_db):
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as session:
        yield session
      
@pytest.fixture(autouse=True)
async def clear_db(db_session):
    await db_session.execute(delete(UserProfile))
    # Если есть Tasks, их тоже можно чистить здесь: await db_session.execute(delete(Task))
    await db_session.commit()
    yield