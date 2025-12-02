"""
MCP Server para Control de Gastos
Servidor de Model Context Protocol para gestión de finanzas personales
"""
from fastmcp import FastMCP
from typing import Optional
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from api_client import APIClient
from utils import (
    parse_amount, 
    infer_payment_type, 
    infer_category,
    format_currency,
    format_date,
    parse_transaction_type,
    is_recurring,
    extract_purpose
)

# Zona horaria por defecto (México)
DEFAULT_TIMEZONE = ZoneInfo("America/Mexico_City")

# Inicializar MCP server
mcp = FastMCP("Control de Gastos")

# Cliente API
api = APIClient()

# === HERRAMIENTAS PARA GASTOS ===

@mcp.tool()
async def registrar_gasto(
    descripcion: str,
    monto: float,
    tipo_pago: Optional[str] = None,
    categoria: Optional[str] = None,
    notas: Optional[str] = None
) -> str:
    """
    Registrar un nuevo gasto en el sistema.
    
    Ejemplos de uso:
    - "Registra un gasto de $150 en el super con tarjeta de crédito"
    - "Gasté 500 pesos en gasolina en efectivo"
    - "Compré libros por $300"
    
    Args:
        descripcion: Descripción del gasto (ej: "Compra de supermercado")
        monto: Cantidad del gasto en pesos mexicanos
        tipo_pago: Tipo de pago (efectivo, tarjeta_debito, tarjeta_credito, transferencia, paypal, otro)
        categoria: Categoría del gasto (Alimentación, Transporte, etc.)
        notas: Notas adicionales opcionales
    
    Returns:
        Confirmación del gasto registrado con detalles
    """
    try:
        # Inferir tipo de pago si no se proporciona
        if not tipo_pago:
            tipo_pago = infer_payment_type(descripcion + " " + (notas or ""))
        
        # Inferir categoría si no se proporciona
        if not categoria:
            categoria = infer_category(descripcion + " " + (notas or ""))
        
        # Obtener fecha/hora actual en zona horaria local
        local_datetime = datetime.now(DEFAULT_TIMEZONE)
        date_str = local_datetime.isoformat()
        
        # Crear gasto
        result = await api.create_expense(
            description=descripcion,
            amount=monto,
            payment_type=tipo_pago,
            category=categoria,
            notes=notas,
            date=date_str
        )
        
        return f"""✅ Gasto registrado exitosamente:

💰 Monto: {format_currency(monto)}
📝 Descripción: {descripcion}
💳 Tipo de pago: {tipo_pago}
📂 Categoría: {categoria or 'Sin categoría'}
📅 Fecha: {format_date(result['date'])}
🆔 ID: {result['id']}
"""
    except Exception as e:
        return f"❌ Error al registrar el gasto: {str(e)}"

@mcp.tool()
async def listar_gastos(limite: int = 10) -> str:
    """
    Listar los gastos más recientes.
    
    Ejemplos de uso:
    - "Muéstrame mis últimos gastos"
    - "¿Cuáles son mis gastos recientes?"
    - "Lista mis últimos 5 gastos"
    
    Args:
        limite: Número máximo de gastos a mostrar (default: 10)
    
    Returns:
        Lista formateada de gastos recientes
    """
    try:
        expenses = await api.get_expenses(limit=limite)
        
        if not expenses:
            return "📋 No tienes gastos registrados aún."
        
        output = f"📋 Últimos {len(expenses)} gastos:\n\n"
        
        total = 0
        for expense in expenses:
            total += expense['amount']
            output += f"""💸 {format_currency(expense['amount'])}
   📝 {expense['description']}
   💳 {expense['payment_type']}
   📂 {expense.get('category', 'Sin categoría')}
   📅 {format_date(expense['date'])}
   
"""
        
        output += f"\n💰 Total: {format_currency(total)}"
        return output
        
    except Exception as e:
        return f"❌ Error al listar gastos: {str(e)}"

# === HERRAMIENTAS PARA INGRESOS ===

