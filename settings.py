from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    sqlite_db_name: str = 'pomodoro.sqlite'

