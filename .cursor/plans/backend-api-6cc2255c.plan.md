<!-- 6cc2255c-155b-465c-ad35-79bfc1d664be 86fba1a7-c81d-4019-8628-73190b251dfe -->
# Plan: Backend API REST para Módulo de Urgencias

## Estructura de archivos a crear

```
backend/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── schemas.py          # Dataclasses para request/response
│   │   ├── dependencies.py     # Inyección de dependencias y auth
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── auth.py         # Endpoints de login/register
│   │       └── urgencias.py    # Endpoints de urgencias
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Configuración (SECRET_KEY, etc)
│   │   └── security.py         # Funciones JWT
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── paciente_repo_impl.py  # Implementación de PacientesRepo
│   └── main.py                 # Aplicación FastAPI principal
└── requirements.txt            # Dependencias (fastapi, uvicorn, python-jose, passlib)
```

## Implementación paso a paso

### 1. Configuración y dependencias

**backend/requirements.txt**

- Agregar: `fastapi`, `uvicorn[standard]`, `python-jose[cryptography]`, `passlib[bcrypt]`, `python-multipart`

**backend/app/core/config.py**

- Definir configuraciones: SECRET_KEY, ALGORITHM (HS256), ACCESS_TOKEN_EXPIRE_MINUTES
- Usar variables de entorno con valores por defecto para desarrollo

**backend/app/core/security.py**

- `create_access_token(data: dict)`: Genera JWT con email, rol y matrícula
- `decode_access_token(token: str)`: Decodifica y valida JWT
- Token expira en 24 horas por defecto

### 2. Schemas con dataclasses

**backend/app/api/schemas.py**

- `LoginRequest`: email, password
- `RegisterRequest`: email, password, rol, matricula
- `TokenResponse`: access_token, token_type, user_info
- `IngresoUrgenciaRequest`: cuil, informe, nivel_emergencia, temperatura, frecuencia_cardiaca, frecuencia_respiratoria, frecuencia_sistolica, frecuencia_diastolica (+ opcionales: nombre, apellido, obra_social)
- `IngresoResponse`: id, cuil_paciente, nivel_emergencia, estado, fecha_ingreso, mensaje_advertencia
- `IngresoListItem`: Versión resumida para listar ingresos pendientes
- `ErrorResponse`: detail

### 3. Repositorio de pacientes

**backend/app/repositories/paciente_repo_impl.py**

- Clase `InMemoryPacientesRepo` que implementa `PacientesRepo`
- Métodos: `guardar_paciente()`, `obtener_paciente_por_cuil()`, `existe_paciente()`
- Usar diccionario en memoria como en `DBPacientes` del test/mocks.py

### 4. Dependencias y autenticación

**backend/app/api/dependencies.py**

- `get_pacientes_repo()`: Singleton del repositorio en memoria
- `get_user_repo()`: Singleton del repositorio de usuarios
- `get_servicio_emergencias()`: Instancia ServicioEmergencias con repo de pacientes
- `get_current_user(token: str = Depends(oauth2_scheme))`: Extrae y valida JWT, retorna Usuario
- `get_current_enfermera()`: Valida que el usuario sea ENFERMERA y retorna objeto Enfermera

### 5. Rutas de autenticación

**backend/app/api/routes/auth.py**

- `POST /api/auth/register`: Registra usuario (email, password, rol, matricula)
- `POST /api/auth/login`: Login y retorna JWT con info del usuario
- Usar funciones de `auth_service.py` existentes
- Generar token JWT con `create_access_token()`

### 6. Rutas de urgencias

**backend/app/api/routes/urgencias.py**

- `POST /api/urgencias/ingresos`: Registra ingreso (requiere auth, extrae enfermera del token)
  - Valida JWT y obtiene enfermera autenticada
  - Convierte nivel_emergencia string a enum NivelEmergencia
  - Llama a `servicio_emergencias.registrar_urgencia()`
  - Maneja ValueError → 400, Exception → 500
  - Retorna IngresoResponse con código 201

