"""
Configuración de la base de datos MongoDB
Maneja la conexión y operaciones básicas con la base de datos
"""
from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
from core.config import settings
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class Database:
    """
    Clase singleton para manejar la conexión a MongoDB
    Utiliza Motor para operaciones asíncronas y ODMantic como ODM
    """
    client: Optional[AsyncIOMotorClient] = None
    engine: Optional[AIOEngine] = None

# Instancia global de la base de datos
database = Database()

async def connect_to_mongo():
    """
    Establece conexión con MongoDB
    Se ejecuta al iniciar la aplicación
    """
    try:
        database.client = AsyncIOMotorClient(settings.mongodb_url)
        database.engine = AIOEngine(
            client=database.client,
            database=settings.database_name
        )
        
        # Verificar conexión
        await database.client.admin.command('ping')
        logger.info(f"Conectado a MongoDB: {settings.database_name}")
        
    except Exception as e:
        logger.error(f"❌ Error conectando a MongoDB: {e}")
        raise e

async def close_mongo_connection():
    """
    Cierra la conexión con MongoDB
    Se ejecuta al cerrar la aplicación
    """
    try:
        if database.client:
            database.client.close()
            logger.info("🔐 Conexión a MongoDB cerrada")
    except Exception as e:
        logger.error(f"❌ Error cerrando conexión MongoDB: {e}")

def get_database() -> AIOEngine:
    """
    Dependency injection para obtener la instancia de la base de datos
    """
    if database.engine is None:
        raise RuntimeError("Database not initialized")
    return database.engine