# 🏦 Control de Gastos - API Backend

Sistema completo de gestión de finanzas personales desarrollado con **FastAPI**, **MongoDB** y **Python 3.11+**.

## 🚀 Características

- ✅ **Autenticación JWT** con registro y login de usuarios
- 💸 **Gestión de gastos** con categorías y tipos de pago
- 💰 **Control de ingresos** con fuentes personalizables
- 🏦 **Seguimiento de ahorros** con metas y propósitos
- 📊 **Estadísticas financieras** completas
- 📈 **Reportes mensuales** detallados
- 🔐 **Seguridad robusta** con validaciones y encriptación
- 📚 **Documentación automática** con Swagger/OpenAPI

## 🛠 Tecnologías Utilizadas

- **FastAPI** - Framework web moderno y rápido
- **MongoDB** - Base de datos NoSQL flexible
- **ODMantic** - ODM moderno para MongoDB
- **Pydantic** - Validación de datos con tipos de Python
- **JWT** - Autenticación con tokens JSON Web
- **Passlib** - Hash seguro de contraseñas con bcrypt
- **Uvicorn** - Servidor ASGI de alta performance

## 📋 Requisitos

- Python 3.11+
- MongoDB 4.4+
- Entorno virtual Python (recomendado)

## ⚙️ Instalación

### 1. Clonar y configurar el entorno

```bash
# Navegar al directorio del backend
cd backend

# Activar el entorno virtual existente
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/macOS

# Instalar dependencias
pip install -r requeriments.txt
```

### 2. Configurar MongoDB

#### Opción A: MongoDB Local
```bash
# Instalar MongoDB Community Edition
# https://www.mongodb.com/try/download/community

# Iniciar el servicio
mongod   # Windows
```

