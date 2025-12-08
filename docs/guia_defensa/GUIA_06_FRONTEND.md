# GUÍA 06: Carpeta `frontend` - Interfaz Web con React y TypeScript

## 🎯 ¿Qué es el Frontend?

El **frontend** es la **interfaz gráfica** del sistema: lo que ven y usan los usuarios (enfermeras y médicos).

**Tecnologías:**
- **React**: Librería para construir interfaces (componentes reutilizables)
- **TypeScript**: JavaScript con tipos (detecta errores antes de ejecutar)
- **Material-UI (MUI)**: Biblioteca de componentes visuales (botones, formularios, tablas)
- **Vite**: Herramienta de build y desarrollo (más rápido que Webpack)
- **Axios**: Cliente HTTP para comunicarse con el backend

---

## 📁 Estructura

```
frontend/
├── package.json           # Dependencias y scripts
├── tsconfig.json          # Configuración de TypeScript
├── vite.config.ts         # Configuración de Vite
├── index.html             # Archivo HTML principal
├── public/                # Archivos estáticos
└── src/                   # Código fuente
    ├── App.tsx            # ⭐ Componente raíz con routing
    ├── main.tsx           # Punto de entrada
    ├── assets/            # Imágenes, iconos, etc.
    ├── components/        # Componentes reutilizables
    │   ├── auth/          # Login, registro, rutas protegidas
    │   ├── common/        # Navbar, etc.
    │   └── urgencias/     # Componentes del módulo de urgencias
    ├── context/           # Contextos de React (estado global)
    │   └── AuthContext.tsx
    ├── hooks/             # Custom hooks
    │   ├── useAuth.ts
    │   └── useUrgencias.ts
    ├── pages/             # Páginas/vistas principales
    │   ├── LoginPage.tsx
    │   ├── UrgenciasPage.tsx
    │   └── RevisionPacientePage.tsx
    ├── services/          # Servicios para llamar al backend
    │   ├── authService.ts
    │   ├── pacientesService.ts
    │   └── urgenciasService.ts
    └── utils/             # Utilidades
        ├── api.ts         # Configuración de Axios
        └── constants.ts   # Constantes
```

---

## 📦 Archivo: `package.json`

Lista las **dependencias** (librerías) del frontend.

```json
{
  "dependencies": {
    "@mui/material": "^7.3.5",        // Material-UI (componentes visuales)
    "@mui/icons-material": "^7.3.5",  // Iconos de Material-UI
    "axios": "^1.13.2",               // Cliente HTTP
    "react": "^19.2.0",               // Librería principal
    "react-dom": "^19.2.0",           // React para el navegador
    "react-hook-form": "^7.66.1",     // Manejo de formularios
    "react-router-dom": "^7.9.6"      // Routing (navegación)
  },
  "devDependencies": {
    "typescript": "~5.9.3",           // TypeScript
    "vite": "^7.2.4",                 // Build tool
    "@vitejs/plugin-react": "^5.1.1"  // Plugin de React para Vite
  }
}
```

---

## 🚀 ¿Cómo ejecutar el frontend?

```bash
cd frontend
npm install      # Instalar dependencias (solo la primera vez)
npm run dev      # Iniciar servidor de desarrollo
```

**Acceso:** http://localhost:3000

---

## ⚛️ React: Conceptos Básicos

### ¿Qué es React?

Una librería para construir **interfaces** usando **componentes**.

**Componente** = Pieza reutilizable de UI (como un botón, formulario, lista)

**Ejemplo:**
```tsx
function Boton() {
  return <button>Click aquí</button>;
}
```

### JSX/TSX

Es **HTML dentro de JavaScript/TypeScript**.

```tsx
const nombre = "Juan";
return <h1>Hola, {nombre}</h1>;  // Hola, Juan
```

### Props (Propiedades)

Parámetros que pasas a un componente.

```tsx
function Saludo(props: { nombre: string }) {
  return <h1>Hola, {props.nombre}</h1>;
}

<Saludo nombre="María" />  // Hola, María
```

### State (Estado)

Variables que, al cambiar, **re-renderizan** el componente.

