# 🤖 MCP Server - Control de Gastos

> **Estado**: ✅ Fase 1 Completada - Funcional

Servidor de Model Context Protocol para interacción en lenguaje natural con el sistema de control de gastos.

## 🎯 Características

- ✅ Registro de gastos, ingresos y ahorros en lenguaje natural
- ✅ Consultas financieras conversacionales
- ✅ Categorización automática de gastos
- ✅ Detección automática de tipo de pago
- ✅ Identificación de ingresos recurrentes
- ✅ Resúmenes y reportes mensuales
- ✅ Integración con Claude Desktop y otros clientes MCP

## 🛠️ Tecnologías

- **Python 3.11+** - Lenguaje principal
- **FastMCP** - Framework MCP simplificado
- **httpx** - Cliente HTTP asíncrono
- **pydantic** - Validación de datos
- **python-dotenv** - Gestión de configuración

## 📋 Herramientas Disponibles

### 💸 Gestión de Gastos
- **`registrar_gasto`** - Registrar gastos con categorización automática
- **`listar_gastos`** - Ver últimos gastos con totales

### 💵 Gestión de Ingresos
- **`registrar_ingreso`** - Registrar ingresos con detección de recurrencia
- **`listar_ingresos`** - Ver últimos ingresos con totales

### 💰 Gestión de Ahorros
- **`registrar_ahorro`** - Depositar o retirar de ahorros con metas
- **`listar_ahorros`** - Ver movimientos de ahorro con balance

### 📊 Consultas y Reportes
- **`resumen_financiero`** - Balance completo con gastos por categoría
- **`reporte_mensual`** - Análisis detallado de un mes específico

## 🚀 Instalación

### 1. Requisitos Previos

Asegúrate de tener:
- Python 3.11 o superior
- Backend de Control de Gastos ejecutándose en `http://localhost:8000`
- Un token de autenticación válido del backend

### 2. Instalar Dependencias

```powershell
cd mcp
pip install fastmcp httpx pydantic python-dotenv
```

O usando el archivo de configuración:

```powershell
pip install -e .
```

### 3. Configurar Variables de Entorno

Crea un archivo `.env` en la carpeta `mcp/`:

```env
API_BASE_URL=http://localhost:8000/api/v1
API_TOKEN=tu_token_jwt_aqui
```

**Para obtener el token:**
1. Abre el frontend en `http://localhost:5173`
2. Inicia sesión con tu usuario
3. Abre las DevTools del navegador (F12)
4. Ve a la pestaña "Application" → "Local Storage"
5. Busca la clave `token` y copia su valor

### 4. Verificar Instalación

```powershell
cd src
python server.py
```

Si ves mensajes de error de conexión, verifica que el backend esté ejecutándose.

## 🎮 Uso con Claude Desktop

### 1. Instalar Claude Desktop

