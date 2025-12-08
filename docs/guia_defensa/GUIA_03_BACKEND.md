# GUÍA 03: Carpeta `backend` - API REST con Python y FastAPI

## 🎯 Visión General

El **backend** es el "cerebro" de tu aplicación. Es un **servidor API REST** construido con:
- **Lenguaje**: Python 3.11
- **Framework**: FastAPI (para crear APIs web rápidas)
- **Arquitectura**: Capas separadas (Clean Architecture)

### ¿Qué hace el backend?
- ✅ Recibe peticiones HTTP del frontend
- ✅ Valida datos
- ✅ Ejecuta lógica de negocio (reglas de urgencias)
- ✅ Almacena/recupera información
- ✅ Devuelve respuestas en formato JSON

---

## 📁 Estructura del Backend

```
backend/
├── __init__.py              # Indica que backend es un paquete Python
├── README.md                # Documentación básica
├── requirements.txt         # Lista de librerías necesarias
├── start.ps1                # Script para iniciar el servidor (Windows)
└── app/                     # Aplicación principal
    ├── __init__.py
    ├── main.py              # ⭐ Punto de entrada de la aplicación
    ├── api/                 # Capa de presentación (endpoints HTTP)
    │   ├── __init__.py
    │   ├── dependencies.py  # Inyección de dependencias
    │   ├── schemas.py       # Modelos de request/response (DTOs)
    │   └── routes/
    │       ├── __init__.py
    │       ├── auth.py      # Endpoints de autenticación
    │       └── urgencias.py # Endpoints de urgencias
    ├── core/                # Configuración central
    │   ├── __init__.py
    │   ├── config.py        # Variables de configuración
    │   └── security.py      # Funciones de JWT
    ├── interfaces/          # Contratos (interfaces/abstracciones)
    │   ├── __init__.py
    │   └── pacientes_repo.py
    ├── models/              # Capa de dominio (entidades, value objects)
    │   ├── __init__.py
    │   └── models.py        # ⭐ Todas las clases de negocio
    ├── repositories/        # Capa de datos (acceso a "BD")
    │   ├── __init__.py
    │   └── paciente_repo_impl.py
    ├── schemas/             # Esquemas adicionales
    │   └── persona.py
    ├── services/            # Capa de servicios (lógica de negocio)
    │   ├── __init__.py
    │   ├── auth_service.py
    │   ├── paciente_service.py
    │   └── servicio_emergencias.py  # ⭐ Lógica de urgencias
    └── test/                # Tests unitarios
        ├── __init__.py
        ├── mocks.py
        ├── test_auth_service.py
        ├── test_auth.py
        ├── test_models.py
        └── test_paciente_service.py
```

---

## 🤔 ¿Por qué hay `__init__.py` en TODAS las carpetas?

### Explicación simple:
En Python, para que una carpeta sea reconocida como un **paquete** (y puedas importar archivos desde ella), DEBE tener un archivo `__init__.py`.

**Ejemplo práctico:**

Sin `__init__.py`:
```python
# ❌ ESTO NO FUNCIONA
from backend.app.models import Paciente  # Error: backend no es un paquete
```

Con `__init__.py`:
```python
# ✅ ESTO SÍ FUNCIONA
from backend.app.models.models import Paciente
```

**¿Qué va dentro de `__init__.py`?**
- Puede estar vacío (solo indica "esto es un paquete")
- Puede tener código de inicialización
- En tu proyecto, la mayoría están vacíos

---

## 📦 Archivo: `requirements.txt`

Este archivo lista TODAS las librerías (dependencias) que necesita el backend.

```txt
fastapi==0.104.1          # Framework web para crear APIs REST
uvicorn[standard]==0.24.0 # Servidor ASGI para ejecutar FastAPI
python-jose[cryptography]==3.3.0  # Para crear/validar tokens JWT
python-multipart==0.0.6   # Para manejar formularios multipart
bcrypt==4.1.1             # Para hashear contraseñas
pytest==7.4.3             # Framework de testing
```

**¿Cómo se instalan?**
```bash
pip install -r requirements.txt
```

---

## ⭐ Archivo Principal: `main.py`

Este es el **punto de entrada** del backend.

### ¿Qué hace?

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Crear la aplicación FastAPI
app = FastAPI(
    title="API Módulo de Urgencias",
    version="1.0.0",
    description="API REST para el módulo de urgencias..."
)
```

**Traducción:** Crea una aplicación web usando FastAPI.

### Configurar CORS

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Permitir frontend
    allow_credentials=True,
    allow_methods=["*"],  # Todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Todos los headers
)
```

