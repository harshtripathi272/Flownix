from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    PROJECT_NAME: str = "Flownix"
    VERSION: str = "0.1.0"
    API_PREFIX: str = "/api/v1"
    
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # CORS settings
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080"
    ]
    
    # Database settings (for future use)
    DATABASE_URL: str = "sqlite:///./flownix.db"
    
    # ML Engine settings
    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024  # 100MB
    TEMP_DIR: str = "./temp"
    MODELS_DIR: str = "./models"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
