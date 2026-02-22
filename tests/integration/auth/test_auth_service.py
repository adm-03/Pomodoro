from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

from app.models.user import UserProfile
from tests.fixtures.users.user_model import EXISTS_GOOGLE_USER_EMAIL, EXISTS_GOOGLE_USER_ID

async def test_google_auth__login_not_exist_user(auth_service, db_session):
    session: AsyncSession = db_session
    code = 'fake_code'
    
    users = (await session.execute(select(UserProfile))).scalars().all()
    user = await auth_service.google_auth(code)
    
    assert len(users) == 0
    assert user is not None

    login_user = (await session.execute(select(UserProfile).where(UserProfile.id == user.user_id))).scalars().first()

    assert login_user is not None 

async def test_google_auth__login_exist_user(auth_service, db_session):
    query = insert(UserProfile).values(
        id=EXISTS_GOOGLE_USER_ID,
        email=EXISTS_GOOGLE_USER_EMAIL
    )
    code = "fake_code"

    await db_session.execute(query)
    await db_session.commit()
    
    user_data = await auth_service.google_auth(code)
    login_user = (await db_session.execute(select(UserProfile).where(UserProfile.id == user_data.user_id))).scalar_one_or_none()

    assert login_user.email == EXISTS_GOOGLE_USER_EMAIL
    assert user_data.user_id == EXISTS_GOOGLE_USER_ID

async def test_base_login__success(auth_service, db_session):
    username = "test_user_name"
    password = "test_user_password"

    query = insert(UserProfile).values(
        username=username,
        password=password
    )
    await db_session.execute(query)
    await db_session.commit()

    user_data = await auth_service.login(username=username, password=password)
    
    login_user = (await db_session.execute(select(UserProfile).where(UserProfile.username == username))).scalar_one_or_none()
    
    assert login_user is not None
    assert user_data.user_id == login_user.id
