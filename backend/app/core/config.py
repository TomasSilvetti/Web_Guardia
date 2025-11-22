"""Configuración de la aplicación"""
import os
from typing import Optional


class Settings:
    """Configuración de la aplicación"""
    
    # JWT Configuration
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production-12345678")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))  # 24 horas
    
    # CORS Configuration
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
    ]
    
    # App Configuration
    APP_NAME: str = "API Módulo de Urgencias"
    APP_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"


settings = Settings()

