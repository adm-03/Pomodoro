from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from settings import settings



engine = create_async_engine(url=settings.db_url, echo=True, pool_pre_ping=True)

AsyncSessionFactory = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False
)

async def get_db_session() -> AsyncSession:
   async with AsyncSessionFactory() as session:
      yield session