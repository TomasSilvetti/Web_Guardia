# API REST - Módulo de Urgencias

API REST para el módulo de urgencias del sistema de gestión hospitalaria.

## Instalación

### 1. Crear entorno virtual

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Instalar dependencias

```powershell
pip install -r requirements.txt
```

## Ejecución

### Modo desarrollo

```powershell
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

### Modo producción

```powershell
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```

## Documentación de la API

Una vez iniciado el servidor, la documentación interactiva está disponible en:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Endpoints

### Autenticación

#### POST /api/auth/register
Registra un nuevo usuario en el sistema.

**Request Body:**
```json
{
  "email": "enfermera@hospital.com",
  "password": "password123",
  "rol": "Enfermera",
  "matricula": "ENF-12345"
}
```

**Response:** (201 Created)
```json
{
  "message": "Usuario registrado exitosamente",
  "email": "enfermera@hospital.com",
  "rol": "Enfermera"
}
```

#### POST /api/auth/login
Autentica un usuario y retorna un token JWT.

**Request Body:**
```json
{
  "email": "enfermera@hospital.com",
  "password": "password123"
}
```

**Response:** (200 OK)
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_info": {
    "email": "enfermera@hospital.com",
    "rol": "Enfermera",
    "matricula": "ENF-12345"
  }
}
```

### Urgencias

#### POST /api/urgencias/ingresos
Registra un nuevo ingreso de urgencia. **Requiere autenticación y rol ENFERMERA**.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "cuil": "20-12345678-9",
  "informe": "Paciente con dolor abdominal agudo",
  "nivel_emergencia": "URGENCIA",
  "temperatura": 37.5,
  "frecuencia_cardiaca": 85,
  "frecuencia_respiratoria": 18,
  "frecuencia_sistolica": 120,
  "frecuencia_diastolica": 80,
  "nombre": "Juan",
  "apellido": "Pérez",
  "obra_social": "OSDE"
}
```

**Response:** (201 Created)
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "cuil_paciente": "20-12345678-9",
  "nivel_emergencia": "URGENCIA",
  "estado": "PENDIENTE",
  "fecha_ingreso": "2024-11-20T10:30:00",
  "mensaje_advertencia": null
}
```

#### GET /api/urgencias/ingresos/pendientes
Lista todos los ingresos pendientes ordenados por prioridad. **Requiere autenticación**.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:** (200 OK)
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "cuil_paciente": "20-12345678-9",
    "nombre_paciente": "Juan",
    "apellido_paciente": "Pérez",
    "nivel_emergencia": "URGENCIA",
    "nivel_emergencia_nombre": "Urgencia",
    "estado": "PENDIENTE",
    "fecha_ingreso": "2024-11-20T10:30:00",
    "temperatura": 37.5,
    "frecuencia_cardiaca": 85,
    "frecuencia_respiratoria": 18,
    "frecuencia_sistolica": 120,
    "frecuencia_diastolica": 80
  }
]
```

#### GET /api/urgencias/niveles-emergencia
Lista todos los niveles de emergencia disponibles. **Endpoint público**.

**Response:** (200 OK)
```json
[
  {
    "valor": "CRITICA",
    "nombre": "Critica",
    "nivel": 0,
    "duracion_max_espera_minutos": 5
  },
  {
    "valor": "EMERGENCIA",
    "nombre": "Emergencia",
    "nivel": 1,
    "duracion_max_espera_minutos": 30
  },
  {
    "valor": "URGENCIA",
    "nombre": "Urgencia",
    "nivel": 2,
    "duracion_max_espera_minutos": 60
  },
  {
    "valor": "URGENCIA_MENOR",
    "nombre": "Urgencia Menor",
    "nivel": 3,
    "duracion_max_espera_minutos": 120
  },
  {
    "valor": "SIN_URGENCIA",
    "nombre": "Sin Urgencia",
    "nivel": 4,
    "duracion_max_espera_minutos": 240
  }
]
```

### Health Check

#### GET /health
Verifica el estado de la API.

**Response:** (200 OK)
```json
{
  "status": "healthy",
  "timestamp": "2024-11-20T10:30:00",
  "version": "1.0.0"
}
```

#### GET /
Información general de la API.

**Response:** (200 OK)
```json
{
  "name": "API Módulo de Urgencias",
  "version": "1.0.0",
  "description": "API REST para el módulo de urgencias",
  "endpoints": {
    "auth": "/api/auth",
    "urgencias": "/api/urgencias",
    "health": "/health",
    "docs": "/docs"
  }
}
```

## Códigos de Estado HTTP

- **200 OK**: Solicitud exitosa
- **201 Created**: Recurso creado exitosamente
- **400 Bad Request**: Datos inválidos o campos faltantes
- **401 Unauthorized**: Token inválido o expirado
- **403 Forbidden**: Usuario no tiene permisos (no es enfermera)
- **404 Not Found**: Recurso no encontrado
- **500 Internal Server Error**: Error inesperado del servidor

## Validaciones

### Campos obligatorios para registro de ingreso:
- `cuil`: CUIL del paciente (formato: XX-XXXXXXXX-X)
- `informe`: Descripción del motivo de ingreso
- `nivel_emergencia`: Nivel de emergencia (CRITICA, EMERGENCIA, URGENCIA, URGENCIA_MENOR, SIN_URGENCIA)
- `temperatura`: Temperatura corporal (≥ 0)
- `frecuencia_cardiaca`: Frecuencia cardíaca (≥ 0)
- `frecuencia_respiratoria`: Frecuencia respiratoria (≥ 0)
- `frecuencia_sistolica`: Presión arterial sistólica (≥ 0)
- `frecuencia_diastolica`: Presión arterial diastólica (≥ 0)

### Campos opcionales:
- `nombre`: Nombre del paciente (requerido si el paciente no existe)
- `apellido`: Apellido del paciente (requerido si el paciente no existe)
- `obra_social`: Obra social del paciente (requerido si el paciente no existe)

## Configuración

Las configuraciones se pueden modificar mediante variables de entorno:

- `SECRET_KEY`: Clave secreta para JWT (default: "dev-secret-key-change-in-production-12345678")
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Tiempo de expiración del token en minutos (default: 1440 = 24 horas)

## Arquitectura

```
backend/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── auth.py          # Endpoints de autenticación
│   │   │   └── urgencias.py     # Endpoints de urgencias
│   │   ├── schemas.py           # Schemas request/response
│   │   └── dependencies.py      # Inyección de dependencias
│   ├── core/
│   │   ├── config.py            # Configuración
│   │   └── security.py          # Funciones JWT
│   ├── models/
│   │   └── models.py            # Modelos de dominio
│   ├── repositories/
│   │   └── paciente_repo_impl.py # Repositorio de pacientes
│   ├── services/
│   │   ├── auth_service.py      # Servicio de autenticación
│   │   └── servicio_emergencias.py # Servicio de urgencias
│   └── main.py                  # Aplicación FastAPI
└── requirements.txt             # Dependencias
```

## Testing

Para ejecutar los tests:

```powershell
pytest backend/app/test/
```

## CORS

La API está configurada para aceptar peticiones desde:
- http://localhost:3000
- http://localhost:3001
- http://127.0.0.1:3000

Para agregar más orígenes, modificar `CORS_ORIGINS` en `backend/app/core/config.py`.

