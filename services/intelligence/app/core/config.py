from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "Aivora Intelligence Service"
    
    # Database
    DATABASE_URL: str
    
    # Redis
    REDIS_URL: str
    
    # AI Provider
    GROQ_API_KEY: str
    
    # Authentication
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()
