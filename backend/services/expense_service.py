"""
Servicios para gestión de gastos
Contiene toda la lógica de negocio relacionada con gastos
"""
from datetime import datetime
from typing import List, Optional
from fastapi import HTTPException, status
from odmantic import AIOEngine, ObjectId
from models.models import Expense, User
from models.schemas import ExpenseCreate, ExpenseUpdate, ExpenseResponse
import logging

logger = logging.getLogger(__name__)

class ExpenseService:
    """
    Servicio para operaciones con gastos
    """
    
    def __init__(self, db: AIOEngine):
        self.db = db
    
    async def create_expense(self, expense_data: ExpenseCreate, user: User) -> ExpenseResponse:
        """
        Crear un nuevo gasto
        """
        try:
            # Usar fecha actual si no se proporciona
            expense_date = expense_data.date if expense_data.date else datetime.utcnow()
            
            # Crear nuevo gasto usando model_validate
            expense_data_dict = {
                "user_id": user.id,
                "date": expense_date,
                "description": expense_data.description,
                "amount": expense_data.amount,
                "payment_type": expense_data.payment_type,
                "category": expense_data.category,
                "notes": expense_data.notes,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            new_expense = Expense.model_validate(expense_data_dict)
            
            # Guardar en base de datos
            saved_expense = await self.db.save(new_expense)
            
            logger.info(f"Gasto creado exitosamente para usuario {user.email}: ${saved_expense.amount}")
            
            return ExpenseResponse(
                id=str(saved_expense.id),
                user_id=str(saved_expense.user_id),
                date=saved_expense.date,
                description=saved_expense.description,
                amount=saved_expense.amount,
                payment_type=saved_expense.payment_type,
                category=saved_expense.category,
                notes=saved_expense.notes,
                created_at=saved_expense.created_at,
                updated_at=saved_expense.updated_at
            )
            
        except Exception as e:
            logger.error(f"Error creando gasto: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    async def get_user_expenses(self, user: User, skip: int = 0, limit: int = 100) -> List[ExpenseResponse]:
        """
        Obtener gastos del usuario
        """
        try:
            expenses = await self.db.find(
                Expense, 
                Expense.user_id == user.id,
                skip=skip, 
                limit=limit
            )
            
            # Ordenar por fecha (más recientes primero)
            expenses = sorted(expenses, key=lambda x: x.date, reverse=True)
            
            return [
                ExpenseResponse(
                    id=str(expense.id),
                    user_id=str(expense.user_id),
                    date=expense.date,
                    description=expense.description,
                    amount=expense.amount,
                    payment_type=expense.payment_type,
                    category=expense.category,
                    notes=expense.notes,
                    created_at=expense.created_at,
                    updated_at=expense.updated_at
                )
                for expense in expenses
            ]
            
        except Exception as e:
            logger.error(f"Error obteniendo gastos: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    async def get_expense_by_id(self, expense_id: str, user: User) -> ExpenseResponse:
        """
        Obtener un gasto específico por ID
        """
        try:
            expense = await self.db.find_one(Expense, Expense.id == ObjectId(expense_id))
            
            if not expense:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Gasto no encontrado"
                )
            
            # Verificar que el gasto pertenece al usuario
            if expense.user_id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tienes permisos para acceder a este gasto"
                )
            
            return ExpenseResponse(
                id=str(expense.id),
                user_id=str(expense.user_id),
                date=expense.date,
                description=expense.description,
                amount=expense.amount,
                payment_type=expense.payment_type,
                category=expense.category,
                notes=expense.notes,
                created_at=expense.created_at,
                updated_at=expense.updated_at
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error obteniendo gasto por ID: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    async def update_expense(self, expense_id: str, update_data: ExpenseUpdate, user: User) -> ExpenseResponse:
        """
        Actualizar un gasto
        """
        try:
            expense = await self.db.find_one(Expense, Expense.id == ObjectId(expense_id))
            
            if not expense:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Gasto no encontrado"
                )
            
            # Verificar que el gasto pertenece al usuario
            if expense.user_id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tienes permisos para modificar este gasto"
                )
            
            # Actualizar campos que no son None
            update_fields = {}
            if update_data.date is not None:
                update_fields["date"] = update_data.date
            if update_data.description is not None:
                update_fields["description"] = update_data.description
            if update_data.amount is not None:
                update_fields["amount"] = update_data.amount
            if update_data.payment_type is not None:
                update_fields["payment_type"] = update_data.payment_type
            if update_data.category is not None:
                update_fields["category"] = update_data.category
            if update_data.notes is not None:
                update_fields["notes"] = update_data.notes
            
            if update_fields:
                update_fields["updated_at"] = datetime.utcnow()
                
                # Actualizar gasto
                for field, value in update_fields.items():
                    setattr(expense, field, value)
                
                updated_expense = await self.db.save(expense)
                logger.info(f"Gasto actualizado exitosamente: {expense_id}")
                
                return ExpenseResponse(
                    id=str(updated_expense.id),
                    user_id=str(updated_expense.user_id),
                    date=updated_expense.date,
                    description=updated_expense.description,
                    amount=updated_expense.amount,
                    payment_type=updated_expense.payment_type,
                    category=updated_expense.category,
                    notes=updated_expense.notes,
                    created_at=updated_expense.created_at,
                    updated_at=updated_expense.updated_at
                )
            else:
                # No hay cambios
                return await self.get_expense_by_id(expense_id, user)
                
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error actualizando gasto: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    async def delete_expense(self, expense_id: str, user: User) -> bool:
        """
        Eliminar un gasto
        """
        try:
            expense = await self.db.find_one(Expense, Expense.id == ObjectId(expense_id))
            
            if not expense:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Gasto no encontrado"
                )
            
            # Verificar que el gasto pertenece al usuario
            if expense.user_id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tienes permisos para eliminar este gasto"
                )
            
            # Eliminar gasto
            await self.db.delete(expense)
            logger.info(f"Gasto eliminado exitosamente: {expense_id}")
            
            return True
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error eliminando gasto: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )