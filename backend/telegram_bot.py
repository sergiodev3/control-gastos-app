"""
Telegram Bot para Control de Gastos
Bot que permite gestionar finanzas personales mediante mensajes de Telegram
"""
import os
import asyncio
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
from dotenv import load_dotenv

# Importar utilidades del MCP
from mcp_utils.api_client import APIClient
from mcp_utils.utils import (
    parse_amount,
    infer_payment_type,
    infer_category,
    format_currency,
    is_recurring,
    parse_transaction_type
)

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

load_dotenv()

# Almacenar tokens de usuarios autenticados
# En producción, usar Redis o base de datos
user_tokens = {}

class TelegramBot:
    def __init__(self):
        self.telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.api_base_url = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")
        
        if not self.telegram_token:
            raise ValueError("TELEGRAM_BOT_TOKEN no configurado en variables de entorno")
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start - Bienvenida"""
        if not update.message:
            return
        
        welcome_message = """
🤖 **¡Bienvenido a Control de Gastos!**

Soy tu asistente financiero personal. Puedo ayudarte a:
💸 Registrar gastos
💵 Registrar ingresos  
💰 Gestionar ahorros
📊 Consultar tu balance

**Para empezar:**
1. Envía `/login tu_email tu_contraseña` para autenticarte
2. Luego puedes enviar mensajes como:
   - "Gasté $200 en gasolina"
   - "¿Cómo van mis finanzas?"
   - "Registra un ingreso de $5000"

**Comandos disponibles:**
/start - Mostrar este mensaje
/login - Iniciar sesión
/logout - Cerrar sesión
/ayuda - Ver ejemplos de uso
/balance - Ver tu balance actual
"""
        await update.message.reply_text(welcome_message, parse_mode='Markdown')
    
    async def login(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /login email password"""
        if not update.message or not update.effective_user or not context.args:
            return
        
        if len(context.args) != 2:
            await update.message.reply_text(
                "❌ Uso: `/login tu_email tu_contraseña`",
                parse_mode='Markdown'
            )
            return
        
        email, password = context.args
        user_id = update.effective_user.id
        
        try:
            # Llamar al endpoint de login del backend
            import httpx
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_base_url}/users/login",
                    json={"email": email, "password": password}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    token = data.get("access_token")
                    
                    # Guardar token del usuario
                    user_tokens[user_id] = token
                    
                    await update.message.reply_text(
                        "✅ **Sesión iniciada correctamente**\n\n"
                        "Ahora puedes enviarme mensajes como:\n"
                        "• 'Gasté $50 en café'\n"
                        "• '¿Cuál es mi balance?'\n"
                        "• 'Ahorra $1000 para vacaciones'",
                        parse_mode='Markdown'
                    )
                else:
                    await update.message.reply_text(
                        "❌ Error al iniciar sesión. Verifica tu email y contraseña."
                    )
        except Exception as e:
            logger.error(f"Error en login: {e}")
            await update.message.reply_text(
                "❌ Error al conectar con el servidor. Intenta más tarde."
            )
    
    async def logout(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /logout"""
        if not update.message or not update.effective_user:
            return
        
        user_id = update.effective_user.id
        if user_id in user_tokens:
            del user_tokens[user_id]
            await update.message.reply_text("✅ Sesión cerrada correctamente")
        else:
            await update.message.reply_text("No tenías una sesión activa")
    
    async def ayuda(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /ayuda - Ejemplos de uso"""
        if not update.message:
            return
        
        help_text = """
📚 **Ejemplos de uso:**

**Registrar gastos:**
• "Gasté $200 en gasolina"
• "Compré comida por $150 en efectivo"
• "$80 en el metro"
• "Pagué $500 de luz con tarjeta de débito"

**Registrar ingresos:**
• "Recibí mi salario de $15,000"
• "Ingreso de $2,500 por freelance"
• "Cobré $800"

**Gestionar ahorros:**
• "Ahorra $1,000 para el auto"
• "Retira $500 de emergencias"
• "Deposita $200 en vacaciones"

**Consultas:**
• "¿Cómo van mis finanzas?"
• "¿Cuál es mi balance?"
• "Muestra mis últimos gastos"
• "Dame un resumen"

💡 **Tip:** Escribe en lenguaje natural, el bot entenderá tu intención.
"""
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def balance(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /balance - Ver balance rápido"""
        if not update.message or not update.effective_user:
            return
        
        user_id = update.effective_user.id
        
        if user_id not in user_tokens:
            await update.message.reply_text(
                "❌ Debes iniciar sesión primero con `/login`",
                parse_mode='Markdown'
            )
            return
        
        try:
            api = APIClient()
            api.token = user_tokens[user_id]
            
            summary = await api.get_summary()
            
            balance_icon = "✅" if summary['balance'] >= 0 else "⚠️"
            
            message = f"""
📊 **TU BALANCE**

{balance_icon} Balance: ${summary['balance']:,.2f} MXN

💵 Ingresos: ${summary['total_incomes']:,.2f}
💸 Gastos: ${summary['total_expenses']:,.2f}
💰 Ahorros: ${summary['total_savings']:,.2f}
"""
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error al obtener balance: {e}")
            await update.message.reply_text(
                "❌ Error al obtener tu balance. Intenta más tarde."
            )
    
    async def process_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Procesar mensajes en lenguaje natural"""
        if not update.message or not update.effective_user or not update.message.text:
            return
        
        user_id = update.effective_user.id
        message = update.message.text.lower()
        
        # Verificar autenticación
        if user_id not in user_tokens:
            await update.message.reply_text(
                "❌ Debes iniciar sesión primero con `/login email password`",
                parse_mode='Markdown'
            )
            return
        
        try:
            # Procesar el mensaje con NLP
            result = await self.process_nlp(user_id, message)
            await update.message.reply_text(result, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error procesando mensaje: {e}")
            await update.message.reply_text(
                "❌ No pude procesar tu mensaje. Usa `/ayuda` para ver ejemplos.",
                parse_mode='Markdown'
            )
    
    async def process_nlp(self, user_id: int, message: str) -> str:
        """Procesar mensaje con NLP y ejecutar acción correspondiente"""
        
        # Configurar API client con el token del usuario
        api = APIClient()
        api.token = user_tokens[user_id]
        
        # Detectar intención
        if any(word in message for word in ['gast', 'compré', 'pagué', 'compr']):
            # REGISTRAR GASTO
            amount = parse_amount(message)
            if not amount:
                return "❌ No pude detectar el monto. Ejemplo: 'Gasté $200 en gasolina'"
            
            payment_type = infer_payment_type(message)
            category = infer_category(message)
            description = message.replace('gasté', '').replace('compré', '').replace('pagué', '')
            description = description.replace(str(amount), '').replace('$', '').strip()
            
            result = await api.create_expense(
                description=description or "Gasto desde Telegram",
                amount=amount,
                payment_type=payment_type,
                category=category
            )
            
            return f"""
✅ **Gasto registrado**

💰 Monto: {format_currency(amount)}
📝 Descripción: {description or 'Gasto desde Telegram'}
💳 Tipo de pago: {payment_type}
📂 Categoría: {category}
"""
        
        elif any(word in message for word in ['ingreso', 'recib', 'cobr', 'salario', 'sueldo']):
            # REGISTRAR INGRESO
            amount = parse_amount(message)
            if not amount:
                return "❌ No pude detectar el monto. Ejemplo: 'Recibí $5000 de salario'"
            
            is_rec = is_recurring(message)
            description = message.replace('recibí', '').replace('cobré', '').replace('ingreso', '')
            description = description.replace(str(amount), '').replace('$', '').strip()
            
            result = await api.create_income(
                description=description or "Ingreso desde Telegram",
                amount=amount,
                is_recurring=is_rec
            )
            
            recurring_text = "📅 Recurrente mensual" if is_rec else "📅 Ingreso único"
            
            return f"""
✅ **Ingreso registrado**

💵 Monto: {format_currency(amount)}
📝 Descripción: {description or 'Ingreso desde Telegram'}
{recurring_text}
"""
        
        elif any(word in message for word in ['ahorro', 'ahorra', 'deposita', 'retira', 'retiro']):
            # REGISTRAR AHORRO
            amount = parse_amount(message)
            if not amount:
                return "❌ No pude detectar el monto. Ejemplo: 'Ahorra $1000 para vacaciones'"
            
            trans_type = parse_transaction_type(message)
            is_withdrawal = trans_type == "retiro"
            
            # Extraer propósito
            purpose = message
            for word in ['ahorra', 'ahorro', 'deposita', 'retira', 'retiro', 'para', str(amount), '$']:
                purpose = purpose.replace(word, '')
            purpose = purpose.strip() or "Ahorro desde Telegram"
            
            result = await api.create_saving(
                amount=amount,
                purpose=purpose,
                transaction_type=trans_type
            )
            
            action = "💸 Retiro" if is_withdrawal else "💰 Depósito"
            
            return f"""
✅ **{action} registrado**

💵 Monto: {format_currency(amount)}
🎯 Propósito: {purpose}
"""
        
        elif any(word in message for word in ['balance', 'finanzas', 'resumen', 'cómo van']):
            # CONSULTAR RESUMEN
            summary = await api.get_summary()
            
            balance_icon = "✅" if summary['balance'] >= 0 else "⚠️"
            
            return f"""
📊 **RESUMEN FINANCIERO**

{balance_icon} Balance: {format_currency(summary['balance'])}

💵 Ingresos: {format_currency(summary['total_incomes'])}
💸 Gastos: {format_currency(summary['total_expenses'])}
💰 Ahorros: {format_currency(summary['total_savings'])}
"""
        
        elif any(word in message for word in ['últimos gastos', 'gastos recientes', 'mis gastos']):
            # LISTAR GASTOS
            expenses = await api.get_expenses(limit=5)
            
            if not expenses:
                return "📋 No tienes gastos registrados aún."
            
            result = "📋 **Tus últimos gastos:**\n\n"
            for exp in expenses:
                result += f"💸 {format_currency(exp['amount'])} - {exp['description']}\n"
            
            return result
        
        else:
            return """
❓ No entendí tu mensaje. Intenta con:
• "Gasté $200 en gasolina"
• "¿Cuál es mi balance?"
• "Recibí $5000 de salario"

Usa `/ayuda` para ver más ejemplos.
"""
    
    def run(self):
        """Iniciar el bot"""
        if not self.telegram_token:
            raise ValueError("TELEGRAM_BOT_TOKEN no configurado")
        
        application = Application.builder().token(self.telegram_token).build()
        
        # Comandos
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("login", self.login))
        application.add_handler(CommandHandler("logout", self.logout))
        application.add_handler(CommandHandler("ayuda", self.ayuda))
        application.add_handler(CommandHandler("balance", self.balance))
        
        # Mensajes de texto
        application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.process_message)
        )
        
        # Iniciar bot
        logger.info("🤖 Bot de Telegram iniciado")
        application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    bot = TelegramBot()
    bot.run()
