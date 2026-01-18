from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    REDIS_URL: str = "redis://localhost:6379/0"
    ENGINE_VERSION: str = "1.2.1"

    class Config:
        env_file = ".env"

settings = Settings()
