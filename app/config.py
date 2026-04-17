from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "NELIE API"
    DEBUG: bool = True
    DATABASE_URL: str
    ANTHROPIC_API_KEY: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()