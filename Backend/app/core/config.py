"""
Configuration management for Perseus Backend
Handles environment variables and application settings
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """

    # API Configuration
    API_TITLE: str = "Perseus API"
    API_DESCRIPTION: str = "API para extracción de requisitos de usabilidad según ISO 25010:2023 desde comentarios de usuarios"
    API_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"

    # CORS Configuration
    CORS_ORIGINS: list = [
        "http://localhost:4200",
        "http://localhost:8080",
        "http://127.0.0.1:4200",
        "http://127.0.0.1:8080",
    ]

    # Model Configuration
    BINARY_MODEL_NAME: str = os.getenv(
        "BINARY_MODEL_NAME",
        "SamuelSoto7/Perseus_binario"
    )
    MULTICLASS_MODEL_NAME: str = os.getenv(
        "MULTICLASS_MODEL_NAME",
        "SamuelSoto7/Perseus_Multiclase"
    )

    # HuggingFace Configuration
    HUGGINGFACE_TOKEN: Optional[str] = os.getenv("HUGGINGFACE_TOKEN", None)

    # AI Provider Configuration
    PROVIDER: str = os.getenv("PROVIDER", "groq")  # "openai" or "groq"

    # OpenAI Configuration
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY", None)

    # Groq Configuration
    GROQ_API_KEY: Optional[str] = os.getenv("GROQ_API_KEY", None)
    GROQ_MODEL_NAME: str = os.getenv("GROQ_MODEL_NAME", "llama-3.1-8b-instant")

    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    RELOAD: bool = os.getenv("RELOAD", "False").lower() == "true"
    WORKERS: int = int(os.getenv("WORKERS", "1"))

    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # File Upload Configuration
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: list = [".csv"]

    # PDF Generation Configuration
    PDF_FONT_SIZE: int = 12
    PDF_MARGIN: int = 25
    PDF_LINE_HEIGHT: int = 15

    # Scraping Configuration
    SCRAPER_USER_AGENT: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    SCRAPER_TIMEOUT: int = 30
    SCRAPER_MAX_COMMENTS: int = 100

    # Cache Configuration
    ENABLE_CACHE: bool = os.getenv("ENABLE_CACHE", "True").lower() == "true"
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "3600"))  # 1 hour

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance
    Returns the same instance on subsequent calls
    """
    return Settings()


# Global settings instance
settings = get_settings()
