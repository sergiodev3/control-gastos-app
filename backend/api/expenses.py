"""
API endpoints para gestión de gastos
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from odmantic import AIOEngine
from db.database import get_database
from services.expense_service import ExpenseService
from models.schemas import ExpenseCreate, ExpenseUpdate, ExpenseResponse
from core.security import get_current_active_user
from models.models import User

# Router para endpoints de gastos
router = APIRouter(prefix="/expenses", tags=["Gastos"])

@router.post("", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
async def create_expense(
    expense_data: ExpenseCreate,
    current_user: User = Depends(get_current_active_user),
    db: AIOEngine = Depends(get_database)
):
    """
    Crear un nuevo gasto
    
    - **date**: Fecha del gasto (opcional, por defecto fecha actual)
    - **description**: Descripción del gasto
    - **amount**: Cantidad gastada (debe ser positiva)
    - **payment_type**: Tipo de pago (efectivo, tarjeta_debito, tarjeta_credito, transferencia, paypal, otro)
    - **category**: Categoría del gasto (opcional)
    - **notes**: Notas adicionales (opcional)
    """
    expense_service = ExpenseService(db)
    return await expense_service.create_expense(expense_data, current_user)

@router.get("", response_model=List[ExpenseResponse])
async def get_user_expenses(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    current_user: User = Depends(get_current_active_user),
    db: AIOEngine = Depends(get_database)
):
    """
    Obtener lista de gastos del usuario actual
    
    - **skip**: Número de registros a omitir (paginación)
    - **limit**: Número máximo de registros a retornar (máximo 1000)
    """
    expense_service = ExpenseService(db)
    return await expense_service.get_user_expenses(current_user, skip, limit)

@router.get("/{expense_id}", response_model=ExpenseResponse)
async def get_expense_by_id(
    expense_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AIOEngine = Depends(get_database)
):
    """
    Obtener un gasto específico por ID
    
    - **expense_id**: ID del gasto a obtener
    """
    expense_service = ExpenseService(db)
    return await expense_service.get_expense_by_id(expense_id, current_user)

@router.put("/{expense_id}", response_model=ExpenseResponse)
async def update_expense(
    expense_id: str,
    update_data: ExpenseUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AIOEngine = Depends(get_database)
):
    """
    Actualizar un gasto existente
    
    - **expense_id**: ID del gasto a actualizar
    - Campos opcionales: date, description, amount, payment_type, category, notes
    """
    expense_service = ExpenseService(db)
    return await expense_service.update_expense(expense_id, update_data, current_user)

@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(
    expense_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AIOEngine = Depends(get_database)
):
    """
    Eliminar un gasto
    
    - **expense_id**: ID del gasto a eliminar
    """
    expense_service = ExpenseService(db)
    await expense_service.delete_expense(expense_id, current_user)
    return None