Descarga e instala Claude Desktop desde [claude.ai](https://claude.ai/download)

### 2. Configurar el Servidor MCP

Edita el archivo de configuración de Claude Desktop:

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

**Linux:** `~/.config/Claude/claude_desktop_config.json`

Agrega la siguiente configuración:

```json
{
  "mcpServers": {
    "control-gastos": {
      "command": "python",
      "args": [
        "C:\\dev\\python\\control-gastos\\mcp\\src\\server.py"
      ],
      "env": {
        "API_BASE_URL": "http://localhost:8000/api/v1",
        "API_TOKEN": "tu_token_jwt_aqui"
      }
    }
  }
}
```

**⚠️ Importante:** 
- Reemplaza la ruta con la ubicación real de tu proyecto
- Usa dobles barras invertidas (`\\`) en Windows
- Reemplaza `tu_token_jwt_aqui` con tu token real

### 3. Reiniciar Claude Desktop

Cierra completamente Claude Desktop y ábrelo de nuevo.

### 4. Verificar Conexión

En Claude Desktop, deberías ver un icono de 🔌 o "MCP" indicando que el servidor está conectado.

## 💬 Ejemplos de Uso con Claude Desktop

Una vez configurado, puedes interactuar en lenguaje natural:

### Registrar Gastos

```
Usuario: Registra un gasto de $450 en el super con tarjeta de débito

Claude: [Usa registrar_gasto]
✅ Gasto registrado exitosamente:
💰 Monto: $450.00 MXN
📝 Descripción: super
💳 Tipo de pago: tarjeta_debito
📂 Categoría: Alimentación
📅 Fecha: 26/11/2025
```

```
Usuario: Gasté 80 pesos en el metro en efectivo

Claude: [Usa registrar_gasto]
✅ Gasto registrado exitosamente:
💰 Monto: $80.00 MXN
📝 Descripción: metro
💳 Tipo de pago: efectivo
📂 Categoría: Transporte
```

### Registrar Ingresos

```
Usuario: Registra mi salario mensual de $15,000

Claude: [Usa registrar_ingreso]
✅ Ingreso registrado exitosamente:
💰 Monto: $15,000.00 MXN
📝 Descripción: salario mensual
🏢 Fuente: No especificada
📅 Recurrente mensual
```

```
Usuario: Recibí $2,500 de un freelance

Claude: [Usa registrar_ingreso]
✅ Ingreso registrado exitosamente:
💰 Monto: $2,500.00 MXN
📝 Descripción: freelance
🏢 Fuente: No especificada
📅 Ingreso único
```

### Gestionar Ahorros

```
Usuario: Ahorra $1,000 para el auto con meta de $50,000

Claude: [Usa registrar_ahorro]
✅ Depósito registrado exitosamente:
💵 Monto: $1,000.00 MXN
🎯 Propósito: auto
🎯 Meta: $50,000.00 MXN
```

```
Usuario: Retira $500 del ahorro de emergencias

Claude: [Usa registrar_ahorro con es_retiro=true]
✅ Retiro registrado exitosamente:
💵 Monto: $500.00 MXN
🎯 Propósito: emergencias
```

### Consultas Financieras

```
Usuario: ¿Cómo van mis finanzas?

Claude: [Usa resumen_financiero]
📊 RESUMEN FINANCIERO

✅ Balance: $5,754.11 MXN (positivo)

💵 Ingresos totales: $42,500.00 MXN
💸 Gastos totales: $36,745.89 MXN
💰 Ahorros totales: $8,500.00 MXN

📂 Gastos por categoría:
   • Alimentación: $12,450.00 MXN
   • Transporte: $8,320.00 MXN
   • Servicios: $6,200.00 MXN
   ...
```

```
Usuario: Dame el reporte de noviembre

Claude: [Usa reporte_mensual]
📅 REPORTE DE NOVIEMBRE 2025

✅ Balance del mes: $5,754.11 MXN

💵 Ingresos: $15,000.00 MXN
💸 Gastos: $9,245.89 MXN
💰 Ahorros: $1,000.00 MXN
```

```
Usuario: Muéstrame mis últimos 5 gastos

Claude: [Usa listar_gastos con limite=5]
📋 Últimos 5 gastos:

💸 $450.00 MXN
   📝 super
   💳 tarjeta_debito
   📂 Alimentación
   📅 26/11/2025
   
💸 $80.00 MXN
   📝 metro
   💳 efectivo
   📂 Transporte
   📅 26/11/2025
...
```

## 🔧 Uso con MCP Inspector (Herramienta de Pruebas)

MCP Inspector es una herramienta de desarrollo que te permite probar tu servidor MCP sin necesidad de Claude Desktop.

### 1. Instalar MCP Inspector

```powershell
npm install -g @modelcontextprotocol/inspector
```

### 2. Configurar Variables de Entorno

Antes de iniciar el inspector, **asegúrate de tener el archivo `.env` configurado** en la carpeta `mcp/`:

```env
API_BASE_URL=http://localhost:8000/api/v1
API_TOKEN=tu_token_jwt_valido_aqui
```

### 3. Iniciar el Inspector

```powershell
cd mcp
mcp-inspector python src/server.py
```

**⚠️ Importante:** 
- El inspector abrirá automáticamente tu navegador
- El puerto es **aleatorio** (ej: `http://localhost:6274`)
- La URL incluye un token de autenticación del inspector (diferente al token de tu API)
- Si tu frontend usa el puerto 5173, **no hay conflicto** - son servidores diferentes

### 4. Configurar el Inspector (Primera Vez)

Cuando abras el inspector, verás varias opciones de configuración:

#### **Transport Type**
- Selecciona: **`stdio`** (Standard Input/Output)
- Es el tipo de transporte que usa FastMCP por defecto

#### **Command**
- Ya está configurado: `python`
- Es el comando para ejecutar Python

#### **Arguments**
- Ya está configurado: `src/server.py`
- Es la ruta al archivo del servidor

#### **Environment Variables**
- Estas se toman del archivo `.env` automáticamente
- Deberías ver: `API_BASE_URL` y `API_TOKEN`
- **Si no aparecen**, agrégalas manualmente:
  ```
  API_BASE_URL=http://localhost:8000/api/v1
  API_TOKEN=tu_token_jwt_aqui
  ```

#### **Authentication**
- Déjalo en **None** (el inspector genera su propio token)
- La autenticación con el backend se hace via `API_TOKEN`

#### **Configuration**
- Déjalo como está (configuración por defecto)

### 5. Conectar el Inspector

1. Haz clic en **"Connect"** (botón arriba a la derecha)
2. Espera unos segundos
3. Verás que el estado cambia a **"Connected ✓"**
4. En el menú lateral aparecerán todas las herramientas disponibles

**Si no conecta:**
- Verifica que el backend esté corriendo: `http://localhost:8000/docs`
- Revisa que el token sea válido (no expirado)
- Verifica que las variables de entorno estén correctas
- Mira la consola del navegador (F12) para ver errores

### 6. Probar Herramientas

Una vez conectado, verás 4 pestañas principales:

#### **📋 Tools** (Herramientas)
Aquí aparecen las 10 herramientas del servidor:
- `registrar_gasto`
- `listar_gastos`
- `registrar_ingreso`
- `listar_ingresos`
- `registrar_ahorro`
- `listar_ahorros`
- `resumen_financiero`
- `reporte_mensual`

**Para probar una herramienta:**

1. **Selecciona una herramienta** del menú lateral (ej: `registrar_gasto`)
2. **Completa los parámetros** en el formulario:
   ```json
   {
     "descripcion": "Café con amigos",
     "monto": 150,
     "tipo_pago": "efectivo",
     "categoria": "Alimentación"
   }
   ```
3. **Haz clic en "Call Tool"** (botón azul)
4. **Observa la respuesta** en el panel derecho:
   ```
   ✅ Gasto registrado exitosamente:
   💰 Monto: $150.00 MXN
   📝 Descripción: Café con amigos
   💳 Tipo de pago: efectivo
   📂 Categoría: Alimentación
   📅 Fecha: 26/11/2025
   🆔 ID: ...
   ```

**Ejemplo: Consultar resumen financiero**
1. Selecciona `resumen_financiero`
2. No requiere parámetros
3. Click en "Call Tool"
4. Verás tu balance, ingresos, gastos y ahorros

**Ejemplo: Listar últimos gastos**
1. Selecciona `listar_gastos`
2. Parámetro opcional: `{"limite": 5}`
3. Click en "Call Tool"
4. Verás los últimos 5 gastos

#### **📦 Resources** (Recursos)
- Actualmente vacío (Fase 2 del roadmap)
- Aquí aparecerán recursos de solo lectura como listas de datos

#### **💬 Prompts** (Plantillas)
- Actualmente vacío (Fase 2 del roadmap)
- Aquí aparecerán plantillas de consultas comunes

#### **⚙️ Server Info** (Información del Servidor)
- Muestra información del servidor MCP
- Versión del protocolo
- Capacidades soportadas

### 7. Debugging y Logs

**Ver logs del servidor:**
- Abre la consola del navegador (F12)
- Ve a la pestaña "Console"
- Verás los mensajes de comunicación entre el inspector y el servidor

**Ver errores de la API:**
- Si hay errores (401, 404, 500), aparecerán en la respuesta de la herramienta
- También puedes ver los logs del backend en la terminal donde corre `uvicorn`

### 8. Casos de Uso del Inspector

**✅ Desarrollo:** Probar herramientas sin abrir Claude Desktop

**✅ Debugging:** Ver exactamente qué parámetros envías y qué respuestas recibes

**✅ Documentación:** Explorar todas las herramientas disponibles

**✅ Validación:** Asegurarte de que el servidor funciona antes de configurar Claude Desktop

### 9. Diferencias: Inspector vs Claude Desktop

| Característica | MCP Inspector | Claude Desktop |
|---------------|---------------|----------------|
| **Propósito** | Herramienta de desarrollo | Uso en producción |
| **Interfaz** | Formularios técnicos | Lenguaje natural conversacional |
| **Uso** | Llamadas directas a herramientas | Claude decide qué herramienta usar |
| **Input** | JSON estructurado | Texto libre en español |
| **Autenticación** | Token de inspector + API_TOKEN | Solo API_TOKEN en variables de entorno |

**Ejemplo con Inspector:**
```json
{
  "descripcion": "gasolina",
  "monto": 400,
  "tipo_pago": "efectivo"
}
```

**Mismo ejemplo con Claude Desktop:**
```
Gasté $400 en gasolina en efectivo
```

### 10. Tips y Mejores Prácticas

**🔄 Recargar cambios:**
- Si modificas el código del servidor, haz clic en "Disconnect" y luego "Connect" nuevamente

**🎯 Probar categorización automática:**
- Prueba `registrar_gasto` sin especificar `categoria`
- El servidor debería inferirla de la descripción
- Ejemplo: `{"descripcion": "super", "monto": 200}` → Categoría: "Alimentación"

**🔍 Validar respuestas:**
- Después de registrar algo, usa `listar_gastos` / `listar_ingresos` / `listar_ahorros`
- Verifica que el dato se guardó correctamente en MongoDB

**⚠️ Token expirado:**
- Si ves errores 401, actualiza el `API_TOKEN` en las variables de entorno del inspector
- Desconecta y vuelve a conectar para aplicar el cambio

## 🧪 Categorización Automática

El servidor incluye detección inteligente de categorías basada en palabras clave:

| Categoría | Palabras Clave |
|-----------|----------------|
| 🍽️ **Alimentación** | comida, restaurante, super, supermercado, mercado, despensa, comestibles |
| 🚗 **Transporte** | gasolina, uber, taxi, transporte, metro, bus, camión |
| 🎬 **Entretenimiento** | cine, teatro, concierto, diversión, salida, fiesta |
| 🏥 **Salud** | doctor, medicina, farmacia, hospital, consulta, médico |
| 💡 **Servicios** | luz, agua, internet, teléfono, celular, netflix, spotify |
| 📚 **Educación** | curso, libro, escuela, universidad, capacitación |
| 👕 **Ropa** | ropa, zapatos, vestuario, calzado |
| 🏠 **Hogar** | muebles, decoración, reparación, mantenimiento |

### Detección de Tipo de Pago

| Tipo | Palabras Clave |
|------|----------------|
| 💵 **efectivo** | efectivo, cash |
| 💳 **tarjeta_debito** | débito, debito, tarjeta de débito |
| 💳 **tarjeta_credito** | crédito, credito, tarjeta de crédito |
| 🏦 **transferencia** | transferencia, transfer |
| 💻 **paypal** | paypal |

### Detección de Ingresos Recurrentes

Palabras que activan `is_recurring = true`:
- mensual, recurrente, sueldo, salario, nómina, nomina

## 🐛 Solución de Problemas

### Fecha incorrecta (un día adelantada)

**Problema:** Los registros aparecen con fecha del día siguiente

**Causa:** Diferencia de zona horaria. El servidor usa UTC por defecto

**Solución implementada:**
El servidor MCP ahora envía fechas con zona horaria `America/Mexico_City` automáticamente. Si estás en otra zona horaria, modifica la constante `DEFAULT_TIMEZONE` en `server.py`:

```python
# Para otros países:
DEFAULT_TIMEZONE = ZoneInfo("America/New_York")      # USA Este
DEFAULT_TIMEZONE = ZoneInfo("America/Los_Angeles")   # USA Oeste
DEFAULT_TIMEZONE = ZoneInfo("America/Argentina/Buenos_Aires")  # Argentina
DEFAULT_TIMEZONE = ZoneInfo("Europe/Madrid")         # España
```

**Para producción multi-región:**
Considera detectar la zona horaria del usuario automáticamente o permitir que la configure en su perfil.

### Warning "Unstructured Content"

**Problema:** `⚠ No text block matches structured content`

**Explicación:** Es un warning del MCP Inspector, no un error. Significa que la respuesta no tiene bloques de código formateados con markdown, solo texto plano. Es completamente normal y no afecta la funcionalidad.

**Puedes ignorarlo:** Las respuestas están diseñadas para ser legibles, con emojis y formato visual, pero no usan bloques de código markdown.

### Token expira constantemente

**Problema:** Cada vez que pruebo el MCP debo copiar un nuevo token

**Causa:** Los tokens JWT tienen fecha de expiración (actualmente configurada en el backend)

**Solución temporal (desarrollo):**
1. Aumenta el tiempo de expiración en el backend
2. Busca en `backend/core/security.py` o similar:
   ```python
   # Cambia de 30 minutos a 7 días
   ACCESS_TOKEN_EXPIRE_MINUTES = 10080  # 7 días
   ```

**Solución permanente (producción):**
- Implementar refresh tokens
- Sistema de tokens de larga duración para MCP
- Autenticación OAuth2 con renovación automática

### El servidor no se conecta al backend

**Problema:** `Error al registrar el gasto: Connection refused`

**Solución:**
1. Verifica que el backend esté ejecutándose: `http://localhost:8000/docs`
2. Revisa la variable `API_BASE_URL` en tu `.env`
3. Asegúrate de que no haya firewall bloqueando el puerto 8000

### Token inválido o expirado

**Problema:** `Error 401: Unauthorized`

**Solución:**
1. Los tokens JWT expiran después de cierto tiempo
2. Inicia sesión nuevamente en el frontend
3. Obtén un nuevo token de Local Storage
4. Actualiza la variable `API_TOKEN` en tu `.env`
5. Reinicia el servidor MCP o Claude Desktop

### Claude Desktop no detecta el servidor

**Problema:** No aparece el icono de MCP

**Solución:**
1. Verifica la ruta en `claude_desktop_config.json`
2. Asegúrate de usar rutas absolutas
3. En Windows, usa dobles barras invertidas (`\\`)
4. Verifica que el archivo `server.py` exista en la ruta especificada
5. Reinicia Claude Desktop completamente (Task Manager → cerrar proceso)

### Error al importar módulos

**Problema:** `ModuleNotFoundError: No module named 'fastmcp'`

**Solución:**
```powershell
pip install fastmcp httpx pydantic python-dotenv
```

### Las categorías no se detectan correctamente

**Problema:** Los gastos siempre quedan en "Otro"

**Solución:**
- Las palabras clave son en español y sensibles a minúsculas
- Usa descripciones claras: "super" en vez de "compras"
- Puedes especificar la categoría manualmente al usar las herramientas

## 🔮 Roadmap

### ✅ Fase 1 - MCP Básico (Completado)
- ✅ Servidor MCP funcional con FastMCP
- ✅ Herramientas para gastos, ingresos y ahorros
- ✅ Categorización automática por palabras clave
- ✅ Integración con backend existente
- ✅ Soporte para Claude Desktop

### 🔄 Fase 2 - Análisis Inteligente (En Progreso)
- [ ] Recursos MCP para acceso directo a datos
- [ ] Prompts para guiar consultas comunes
- [ ] Análisis de patrones de gasto
- [ ] Detección de gastos inusuales
- [ ] Recomendaciones básicas de ahorro

### 📋 Fase 3 - IA Avanzada (Planificado)
- [ ] Predicción de gastos futuros con ML
- [ ] Optimización automática de presupuestos
- [ ] Alertas inteligentes personalizadas
- [ ] Categorización con modelos de lenguaje

### 🌐 Fase 4 - Ecosistema (Futuro)
- [ ] Soporte para múltiples clientes MCP
- [ ] API pública para desarrolladores
- [ ] Plugins para otras aplicaciones de finanzas
- [ ] Análisis comparativo con otros usuarios (anónimo)

## 🚀 Integración con Otras Plataformas

### WhatsApp Bot (Producción)

Para permitir que usuarios registren gastos por WhatsApp:

**Opción 1: Twilio + FastMCP (Recomendado)**

1. **Crear cuenta en Twilio** (WhatsApp Business API)
2. **Crear webhook endpoint** que reciba mensajes de WhatsApp:

```python
# backend/api/whatsapp.py
from fastapi import APIRouter, Request
from twilio.twiml.messaging_response import MessagingResponse
import httpx

router = APIRouter()

@router.post("/whatsapp/webhook")
async def whatsapp_webhook(request: Request):
    # Obtener mensaje del usuario
    form = await request.form()
    from_number = form.get('From')
    message_body = form.get('Body')
    
    # Obtener user_id del número de teléfono
    user = await get_user_by_phone(from_number)
    
    # Llamar al MCP server internamente
    # (el MCP server procesará el lenguaje natural)
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/v1/nlp/process",
            json={
                "user_id": user.id,
                "message": message_body
            }
        )
    
    # Enviar respuesta por WhatsApp
    resp = MessagingResponse()
    resp.message(response.json()['message'])
    return str(resp)
```

3. **Adaptar el MCP server como servicio interno:**

```python
# backend/services/nlp_service.py
from mcp.src.server import (
    registrar_gasto,
    registrar_ingreso,
    registrar_ahorro,
    resumen_financiero
)

async def process_natural_language(user_id: str, message: str):
    """Procesa mensaje en lenguaje natural"""
    
    # Detectar intención
    if "gast" in message.lower():
        # Extraer datos del mensaje
        monto = extract_amount(message)
        descripcion = extract_description(message)
        
        # Llamar a la función del MCP
        result = await registrar_gasto(
            descripcion=descripcion,
            monto=monto
        )
        return result
    
    elif "ingreso" in message.lower() or "cobr" in message.lower():
        # Procesar ingreso...
        pass
    
    elif "ahorro" in message.lower():
        # Procesar ahorro...
        pass
    
    elif "resumen" in message.lower() or "balance" in message.lower():
        return await resumen_financiero()
```

**Opción 2: WhatsApp Business API + Claude API**

1. Configurar webhook de WhatsApp Business API
2. Enviar mensajes a Claude via API con contexto del MCP
3. Claude responderá usando las herramientas MCP
4. Retornar respuesta al usuario via WhatsApp

```python
import anthropic

client = anthropic.Anthropic(api_key="tu-api-key")

# Configurar herramientas MCP disponibles para Claude
tools = [
    {
        "name": "registrar_gasto",
        "description": "Registrar un nuevo gasto",
        "input_schema": {
            "type": "object",
            "properties": {
                "descripcion": {"type": "string"},
                "monto": {"type": "number"},
                "tipo_pago": {"type": "string"}
            }
        }
    },
    # ... más herramientas
]

# Procesar mensaje
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": mensaje_usuario}]
)
```

### Telegram Bot

Similar a WhatsApp pero más sencillo (API gratuita):

```python
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler

async def handle_message(update: Update, context):
    message = update.message.text
    
    # Procesar con el sistema NLP
    result = await process_natural_language(
        user_id=update.effective_user.id,
        message=message
    )
    
    await update.message.reply_text(result)

app = Application.builder().token("BOT_TOKEN").build()
app.add_handler(MessageHandler(filters.TEXT, handle_message))
app.run_polling()
```

### Slack Bot

Para equipos o uso empresarial:

```python
from slack_bolt import App

app = App(token="SLACK_BOT_TOKEN")

@app.message()
async def handle_message(message, say):
    result = await process_natural_language(
        user_id=message['user'],
        message=message['text']
    )
    await say(result)

app.start(port=3000)
```

### Consideraciones para Producción

**🔐 Seguridad:**
- Implementar autenticación por número de teléfono
- Verificar identidad del usuario antes de permitir acceso
- Rate limiting para prevenir abuso
- Encriptar datos sensibles en tránsito

**📊 Escalabilidad:**
- Usar queue system (Redis/RabbitMQ) para procesar mensajes
- Caché para respuestas frecuentes
- Load balancing para múltiples instancias

**💰 Costos:**
- Twilio WhatsApp: ~$0.005 por mensaje
- Telegram: Gratuito
- Claude API: $3 por 1M tokens input, $15 por 1M output
- Alternativa: Self-host un LLM con Ollama (gratuito)

**🌍 Multi-región:**
- Detectar timezone automáticamente del usuario
- Soportar múltiples idiomas
- Formatear monedas según región

**📱 Ejemplo de flujo completo:**

```
Usuario (WhatsApp): "Gasté $250 en uber"
    ↓
Twilio Webhook → Backend API
    ↓
NLP Service → MCP Server Tools
    ↓
registrar_gasto(descripcion="uber", monto=250, tipo_pago="tarjeta_debito", categoria="Transporte")
    ↓
MongoDB ← Backend guarda registro
    ↓
Respuesta: "✅ Gasto de $250.00 MXN en Transporte registrado"
    ↓
Twilio → WhatsApp → Usuario
```


## 🤝 Contribuir

¿Tienes ideas para mejorar el servidor MCP? ¡Las contribuciones son bienvenidas!

### Áreas de Mejora
- 🧠 **Categorización**: Mejorar palabras clave y agregar más categorías
- 🔧 **Herramientas**: Añadir nuevas funcionalidades MCP
- 📊 **Análisis**: Implementar análisis de patrones de gasto
- 🧪 **Testing**: Pruebas de integración con diferentes clientes MCP
- 📝 **Documentación**: Mejorar guías y ejemplos

## 📞 Soporte

Si encuentras problemas o tienes preguntas:

1. Revisa la sección **Solución de Problemas** arriba
2. Verifica que el backend esté ejecutándose correctamente
3. Asegúrate de tener un token válido
4. Revisa los logs del servidor para más detalles

## 🔗 Referencias

- [Model Context Protocol](https://modelcontextprotocol.io/) - Especificación oficial del protocolo
- [FastMCP Documentation](https://github.com/jlowin/fastmcp) - Framework usado en este proyecto
- [Claude Desktop](https://claude.ai/download) - Cliente MCP oficial de Anthropic
- [Backend API](../backend/README.md) - Documentación del backend

---

**✨ ¡Disfruta de tu asistente financiero conversacional!**