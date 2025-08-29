from typing import List

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv('.env')


class Settings(BaseSettings):
    BOT_TOKEN: str
    ADMINS: List[int]
    DB_USER: str
    DB_NAME: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int
    BASE_SITE: str

    model_config = SettingsConfigDict(
        env_file=".env",  # automatically load
        extra="ignore"  # optional: ignore unknown env vars
    )

    @property
    def DB_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    def get_webhook_url(self) -> str:
        return f"{self.BASE_SITE}/webhook"


settings = Settings()
database_url = settings.DB_URL
