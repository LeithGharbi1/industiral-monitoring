from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_PORT: int = 5432

    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379

    QUEUE_NAME: str = "machine_events"

    API_URL: str = "http://api:8000/ingest"

    class Config:
        env_file = ".env"


settings = Settings()