- `GET /api/urgencias/ingresos/pendientes`: Lista ingresos ordenados (requiere auth)
  - Llama a `servicio_emergencias.obtener_ingresos_pendientes()`
  - Retorna lista de IngresoListItem

- `GET /api/urgencias/niveles-emergencia`: Lista niveles disponibles (público)
  - Retorna todos los valores de NivelEmergencia enum

### 7. Aplicación principal

**backend/app/main.py**

- Crear instancia FastAPI con título y versión
- Configurar CORS: allow_origins=["http://localhost:3000"], allow_methods=["*"]
- Incluir routers: auth_router (prefix="/api/auth") y urgencias_router (prefix="/api/urgencias")
- Agregar endpoint raíz `GET /` que retorna info de la API
- Agregar endpoint `GET /health` para health check

### 8. Ajustes en código existente

**backend/app/models/models.py**

- Verificar que Usuario tenga atributo `matricula` (agregar si falta)
- Asegurar que Enfermera pueda crearse con matricula del usuario

**backend/app/services/servicio_emergencias.py**

- Verificar que el constructor de Paciente en línea 110 sea compatible (actualmente pasa obra_social como string, debería ser Domicilio)
- Ajustar para crear Paciente con Domicilio mock cuando no existe

## Validaciones implementadas

- Campos mandatorios: cuil, informe, nivel_emergencia, signos vitales
- Valores no negativos: frecuencias cardíaca, respiratoria, tensión arterial
- Formato CUIL: validado en modelo Paciente
- Nivel emergencia: validar que sea un valor del enum
- JWT: validar firma, expiración y estructura
- Rol: solo ENFERMERA puede registrar ingresos

## Manejo de errores HTTP

- 400 Bad Request: Datos inválidos, campos faltantes, valores negativos
- 401 Unauthorized: Token inválido o expirado
- 403 Forbidden: Usuario no es enfermera
- 404 Not Found: Recurso no encontrado
- 500 Internal Server Error: Errores inesperados

## Endpoints resultantes

```
POST   /api/auth/register
POST   /api/auth/login
POST   /api/urgencias/ingresos          (requiere auth ENFERMERA)
GET    /api/urgencias/ingresos/pendientes (requiere auth)
GET    /api/urgencias/niveles-emergencia (público)
GET    /health
GET    /
```

## Notas de implementación

- Usar `HTTPException` de FastAPI para errores
- Dataclasses con `@dataclass` decorator
- JWT con librería `python-jose`
- OAuth2PasswordBearer para esquema de auth
- Repositorios como singletons globales para desarrollo (en producción usar FastAPI dependencies con scope)
- CORS configurado para localhost:3000 (React default port)

## ✅ Implementación Completada

Todos los componentes del plan han sido implementados exitosamente. Ver `backend/IMPLEMENTACION_COMPLETA.md` para detalles completos.

### Archivos Adicionales Creados

- `backend/README.md`: Documentación completa de la API
- `backend/API_EXAMPLES.md`: Ejemplos de uso con PowerShell
- `backend/INICIO_RAPIDO.md`: Guía de inicio rápido
- `backend/start.ps1`: Script de inicio automático
- `backend/test-api.ps1`: Script de prueba automatizado
- `backend/IMPLEMENTACION_COMPLETA.md`: Resumen de implementación

### To-dos

- [x] Crear requirements.txt con dependencias FastAPI y JWT
- [x] Implementar config.py y security.py con funciones JWT
- [x] Crear schemas.py con dataclasses para request/response
- [x] Implementar InMemoryPacientesRepo en repositories/
- [x] Crear dependencies.py con inyección y autenticación
- [x] Implementar routes/auth.py con login y register
- [x] Implementar routes/urgencias.py con endpoints de urgencias
- [x] Crear main.py con FastAPI app y configuración CORS
- [x] Ajustar models.py y servicio_emergencias.py según necesidades