**¿Qué es CORS?**
- **CORS** = Cross-Origin Resource Sharing
- Por seguridad, los navegadores bloquean peticiones entre dominios diferentes
- Esto permite que tu frontend (localhost:3000) se comunique con el backend (localhost:8000)

### Incluir rutas

```python
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(urgencias.router, prefix="/api/urgencias", tags=["urgencias"])
```

**Traducción:** 
- Todos los endpoints de `auth.py` estarán bajo `/api/auth/...`
- Todos los endpoints de `urgencias.py` estarán bajo `/api/urgencias/...`

### Endpoints raíz

```python
@app.get("/")
def root():
    return {"name": "API Módulo de Urgencias", ...}

@app.get("/health")
def health_check():
    return {"status": "healthy", ...}
```

**Uso:**
- `/` → Info básica de la API
- `/health` → Verificar si el servidor está funcionando

---

## 🏗️ Arquitectura por Capas

Tu proyecto sigue **Clean Architecture** / **Arquitectura Hexagonal**:

```
┌─────────────────────────────────────────┐
│  CAPA DE PRESENTACIÓN (API)             │
│  - Recibe requests HTTP                 │
│  - Devuelve responses JSON              │
│  📁 api/routes/*.py                     │
└───────────────┬─────────────────────────┘
                │
┌───────────────▼─────────────────────────┐
│  CAPA DE SERVICIOS (Lógica de Negocio)  │
│  - Valida reglas de negocio             │
│  - Coordina operaciones                 │
│  📁 services/*.py                       │
└───────────────┬─────────────────────────┘
                │
┌───────────────▼─────────────────────────┐
│  CAPA DE DOMINIO (Entidades)            │
│  - Define objetos del negocio           │
│  - Paciente, Ingreso, NivelEmergencia   │
│  📁 models/models.py                    │
└───────────────┬─────────────────────────┘
                │
┌───────────────▼─────────────────────────┐
│  CAPA DE DATOS (Repositorios)           │
│  - Acceso a almacenamiento              │
│  - En este caso: memoria (diccionarios) │
│  📁 repositories/*.py                   │
└─────────────────────────────────────────┘
```

**¿Por qué esta separación?**
- ✅ **Mantenibilidad**: Cada capa tiene su responsabilidad
- ✅ **Testabilidad**: Puedes testear cada capa por separado
- ✅ **Escalabilidad**: Puedes cambiar una capa sin afectar otras
- ✅ **Profesionalismo**: Es la forma "correcta" en ingeniería de software

---

## 📂 Desglose de Subcarpetas

### 1. `api/` - Capa de Presentación

**Propósito:** Manejar peticiones HTTP y convertirlas en llamadas a servicios.

#### `api/schemas.py` - DTOs (Data Transfer Objects)

Define la estructura de los datos que se envían/reciben por HTTP:

```python
@dataclass
class LoginRequest:
    email: str
    password: str

@dataclass  
class IngresoUrgenciaRequest:
    cuil: str
    informe: str
    nivel_emergencia: str
    temperatura: float
    frecuencia_cardiaca: float
    # ... más campos
```

**¿Para qué?**
- Validar que el cliente envíe los datos correctos
- Documentación automática (FastAPI genera docs en `/docs`)

#### `api/dependencies.py` - Inyección de Dependencias

```python
def get_servicio_emergencias() -> ServicioEmergencias:
    """Retorna una instancia del servicio de emergencias"""
    repo = get_pacientes_repo()
    return ServicioEmergencias(repo)

def get_current_user(token: str = Depends(oauth2_scheme)) -> Usuario:
    """Extrae y valida el token JWT, retorna el usuario"""
    # Decodifica JWT y verifica que sea válido
```

**¿Qué es inyección de dependencias?**
- En vez de crear objetos manualmente, FastAPI los "inyecta" automáticamente
- Facilita testing (puedes inyectar mocks)

#### `api/routes/auth.py` - Endpoints de Autenticación

```python
@router.post("/register")
def register_user(request: RegisterRequest, ...):
    """Registra un nuevo usuario (enfermera o médico)"""
    
@router.post("/login")
def login_user(request: LoginRequest, ...):
    """Login, retorna JWT token"""
```

**Flujo de login:**
1. Usuario envía email + password
2. Backend verifica credenciales
3. Si son correctas, genera un **JWT token**
4. Cliente guarda el token
5. En cada petición futura, cliente envía el token en el header

#### `api/routes/urgencias.py` - Endpoints del Módulo de Urgencias

