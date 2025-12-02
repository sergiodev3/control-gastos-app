"""
API endpoints para estadísticas y resúmenes financieros
"""
from fastapi import APIRouter, Depends, Query, Path
from typing import Dict, Any
from datetime import datetime, timedelta
from odmantic import AIOEngine
from db.database import get_database
from models.models import User, Expense, Income, Saving, SavingType
from models.schemas import FinancialSummary
from core.security import get_current_active_user
import calendar

# Router para endpoints de estadísticas
router = APIRouter(prefix="/stats", tags=["Estadísticas"])

@router.get("/summary", response_model=FinancialSummary)
async def get_financial_summary(
    current_user: User = Depends(get_current_active_user),
    db: AIOEngine = Depends(get_database)
):
    """
    Obtener resumen financiero general del usuario
    
    Incluye totales de ingresos, gastos, ahorros y balance,
    así como desglose por categorías y tipos de pago
    """
    try:
        # Obtener todos los registros del usuario
        expenses = await db.find(Expense, Expense.user_id == current_user.id)
        incomes = await db.find(Income, Income.user_id == current_user.id)
        savings = await db.find(Saving, Saving.user_id == current_user.id)
        
        # Calcular totales
        total_expenses = sum(expense.amount for expense in expenses)
        total_incomes = sum(income.amount for income in incomes)  # Cambiado a plural
        
        # Calcular ahorros netos: depósitos - retiros
        total_savings = sum(
            saving.amount if saving.transaction_type == SavingType.DEPOSITO else -saving.amount
            for saving in savings
        )
        
        balance = total_incomes - total_expenses  # Balance = Ingresos - Gastos (los ahorros no se restan)
        
        # Gastos por categoría
        expenses_by_category = {}
        for expense in expenses:
            category = expense.category or "Sin categoría"
            expenses_by_category[category] = expenses_by_category.get(category, 0) + expense.amount
        
        # Gastos por tipo de pago
        expenses_by_payment_type = {}
        for expense in expenses:
            payment_type = expense.payment_type.value
            expenses_by_payment_type[payment_type] = expenses_by_payment_type.get(payment_type, 0) + expense.amount
        
        return FinancialSummary(
            total_incomes=round(total_incomes, 2),  # Cambiado a plural
            total_expenses=round(total_expenses, 2),
            total_savings=round(total_savings, 2),
            balance=round(balance, 2),
            expenses_by_category=expenses_by_category,
            expenses_by_payment_type=expenses_by_payment_type
        )
        
    except Exception as e:
        from fastapi import HTTPException, status
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error obteniendo resumen financiero: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.get("/monthly/{year}/{month}")
async def get_monthly_report(
    year: int = Path(..., ge=2020, le=2030, description="Año (2020-2030)"),
    month: int = Path(..., ge=1, le=12, description="Mes (1-12)"),
    current_user: User = Depends(get_current_active_user),
    db: AIOEngine = Depends(get_database)
) -> Dict[str, Any]:
    """
    Obtener reporte mensual detallado
    
    - **year**: Año del reporte
    - **month**: Mes del reporte (1-12)
    """
    try:
        # Calcular fechas de inicio y fin del mes
        start_date = datetime(year, month, 1)
        
        # Último día del mes
        last_day = calendar.monthrange(year, month)[1]
        end_date = datetime(year, month, last_day, 23, 59, 59)
        
        # Obtener registros del mes específico
        expenses = await db.find(
            Expense, 
            Expense.user_id == current_user.id,
            Expense.date >= start_date,
            Expense.date <= end_date
        )
        
        incomes = await db.find(
            Income, 
            Income.user_id == current_user.id,
            Income.date >= start_date,
            Income.date <= end_date
        )
        
        savings = await db.find(
            Saving, 
            Saving.user_id == current_user.id,
            Saving.date >= start_date,
            Saving.date <= end_date
        )
        
        # Calcular totales del mes
        total_expenses = sum(expense.amount for expense in expenses)
        total_incomes = sum(income.amount for income in incomes)  # Cambiado a plural
        total_savings = sum(saving.amount for saving in savings)
        balance = total_incomes - total_expenses - total_savings  # Actualizado
        
        # Convertir a esquemas de respuesta
        from models.schemas import ExpenseResponse, IncomeResponse, SavingResponse
        
        expense_responses = [
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
        
        income_responses = [
            IncomeResponse(
                id=str(income.id),
                user_id=str(income.user_id),
                date=income.date,
                description=income.description,
                amount=income.amount,
                source=income.source,
                notes=income.notes,
                created_at=income.created_at,
                updated_at=income.updated_at
            )
            for income in incomes
        ]
        
        saving_responses = [
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
        
        return {
            "month": calendar.month_name[month],
            "year": year,
            "total_incomes": round(total_incomes, 2),  # Cambiado a plural
            "total_expenses": round(total_expenses, 2),
            "total_savings": round(total_savings, 2),
            "balance": round(balance, 2),
            "expenses": expense_responses,
            "incomes": income_responses,
            "savings": saving_responses,
            "stats": {
                "expenses_count": len(expenses),
                "incomes_count": len(incomes),
                "savings_count": len(savings),
                "average_expense": round(total_expenses / len(expenses), 2) if expenses else 0,
                "average_income": round(total_incomes / len(incomes), 2) if incomes else 0,  # Actualizado
                "average_saving": round(total_savings / len(savings), 2) if savings else 0
            }
        }
        
    except Exception as e:
        from fastapi import HTTPException, status
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error obteniendo reporte mensual: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.get("/categories")
async def get_expense_categories(
    current_user: User = Depends(get_current_active_user),
    db: AIOEngine = Depends(get_database)
) -> Dict[str, Any]:
    """
    Obtener lista de categorías de gastos más utilizadas
    """
    try:
        expenses = await db.find(Expense, Expense.user_id == current_user.id)
        
        category_stats = {}
        for expense in expenses:
            category = expense.category or "Sin categoría"
            if category not in category_stats:
                category_stats[category] = {
                    "total_amount": 0,
                    "count": 0,
                    "average": 0
                }
            category_stats[category]["total_amount"] += expense.amount
            category_stats[category]["count"] += 1
        
        # Calcular promedios
        for category, stats in category_stats.items():
            stats["average"] = round(stats["total_amount"] / stats["count"], 2)
            stats["total_amount"] = round(stats["total_amount"], 2)
        
        # Ordenar por total gastado
        sorted_categories = dict(
            sorted(category_stats.items(), key=lambda x: x[1]["total_amount"], reverse=True)
        )
        
        return {
            "categories": sorted_categories,
            "total_categories": len(sorted_categories)
        }
        
    except Exception as e:
        from fastapi import HTTPException, status
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error obteniendo categorías: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )