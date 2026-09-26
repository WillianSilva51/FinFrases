from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "FinFrases API"
    VERSION: str = "1.1.2"
    API_PREFIX: str = "/api"
    MONGO_URI: str
    API_KEY: str
    REDIS_URI: str

    model_config = SettingsConfigDict(
        env_file="api/.env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
