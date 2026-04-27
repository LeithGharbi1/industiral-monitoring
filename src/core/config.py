from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --- DATABASE ---
    DATABASE_URL: str

    # --- REDIS ---
    REDIS_URL: str | None = None
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379

    # --- QUEUE ---
    QUEUE_NAME: str = "machine_events"

    # --- API ---
    API_URL: str = "http://api:8000/ingest"

    # --- CONFIG ---
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"   # 👈 CRITICAL (fixes your previous errors)
    )


settings = Settings()