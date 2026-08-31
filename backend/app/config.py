import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application configuration settings."""
    
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "task_management")
    BACKEND_PORT: int = int(os.getenv("BACKEND_PORT", 8000))
    
    # CORS configuration
    CORS_ORIGINS = ["http://localhost:3000", "http://localhost:8000"]


settings = Settings()
