from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "NLP Dashboard"
    DATABASE_URL: str = "postgresql+asyncpg://nlpuser:nlppass123@127.0.0.1:5433/nlp_dashboard"
    SYNC_DATABASE_URL: str = "postgresql+psycopg2://nlpuser:nlppass123@127.0.0.1:5433/nlp_dashboard"
    REDIS_URL: str = "redis://localhost:6379/0"

    class Config:
        env_file = ".env"


settings = Settings()