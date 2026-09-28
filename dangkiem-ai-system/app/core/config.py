from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "Hệ thống Quản lý Đăng kiểm AI"
    APP_VERSION: str = "1.1.0"
    ENV: str = "development"
    PORT: int = 8000
    DATABASE_URL: str = "sqlite:///./dangkiem.db"
    SECRET_KEY: str = "super_secret_key_12345"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480
    OPENAI_API_KEY: str = ""


settings = Settings()