from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_HOST: str = 'localhost'
    DB_PORT: int = 5433
    DB_USER: str = 'postrges'
    DB_PASSWORD: str = 'password'
    DB_NAME: str = 'pomodoro'

    CACHE_HOST: str = 'localhost'
    CACHE_PORT: int = 6379
    CAHCE_DB: int = 0
