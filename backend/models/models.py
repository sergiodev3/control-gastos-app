"""
Modelos de datos para la aplicación
Utilizamos ODMantic que es un ODM moderno para MongoDB con soporte completo de tipos
"""
from odmantic import Model, Field, ObjectId
from pydantic import EmailStr, validator
from typing import Optional
from datetime import datetime
from enum import Enum

class PaymentType(str, Enum):
    """
    Tipos de pago disponibles para los gastos
    """
    EFECTIVO = "efectivo"
    TARJETA_DEBITO = "tarjeta_debito"
    TARJETA_CREDITO = "tarjeta_credito"
    TRANSFERENCIA = "transferencia"
    PAYPAL = "paypal"
    OTRO = "otro"

class User(Model):
    """
    Modelo de usuario del sistema
    Incluye campos básicos para autenticación y perfil
    """
    email: EmailStr = Field(unique=True)
    username: str = Field(min_length=3, max_length=50)
    full_name: str = Field(min_length=1, max_length=100)
    hashed_password: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Expense(Model):
    """
    Modelo para registrar gastos
    Contiene información detallada de cada gasto realizado
    """
    user_id: ObjectId = Field(...)  # Referencia al usuario
    date: datetime = Field(default_factory=datetime.utcnow)
    description: str = Field(min_length=1, max_length=200)
    amount: float = Field(gt=0)  # Mayor que 0
    payment_type: PaymentType
    category: Optional[str] = Field(default=None, max_length=50)
    notes: Optional[str] = Field(default=None, max_length=500)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    @validator('amount')
    def validate_amount(cls, v):
        """Validar que el monto sea positivo y tenga máximo 2 decimales"""
        if v <= 0:
            raise ValueError('El monto debe ser mayor que 0')
        if round(v, 2) != v:
            raise ValueError('El monto debe tener máximo 2 decimales')
        return v

class Income(Model):
    """
    Modelo para registrar ingresos
    Registra todas las fuentes de ingresos del usuario
    """
    user_id: ObjectId = Field(...)  # Referencia al usuario
    date: datetime = Field(default_factory=datetime.utcnow)
    description: str = Field(min_length=1, max_length=200)
    amount: float = Field(gt=0)  # Mayor que 0
    source: Optional[str] = Field(default=None, max_length=50)
    notes: Optional[str] = Field(default=None, max_length=500)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    @validator('amount')
    def validate_amount(cls, v):
        """Validar que el monto sea positivo y tenga máximo 2 decimales"""
        if v <= 0:
            raise ValueError('El monto debe ser mayor que 0')
        if round(v, 2) != v:
            raise ValueError('El monto debe tener máximo 2 decimales')
        return v

class Saving(Model):
    """
    Modelo para registrar ahorros
    Permite llevar control de metas y ahorros del usuario
    """
    user_id: ObjectId = Field(...)  # Referencia al usuario
    date: datetime = Field(default_factory=datetime.utcnow)
    amount: float = Field(gt=0)  # Mayor que 0
    purpose: str = Field(min_length=1, max_length=200)
    goal_amount: Optional[float] = Field(default=None, gt=0)
    notes: Optional[str] = Field(default=None, max_length=500)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    @validator('amount', 'goal_amount')
    def validate_amounts(cls, v):
        """Validar que los montos sean positivos y tengan máximo 2 decimales"""
        if v is not None:
            if v <= 0:
                raise ValueError('El monto debe ser mayor que 0')
            if round(v, 2) != v:
                raise ValueError('El monto debe tener máximo 2 decimales')
        return v