"""
Cliente HTTP para comunicación con el backend de Control de Gastos
"""
import httpx
from typing import Optional, Dict, Any, List
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

class APIClient:
    """Cliente para interactuar con el backend API"""
    
    def __init__(self):
        self.base_url = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")
        self.token = os.getenv("API_TOKEN", "")
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
    
    async def _request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Any:
        """Realizar petición HTTP al backend"""
        async with httpx.AsyncClient() as client:
            url = f"{self.base_url}{endpoint}"
            response = await client.request(
                method=method,
                url=url,
                headers=self.headers,
                json=data,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    
    # === GASTOS ===
    
    async def create_expense(
        self,
        description: str,
        amount: float,
        payment_type: str,
        category: Optional[str] = None,
        notes: Optional[str] = None,
        date: Optional[str] = None
    ) -> Dict[str, Any]:
        """Crear un nuevo gasto"""
        data = {
            "description": description,
            "amount": amount,
            "payment_type": payment_type,
            "category": category,
            "notes": notes
        }
        if date:
            data["date"] = date
        return await self._request("POST", "/expenses", data)
    
    async def get_expenses(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Obtener lista de gastos"""
        result = await self._request("GET", f"/expenses?limit={limit}")
        return result if isinstance(result, list) else []
    
    async def delete_expense(self, expense_id: str) -> None:
        """Eliminar un gasto"""
        await self._request("DELETE", f"/expenses/{expense_id}")
    
    # === INGRESOS ===
    
    async def create_income(
        self,
        description: str,
        amount: float,
        source: Optional[str] = None,
        is_recurring: bool = False,
        notes: Optional[str] = None,
        date: Optional[str] = None
    ) -> Dict[str, Any]:
        """Crear un nuevo ingreso"""
        data = {
            "description": description,
            "amount": amount,
            "source": source,
            "is_recurring": is_recurring,
            "notes": notes
        }
        if date:
            data["date"] = date
        return await self._request("POST", "/incomes", data)
    
    async def get_incomes(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Obtener lista de ingresos"""
        result = await self._request("GET", f"/incomes?limit={limit}")
        return result if isinstance(result, list) else []
    
    async def delete_income(self, income_id: str) -> None:
        """Eliminar un ingreso"""
        await self._request("DELETE", f"/incomes/{income_id}")
    
    # === AHORROS ===
    
    async def create_saving(
        self,
        amount: float,
        purpose: str,
        transaction_type: str = "deposito",
        goal_amount: Optional[float] = None,
        notes: Optional[str] = None,
        date: Optional[str] = None
    ) -> Dict[str, Any]:
        """Crear un nuevo ahorro o retiro"""
        data = {
            "amount": amount,
            "transaction_type": transaction_type,
            "purpose": purpose,
            "goal_amount": goal_amount,
            "notes": notes
        }
        if date:
            data["date"] = date
        return await self._request("POST", "/savings", data)
    
    async def get_savings(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Obtener lista de ahorros"""
        result = await self._request("GET", f"/savings?limit={limit}")
        return result if isinstance(result, list) else []
    
    async def delete_saving(self, saving_id: str) -> None:
        """Eliminar un ahorro"""
        await self._request("DELETE", f"/savings/{saving_id}")
    
    # === ESTADÍSTICAS ===
    
    async def get_summary(self) -> Dict[str, Any]:
        """Obtener resumen financiero general"""
        return await self._request("GET", "/stats/summary")
    
    async def get_monthly_report(self, year: int, month: int) -> Dict[str, Any]:
        """Obtener reporte mensual"""
        return await self._request("GET", f"/stats/monthly/{year}/{month}")
