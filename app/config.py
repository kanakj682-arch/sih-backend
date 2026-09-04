from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Artisan AI Market Linkage API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    DATABASE_URL: str = "sqlite:///./sih_artisan.db"
    GEMINI_API_KEY: Optional[str] = None
    ONDC_GATEWAY_URL: str = "https://staging.ondc.org/api/v1"
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()