```python
@router.post("/ingresos")
def registrar_ingreso(
    request: IngresoUrgenciaRequest,
    enfermera: Enfermera = Depends(get_current_enfermera),
    servicio: ServicioEmergencias = Depends(get_servicio_emergencias)
):
    """Registra un nuevo ingreso de urgencia"""
    # 1. Valida que el usuario sea enfermera (ya hecho por Depends)
    # 2. Llama al servicio para registrar
    # 3. Retorna respuesta

@router.get("/ingresos/pendientes")
def listar_pendientes(...):
    """Lista ingresos ordenados por prioridad"""

@router.post("/ingresos/reclamar")
def reclamar_paciente(...):
    """Médico reclama el siguiente paciente"""
```

---

### 2. `core/` - Configuración Central

#### `core/config.py`

```python
class Settings:
    SECRET_KEY: str = "dev-secret-key-..."  # Para firmar JWT
    ALGORITHM: str = "HS256"  # Algoritmo de cifrado
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 horas
    
    CORS_ORIGINS: list = ["http://localhost:3000"]
    
    APP_NAME: str = "API Módulo de Urgencias"
    API_PREFIX: str = "/api"

settings = Settings()
```

**¿Por qué centralizar config?**
- Fácil cambiar valores
- No repetir "magic numbers"
- Poder usar variables de entorno en producción

#### `core/security.py` - Funciones JWT

```python
def create_access_token(data: dict) -> str:
    """Crea un token JWT con los datos del usuario"""
    # Agrega expiración
    # Firma con SECRET_KEY
    # Retorna string codificado

def decode_access_token(token: str) -> dict:
    """Decodifica y valida un token JWT"""
    # Verifica firma
    # Verifica expiración
    # Retorna datos del token
```

**¿Qué es JWT?**
- **JSON Web Token**
- Es un string codificado que contiene información del usuario
- No se puede falsificar (está firmado)
- Ejemplo: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

---

### 3. `models/models.py` - ⭐ Capa de Dominio (LO MÁS IMPORTANTE)

Aquí están TODAS las clases de negocio. Es el "corazón" del sistema.

#### Value Objects (Objetos de Valor)

```python
class Temperatura:
    def __init__(self, valor: float):
        if valor < 0:
            raise ValueError("La temperatura no puede ser negativa")
        self.valor = valor
```

**¿Qué es un Value Object?**
- Representa un valor con validaciones
- No tiene identidad propia
- Es inmutable (no cambia)

**Otros Value Objects:**
- `FrecuenciaCardiaca`
- `FrecuenciaRespiratoria`
- `TensionArterial`

#### Enums (Enumeraciones)

```python
class NivelEmergencia(Enum):
    CRITICA = {
        "nivel": 0,
        "nombre": "Critica",
        "duracionMaxEspera": timedelta(minutes=5)
    }
    EMERGENCIA = {...}
    URGENCIA = {...}
    URGENCIA_MENOR = {...}
    SIN_URGENCIA = {...}
```

**¿Qué es un Enum?**
- Lista fija de valores posibles
- Evita errores (no puedes poner un nivel inventado)

```python
class EstadoIngreso(Enum):
    PENDIENTE = "PENDIENTE"      # Esperando atención
    EN_PROCESO = "EN_PROCESO"    # Siendo atendido
    FINALIZADO = "FINALIZADO"    # Atención completada
```

#### Entidades (Entities)

```python
class Paciente(Persona):
    def __init__(self, nombre, apellido, cuil, domicilio, afiliado, email):
        # Valida formato CUIL (XX-XXXXXXXX-X)
        # Valida que domicilio no sea None
        super().__init__(cuil, nombre, apellido, email)
        self.domicilio = domicilio
        self.afiliado = afiliado
```

**¿Qué es una Entidad?**
- Objeto con identidad única (CUIL, ID)
- Puede cambiar sus atributos

**Otras Entidades:**
- `Doctor`: tiene matrícula
- `Enfermera`: tiene matrícula
- `Usuario`: tiene email y contraseña hasheada

```python
class Ingreso:
    def __init__(self, cuil_paciente, enfermera, informe, nivel_emergencia, ...):
        self.id = str(uuid.uuid4())  # ID único
        self.cuil_paciente = cuil_paciente
        self.enfermera = enfermera
        self.informe = informe
        self.nivel_emergencia = nivel_emergencia
        self.estado = EstadoIngreso.PENDIENTE
        self.fecha_ingreso = datetime.now()
        # Signos vitales
        self.temperatura = Temperatura(temperatura)
        self.frecuencia_cardiaca = FrecuenciaCardiaca(frecuencia_cardiaca)
        # ...
```

**Clase `Ingreso`:**
- Representa una admisión a urgencias
- Tiene todos los signos vitales
- Tiene nivel de emergencia
- Tiene estado (pendiente, en proceso, finalizado)

---

### 4. `services/` - Capa de Servicios (Lógica de Negocio)

#### `services/servicio_emergencias.py` - ⭐ EL CORAZÓN DEL SISTEMA

```python
class ServicioEmergencias:
    def __init__(self, pacientes_repo: PacientesRepo):
        self.pacientes_repo = pacientes_repo
        self._ingresos_pendientes: List[Ingreso] = []
        self._ingresos_en_proceso: List[Ingreso] = []
        self._ingresos_finalizados: List[Ingreso] = []
```

**Método principal: `registrar_urgencia()`**

```python
def registrar_urgencia(self, cuil, enfermera, informe, nivel_emergencia, ...):
    # 1. Validar campos mandatorios
    if informe is None:
        raise ValueError("El campo informe es obligatorio")
    
    # 2. Buscar paciente
    paciente = self.pacientes_repo.obtener_paciente_por_cuil(cuil)
    
    # 3. Si no existe, crearlo (si hay datos)
    if paciente is None:
        if nombre and apellido and obra_social:
            # Crear paciente automáticamente
            paciente = Paciente(...)
            self.pacientes_repo.guardar_paciente(paciente)
            mensaje = "Paciente creado automáticamente"
        else:
            raise Exception("Paciente no existe")
    
    # 4. Crear value objects
    temp = Temperatura(temperatura)
    fc = FrecuenciaCardiaca(frecuencia_cardiaca)
    # ...
    
    # 5. Crear ingreso
    ingreso = Ingreso(cuil, enfermera, informe, nivel_emergencia, ...)
    
    # 6. Insertar en lista ordenada
    self._insertar_ordenado(ingreso)
    
    return ingreso, mensaje
```

**Método: `_insertar_ordenado()`**

```python
def _insertar_ordenado(self, nuevo_ingreso: Ingreso):
    # Inserta manteniendo orden por:
    # 1. Prioridad (nivel de emergencia, menor = más urgente)
    # 2. Fecha de llegada (el que llegó antes, primero)
    
    for i, ing in enumerate(self._ingresos_pendientes):
        if nuevo_ingreso.nivel_emergencia.value["nivel"] < ing.nivel_emergencia.value["nivel"]:
            # Más urgente, insertar antes
            self._ingresos_pendientes.insert(i, nuevo_ingreso)
            return
        elif mismo_nivel and nuevo_llegó_antes:
            # Mismo nivel, llegó antes
            self._ingresos_pendientes.insert(i, nuevo_ingreso)
            return
    
    # Si no se insertó, agregar al final
    self._ingresos_pendientes.append(nuevo_ingreso)
```

**Otros métodos importantes:**

```python
def obtener_ingresos_pendientes() -> List[Ingreso]:
    """Retorna lista ordenada de ingresos pendientes"""

def reclamar_siguiente_paciente(medico: Doctor) -> Ingreso:
    """Médico reclama el primer paciente de la lista"""
    # Saca el primero de pendientes
    # Lo mueve a en_proceso
    # Crea una Atencion
    # Retorna el ingreso

def finalizar_atencion(id_ingreso: str, diagnostico: str, tratamiento: str):
    """Médico finaliza la atención de un paciente"""
    # Busca el ingreso
    # Actualiza la atención
    # Cambia estado a FINALIZADO
    # Mueve a lista de finalizados
```

---

### 5. `repositories/` - Capa de Datos

#### `repositories/paciente_repo_impl.py`

```python
class InMemoryPacientesRepo(PacientesRepo):
    """Implementación en memoria del repositorio de pacientes"""
    
    def __init__(self):
        self._pacientes: Dict[str, Paciente] = {}  # cuil -> Paciente
    
    def guardar_paciente(self, paciente: Paciente):
        self._pacientes[paciente.cuil] = paciente
    
    def obtener_paciente_por_cuil(self, cuil: str) -> Optional[Paciente]:
        return self._pacientes.get(cuil)
    
    def existe_paciente(self, cuil: str) -> bool:
        return cuil in self._pacientes
```

**¿Por qué un repositorio?**
- Abstrae el almacenamiento
- Ahora usa diccionarios en memoria
- Mañana podría usar PostgreSQL, MongoDB, etc.
- El resto del código no necesita cambiar

---

### 6. `interfaces/` - Contratos

