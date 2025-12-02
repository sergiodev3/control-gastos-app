"""
Esquemas Pydantic para validación de entrada y salida de la API
Separamos los modelos de base de datos de los esquemas de API para mayor flexibilidad
"""
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from models.models import PaymentType, SavingType

# === ESQUEMAS DE USUARIO ===

class UserCreate(BaseModel):
    """Esquema para crear un nuevo usuario"""
    email: EmailStr
    username: str = Field(min_length=3, max_length=50)
    full_name: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=8, max_length=100)
    
    @validator('password')
    def validate_password(cls, v):
        """Validar que la contraseña tenga al menos una letra y un número"""
        if not any(c.isalpha() for c in v):
            raise ValueError('La contraseña debe contener al menos una letra')
        if not any(c.isdigit() for c in v):
            raise ValueError('La contraseña debe contener al menos un número')
        return v

class UserLogin(BaseModel):
    """Esquema para login de usuario"""
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    """Esquema de respuesta de usuario (sin contraseña)"""
    id: str
    email: EmailStr
    username: str
    full_name: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    """Esquema para actualizar datos de usuario"""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, min_length=1, max_length=100)

# === ESQUEMAS DE AUTENTICACIÓN ===

class Token(BaseModel):
    """Esquema de respuesta de token de acceso"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse

class TokenData(BaseModel):
    """Datos contenidos en el token"""
    user_id: Optional[str] = None

# === ESQUEMAS DE GASTOS ===

class ExpenseCreate(BaseModel):
    """Esquema para crear un nuevo gasto"""
    date: Optional[datetime] = None
    description: str = Field(min_length=1, max_length=200)
    amount: float = Field(gt=0)
    payment_type: PaymentType
    category: Optional[str] = Field(None, max_length=50)
    notes: Optional[str] = Field(None, max_length=500)
    
    @validator('amount')
    def validate_amount(cls, v):
        if round(v, 2) != v:
            raise ValueError('El monto debe tener máximo 2 decimales')
        return v

class ExpenseUpdate(BaseModel):
    """Esquema para actualizar un gasto"""
    date: Optional[datetime] = None
    description: Optional[str] = Field(None, min_length=1, max_length=200)
    amount: Optional[float] = Field(None, gt=0)
    payment_type: Optional[PaymentType] = None
    category: Optional[str] = Field(None, max_length=50)
    notes: Optional[str] = Field(None, max_length=500)
    
    @validator('amount')
    def validate_amount(cls, v):
        if v is not None and round(v, 2) != v:
            raise ValueError('El monto debe tener máximo 2 decimales')
        return v

class ExpenseResponse(BaseModel):
    """Esquema de respuesta de gasto"""
    id: str
    user_id: str
    date: datetime
    description: str
    amount: float
    payment_type: PaymentType
    category: Optional[str]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# === ESQUEMAS DE INGRESOS ===

class IncomeCreate(BaseModel):
    """Esquema para crear un nuevo ingreso"""
    date: Optional[datetime] = None
    description: str = Field(min_length=1, max_length=200)
    amount: float = Field(gt=0)
    source: Optional[str] = Field(None, max_length=50)
    is_recurring: Optional[bool] = Field(default=False)
    notes: Optional[str] = Field(None, max_length=500)
    
    @validator('amount')
    def validate_amount(cls, v):
        if round(v, 2) != v:
            raise ValueError('El monto debe tener máximo 2 decimales')
        return v

class IncomeUpdate(BaseModel):
    """Esquema para actualizar un ingreso"""
    date: Optional[datetime] = None
    description: Optional[str] = Field(None, min_length=1, max_length=200)
    amount: Optional[float] = Field(None, gt=0)
    source: Optional[str] = Field(None, max_length=50)
    is_recurring: Optional[bool] = None
    notes: Optional[str] = Field(None, max_length=500)
    
    @validator('amount')
    def validate_amount(cls, v):
        if v is not None and round(v, 2) != v:
            raise ValueError('El monto debe tener máximo 2 decimales')
        return v

class IncomeResponse(BaseModel):
    """Esquema de respuesta de ingreso"""
    id: str
    user_id: str
    date: datetime
    description: str
    amount: float
    source: Optional[str]
    is_recurring: bool
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# === ESQUEMAS DE AHORROS ===

class SavingCreate(BaseModel):
    """Esquema para crear un nuevo ahorro o retiro"""
    date: Optional[datetime] = None
    amount: float = Field(gt=0)
    transaction_type: SavingType = Field(default=SavingType.DEPOSITO)
    purpose: str = Field(min_length=1, max_length=200)
    goal_amount: Optional[float] = Field(None, gt=0)
    notes: Optional[str] = Field(None, max_length=500)
    
    @validator('amount', 'goal_amount')
    def validate_amounts(cls, v):
        if v is not None and round(v, 2) != v:
            raise ValueError('El monto debe tener máximo 2 decimales')
        return v

class SavingUpdate(BaseModel):
    """Esquema para actualizar un ahorro o retiro"""
    date: Optional[datetime] = None
    amount: Optional[float] = Field(None, gt=0)
    transaction_type: Optional[SavingType] = None
    purpose: Optional[str] = Field(None, min_length=1, max_length=200)
    goal_amount: Optional[float] = Field(None, gt=0)
    notes: Optional[str] = Field(None, max_length=500)
    
    @validator('amount', 'goal_amount')
    def validate_amounts(cls, v):
        if v is not None and round(v, 2) != v:
            raise ValueError('El monto debe tener máximo 2 decimales')
        return v

class SavingResponse(BaseModel):
    """Esquema de respuesta de ahorro o retiro"""
    id: str
    user_id: str
    date: datetime
    amount: float
    transaction_type: SavingType
    purpose: str
    goal_amount: Optional[float]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# === ESQUEMAS DE RESUMEN Y ESTADÍSTICAS ===

class FinancialSummary(BaseModel):
    """Resumen financiero del usuario"""
    total_incomes: float  # Cambiado a plural para coincidir con frontend
    total_expenses: float
    total_savings: float
    balance: float
    expenses_by_category: dict
    expenses_by_payment_type: dict

class MonthlyReport(BaseModel):
    """Reporte mensual"""
    month: str
    year: int
    total_incomes: float  # Cambiado a plural
    total_expenses: float
    total_savings: float
    balance: float
    expenses: List[ExpenseResponse]
    incomes: List[IncomeResponse]
    savings: List[SavingResponse]