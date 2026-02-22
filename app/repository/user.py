from sqlalchemy import select, delete, update, insert
from sqlalchemy.ext.asyncio import AsyncSession
from dataclasses import dataclass
from app.models import UserProfile
from app.schema import UserCreateSchema

@dataclass
class UserRepository:
    db_session: AsyncSession

    async def create_user(self, user: UserCreateSchema) -> UserProfile:
        query = insert(UserProfile).values(
            **user.model_dump()
            ).returning(UserProfile.id)
        
        user_id: int = await self.db_session.scalar(query)
        await self.db_session.commit()
        return await self.get_user(user_id)
        
    async def get_user(self, user_id: int) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.id == user_id)
        return await self.db_session.scalar(query)
        
    async def get_user_by_username(self, username: str) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.username == username)
        return (await self.db_session.execute(query)).scalar_one_or_none()
        
    async def get_user_by_email(self, email: str) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.email == email)
        result = await self.db_session.execute(query)
        return result.scalar_one_or_none()