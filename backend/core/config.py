"""
Configuración de la aplicación
Maneja variables de entorno y configuraciones globales
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """
    Configuraciones de la aplicación usando Pydantic Settings
    Las variables se pueden sobrescribir con variables de entorno
    """
    # Configuración de la aplicación
    app_name: str = "Control de Gastos API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Configuración de MongoDB
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "control_gastos"
    
    # Configuración de seguridad
    secret_key: str = "tu_clave_secreta_super_segura_cambiala_en_produccion"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Configuración de CORS - se parseará desde string separado por comas
    allowed_origins: str = "http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000,http://127.0.0.1:5173"
    
    def get_allowed_origins(self) -> list[str]:
        """Convertir string de orígenes separados por comas a lista"""
        return [origin.strip() for origin in self.allowed_origins.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Instancia global de configuración
settings = Settings()