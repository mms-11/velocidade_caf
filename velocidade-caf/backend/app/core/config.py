from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Velocidade CAF"
    admin_email: str = "admin@example.com"
    items_per_page: int = 50
    secret_key: str = "your_secret_key"
    debug: bool = True

    class Config:
        env_file = ".env"

settings = Settings()