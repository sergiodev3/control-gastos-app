"""
API endpoints para gestión de ingresos
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from odmantic import AIOEngine
from db.database import get_database
from services.income_service import IncomeService
from models.schemas import IncomeCreate, IncomeUpdate, IncomeResponse
from core.security import get_current_active_user
from models.models import User

# Router para endpoints de ingresos
router = APIRouter(prefix="/incomes", tags=["Ingresos"])

@router.post("", response_model=IncomeResponse, status_code=status.HTTP_201_CREATED)
async def create_income(
    income_data: IncomeCreate,
    current_user: User = Depends(get_current_active_user),
    db: AIOEngine = Depends(get_database)
):
    """
    Crear un nuevo ingreso
    
    - **date**: Fecha del ingreso (opcional, por defecto fecha actual)
    - **description**: Descripción del ingreso
    - **amount**: Cantidad del ingreso (debe ser positiva)
    - **source**: Fuente del ingreso (opcional)
    - **notes**: Notas adicionales (opcional)
    """
    income_service = IncomeService(db)
    return await income_service.create_income(income_data, current_user)

@router.get("", response_model=List[IncomeResponse])
async def get_user_incomes(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    current_user: User = Depends(get_current_active_user),
    db: AIOEngine = Depends(get_database)
):
    """
    Obtener lista de ingresos del usuario actual
    
    - **skip**: Número de registros a omitir (paginación)
    - **limit**: Número máximo de registros a retornar (máximo 1000)
    """
    income_service = IncomeService(db)
    return await income_service.get_user_incomes(current_user, skip, limit)

@router.get("/{income_id}", response_model=IncomeResponse)
async def get_income_by_id(
    income_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AIOEngine = Depends(get_database)
):
    """
    Obtener un ingreso específico por ID
    
    - **income_id**: ID del ingreso a obtener
    """
    income_service = IncomeService(db)
    return await income_service.get_income_by_id(income_id, current_user)

@router.put("/{income_id}", response_model=IncomeResponse)
async def update_income(
    income_id: str,
    update_data: IncomeUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AIOEngine = Depends(get_database)
):
    """
    Actualizar un ingreso existente
    
    - **income_id**: ID del ingreso a actualizar
    - Campos opcionales: date, description, amount, source, notes
    """
    income_service = IncomeService(db)
    return await income_service.update_income(income_id, update_data, current_user)

@router.delete("/{income_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_income(
    income_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AIOEngine = Depends(get_database)
):
    """
    Eliminar un ingreso
    
    - **income_id**: ID del ingreso a eliminar
    """
    income_service = IncomeService(db)
    await income_service.delete_income(income_id, current_user)
    return None