```tsx
const [contador, setContador] = useState(0);

return (
  <button onClick={() => setContador(contador + 1)}>
    Contador: {contador}
  </button>
);
```

---

## 🗂️ TypeScript: ¿Por qué?

**TypeScript** = JavaScript + tipos estáticos

### Sin tipos (JavaScript):
```javascript
function sumar(a, b) {
  return a + b;
}

sumar(5, "10");  // "510" (concatenación, no suma) ❌
```

### Con tipos (TypeScript):
```typescript
function sumar(a: number, b: number): number {
  return a + b;
}

sumar(5, "10");  // ❌ ERROR en tiempo de compilación
```

**Ventajas:**
- ✅ Detecta errores antes de ejecutar
- ✅ Autocompletado en el editor
- ✅ Refactoring más seguro
- ✅ Documentación automática

---

## 📂 Desglose de Subcarpetas

### 1. `App.tsx` - ⭐ Componente Raíz

Define las **rutas** de la aplicación.

```tsx
function App() {
  return (
    <ThemeProvider theme={theme}>
      <AuthProvider>
        <Router>
          <Routes>
            {/* Ruta raíz redirige a urgencias */}
            <Route path="/" element={<Navigate to="/urgencias" />} />
            
            {/* Ruta pública */}
            <Route path="/login" element={<LoginPage />} />
            
            {/* Rutas protegidas (requieren autenticación) */}
            <Route
              path="/urgencias"
              element={
                <ProtectedRoute allowedRoles={['ENFERMERA', 'MEDICO']}>
                  <UrgenciasPage />
                </ProtectedRoute>
              }
            />
            
            <Route
              path="/urgencias/revision/:id"
              element={
                <ProtectedRoute allowedRoles={['MEDICO']}>
                  <RevisionPacientePage />
                </ProtectedRoute>
              }
            />
          </Routes>
        </Router>
      </AuthProvider>
    </ThemeProvider>
  );
}
```

**¿Qué hace?**
1. **ThemeProvider**: Aplica el tema de Material-UI (colores, fuentes)
2. **AuthProvider**: Provee contexto de autenticación (usuario logueado)
3. **Router**: Habilita navegación (URLs)
4. **Routes**: Define qué componente mostrar según la URL
5. **ProtectedRoute**: Protege rutas que requieren login

---

### 2. `context/AuthContext.tsx` - Estado Global de Autenticación

**¿Qué es un Context?**
- Estado compartido entre **muchos** componentes
- Evita pasar props manualmente por cada nivel

```tsx
const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC = ({ children }) => {
  const [user, setUser] = useState<UserInfo | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Al cargar, verificar si hay usuario en localStorage
  useEffect(() => {
    if (isAuthenticated()) {
      const currentUser = getCurrentUser();
      setUser(currentUser);
    }
    setIsLoading(false);
  }, []);

  const login = async (credentials: LoginCredentials) => {
    const response = await loginService(credentials);
    setUser(response.user_info);
  };

  const logout = () => {
    logoutService();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, isLoading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
```

**Flujo:**
1. Al cargar, verifica si hay token en `localStorage`
2. Si hay token válido, carga datos del usuario
3. Expone funciones `login()` y `logout()` a todos los componentes

---

### 3. `services/` - Comunicación con el Backend

#### `services/api.ts` - Configuración de Axios

```typescript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',  // URL del backend
  timeout: 10000,
});

// Interceptor: agrega el token JWT a cada petición
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  }
);

export default api;
```

**¿Qué es un interceptor?**
- Función que se ejecuta **antes** de cada petición
- En este caso: Agrega el header `Authorization: Bearer <token>`

---

#### `services/authService.ts` - Servicios de Autenticación

```typescript
export const login = async (credentials: LoginCredentials): Promise<LoginResponse> => {
  const response = await api.post('/auth/login', credentials);
  
  // Guardar token en localStorage
  localStorage.setItem('token', response.data.access_token);
  localStorage.setItem('user', JSON.stringify(response.data.user_info));
  
  return response.data;
};

export const logout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
};

export const isAuthenticated = (): boolean => {
  return !!localStorage.getItem('token');
};

export const getCurrentUser = (): UserInfo | null => {
  const userStr = localStorage.getItem('user');
  return userStr ? JSON.parse(userStr) : null;
};
```

