from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    MODE: Literal["DEV", "TEST", "PROD"]

    SECRET_KEY: str
    ALGORITHM: str

    ACCESS_TOKEN_EXP_MINUTES: int = 999999999
    REFRESH_TOKEN_EXP_DAYS: int = 30

    MONGODB_HOST: str
    MONGODB_PORT: int
    MONGODB_USER: str
    MONGODB_PASSWORD: str
    MONGODB_NAME: str = "chat_app"

    @property
    def MONGODB_CONN_STRING(self):
        return f"mongodb://{self.MONGODB_USER}:{self.MONGODB_PASSWORD}@{self.MONGODB_HOST}:{self.MONGODB_PORT}"

    RABBITMQ_HOST: str
    RABBITMQ_USER:str
    RABBITMQ_PASS:str

    @property
    def RABBITMQ_URI(self):
        return f"amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASS}@{self.RABBITMQ_HOST}/"

    REDIS_HOST: str
    REDIS_PORT: int

    @property
    def REDIS_URI(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"

    CACHE_TTL: int = 60


settings = Settings()
