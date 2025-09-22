"""
Application configuration settings
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    
    MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "")
    MISTRAL_MODEL = os.getenv("MISTRAL_MODEL", "mistral-medium-2508")
    MISTRAL_BASE_URL = os.getenv("MISTRAL_BASE_URL", "https://api.mistral.ai/v1/chat/completions")
    
   
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    
    
    CORS_ORIGINS = ["*"]
    CORS_CREDENTIALS = True
    CORS_METHODS = ["*"]
    CORS_HEADERS = ["*"]
    
    
    WEBSOCKET_CORS_ORIGINS = "*"
    
    def __post_init__(self):
        """Validate required environment variables"""
        if not self.MISTRAL_API_KEY:
            raise ValueError("MISTRAL_API_KEY environment variable is required")

settings = Settings()