**¿Por qué localStorage?**
- Almacenamiento persistente en el navegador
- El token se mantiene incluso si cierras la pestaña
- **Nota**: En producción se usan cookies httpOnly para más seguridad

---

#### `services/urgenciasService.ts` - Servicios de Urgencias

```typescript
export const registrarIngreso = async (data: IngresoUrgenciaRequest): Promise<IngresoResponse> => {
  const response = await api.post('/urgencias/ingresos', data);
  return response.data;
};

export const listarIngresosPendientes = async (): Promise<IngresoListItem[]> => {
  const response = await api.get('/urgencias/ingresos/pendientes');
  return response.data;
};

export const reclamarPaciente = async (): Promise<ReclamarResponse> => {
  const response = await api.post('/urgencias/ingresos/reclamar');
  return response.data;
};

export const buscarPacientePorCuil = async (cuil: string): Promise<PacienteResponse | null> => {
  try {
    const response = await api.get(`/urgencias/pacientes/${cuil}`);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response?.status === 404) {
      return null;  // Paciente no existe
    }
    throw error;
  }
};
```

**Patrón:**
1. Hace petición HTTP al backend con `api.post()` o `api.get()`
2. El backend procesa y responde JSON
3. Retorna los datos parseados

---

### 4. `hooks/` - Custom Hooks

#### ¿Qué es un Hook?

Función que "engancha" funcionalidades de React (estado, efectos, etc.)

**Hooks built-in:**
- `useState`: Estado local
- `useEffect`: Efectos secundarios
- `useContext`: Acceder a contexto

**Custom hooks**: Encapsulan lógica reutilizable.

---

#### `hooks/useAuth.ts`

```typescript
export const useAuth = () => {
  const context = useAuthContext();
  
  if (!context) {
    throw new Error('useAuth debe usarse dentro de AuthProvider');
  }
  
  return context;
};
```

**Uso en componentes:**
```tsx
function MiComponente() {
  const { user, login, logout } = useAuth();
  
  if (!user) {
    return <div>No autenticado</div>;
  }
  
  return <div>Hola, {user.email}</div>;
}
```

---

#### `hooks/useUrgencias.ts`

```typescript
export const useUrgencias = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const registrar = async (data: IngresoUrgenciaRequest) => {
    setLoading(true);
    setError(null);
    
    try {
      const result = await registrarIngreso(data);
      return result;
    } catch (err) {
      const message = getErrorMessage(err);
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const reclamar = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const result = await reclamarPaciente();
      return result;
    } catch (err) {
      const message = getErrorMessage(err);
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { registrar, reclamar, loading, error };
};
```

**¿Por qué un hook personalizado?**
- Encapsula lógica de loading y manejo de errores
- Reutilizable en múltiples componentes
- Código más limpio

---

### 5. `components/` - Componentes Reutilizables

#### `components/auth/ProtectedRoute.tsx`

```tsx
interface ProtectedRouteProps {
  allowedRoles: string[];
  children: ReactNode;
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ allowedRoles, children }) => {
  const { user, isLoading } = useAuth();

  if (isLoading) {
    return <CircularProgress />;  // Spinner de carga
  }

  if (!user) {
    return <Navigate to="/login" />;  // Redirigir a login
  }

  if (!allowedRoles.includes(user.rol)) {
    return <Alert severity="error">No tienes permisos</Alert>;
  }

  return <>{children}</>;  // Mostrar el componente hijo
};
```

**¿Cómo funciona?**
1. Verifica si está cargando → Muestra spinner
2. Verifica si hay usuario → Si no, redirige a login
3. Verifica el rol → Si no tiene permisos, muestra error
4. Si todo ok → Muestra el componente hijo

---

#### `components/urgencias/FormularioAdmision.tsx`

Formulario grande con:
- Campo CUIL con búsqueda
- Datos del paciente (si no existe)
- Domicilio (si es nuevo)
- Informe
- Nivel de emergencia
- Signos vitales

**Flujo:**
1. Usuario ingresa CUIL y presiona "Buscar"
2. Si paciente existe: Autocompleta datos
3. Si no existe: Muestra campos adicionales
4. Usuario completa signos vitales
5. Al enviar: Llama a `useUrgencias().registrar()`

```tsx
const buscarPaciente = async () => {
  const paciente = await buscarPacientePorCuil(cuil);
  
  if (paciente) {
    setPacienteExiste(true);
    setNombre(paciente.nombre);
    setApellido(paciente.apellido);
    // ...
    setSuccess('Paciente encontrado');
  } else {
    setPacienteExiste(false);
    setWarning('Paciente no existe. Complete los datos.');
  }
};

const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();
  
  try {
    const response = await registrar({
      cuil,
      informe,
      nivel_emergencia: nivelEmergencia,
      temperatura: parseFloat(temperatura),
      // ... más campos
      nombre: pacienteExiste ? undefined : nombre,
      apellido: pacienteExiste ? undefined : apellido,
      // ...
    });
    
    setSuccess('Ingreso registrado exitosamente');
    onSuccess?.();  // Callback para refrescar lista
  } catch (err) {
    // Error ya manejado por el hook
  }
};
```

---

#### `components/urgencias/ListaEspera.tsx`

Muestra tabla de pacientes pendientes, ordenados por prioridad.

```tsx
export const ListaEspera: React.FC = ({ refreshTrigger, showReclamarButton, onReclamar }) => {
  const [ingresos, setIngresos] = useState<IngresoListItem[]>([]);

  useEffect(() => {
    const cargar = async () => {
      const data = await listarIngresosPendientes();
      setIngresos(data);
    };
    cargar();
  }, [refreshTrigger]);  // Se re-ejecuta cuando cambia refreshTrigger

  return (
    <Paper>
      <Typography variant="h6">Lista de Espera</Typography>
      
      {showReclamarButton && (
        <Button onClick={onReclamar}>Reclamar Siguiente Paciente</Button>
      )}
      
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Posición</TableCell>
            <TableCell>CUIL</TableCell>
            <TableCell>Paciente</TableCell>
            <TableCell>Nivel</TableCell>
            <TableCell>Fecha Ingreso</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {ingresos.map((ingreso, index) => (
            <TableRow key={ingreso.id}>
              <TableCell>{index + 1}</TableCell>
              <TableCell>{ingreso.cuil_paciente}</TableCell>
              <TableCell>{ingreso.nombre_paciente} {ingreso.apellido_paciente}</TableCell>
              <TableCell>
                <Chip label={ingreso.nivel_emergencia_nombre} color={getColor(ingreso.nivel_emergencia)} />
              </TableCell>
              <TableCell>{formatFecha(ingreso.fecha_ingreso)}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </Paper>
  );
};
```

**Detalles:**
- **useEffect con refreshTrigger**: Cada vez que el padre incrementa `refreshTrigger`, se recarga la lista
- **Chip con color**: Muestra el nivel con color (rojo=crítico, verde=menor)
- **Botón condicional**: Solo médicos ven "Reclamar"

---

### 6. `pages/` - Vistas Principales

#### `pages/LoginPage.tsx`

```tsx
export const LoginPage: React.FC = () => {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      await login({ email, password });
      navigate('/urgencias');  // Redirigir tras login exitoso
    } catch (err) {
      alert('Error de autenticación');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <TextField label="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
      <TextField label="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
      <Button type="submit">Iniciar Sesión</Button>
    </form>
  );
};
```

---

#### `pages/UrgenciasPage.tsx`

Página principal con:
1. Formulario de admisión
2. Lista de pacientes en proceso
3. Lista de espera

```tsx
export const UrgenciasPage: React.FC = () => {
  const [refreshPendientes, setRefreshPendientes] = useState(0);
  const [refreshEnProceso, setRefreshEnProceso] = useState(0);

  const handleIngresoSuccess = () => {
    setRefreshPendientes(prev => prev + 1);  // Trigger refresh
  };

  const handleReclamar = async () => {
    await reclamar();
    setRefreshPendientes(prev => prev + 1);
    setRefreshEnProceso(prev => prev + 1);
  };

  return (
    <Box>
      <Navbar />
      <FormularioAdmision onSuccess={handleIngresoSuccess} />
      <ListaRevisionEnProceso refreshTrigger={refreshEnProceso} />
      <ListaEspera 
        refreshTrigger={refreshPendientes}
        showReclamarButton={isMedico()}
        onReclamar={handleReclamar}
      />
    </Box>
  );
};
```

