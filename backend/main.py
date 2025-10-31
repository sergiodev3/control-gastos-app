"""
Aplicación principal FastAPI para Control de Gastos
Sistema de gestión de finanzas personales con autenticación JWT
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import sys
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("app.log")
    ]
)

logger = logging.getLogger(__name__)

# Importaciones de la aplicación
from core.config import settings
from db.database import connect_to_mongo, close_mongo_connection

# Importar routers
from api.auth import router as auth_router
from api.expenses import router as expenses_router
from api.incomes import router as incomes_router
from api.savings import router as savings_router
from api.stats import router as stats_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestor de ciclo de vida de la aplicación
    Maneja la conexión a la base de datos al iniciar y cerrar
    """
    try:
        # Inicialización
        logger.info("Iniciando aplicación Control de Gastos...")
        await connect_to_mongo()
        logger.info("Aplicación iniciada correctamente")
        
        yield
        
    except Exception as e:
        logger.error(f"Error en inicialización: {e}")
        raise
    finally:
        # Limpieza al cerrar
        logger.info("Cerrando aplicación...")
        await close_mongo_connection()
        logger.info("✅ Aplicación cerrada correctamente")

# Crear instancia de FastAPI
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
    **Control de Gastos API** 🏦
    
    Sistema completo para gestión de finanzas personales que permite:
    
    * 👤 **Autenticación**: Registro y login de usuarios con JWT
    * 💸 **Gastos**: Registrar y gestionar gastos con categorías y tipos de pago
    * 💰 **Ingresos**: Llevar control de todas las fuentes de ingresos
    * 🏦 **Ahorros**: Gestionar metas y propósitos de ahorro
    * 📊 **Estadísticas**: Resúmenes financieros y reportes mensuales
    
    ## Autenticación
    
    La API utiliza **Bearer Token (JWT)** para autenticación. 
    
    1. Regístrate en `/auth/register`
    2. Inicia sesión en `/auth/login` para obtener tu token
    3. Incluye el token en el header `Authorization: Bearer <tu_token>`
    
    ## Tipos de Pago Disponibles
    
    * `efectivo`
    * `tarjeta_debito`
    * `tarjeta_credito`
    * `transferencia`
    * `paypal`
    * `otro`
    """,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Middleware para logging de requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Middleware para logging de todas las requests
    """
    start_time = datetime.now()
    
    # Log de request
    logger.info(f"🔄 {request.method} {request.url}")
    
    # Procesar request
    response = await call_next(request)
    
    # Calcular tiempo de procesamiento
    process_time = datetime.now() - start_time
    process_time_ms = round(process_time.total_seconds() * 1000, 2)
    
    # Log de response
    logger.info(f"✅ {request.method} {request.url} - {response.status_code} - {process_time_ms}ms")
    
    return response

# Manejador global de excepciones
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Manejador global de excepciones no controladas
    """
    import traceback
    error_detail = str(exc)
    error_traceback = traceback.format_exc()
    
    logger.error(f"Error no controlado en {request.method} {request.url}: {error_detail}")
    logger.error(f"Traceback completo: {error_traceback}")
    
    return JSONResponse(
        status_code=500,
        content={
            "detail": f"Error interno del servidor: {error_detail}",
            "timestamp": datetime.now().isoformat(),
            "path": str(request.url)
        }
    )

# Registrar routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(expenses_router, prefix="/api/v1")
app.include_router(incomes_router, prefix="/api/v1")
app.include_router(savings_router, prefix="/api/v1")
app.include_router(stats_router, prefix="/api/v1")

# Endpoint raíz
@app.get("/", tags=["Información"])
async def root():
    """
    Endpoint raíz con información de la API
    """
    return {
        "message": "🏦 Control de Gastos API",
        "version": settings.app_version,
        "status": "🟢 Activo",
        "docs": "/docs",
        "redoc": "/redoc",
        "timestamp": datetime.now().isoformat(),
        "features": [
            "Autenticación JWT",
            "Gestión de gastos",
            "Gestión de ingresos", 
            "Gestión de ahorros",
            "Estadísticas financieras",
            "Reportes mensuales"
        ]
    }

# Endpoint de salud
@app.get("/health", tags=["Información"])
async def health_check():
    """
    Endpoint para verificar el estado de la aplicación
    """
    return {
        "status": "🟢 Saludable",
        "timestamp": datetime.now().isoformat(),
        "version": settings.app_version,
        "database": "� Conectado"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info"
    )