#### `interfaces/pacientes_repo.py`

```python
from abc import ABC, abstractmethod

class PacientesRepo(ABC):
    """Interfaz abstracta para el repositorio de pacientes"""
    
    @abstractmethod
    def guardar_paciente(self, paciente: Paciente) -> None:
        pass
    
    @abstractmethod
    def obtener_paciente_por_cuil(self, cuil: str) -> Optional[Paciente]:
        pass
```

**¿Qué es una interfaz/contrato?**
- Define QUÉ métodos debe tener una clase
- No define CÓMO implementarlos
- Permite cambiar implementaciones fácilmente

---

### 7. `test/` - Tests Unitarios

```python
def test_registrar_urgencia_paciente_existente():
    # ARRANGE (preparar)
    repo = InMemoryPacientesRepo()
    paciente = Paciente(...)
    repo.guardar_paciente(paciente)
    servicio = ServicioEmergencias(repo)
    enfermera = Enfermera("Maria", "Lopez")
    
    # ACT (actuar)
    ingreso, msg = servicio.registrar_urgencia(
        cuil="20-12345678-9",
        enfermera=enfermera,
        informe="Dolor toracico",
        nivel_emergencia=NivelEmergencia.EMERGENCIA,
        # ...
    )
    
    # ASSERT (verificar)
    assert ingreso is not None
    assert ingreso.estado == EstadoIngreso.PENDIENTE
    assert msg is None
```

**Patrón AAA:**
- **Arrange**: Preparar datos
- **Act**: Ejecutar acción
- **Assert**: Verificar resultado

---

## 🚀 ¿Cómo se ejecuta el backend?

### Opción 1: Con el script (Windows)
```powershell
.\backend\start.ps1
```

### Opción 2: Manual
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Flags:**
- `--reload`: Reinicia automáticamente al cambiar código
- `--host 0.0.0.0`: Escucha en todas las interfaces
- `--port 8000`: Puerto donde escucha

### Acceder a la API
- **Raíz**: http://localhost:8000
- **Health check**: http://localhost:8000/health
- **Documentación interactiva**: http://localhost:8000/docs ⭐
- **Endpoints de auth**: http://localhost:8000/api/auth/...
- **Endpoints de urgencias**: http://localhost:8000/api/urgencias/...

---

## 📚 Tecnologías y Conceptos Clave

| Concepto | Explicación |
|----------|-------------|
| **Python** | Lenguaje de programación (versión 3.11) |
| **FastAPI** | Framework web moderno para crear APIs REST |
| **Uvicorn** | Servidor ASGI para ejecutar FastAPI |
| **Pydantic** | Validación de datos (usado por FastAPI) |
| **JWT** | Tokens para autenticación sin sesiones |
| **bcrypt** | Algoritmo para hashear contraseñas |
| **pytest** | Framework para escribir tests |
| **REST API** | Arquitectura para servicios web (GET, POST, etc.) |
| **JSON** | Formato de datos (JavaScript Object Notation) |
| **CORS** | Política para permitir peticiones entre dominios |
| **Dependency Injection** | Patrón para inyectar dependencias |
| **Repository Pattern** | Patrón para abstraer acceso a datos |
| **Value Objects** | Objetos inmutables con validaciones |
| **Clean Architecture** | Separación en capas independientes |

---

## 🎤 Resumen para tu Defensa

**Pregunta:** "Explica la arquitectura del backend"

**Respuesta:**
> "El backend está construido con **Python y FastAPI**, siguiendo una arquitectura por capas. Tenemos 4 capas principales:
> 
> 1. **API (presentación)**: Expone endpoints REST que reciben requests HTTP y devuelven JSON. Usamos FastAPI porque genera documentación automática y valida datos.
> 
> 2. **Servicios (lógica de negocio)**: Aquí está toda la lógica del dominio, como el algoritmo de priorización de urgencias que ordena por nivel de emergencia y hora de llegada.
> 
> 3. **Modelos (dominio)**: Define las entidades como Paciente, Ingreso, Doctor, y value objects como FrecuenciaCardiaca que validan datos.
> 
> 4. **Repositorios (datos)**: Abstrae el almacenamiento. Actualmente usa diccionarios en memoria, pero podríamos cambiar a una base de datos sin modificar el resto del código.
> 
> También implementamos autenticación JWT para que solo enfermeras y médicos autorizados accedan al sistema, y CI/CD con GitHub Actions para ejecutar tests automáticamente."

---

**Siguiente:** Ahora que entiendes el backend, seguimos con `docs/`, `features/` y `frontend/`. 🚀
