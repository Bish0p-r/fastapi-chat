from typing import Literal

from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    MODE: Literal["DEV", "TEST", "PROD"]

    SECRET_KEY: str
    ALGORITHM: str

    MONGODB_HOST: str
    MONGODB_PORT: int
    MONGODB_USER: str
    MONGODB_PASSWORD: str
    MONGODB_NAME: str = 'chat_app'

    @property
    def MONGODB_CONN_STRING(self):
        return f"mongodb://{self.MONGODB_USER}:{self.MONGODB_PASSWORD}@{self.MONGODB_HOST}:{self.MONGODB_PORT}"

settings = Settings()
