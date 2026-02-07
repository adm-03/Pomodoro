from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".local.env")

    DB_HOST: str = 'localhost'
    DB_PORT: int = 5433
    DB_USER: str = 'postgres'
    DB_PASSWORD: str = ''
    DB_NAME: str = 'pomodoro'
    DB_DRIVER:str = 'postgresql+psycopg2'
    CACHE_HOST: str = 'localhost'
    CACHE_PORT: int = 6379
    CAHCE_DB: int = 0
    JWT_SECRET_KEY: str = ''
    JWT_ENCODE_ALGORITHM: str = 'HS256'
    GOOGLE_CLIENT_ID: str = ''
    GOOGLE_CLIENT_SECRET: str = ''
    GOOGLE_REDIRECT_URI: str = 'http://localhost:8000/auth/google'
    GOOGLE_TOKEN_URL: str = 'https://accounts.google.com/o/oauth2/token'

    YANDEX_CLIENT_ID: str = 'e8f5512881af4779976e4d735f1400ba'
    YANDEX_CLIENT_SECRET: str = 'ba8a293f82f74d859ec3568c6a2e57c0'
    YANDEX_REDIRECT_URI: str = 'http://localhost:8000/auth/yandex/'
    YANDEX_TOKEN_URL: str = 'https://oauth.yandex.ru/token'

    @property
    def db_url(self):
        return f'{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
    
    @property
    def google_redirect_url(self) -> str:
        return f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={self.GOOGLE_CLIENT_ID}&redirect_uri={self.GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"

    @property
    def yandex_redirect_url(self) -> str:
        return f'https://oauth.yandex.ru/authorize?response_type=code&client_id={self.YANDEX_CLIENT_ID}&redirect_uri={self.YANDEX_REDIRECT_URI}'
settings = Settings()