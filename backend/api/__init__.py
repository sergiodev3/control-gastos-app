"""
Endpoints API para Control de Gastos
"""

from .auth import router as auth_router
from .expenses import router as expenses_router
from .incomes import router as incomes_router
from .savings import router as savings_router
from .stats import router as stats_router

__all__ = [
    "auth_router",
    "expenses_router", 
    "incomes_router",
    "savings_router",
    "stats_router"
]