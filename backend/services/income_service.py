"""
Servicios para gestión de ingresos
Contiene toda la lógica de negocio relacionada con ingresos
"""
from datetime import datetime
from typing import List
from fastapi import HTTPException, status
from odmantic import AIOEngine, ObjectId
from models.models import Income, User
from models.schemas import IncomeCreate, IncomeUpdate, IncomeResponse
import logging

logger = logging.getLogger(__name__)

class IncomeService:
    """
    Servicio para operaciones con ingresos
    """
    
    def __init__(self, db: AIOEngine):
        self.db = db
    
    async def create_income(self, income_data: IncomeCreate, user: User) -> IncomeResponse:
        """
        Crear un nuevo ingreso
        """
        try:
            # Usar fecha actual si no se proporciona
            income_date = income_data.date if income_data.date else datetime.utcnow()
            
            # Crear nuevo ingreso usando model_validate
            income_data_dict = {
                "user_id": user.id,
                "date": income_date,
                "description": income_data.description,
                "amount": income_data.amount,
                "source": income_data.source,
                "is_recurring": income_data.is_recurring if income_data.is_recurring is not None else False,
                "notes": income_data.notes,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            new_income = Income.model_validate(income_data_dict)
            
            # Guardar en base de datos
            saved_income = await self.db.save(new_income)
            
            logger.info(f"Ingreso creado exitosamente para usuario {user.email}: ${saved_income.amount}")
            
            return IncomeResponse(
                id=str(saved_income.id),
                user_id=str(saved_income.user_id),
                date=saved_income.date,
                description=saved_income.description,
                amount=saved_income.amount,
                source=saved_income.source,
                is_recurring=saved_income.is_recurring,
                notes=saved_income.notes,
                created_at=saved_income.created_at,
                updated_at=saved_income.updated_at
            )
            
        except Exception as e:
            logger.error(f"Error creando ingreso: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    async def get_user_incomes(self, user: User, skip: int = 0, limit: int = 100) -> List[IncomeResponse]:
        """
        Obtener ingresos del usuario
        """
        try:
            incomes = await self.db.find(
                Income, 
                Income.user_id == user.id,
                skip=skip, 
                limit=limit
            )
            
            # Ordenar por fecha (más recientes primero)
            incomes = sorted(incomes, key=lambda x: x.date, reverse=True)
            
            return [
                IncomeResponse(
                    id=str(income.id),
                    user_id=str(income.user_id),
                    date=income.date,
                    description=income.description,
                    amount=income.amount,
                    source=income.source,
                    is_recurring=getattr(income, 'is_recurring', False),
                    notes=income.notes,
                    created_at=income.created_at,
                    updated_at=income.updated_at
                )
                for income in incomes
            ]
            
        except Exception as e:
            logger.error(f"Error obteniendo ingresos: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    async def get_income_by_id(self, income_id: str, user: User) -> IncomeResponse:
        """
        Obtener un ingreso específico por ID
        """
        try:
            income = await self.db.find_one(Income, Income.id == ObjectId(income_id))
            
            if not income:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Ingreso no encontrado"
                )
            
            # Verificar que el ingreso pertenece al usuario
            if income.user_id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tienes permisos para acceder a este ingreso"
                )
            
            return IncomeResponse(
                id=str(income.id),
                user_id=str(income.user_id),
                date=income.date,
                description=income.description,
                amount=income.amount,
                source=income.source,
                is_recurring=getattr(income, 'is_recurring', False),
                notes=income.notes,
                created_at=income.created_at,
                updated_at=income.updated_at
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error obteniendo ingreso por ID: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    async def update_income(self, income_id: str, update_data: IncomeUpdate, user: User) -> IncomeResponse:
        """
        Actualizar un ingreso
        """
        try:
            income = await self.db.find_one(Income, Income.id == ObjectId(income_id))
            
            if not income:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Ingreso no encontrado"
                )
            
            # Verificar que el ingreso pertenece al usuario
            if income.user_id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tienes permisos para modificar este ingreso"
                )
            
            # Actualizar campos que no son None
            update_fields = {}
            if update_data.date is not None:
                update_fields["date"] = update_data.date
            if update_data.description is not None:
                update_fields["description"] = update_data.description
            if update_data.amount is not None:
                update_fields["amount"] = update_data.amount
            if update_data.source is not None:
                update_fields["source"] = update_data.source
            if update_data.is_recurring is not None:
                update_fields["is_recurring"] = update_data.is_recurring
            if update_data.notes is not None:
                update_fields["notes"] = update_data.notes
            
            if update_fields:
                update_fields["updated_at"] = datetime.utcnow()
                
                # Actualizar ingreso
                for field, value in update_fields.items():
                    setattr(income, field, value)
                
                updated_income = await self.db.save(income)
                logger.info(f"Ingreso actualizado exitosamente: {income_id}")
                
                return IncomeResponse(
                    id=str(updated_income.id),
                    user_id=str(updated_income.user_id),
                    date=updated_income.date,
                    description=updated_income.description,
                    amount=updated_income.amount,
                    source=updated_income.source,
                    is_recurring=getattr(updated_income, 'is_recurring', False),
                    notes=updated_income.notes,
                    created_at=updated_income.created_at,
                    updated_at=updated_income.updated_at
                )
            else:
                # No hay cambios
                return await self.get_income_by_id(income_id, user)
                
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error actualizando ingreso: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    async def delete_income(self, income_id: str, user: User) -> bool:
        """
        Eliminar un ingreso
        """
        try:
            income = await self.db.find_one(Income, Income.id == ObjectId(income_id))
            
            if not income:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Ingreso no encontrado"
                )
            
            # Verificar que el ingreso pertenece al usuario
            if income.user_id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tienes permisos para eliminar este ingreso"
                )
            
            # Eliminar ingreso
            await self.db.delete(income)
            logger.info(f"Ingreso eliminado exitosamente: {income_id}")
            
            return True
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error eliminando ingreso: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )