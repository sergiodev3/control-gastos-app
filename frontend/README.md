# 🎨 Frontend - Control de Gastos

> **Estado**: ✅ En desarrollo activo | 🚀 Base funcional completada

Interfaz de usuario moderna y responsiva para la aplicación de Control de Gastos, optimizada especialmente para dispositivos móviles.

## 🎯 Características Implementadas

### ✅ Completado
- **Autenticación completa**: Login, registro, protección de rutas
- **UI/UX moderna**: Diseño mobile-first con Tailwind CSS
- **Gestión de estado**: Zustand para estado global
- **Componentes reutilizables**: Button, Input, Card, Layout
- **Integración con backend**: Axios configurado con interceptors
- **Notificaciones**: Toast messages con react-hot-toast
- **Navegación**: React Router con rutas protegidas
- **Dashboard principal**: Resumen financiero en tiempo real

### 🚧 En Desarrollo
- Pantallas de gastos, ingresos y ahorros
- Gráficos y visualizaciones
- Perfil de usuario
- Filtros y búsqueda

## 🛠️ Tecnologías Utilizadas

- **React 18** - Biblioteca UI
- **TypeScript** - Tipado estático
- **Vite** - Build tool ultra-rápido
- **Tailwind CSS** - Framework de estilos utility-first
- **React Router v6** - Enrutamiento
- **Zustand** - Gestión de estado ligera
- **Axios** - Cliente HTTP
- **React Hot Toast** - Notificaciones
- **Lucide React** - Iconos modernos
- **date-fns** - Manejo de fechas
- **Recharts** - Gráficos (planificado)

## � Estructura del Proyecto

```
frontend/
├── src/
│   ├── components/          # Componentes reutilizables
│   │   ├── ui/             # Componentes base (Button, Input, Card)
│   │   └── MobileLayout.tsx # Layout principal mobile-first
│   ├── pages/              # Páginas de la aplicación
│   │   ├── LoginPage.tsx
│   │   ├── RegisterPage.tsx
│   │   └── DashboardPage.tsx
│   ├── services/           # Servicios API
│   │   ├── auth.service.ts
│   │   ├── expense.service.ts
│   │   ├── income.service.ts
│   │   ├── saving.service.ts
│   │   └── stats.service.ts
│   ├── store/              # Estado global (Zustand)
│   │   └── auth.store.ts
│   ├── types/              # Tipos TypeScript
│   │   └── index.ts
│   ├── lib/                # Configuraciones
│   │   └── axios.ts
│   ├── App.tsx             # Componente principal
│   └── main.tsx            # Punto de entrada
├── tailwind.config.js      # Configuración Tailwind
├── postcss.config.js       # PostCSS
├── .env                    # Variables de entorno
└── package.json
```

## 🚀 Inicio Rápido

### 1. Instalar dependencias
```bash
npm install
```

### 2. Configurar variables de entorno
Archivo `.env`:
```env
VITE_API_URL=http://localhost:8000/api/v1
```

### 3. Iniciar servidor de desarrollo
```bash
npm run dev
```

La aplicación estará disponible en http://localhost:5173

### 4. Build para producción
```bash
npm run build
npm run preview
```

## 📱 Características Mobile-First

El frontend está optimizado especialmente para dispositivos móviles:

- **Navegación inferior**: Bottom nav bar para fácil acceso con el pulgar
- **Touch feedback**: Animaciones de escala al tocar botones
- **Gestos táctiles**: Swipe y tap optimizados
- **Diseño adaptativo**: Se ve perfecto en cualquier tamaño de pantalla
- **Performance**: Carga rápida y transiciones suaves
- **Safe areas**: Soporte para notches y áreas seguras de iOS/Android

## 🎨 Sistema de Diseño

### Colores
- **Primary**: Azul (`#0ea5e9`) - Acciones principales
- **Secondary**: Púrpura (`#d946ef`) - Elementos secundarios
- **Success**: Verde (`#10b981`) - Ingresos, confirmaciones
- **Warning**: Amarillo (`#f59e0b`) - Alertas
- **Error**: Rojo (`#ef4444`) - Gastos, errores

### Componentes UI
Todos los componentes están en `src/components/ui/`:
- `Button` - Botones con variantes y estados de carga
- `Input` - Inputs con labels, errores y helper text
- `Card` - Tarjetas con shadow y hover effects

### Layout
- `MobileLayout` - Layout principal con header y bottom navigation

## 🔌 Integración con Backend

El frontend se comunica con el backend a través de Axios:

```typescript
// Configuración en src/lib/axios.ts
- Base URL: http://localhost:8000/api/v1
- Interceptor de request: Agrega token automáticamente
- Interceptor de response: Maneja errores 401 (token expirado)
```

### Servicios disponibles:
- `authService` - Login, registro, perfil
- `expenseService` - CRUD de gastos
- `incomeService` - CRUD de ingresos
- `savingService` - CRUD de ahorros
- `statsService` - Estadísticas y reportes

## 🧪 Cómo Probar

### 1. Asegúrate de que el backend esté corriendo
```bash
cd ../backend
uvicorn main:app --reload
```

### 2. Inicia el frontend
```bash
cd frontend
npm run dev
```

### 3. Navega a http://localhost:5173

### 4. Flujo de prueba:
1. **Registro**: Crea una cuenta nueva en `/register`
2. **Login**: Inicia sesión con tus credenciales
3. **Dashboard**: Verás el resumen financiero
4. **Navegación**: Usa la barra inferior para moverte entre secciones

## 🐛 Troubleshooting

### Error de CORS
Si ves errores de CORS, verifica que el backend tenga configurado:
```python
# backend/core/config.py
ALLOWED_ORIGINS="http://localhost:5173"
```

### Token expirado
Si te desloguea automáticamente, el token expiró (30 min por defecto).
Vuelve a iniciar sesión.

### Error de conexión
Verifica que:
1. El backend esté corriendo en http://localhost:8000
2. La variable `VITE_API_URL` en `.env` sea correcta
3. No haya firewall bloqueando las conexiones

## 📝 Próximas Funcionalidades

### Alta Prioridad
- [ ] Pantalla de gestión de gastos (lista, crear, editar, eliminar)
- [ ] Pantalla de gestión de ingresos
- [ ] Pantalla de gestión de ahorros
- [ ] Filtros y búsqueda en todas las listas
- [ ] Gráficos de estadísticas con Recharts

### Media Prioridad
- [ ] Perfil de usuario completo
- [ ] Exportación de datos (CSV, PDF)
- [ ] Categorías personalizables
- [ ] Modo oscuro
- [ ] Internacionalización (i18n)

### Baja Prioridad
- [ ] PWA (Progressive Web App)
- [ ] Notificaciones push
- [ ] Compartir gastos
- [ ] Recordatorios de gastos recurrentes

## 🤝 Contribuir

¿Quieres ayudar a mejorar el frontend?

1. Clona el repositorio
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Haz tus cambios
4. Commit (`git commit -am 'Agregar nueva funcionalidad'`)
5. Push (`git push origin feature/nueva-funcionalidad`)
6. Crea un Pull Request

### Áreas donde necesitamos ayuda:
- 🎨 Mejoras de UI/UX
- 📱 Optimizaciones móviles
- 📊 Componentes de gráficos
- ♿ Accesibilidad
- 🧪 Tests unitarios y E2E

## 📞 Tecnologías que necesitas conocer:
- React + TypeScript
- Tailwind CSS
- Zustand (muy fácil de aprender)
- React Router

---

**Desarrollado con React + Tailwind CSS | Optimizado para móviles** 📱

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) (or [oxc](https://oxc.rs) when used in [rolldown-vite](https://vite.dev/guide/rolldown)) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## React Compiler

The React Compiler is currently not compatible with SWC. See [this issue](https://github.com/vitejs/vite-plugin-react/issues/428) for tracking the progress.

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

```js
export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...

      // Remove tseslint.configs.recommended and replace with this
      tseslint.configs.recommendedTypeChecked,
      // Alternatively, use this for stricter rules
      tseslint.configs.strictTypeChecked,
      // Optionally, add this for stylistic rules
      tseslint.configs.stylisticTypeChecked,

      // Other configs...
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```

You can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...
      // Enable lint rules for React
      reactX.configs['recommended-typescript'],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```
