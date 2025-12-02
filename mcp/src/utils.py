"""
Utilidades para procesamiento de lenguaje natural y formateo
"""
from datetime import datetime
from typing import Optional, Tuple
import re

def parse_amount(text: str) -> Optional[float]:
    """
    Extraer monto de un texto
    Ejemplos: "$500", "500 pesos", "1,500.50"
    """
    # Remover caracteres no numéricos excepto puntos y comas
    text = text.replace("$", "").replace("pesos", "").replace("MXN", "")
    text = text.replace(",", "").strip()
    
    try:
        return float(text)
    except:
        return None

def infer_payment_type(text: str) -> str:
    """
    Inferir tipo de pago del texto
    """
    text_lower = text.lower()
    
    if any(word in text_lower for word in ["efectivo", "cash", "dinero"]):
        return "efectivo"
    elif any(word in text_lower for word in ["débito", "debito", "tarjeta de débito"]):
        return "tarjeta_debito"
    elif any(word in text_lower for word in ["crédito", "credito", "tarjeta de crédito", "tc"]):
        return "tarjeta_credito"
    elif any(word in text_lower for word in ["transferencia", "transfer"]):
        return "transferencia"
    elif any(word in text_lower for word in ["paypal"]):
        return "paypal"
    else:
        return "efectivo"  # Por defecto

def infer_category(text: str) -> Optional[str]:
    """
    Inferir categoría de gasto del texto
    """
    text_lower = text.lower()
    
    categories = {
        "Alimentación": ["comida", "restaurante", "super", "supermercado", "mercado", "despensa", "comestibles"],
        "Transporte": ["gasolina", "uber", "taxi", "transporte", "metro", "bus", "camión"],
        "Entretenimiento": ["cine", "teatro", "concierto", "diversión", "salida", "fiesta"],
        "Salud": ["doctor", "medicina", "farmacia", "hospital", "consulta", "médico"],
        "Servicios": ["luz", "agua", "internet", "teléfono", "celular", "netflix", "spotify"],
        "Educación": ["curso", "libro", "escuela", "universidad", "capacitación"],
        "Ropa": ["ropa", "zapatos", "vestuario", "calzado"],
        "Hogar": ["muebles", "decoración", "reparación", "mantenimiento"],
    }
    
    for category, keywords in categories.items():
        if any(keyword in text_lower for keyword in keywords):
            return category
    
    return None

def format_currency(amount: float) -> str:
    """Formatear monto como moneda mexicana"""
    return f"${amount:,.2f} MXN"

def format_date(date_str: str) -> str:
    """Formatear fecha para mostrar"""
    try:
        date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return date.strftime("%d/%m/%Y")
    except:
        return date_str

def parse_transaction_type(text: str) -> str:
    """
    Determinar si es depósito o retiro
    """
    text_lower = text.lower()
    
    if any(word in text_lower for word in ["retiro", "retirar", "sacar", "emergencia"]):
        return "retiro"
    else:
        return "deposito"

def is_recurring(text: str) -> bool:
    """
    Determinar si un ingreso es recurrente
    """
    text_lower = text.lower()
    return any(word in text_lower for word in ["mensual", "recurrente", "sueldo", "salario", "nómina", "nomina"])

def extract_purpose(text: str) -> str:
    """
    Extraer propósito/meta de ahorro del texto
    """
    text_lower = text.lower()
    
    # Patrones comunes
    patterns = [
        r"para\s+(.+?)(?:\s+de\s+|$)",
        r"meta\s+(?:de\s+)?(.+?)(?:\s+|$)",
        r"ahorro\s+(?:para\s+)?(.+?)(?:\s+|$)",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text_lower)
        if match:
            purpose = match.group(1).strip()
            # Capitalizar primera letra
            return purpose.capitalize()
    
    return "Ahorro general"
