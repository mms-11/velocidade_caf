import os
import secrets
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Configurações da aplicação."""
    
    # App
    PROJECT_NAME: str = "Velocidade CAF API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "cockroachdb://root@localhost:26257/caf?sslmode=disable")
    
    # Security - IMPORTANTE: Mude em produção!
    SECRET_KEY: str = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 dias
    
    # CORS
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:5173"]
    
    class Config:
        case_sensitive = True


settings = Settings()