@mcp.tool()
async def registrar_ingreso(
    descripcion: str,
    monto: float,
    fuente: Optional[str] = None,
    recurrente: Optional[bool] = None,
    notas: Optional[str] = None
) -> str:
    """
    Registrar un nuevo ingreso en el sistema.
    
    Ejemplos de uso:
    - "Registra mi salario mensual de $15,000"
    - "Recibí $500 de freelance"
    - "Ingreso recurrente de renta por $8,000"
    
    Args:
        descripcion: Descripción del ingreso (ej: "Salario mensual")
        monto: Cantidad del ingreso en pesos mexicanos
        fuente: Fuente del ingreso (ej: "Trabajo", "Freelance", "Renta")
        recurrente: Si es un ingreso mensual recurrente
        notas: Notas adicionales opcionales
    
    Returns:
        Confirmación del ingreso registrado con detalles
    """
    try:
        # Determinar si es recurrente si no se especifica
        if recurrente is None:
            recurrente = is_recurring(descripcion + " " + (notas or ""))
        
        # Obtener fecha/hora actual en zona horaria local
        local_datetime = datetime.now(DEFAULT_TIMEZONE)
        date_str = local_datetime.isoformat()
        
        # Crear ingreso
        result = await api.create_income(
            description=descripcion,
            amount=monto,
            source=fuente,
            is_recurring=recurrente,
            notes=notas,
            date=date_str
        )
        
        recurring_text = "📅 Recurrente mensual" if recurrente else "📅 Ingreso único"
        
        return f"""✅ Ingreso registrado exitosamente:

💰 Monto: {format_currency(monto)}
📝 Descripción: {descripcion}
🏢 Fuente: {fuente or 'No especificada'}
{recurring_text}
📅 Fecha: {format_date(result['date'])}
🆔 ID: {result['id']}
"""
    except Exception as e:
        return f"❌ Error al registrar el ingreso: {str(e)}"

@mcp.tool()
async def listar_ingresos(limite: int = 10) -> str:
    """
    Listar los ingresos más recientes.
    
    Ejemplos de uso:
    - "Muéstrame mis ingresos"
    - "¿Cuáles son mis ingresos recientes?"
    - "Lista mis últimos ingresos"
    
    Args:
        limite: Número máximo de ingresos a mostrar (default: 10)
    
    Returns:
        Lista formateada de ingresos recientes
    """
    try:
        incomes = await api.get_incomes(limit=limite)
        
        if not incomes:
            return "📋 No tienes ingresos registrados aún."
        
        output = f"📋 Últimos {len(incomes)} ingresos:\n\n"
        
        total = 0
        for income in incomes:
            total += income['amount']
            recurring = "📅 Recurrente" if income.get('is_recurring', False) else ""
            output += f"""💵 {format_currency(income['amount'])}
   📝 {income['description']}
   🏢 {income.get('source', 'No especificada')}
   {recurring}
   📅 {format_date(income['date'])}
   
"""
        
        output += f"\n💰 Total: {format_currency(total)}"
        return output
        
    except Exception as e:
        return f"❌ Error al listar ingresos: {str(e)}"

# === HERRAMIENTAS PARA AHORROS ===

@mcp.tool()
async def registrar_ahorro(
    monto: float,
    proposito: str,
    es_retiro: bool = False,
    meta: Optional[float] = None,
    notas: Optional[str] = None
) -> str:
    """
    Registrar un depósito o retiro de ahorro.
    
    Ejemplos de uso:
    - "Ahorra $1,000 para el auto con meta de $50,000"
    - "Deposita 500 pesos para vacaciones"
    - "Retira $200 del ahorro de emergencias"
    
    Args:
        monto: Cantidad a ahorrar o retirar en pesos mexicanos
        proposito: Propósito o meta del ahorro (ej: "Auto nuevo", "Vacaciones", "Emergencias")
        es_retiro: True si es un retiro, False si es un depósito (default: False)
        meta: Meta de ahorro total para este propósito (opcional)
        notas: Notas adicionales opcionales
    
    Returns:
        Confirmación del ahorro/retiro registrado con detalles
    """
    try:
        transaction_type = "retiro" if es_retiro else "deposito"
        
        # Obtener fecha/hora actual en zona horaria local
        local_datetime = datetime.now(DEFAULT_TIMEZONE)
        date_str = local_datetime.isoformat()
        
        # Crear ahorro
        result = await api.create_saving(
            amount=monto,
            purpose=proposito,
            transaction_type=transaction_type,
            goal_amount=meta,
            notes=notas,
            date=date_str
        )
        
        action = "💸 Retiro" if es_retiro else "💰 Depósito"
        meta_text = f"\n🎯 Meta: {format_currency(meta)}" if meta else ""
        
        return f"""✅ {action} registrado exitosamente:

💵 Monto: {format_currency(monto)}
🎯 Propósito: {proposito}{meta_text}
📅 Fecha: {format_date(result['date'])}
🆔 ID: {result['id']}
"""
    except Exception as e:
        return f"❌ Error al registrar el ahorro: {str(e)}"