---

## 🎨 Material-UI (MUI)

**MUI** provee componentes pre-construidos con diseño "Material Design" (diseño de Google).

**Componentes usados:**
- `Button`, `TextField`: Inputs
- `Paper`, `Card`: Contenedores con sombra
- `Table`, `TableRow`: Tablas
- `Chip`: Etiquetas de color
- `Alert`, `Snackbar`: Notificaciones
- `CircularProgress`: Spinner de carga
- `Typography`: Textos con estilos

**Ejemplo:**
```tsx
<Button variant="contained" color="primary" startIcon={<SaveIcon />}>
  Guardar
</Button>
```

---

## 🔄 Flujo Completo: Registrar Ingreso

1. **Usuario**: Abre `/urgencias`
2. **ProtectedRoute**: Verifica autenticación → OK
3. **UrgenciasPage**: Renderiza componentes
4. **FormularioAdmision**: Usuario completa datos
5. **Click "Guardar"**: 
   - Llama `useUrgencias().registrar()`
   - Llama `urgenciasService.registrarIngreso()`
   - Axios hace `POST http://localhost:8000/api/urgencias/ingresos`
   - Backend procesa y responde
6. **Respuesta exitosa**: 
   - Muestra mensaje de éxito
   - Llama `onSuccess()` → incrementa `refreshTrigger`
   - `ListaEspera` detecta cambio y recarga datos

---

## 🎤 Resumen para tu Defensa

**Pregunta:** "Explica la arquitectura del frontend"

**Respuesta:**
> "El frontend está construido con **React y TypeScript**, usando **Vite** como build tool. Implementamos una arquitectura basada en componentes reutilizables organizados en capas:
> 
> - **Pages**: Vistas principales (Login, Urgencias, Revisión)
> - **Components**: Componentes reutilizables (FormularioAdmision, ListaEspera)
> - **Services**: Capa de comunicación con el backend via Axios
> - **Hooks**: Lógica reutilizable (useAuth, useUrgencias)
> - **Context**: Estado global (autenticación)
> 
> Para la UI usamos **Material-UI** que provee componentes con diseño Material Design. La autenticación se maneja con **JWT tokens** almacenados en localStorage, y cada petición al backend incluye el token en el header Authorization.
> 
> Implementamos **rutas protegidas** que verifican el rol del usuario (enfermeras pueden registrar, solo médicos pueden reclamar pacientes). El routing se maneja con **React Router**, y el estado se actualiza reactivamente usando hooks como useState y useEffect."

**Puntos clave:**
- 📌 **React**: Componentes reutilizables
- 📌 **TypeScript**: Tipado estático
- 📌 **Vite**: Build tool moderno
- 📌 **Material-UI**: Biblioteca de componentes
- 📌 **Axios**: Cliente HTTP con interceptors
- 📌 **React Router**: Navegación
- 📌 **Custom Hooks**: Lógica reutilizable
- 📌 **Context API**: Estado global

---

## 📚 Conceptos Clave

| Concepto | Explicación |
|----------|-------------|
| **React** | Librería para construir UIs con componentes |
| **TypeScript** | JavaScript con tipos estáticos |
| **Component** | Pieza reutilizable de UI |
| **Props** | Parámetros que recibe un componente |
| **State** | Datos que cambian y re-renderizan el componente |
| **Hook** | Función que "engancha" funcionalidades de React |
| **Context** | Estado compartido entre muchos componentes |
| **Routing** | Navegación entre páginas (URLs) |
| **JWT** | Token de autenticación |
| **Axios** | Cliente HTTP para hacer peticiones |
| **Interceptor** | Función que modifica peticiones/respuestas |
| **Material-UI** | Biblioteca de componentes visuales |

---

**Siguiente:** Ahora crearemos la guía final de **integración** que explica cómo todo funciona junto. 🚀
