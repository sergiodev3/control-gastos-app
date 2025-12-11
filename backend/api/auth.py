"""
API endpoints para autenticación y gestión de usuarios
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from odmantic import AIOEngine
from db.database import get_database
from services.user_service import UserService
from models.schemas import UserCreate, UserLogin, UserResponse, Token, UserUpdate, PasswordChange
from core.security import get_current_active_user
from models.models import User

# Router para endpoints de usuarios
router = APIRouter(prefix="/auth", tags=["Autenticación"])

# Seguridad Bearer
security = HTTPBearer()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    db: AIOEngine = Depends(get_database)
):
    """
    Registrar un nuevo usuario
    
    - **email**: Email único del usuario
    - **username**: Nombre de usuario único 
    - **full_name**: Nombre completo
    - **password**: Contraseña (mínimo 8 caracteres, debe contener letras y números)
    """
    try:
        user_service = UserService(db)
        return await user_service.create_user(user_data)
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error en registro de usuario: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en registro: {str(e)}"
        )

@router.post("/login", response_model=Token)
async def login_user(
    login_data: UserLogin,
    db: AIOEngine = Depends(get_database)
):
    """
    Iniciar sesión
    
    - **email**: Email del usuario
    - **password**: Contraseña del usuario
    
    Retorna un token JWT para autenticación
    """
    user_service = UserService(db)
    return await user_service.login_user(login_data.email, login_data.password)

@router.get("/profile", response_model=UserResponse)
async def get_user_profile(
    current_user: User = Depends(get_current_active_user),
    db: AIOEngine = Depends(get_database)
):
    """
    Obtener perfil del usuario actual
    
    Requiere autenticación Bearer token
    """
    user_service = UserService(db)
    return await user_service.get_user_profile(current_user)

@router.put("/profile", response_model=UserResponse)
async def update_user_profile(
    update_data: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AIOEngine = Depends(get_database)
):
    """
    Actualizar perfil del usuario actual
    
    - **username**: Nuevo nombre de usuario (opcional)
    - **full_name**: Nuevo nombre completo (opcional)
    
    Requiere autenticación Bearer token
    """
    user_service = UserService(db)
    return await user_service.update_user_profile(current_user, update_data)

@router.post("/change-password")
async def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_active_user),
    db: AIOEngine = Depends(get_database)
):
    """
    Cambiar contraseña del usuario actual
    
    - **current_password**: Contraseña actual del usuario (requerida)
    - **new_password**: Nueva contraseña (mínimo 8 caracteres, debe contener letras y números)
    
    Requiere autenticación Bearer token
    """
    user_service = UserService(db)
    return await user_service.change_password(
        current_user,
        password_data.current_password,
        password_data.new_password
    )