@mcp.tool()
async def listar_ahorros(limite: int = 10) -> str:
    """
    Listar los movimientos de ahorro más recientes.
    
    Ejemplos de uso:
    - "Muéstrame mis ahorros"
    - "¿Cuánto tengo ahorrado?"
    - "Lista mis movimientos de ahorro"
    
    Args:
        limite: Número máximo de movimientos a mostrar (default: 10)
    
    Returns:
        Lista formateada de movimientos de ahorro recientes
    """
    try:
        savings = await api.get_savings(limit=limite)
        
        if not savings:
            return "📋 No tienes ahorros registrados aún."
        
        output = f"📋 Últimos {len(savings)} movimientos de ahorro:\n\n"
        
        total = 0
        for saving in savings:
            is_withdrawal = saving.get('transaction_type') == 'retiro'
            amount = -saving['amount'] if is_withdrawal else saving['amount']
            total += amount
            
            icon = "💸" if is_withdrawal else "💰"
            sign = "-" if is_withdrawal else "+"
            
            output += f"""{icon} {sign}{format_currency(saving['amount'])}
   🎯 {saving['purpose']}
   📅 {format_date(saving['date'])}
   
"""
        
        output += f"\n💵 Total ahorrado: {format_currency(total)}"
        return output
        
    except Exception as e:
        return f"❌ Error al listar ahorros: {str(e)}"

# === HERRAMIENTAS DE CONSULTA ===

@mcp.tool()
async def resumen_financiero() -> str:
    """
    Obtener resumen financiero completo.
    
    Muestra el balance total, ingresos, gastos y ahorros.
    
    Ejemplos de uso:
    - "¿Cómo van mis finanzas?"
    - "Dame un resumen de mi situación financiera"
    - "¿Cuál es mi balance?"
    
    Returns:
        Resumen financiero con totales y balance
    """
    try:
        summary = await api.get_summary()
        
        balance_icon = "✅" if summary['balance'] >= 0 else "⚠️"
        balance_status = "positivo" if summary['balance'] >= 0 else "negativo"
        
        output = f"""📊 RESUMEN FINANCIERO

{balance_icon} Balance: {format_currency(summary['balance'])} ({balance_status})

💵 Ingresos totales: {format_currency(summary['total_incomes'])}
💸 Gastos totales: {format_currency(summary['total_expenses'])}
💰 Ahorros totales: {format_currency(summary['total_savings'])}

"""
        
        # Gastos por categoría
        if summary.get('expenses_by_category'):
            output += "\n📂 Gastos por categoría:\n"
            for category, amount in sorted(
                summary['expenses_by_category'].items(), 
                key=lambda x: x[1], 
                reverse=True
            ):
                output += f"   • {category}: {format_currency(amount)}\n"
        
        return output
        
    except Exception as e:
        return f"❌ Error al obtener el resumen: {str(e)}"

@mcp.tool()
async def reporte_mensual(año: Optional[int] = None, mes: Optional[int] = None) -> str:
    """
    Obtener reporte financiero de un mes específico.
    
    Ejemplos de uso:
    - "Dame el reporte de este mes"
    - "¿Cómo fue noviembre de 2025?"
    - "Reporte del mes pasado"
    
    Args:
        año: Año del reporte (default: año actual)
        mes: Mes del reporte 1-12 (default: mes actual)
    
    Returns:
        Reporte detallado del mes
    """
    try:
        now = datetime.now()
        año = año or now.year
        mes = mes or now.month
        
        report = await api.get_monthly_report(año, mes)
        
        month_names = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]
        
        balance_icon = "✅" if report['balance'] >= 0 else "⚠️"
        
        return f"""📅 REPORTE DE {month_names[mes-1].upper()} {año}

{balance_icon} Balance del mes: {format_currency(report['balance'])}

💵 Ingresos: {format_currency(report['total_incomes'])}
💸 Gastos: {format_currency(report['total_expenses'])}
💰 Ahorros: {format_currency(report['total_savings'])}

📊 Total de movimientos:
   • {len(report.get('incomes', []))} ingresos
   • {len(report.get('expenses', []))} gastos
   • {len(report.get('savings', []))} movimientos de ahorro
"""
        
    except Exception as e:
        return f"❌ Error al obtener el reporte mensual: {str(e)}"

if __name__ == "__main__":
    # Iniciar servidor MCP
    mcp.run()
