"""
Servicios de autenticación y gestión de usuarios
Contiene toda la lógica de negocio relacionada con usuarios
"""
from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status
from odmantic import AIOEngine
from models.models import User
from models.schemas import UserCreate, UserResponse, Token, UserUpdate
from core.security import security_utils, authenticate_user
from core.config import settings
import logging

logger = logging.getLogger(__name__)

class UserService:
    """
    Servicio para operaciones con usuarios
    Centraliza toda la lógica de negocio de usuarios
    """
    
    def __init__(self, db: AIOEngine):
        self.db = db
    
    async def create_user(self, user_data: UserCreate) -> UserResponse:
        """
        Crear un nuevo usuario
        """
        try:
            # Verificar si el email ya existe
            existing_user = await self.db.find_one(User, User.email == user_data.email)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El email ya está registrado"
                )
            
            # Verificar si el username ya existe
            existing_username = await self.db.find_one(User, User.username == user_data.username)
            if existing_username:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El nombre de usuario ya está en uso"
                )
            
            # Crear hash de la contraseña
            hashed_password = security_utils.get_password_hash(user_data.password)
            
            # Crear nuevo usuario usando model_validate
            user_data_dict = {
                "email": user_data.email,
                "username": user_data.username,
                "full_name": user_data.full_name,
                "hashed_password": hashed_password,
                "is_active": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            new_user = User.model_validate(user_data_dict)
            
            # Guardar en base de datos
            saved_user = await self.db.save(new_user)
            
            logger.info(f"Usuario creado exitosamente: {saved_user.email}")
            
            return UserResponse(
                id=str(saved_user.id),
                email=saved_user.email,
                username=saved_user.username,
                full_name=saved_user.full_name,
                is_active=saved_user.is_active,
                created_at=saved_user.created_at
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error creando usuario: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    async def login_user(self, email: str, password: str) -> Token:
        """
        Iniciar sesión de usuario
        """
        try:
            # Autenticar usuario
            user = await authenticate_user(email, password, self.db)
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Email o contraseña incorrectos",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            if not user.is_active:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Usuario inactivo"
                )
            
            # Crear token de acceso
            access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
            access_token = security_utils.create_access_token(
                data={"sub": str(user.id)},
                expires_delta=access_token_expires
            )
            
            logger.info(f"Usuario logueado exitosamente: {user.email}")
            
            return Token(
                access_token=access_token,
                token_type="bearer",
                expires_in=settings.access_token_expire_minutes * 60,
                user=UserResponse(
                    id=str(user.id),
                    email=user.email,
                    username=user.username,
                    full_name=user.full_name,
                    is_active=user.is_active,
                    created_at=user.created_at
                )
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error en login: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    async def get_user_profile(self, user: User) -> UserResponse:
        """
        Obtener perfil de usuario
        """
        return UserResponse(
            id=str(user.id),
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            is_active=user.is_active,
            created_at=user.created_at
        )
    
    async def update_user_profile(self, user: User, update_data: UserUpdate) -> UserResponse:
        """
        Actualizar perfil de usuario
        """
        try:
            # Verificar si el nuevo username ya existe (si se proporciona)
            if update_data.username and update_data.username != user.username:
                existing_username = await self.db.find_one(
                    User, 
                    User.username == update_data.username
                )
                if existing_username:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="El nombre de usuario ya está en uso"
                    )
            
            # Actualizar campos que no son None
            update_fields = {}
            if update_data.username is not None:
                update_fields["username"] = update_data.username
            if update_data.full_name is not None:
                update_fields["full_name"] = update_data.full_name
            
            if update_fields:
                update_fields["updated_at"] = datetime.utcnow()
                
                # Actualizar usuario
                for field, value in update_fields.items():
                    setattr(user, field, value)
                
                updated_user = await self.db.save(user)
                logger.info(f"Usuario actualizado exitosamente: {updated_user.email}")
                
                return UserResponse(
                    id=str(updated_user.id),
                    email=updated_user.email,
                    username=updated_user.username,
                    full_name=updated_user.full_name,
                    is_active=updated_user.is_active,
                    created_at=updated_user.created_at
                )
            else:
                # No hay cambios
                return await self.get_user_profile(user)
                
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error actualizando usuario: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    async def change_password(self, user: User, current_password: str, new_password: str) -> dict:
        """
        Cambiar contraseña del usuario
        """
        try:
            # Verificar que la contraseña actual sea correcta
            if not security_utils.verify_password(current_password, user.hashed_password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="La contraseña actual es incorrecta"
                )
            
            # Verificar que la nueva contraseña sea diferente
            if security_utils.verify_password(new_password, user.hashed_password):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="La nueva contraseña debe ser diferente a la actual"
                )
            
            # Actualizar contraseña
            user.hashed_password = security_utils.get_password_hash(new_password)
            user.updated_at = datetime.utcnow()
            
            await self.db.save(user)
            logger.info(f"Contraseña actualizada exitosamente para: {user.email}")
            
            return {"message": "Contraseña actualizada exitosamente"}
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error cambiando contraseña: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )