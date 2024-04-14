from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USERNAME: str
    DB_PASSWORD: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    RABBITMQ_HOST: str
    RABBITMQ_PORT: str
    RABBITMQ_USERNAME: str
    RABBITMQ_PASSWORD: str

    RABBITMQ_ORDER_EXCHANGE_NAME: str
    RABBITMQ_ORDER_EXCHANGE_TYPE: str
    RABBITMQ_ORDER_CREATED_QUEUE_NAME: str
    RABBITMQ_ORDER_CREATED_QUEUE_ROUTING_KEY: str

    model_config = SettingsConfigDict(env_file='.env')

@lru_cache
def get_settings():
    return Settings()