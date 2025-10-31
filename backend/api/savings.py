"""
API endpoints para gestión de ahorros
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from odmantic import AIOEngine
from db.database import get_database
from services.saving_service import SavingService
from models.schemas import SavingCreate, SavingUpdate, SavingResponse
from core.security import get_current_active_user
from models.models import User

# Router para endpoints de ahorros
router = APIRouter(prefix="/savings", tags=["Ahorros"])

@router.post("", response_model=SavingResponse, status_code=status.HTTP_201_CREATED)
async def create_saving(
    saving_data: SavingCreate,
    current_user: User = Depends(get_current_active_user),
    db: AIOEngine = Depends(get_database)
):
    """
    Crear un nuevo ahorro
    
    - **date**: Fecha del ahorro (opcional, por defecto fecha actual)
    - **amount**: Cantidad del ahorro (debe ser positiva)
    - **purpose**: Propósito o meta del ahorro
    - **goal_amount**: Meta de ahorro total (opcional)
    - **notes**: Notas adicionales (opcional)
    """
    saving_service = SavingService(db)
    return await saving_service.create_saving(saving_data, current_user)

@router.get("", response_model=List[SavingResponse])
async def get_user_savings(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    current_user: User = Depends(get_current_active_user),
    db: AIOEngine = Depends(get_database)
):
    """
    Obtener lista de ahorros del usuario actual
    
    - **skip**: Número de registros a omitir (paginación)
    - **limit**: Número máximo de registros a retornar (máximo 1000)
    """
    saving_service = SavingService(db)
    return await saving_service.get_user_savings(current_user, skip, limit)

@router.get("/{saving_id}", response_model=SavingResponse)
async def get_saving_by_id(
    saving_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AIOEngine = Depends(get_database)
):
    """
    Obtener un ahorro específico por ID
    
    - **saving_id**: ID del ahorro a obtener
    """
    saving_service = SavingService(db)
    return await saving_service.get_saving_by_id(saving_id, current_user)

@router.put("/{saving_id}", response_model=SavingResponse)
async def update_saving(
    saving_id: str,
    update_data: SavingUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AIOEngine = Depends(get_database)
):
    """
    Actualizar un ahorro existente
    
    - **saving_id**: ID del ahorro a actualizar
    - Campos opcionales: date, amount, purpose, goal_amount, notes
    """
    saving_service = SavingService(db)
    return await saving_service.update_saving(saving_id, update_data, current_user)

@router.delete("/{saving_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_saving(
    saving_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AIOEngine = Depends(get_database)
):
    """
    Eliminar un ahorro
    
    - **saving_id**: ID del ahorro a eliminar
    """
    saving_service = SavingService(db)
    await saving_service.delete_saving(saving_id, current_user)
    return None