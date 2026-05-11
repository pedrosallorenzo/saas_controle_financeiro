from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str                          # asyncpg — runtime da aplicação
    alembic_database_url: str | None = None   # psycopg2 — exclusivo para migrations
    supabase_url: str
    supabase_service_role_key: str
    anthropic_api_key: str
    upstash_redis_url: str
    upstash_redis_token: str
    environment: str = "development"
    cors_origins: list[str] = ["http://localhost:3000"]

    model_config = {"env_file": ".env"}


settings = Settings()
