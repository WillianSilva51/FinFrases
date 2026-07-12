from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "FinFrases API"
    VERSION: str = "1.0.1"
    MONGO_URI: str
    API_KEY: str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    REDIS_PASSWORD: str

    model_config = SettingsConfigDict(
        env_file="api/.env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
