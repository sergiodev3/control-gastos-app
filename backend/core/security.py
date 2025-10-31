"""
Utilidades de seguridad para autenticación y autorización
Incluye funciones para hash de contraseñas, JWT tokens, y validación de usuarios
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from odmantic import ObjectId
from core.config import settings
from db.database import get_database
from models.models import User
from models.schemas import TokenData
import logging

logger = logging.getLogger(__name__)

# Configuración de encriptación de contraseñas
# Usamos scrypt que es más simple y evita problemas de compatibilidad de bcrypt
pwd_context = CryptContext(schemes=["scrypt"], deprecated="auto")

# Configuración de autenticación Bearer
security = HTTPBearer()

class SecurityUtils:
    """
    Clase con utilidades de seguridad
    Centraliza todas las operaciones criptográficas y de autenticación
    """
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verificar si una contraseña en texto plano coincide con el hash
        """
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        Generar hash de una contraseña
        """
        return pwd_context.hash(password)
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Crear un token JWT de acceso
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.access_token_expire_minutes
            )
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, 
            settings.secret_key, 
            algorithm=settings.algorithm
        )
        
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> TokenData:
        """
        Verificar y decodificar un token JWT
        """
        try:
            payload = jwt.decode(
                token, 
                settings.secret_key, 
                algorithms=[settings.algorithm]
            )
            user_id: Optional[str] = payload.get("sub")
            
            if user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token inválido",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            return TokenData(user_id=user_id)
            
        except JWTError as e:
            logger.warning(f"Error verificando token: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )

# Instancia global de utilidades de seguridad
security_utils = SecurityUtils()

async def authenticate_user(email: str, password: str, db) -> Optional[User]:
    """
    Autenticar un usuario con email y contraseña
    """
    try:
        user = await db.find_one(User, User.email == email)
        
        if not user:
            return None
        
        if not security_utils.verify_password(password, user.hashed_password):
            return None
        
        return user
        
    except Exception as e:
        logger.error(f"Error autenticando usuario: {e}")
        return None

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db = Depends(get_database)
) -> User:
    """
    Dependency para obtener el usuario actual desde el token JWT
    """
    try:
        # Extraer token del header Authorization
        token = credentials.credentials
        
        # Verificar token
        token_data = security_utils.verify_token(token)
        
        if token_data.user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Buscar usuario en la base de datos
        user = await db.find_one(User, User.id == ObjectId(token_data.user_id))
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no encontrado",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuario inactivo"
            )
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error obteniendo usuario actual: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Error de autenticación",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency para obtener el usuario actual activo
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario inactivo"
        )
    return current_user