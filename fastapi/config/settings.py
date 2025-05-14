from pydantic_settings import BaseSettings
from pathlib import Path
import os

class Settings(BaseSettings):
    # Server settings
    SERVER_HOST: str = "localhost"
    SERVER_PORT: int = 8000
    SERVER_URL: str = f"http://{SERVER_HOST}:{SERVER_PORT}"
    
    # Leonardo API settings
    LEONARDO_API_KEY: str = "4e289ba7-88c3-41e6-a84c-348815cab808"
    LEONARDO_API_URL: str = "https://cloud.leonardo.ai/api/rest/v1"
    
    # File storage settings
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    STATIC_FOLDER: Path = BASE_DIR / "static" / "generated"
    MAX_FILE_AGE_SECONDS: int = 300  # 5 minutes
    
    # Model settings
    MODEL_ID: str = "b2614463-296c-462a-9586-aafdb8f00e36"  # Custom Model
    IMAGE_WIDTH: int = 768
    IMAGE_HEIGHT: int = 768
    
    # Database settings
    DATABASE_URL: str = "mysql://root:matvei1@localhost:3306/meme_app"
    
    # OpenAI settings
    OPENAI_API_KEY: str = "sk-proj-hze9pZk45KeKhtbb..F1YgBSTMtWoCMPORU9qs2oA"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings() 