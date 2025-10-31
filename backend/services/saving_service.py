"""
Servicios para gestión de ahorros
Contiene toda la lógica de negocio relacionada con ahorros
"""
from datetime import datetime
from typing import List
from fastapi import HTTPException, status
from odmantic import AIOEngine, ObjectId
from models.models import Saving, User
from models.schemas import SavingCreate, SavingUpdate, SavingResponse
import logging

logger = logging.getLogger(__name__)

class SavingService:
    """
    Servicio para operaciones con ahorros
    """
    
    def __init__(self, db: AIOEngine):
        self.db = db
    
    async def create_saving(self, saving_data: SavingCreate, user: User) -> SavingResponse:
        """
        Crear un nuevo ahorro
        """
        try:
            # Usar fecha actual si no se proporciona
            saving_date = saving_data.date if saving_data.date else datetime.utcnow()
            
            # Crear nuevo ahorro usando model_validate
            saving_data_dict = {
                "user_id": user.id,
                "date": saving_date,
                "amount": saving_data.amount,
                "purpose": saving_data.purpose,
                "goal_amount": saving_data.goal_amount,
                "notes": saving_data.notes,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            new_saving = Saving.model_validate(saving_data_dict)
            
            # Guardar en base de datos
            saved_saving = await self.db.save(new_saving)
            
            logger.info(f"Ahorro creado exitosamente para usuario {user.email}: ${saved_saving.amount}")
            
            return SavingResponse(
                id=str(saved_saving.id),
                user_id=str(saved_saving.user_id),
                date=saved_saving.date,
                amount=saved_saving.amount,
                purpose=saved_saving.purpose,
                goal_amount=saved_saving.goal_amount,
                notes=saved_saving.notes,
                created_at=saved_saving.created_at,
                updated_at=saved_saving.updated_at
            )
            
        except Exception as e:
            logger.error(f"Error creando ahorro: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    async def get_user_savings(self, user: User, skip: int = 0, limit: int = 100) -> List[SavingResponse]:
        """
        Obtener ahorros del usuario
        """
        try:
            savings = await self.db.find(
                Saving, 
                Saving.user_id == user.id,
                skip=skip, 
                limit=limit
            )
            
            # Ordenar por fecha (más recientes primero)
            savings = sorted(savings, key=lambda x: x.date, reverse=True)
            
            return [
                SavingResponse(
                    id=str(saving.id),
                    user_id=str(saving.user_id),
                    date=saving.date,
                    amount=saving.amount,
                    purpose=saving.purpose,
                    goal_amount=saving.goal_amount,
                    notes=saving.notes,
                    created_at=saving.created_at,
                    updated_at=saving.updated_at
                )
                for saving in savings
            ]
            
        except Exception as e:
            logger.error(f"Error obteniendo ahorros: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    async def get_saving_by_id(self, saving_id: str, user: User) -> SavingResponse:
        """
        Obtener un ahorro específico por ID
        """
        try:
            saving = await self.db.find_one(Saving, Saving.id == ObjectId(saving_id))
            
            if not saving:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Ahorro no encontrado"
                )
            
            # Verificar que el ahorro pertenece al usuario
            if saving.user_id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tienes permisos para acceder a este ahorro"
                )
            
            return SavingResponse(
                id=str(saving.id),
                user_id=str(saving.user_id),
                date=saving.date,
                amount=saving.amount,
                purpose=saving.purpose,
                goal_amount=saving.goal_amount,
                notes=saving.notes,
                created_at=saving.created_at,
                updated_at=saving.updated_at
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error obteniendo ahorro por ID: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    async def update_saving(self, saving_id: str, update_data: SavingUpdate, user: User) -> SavingResponse:
        """
        Actualizar un ahorro
        """
        try:
            saving = await self.db.find_one(Saving, Saving.id == ObjectId(saving_id))
            
            if not saving:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Ahorro no encontrado"
                )
            
            # Verificar que el ahorro pertenece al usuario
            if saving.user_id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tienes permisos para modificar este ahorro"
                )
            
            # Actualizar campos que no son None
            update_fields = {}
            if update_data.date is not None:
                update_fields["date"] = update_data.date
            if update_data.amount is not None:
                update_fields["amount"] = update_data.amount
            if update_data.purpose is not None:
                update_fields["purpose"] = update_data.purpose
            if update_data.goal_amount is not None:
                update_fields["goal_amount"] = update_data.goal_amount
            if update_data.notes is not None:
                update_fields["notes"] = update_data.notes
            
            if update_fields:
                update_fields["updated_at"] = datetime.utcnow()
                
                # Actualizar ahorro
                for field, value in update_fields.items():
                    setattr(saving, field, value)
                
                updated_saving = await self.db.save(saving)
                logger.info(f"Ahorro actualizado exitosamente: {saving_id}")
                
                return SavingResponse(
                    id=str(updated_saving.id),
                    user_id=str(updated_saving.user_id),
                    date=updated_saving.date,
                    amount=updated_saving.amount,
                    purpose=updated_saving.purpose,
                    goal_amount=updated_saving.goal_amount,
                    notes=updated_saving.notes,
                    created_at=updated_saving.created_at,
                    updated_at=updated_saving.updated_at
                )
            else:
                # No hay cambios
                return await self.get_saving_by_id(saving_id, user)
                
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error actualizando ahorro: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    async def delete_saving(self, saving_id: str, user: User) -> bool:
        """
        Eliminar un ahorro
        """
        try:
            saving = await self.db.find_one(Saving, Saving.id == ObjectId(saving_id))
            
            if not saving:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Ahorro no encontrado"
                )
            
            # Verificar que el ahorro pertenece al usuario
            if saving.user_id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tienes permisos para eliminar este ahorro"
                )
            
            # Eliminar ahorro
            await self.db.delete(saving)
            logger.info(f"Ahorro eliminado exitosamente: {saving_id}")
            
            return True
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error eliminando ahorro: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )