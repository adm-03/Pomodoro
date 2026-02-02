from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from settings import settings



engine = create_engine(settings.db_url)


SessionLocal = sessionmaker(engine)

def get_db_session() -> Session:
    return SessionLocal()  