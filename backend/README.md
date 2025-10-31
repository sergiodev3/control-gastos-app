# 🏦 Control de Gastos - API Backend

Sistema completo de gestión de finanzas personales desarrollado con **FastAPI**, **MongoDB** y **Python 3.11+**.

## 🚀 Inicio Rápido

### 1. Activar entorno virtual e instalar dependencias
```bash
# Activar entorno virtual
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/macOS

# Instalar dependencias
pip install -r requeriments.txt
```

### 2. Configurar MongoDB
Asegúrate de tener MongoDB ejecutándose en `mongodb://localhost:27017` o actualiza la URL en `.env`.

### 3. Iniciar servidor
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

La API estará disponible en:
- **Servidor**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📚 Endpoints Principales

### 🔐 Autenticación (`/api/v1/auth`)
- `POST /register` - Registrar nuevo usuario
- `POST /login` - Iniciar sesión
- `GET /profile` - Obtener perfil del usuario
- `PUT /profile` - Actualizar perfil del usuario

### 💸 Gastos (`/api/v1/expenses`)
- `POST /` - Crear gasto
- `GET /` - Listar gastos del usuario
- `GET /{expense_id}` - Obtener gasto específico
- `PUT /{expense_id}` - Actualizar gasto
- `DELETE /{expense_id}` - Eliminar gasto

### 💰 Ingresos (`/api/v1/incomes`)
- `POST /` - Crear ingreso
- `GET /` - Listar ingresos del usuario
- `GET /{income_id}` - Obtener ingreso específico
- `PUT /{income_id}` - Actualizar ingreso
- `DELETE /{income_id}` - Eliminar ingreso

### 🏦 Ahorros (`/api/v1/savings`)
- `POST /` - Crear ahorro
- `GET /` - Listar ahorros del usuario
- `GET /{saving_id}` - Obtener ahorro específico
- `PUT /{saving_id}` - Actualizar ahorro
- `DELETE /{saving_id}` - Eliminar ahorro

### 📊 Estadísticas (`/api/v1/stats`)
- `GET /summary` - Resumen financiero general
- `GET /monthly/{year}/{month}` - Reporte mensual
- `GET /categories` - Estadísticas por categorías

## 🧪 Prueba Rápida con Thunder Client

1. **Registrar usuario**
   ```http
   POST http://localhost:8000/api/v1/auth/register
   Content-Type: application/json

   {
     "email": "usuario@example.com",
     "username": "miusuario",
     "full_name": "Mi Nombre Completo",
     "password": "mipassword123"
   }
   ```

2. **Iniciar sesión**
   ```http
   POST http://localhost:8000/api/v1/auth/login
   Content-Type: application/json

   {
     "email": "usuario@example.com",
     "password": "mipassword123"
   }
   ```

3. **Crear gasto (usar token del login)**
   ```http
   POST http://localhost:8000/api/v1/expenses
   Content-Type: application/json
   Authorization: Bearer <tu_access_token>

   {
     "description": "Compra de supermercado",
     "amount": 150.75,
     "payment_type": "tarjeta_debito",
     "category": "Alimentación",
     "notes": "Compras de la semana"
   }
   ```

## 📝 Tipos de Pago Disponibles

- `efectivo`
- `tarjeta_debito`
- `tarjeta_credito`
- `transferencia`
- `paypal`
- `otro`

## 🏗 Arquitectura

```
backend/
├── api/                    # Endpoints de la API
├── core/                  # Configuración central
├── db/                    # Base de datos
├── models/                # Modelos y esquemas
├── services/              # Lógica de negocio
├── main.py                # Aplicación principal
├── requirements.txt       # Dependencias
└── .env                   # Variables de entorno
```

## 🔒 Características de Seguridad

- ✅ Autenticación JWT con expiración
- ✅ Hash seguro de contraseñas (bcrypt)
- ✅ Validación estricta de datos
- ✅ CORS configurado
- ✅ Autorización por recurso
- ✅ Logging de seguridad

Ver `README_COMPLETO.md` para documentación detallada.

---

**¡Desarrollado con ❤️ y ☕ para el control financiero personal!**