#### Opción B: MongoDB Atlas (Nube)
1. Crear cuenta en [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Crear cluster gratuito
3. Obtener string de conexión
4. Actualizar `MONGODB_URL` en `.env`

### 3. Configurar variables de entorno

El archivo `.env` ya está configurado con valores por defecto:

```env
# Configuración de la aplicación
APP_NAME="Control de Gastos API"
APP_VERSION="1.0.0"
DEBUG=true

# Configuración de MongoDB
MONGODB_URL="mongodb://localhost:27017"
DATABASE_NAME="control_gastos"

# Configuración de seguridad
SECRET_KEY="tu_clave_secreta_super_segura_cambiala_en_produccion_2024"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Configuración de CORS
ALLOWED_ORIGINS="http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000,http://127.0.0.1:5173"
```

⚠️ **IMPORTANTE**: Cambia `SECRET_KEY` en producción por una clave segura.

## 🚀 Iniciar el Servidor

### Desarrollo
```bash
# Activar entorno virtual
.venv\Scripts\activate

# Iniciar servidor con recarga automática
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Producción
```bash
# Activar entorno virtual
.venv\Scripts\activate

# Iniciar servidor de producción
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

La API estará disponible en:
- **Servidor**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📚 Documentación de la API

### Endpoints Principales

#### 🔐 Autenticación (`/api/v1/auth`)
- `POST /register` - Registrar nuevo usuario
- `POST /login` - Iniciar sesión
- `GET /profile` - Obtener perfil del usuario
- `PUT /profile` - Actualizar perfil del usuario

#### 💸 Gastos (`/api/v1/expenses`)
- `POST /` - Crear gasto
- `GET /` - Listar gastos del usuario
- `GET /{expense_id}` - Obtener gasto específico
- `PUT /{expense_id}` - Actualizar gasto
- `DELETE /{expense_id}` - Eliminar gasto

#### 💰 Ingresos (`/api/v1/incomes`)
- `POST /` - Crear ingreso
- `GET /` - Listar ingresos del usuario
- `GET /{income_id}` - Obtener ingreso específico
- `PUT /{income_id}` - Actualizar ingreso
- `DELETE /{income_id}` - Eliminar ingreso

#### 🏦 Ahorros (`/api/v1/savings`)
- `POST /` - Crear ahorro
- `GET /` - Listar ahorros del usuario
- `GET /{saving_id}` - Obtener ahorro específico
- `PUT /{saving_id}` - Actualizar ahorro
- `DELETE /{saving_id}` - Eliminar ahorro

#### 📊 Estadísticas (`/api/v1/stats`)
- `GET /summary` - Resumen financiero general
- `GET /monthly/{year}/{month}` - Reporte mensual
- `GET /categories` - Estadísticas por categorías

## 🧪 Probar los Endpoints

### Con Thunder Client (VS Code)

1. **Instalar Thunder Client**
   - Abrir VS Code
   - Ir a Extensions (Ctrl+Shift+X)
   - Buscar "Thunder Client"
   - Instalar la extensión

2. **Registrar un usuario**
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

3. **Iniciar sesión**
   ```http
   POST http://localhost:8000/api/v1/auth/login
   Content-Type: application/json

   {
     "email": "usuario@example.com",
     "password": "mipassword123"
   }
   ```

4. **Crear un gasto (requiere token)**
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

### Con cURL

```bash
# Registrar usuario
curl -X POST "http://localhost:8000/api/v1/auth/register" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "usuario@example.com",
       "username": "miusuario", 
       "full_name": "Mi Nombre Completo",
       "password": "mipassword123"
     }'

# Iniciar sesión
curl -X POST "http://localhost:8000/api/v1/auth/login" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "usuario@example.com",
       "password": "mipassword123"
     }'

# Crear gasto (reemplazar <TOKEN> con el token obtenido)
curl -X POST "http://localhost:8000/api/v1/expenses" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <TOKEN>" \
     -d '{
       "description": "Compra de supermercado",
       "amount": 150.75,
       "payment_type": "tarjeta_debito",
       "category": "Alimentación"
     }'
```

## 🏗 Arquitectura del Proyecto

```
backend/
├── api/                    # Endpoints de la API
│   ├── auth.py            # Autenticación
│   ├── expenses.py        # Gastos
│   ├── incomes.py         # Ingresos
│   ├── savings.py         # Ahorros
│   └── stats.py           # Estadísticas
├── core/                  # Configuración central
│   ├── config.py          # Configuraciones
│   └── security.py        # Seguridad y JWT
├── db/                    # Base de datos
│   └── database.py        # Conexión MongoDB
├── models/                # Modelos y esquemas
│   ├── models.py          # Modelos ODMantic
│   └── schemas.py         # Esquemas Pydantic
├── services/              # Lógica de negocio
│   ├── user_service.py    # Servicio usuarios
│   ├── expense_service.py # Servicio gastos
│   ├── income_service.py  # Servicio ingresos
│   └── saving_service.py  # Servicio ahorros
├── main.py                # Aplicación principal
├── requirements.txt       # Dependencias
└── .env                   # Variables de entorno
```

## 🔒 Seguridad Implementada

- **Autenticación JWT**: Tokens seguros con expiración
- **Hash de contraseñas**: Bcrypt para almacenamiento seguro
- **Validación de datos**: Pydantic para validación estricta
- **CORS configurado**: Orígenes permitidos específicos
- **Autorización por recurso**: Los usuarios solo acceden a sus datos
- **Logging de seguridad**: Seguimiento de accesos y errores

## 📝 Tipos de Pago

La API soporta los siguientes tipos de pago:
- `efectivo`
- `tarjeta_debito`
- `tarjeta_credito`
- `transferencia`
- `paypal`
- `otro`

## 🐛 Solución de Problemas

### Error de conexión a MongoDB
```bash
# Verificar que MongoDB esté ejecutándose
mongosh --eval "db.adminCommand('ping')"

# Si usas MongoDB Atlas, verifica la string de conexión
```

### Error de dependencias
```bash
# Reinstalar dependencias
pip install --upgrade -r requirements.txt
```

### Error de permisos CORS
```bash
# Verificar ALLOWED_ORIGINS en .env
# Asegúrate de incluir el puerto correcto del frontend
```

## 🚀 Consejos para Desarrollo

1. **Usar el entorno virtual siempre**
   ```bash
   .venv\Scripts\activate
   ```

2. **Monitorear logs en desarrollo**
   ```bash
   tail -f app.log  # Linux/macOS
   Get-Content app.log -Wait  # Windows PowerShell
   ```

3. **Explorar la documentación interactiva**
   - Visita http://localhost:8000/docs
   - Prueba los endpoints directamente

4. **Validar datos con los esquemas**
   - Revisa `models/schemas.py` para ver validaciones
   - Usa los ejemplos en la documentación

5. **Monitorear la base de datos**
   ```bash
   # Conectar a MongoDB
   mongosh
   
   # Cambiar a la base de datos
   use control_gastos
   
   # Ver colecciones
   show collections
   
   # Ver usuarios
   db.users.find()
   ```

## 📊 Próximas Características

- [ ] Categorías personalizables
- [ ] Metas de ahorro con notificaciones
- [ ] Exportación de datos (CSV, PDF)
- [ ] Reportes gráficos
- [ ] Recordatorios de gastos recurrentes
- [ ] API de bancos para importación automática
- [ ] Dashboard de administrador

## 🤝 Contribuir

1. Fork el proyecto
2. Crear rama para feature (`git checkout -b feature/nueva-caracteristica`)
3. Commit cambios (`git commit -am 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

---

**¡Desarrollado con ❤️ y ☕ para el control financiero personal!**