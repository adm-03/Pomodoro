from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session


engine = create_engine("postgresql+psycopg2://postgres:password@localhost:5433/pomodoro")


SessionLocal = sessionmaker(engine)

def get_db_session() -> Session:
    return SessionLocal()  

