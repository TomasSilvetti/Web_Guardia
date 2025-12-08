# GUÍA 07: Integración Completa - Cómo Funciona Todo el Sistema

## 🎯 Visión General del Sistema

**Web_Guardia** es un sistema completo de gestión de urgencias hospitalarias con arquitectura **cliente-servidor**.

```
┌────────────────────────────────────────────────────────────┐
│                        NAVEGADOR                            │
│                                                             │
│  ┌──────────────────────────────────────────────────┐     │
│  │          FRONTEND (React + TypeScript)            │     │
│  │                                                   │     │
│  │  - Interfaz gráfica                              │     │
│  │  - Formularios                                   │     │
│  │  - Tablas de espera                              │     │
│  │  - Autenticación con JWT                         │     │
│  └────────────────────┬─────────────────────────────┘     │
│                       │ HTTP/HTTPS                         │
└───────────────────────┼────────────────────────────────────┘
                        │
                        │ Axios Requests
                        │ (JSON)
                        ▼
┌────────────────────────────────────────────────────────────┐
│                    SERVIDOR (Python)                        │
│                                                             │
│  ┌──────────────────────────────────────────────────┐     │
│  │         BACKEND (FastAPI + Python)                │     │
│  │                                                   │     │
│  │  ┌─────────────────────────────────────┐        │     │
│  │  │  API REST (routes/)                  │        │     │
│  │  │  - /api/auth/*    (login/register)   │        │     │
│  │  │  - /api/urgencias/* (ingresos, etc)  │        │     │
│  │  └────────────┬────────────────────────┘        │     │
│  │               │                                   │     │
│  │  ┌────────────▼────────────────────────┐        │     │
│  │  │  SERVICIOS (services/)               │        │     │
│  │  │  - ServicioEmergencias               │        │     │
│  │  │  - Lógica de priorización            │        │     │
│  │  └────────────┬────────────────────────┘        │     │
│  │               │                                   │     │
│  │  ┌────────────▼────────────────────────┐        │     │
│  │  │  MODELOS (models/)                   │        │     │
│  │  │  - Paciente, Ingreso, Doctor         │        │     │
│  │  │  - Value Objects, Enums              │        │     │
│  │  └────────────┬────────────────────────┘        │     │
│  │               │                                   │     │
│  │  ┌────────────▼────────────────────────┐        │     │
│  │  │  REPOSITORIOS (repositories/)        │        │     │
│  │  │  - Almacenamiento en memoria         │        │     │
│  │  │  - Diccionarios Python               │        │     │
│  │  └──────────────────────────────────────┘        │     │
│  └──────────────────────────────────────────────────┘     │
└────────────────────────────────────────────────────────────┘
```

---

## 🔄 Flujo Completo: Caso de Uso Real

### Caso: **Enfermera Registra un Ingreso de Urgencia**

#### Paso 1: Autenticación

1. **Usuario abre** http://localhost:3000
2. **Frontend detecta** que no hay token → Redirige a `/login`
3. **Enfermera ingresa**:
   - Email: `enfermera@hospital.com`
   - Password: `password123`
4. **Frontend** llama:
   ```typescript
   // authService.ts
   const response = await api.post('/auth/login', { email, password });
   ```
5. **Backend** (`auth.py`):
   ```python
   def login_user(request):
       user = login(email, password, repo)  # Valida credenciales
       token = create_access_token({"email": user.email, "rol": "ENFERMERA"})
       return {"access_token": token, "user_info": {...}}
   ```
6. **Frontend** guarda token en `localStorage`
7. **Usuario redirigido** a `/urgencias`

---

#### Paso 2: Cargar Página de Urgencias

1. **React Router** activa `<UrgenciasPage />`
2. **ProtectedRoute** verifica:
   - ✅ Hay token
   - ✅ Token válido
   - ✅ Rol permitido (ENFERMERA)
3. **Página renderiza**:
   - `<FormularioAdmision />`
   - `<ListaRevisionEnProceso />`
   - `<ListaEspera />`

---

#### Paso 3: Buscar Paciente

1. **Enfermera ingresa CUIL**: `20-12345678-9`
2. **Click "Buscar Paciente"**
3. **Frontend** llama:
   ```typescript
   const paciente = await buscarPacientePorCuil("20-12345678-9");
   ```
4. **Backend** (`urgencias.py`):
   ```python
   @router.get("/pacientes/{cuil}")
   def buscar_paciente(cuil: str):
       paciente = repo.obtener_paciente_por_cuil(cuil)
       if not paciente:
           raise HTTPException(404, "Paciente no encontrado")
       return paciente_to_dict(paciente)
   ```
5. **Si existe**: Frontend autocompleta nombre, apellido, domicilio
6. **Si no existe**: Muestra campos para crear paciente

---

#### Paso 4: Completar Datos del Ingreso

**Enfermera completa:**
- ✅ Informe: "Dolor torácico intenso"
- ✅ Nivel emergencia: "Emergencia"
- ✅ Temperatura: 37.5°C
- ✅ Frecuencia cardíaca: 95 lpm
- ✅ Frecuencia respiratoria: 20 rpm
- ✅ Tensión arterial: 140/90 mmHg

---

#### Paso 5: Enviar Registro

1. **Click "Guardar Ingreso"**
2. **Frontend valida** datos localmente
3. **Frontend** construye objeto:
   ```typescript
   const data = {
     cuil: "20-12345678-9",
     informe: "Dolor torácico intenso",
     nivel_emergencia: "EMERGENCIA",
     temperatura: 37.5,
     frecuencia_cardiaca: 95,
     frecuencia_respiratoria: 20,
     frecuencia_sistolica: 140,
     frecuencia_diastolica: 90
   };
   ```
4. **Frontend** llama:
   ```typescript
   const response = await registrarIngreso(data);
   ```
5. **Axios interceptor** agrega header:
   ```
   Authorization: Bearer eyJhbGc...
   ```

---

#### Paso 6: Backend Procesa

1. **FastAPI recibe** `POST /api/urgencias/ingresos`
2. **Dependency Injection** ejecuta:
   ```python
   enfermera = get_current_enfermera(token)  # Extrae enfermera del JWT
   servicio = get_servicio_emergencias()
   ```
3. **Route handler** (`urgencias.py`):
   ```python
   def registrar_ingreso(request, enfermera, servicio):
       nivel_enum = NivelEmergencia[request.nivel_emergencia]
       
       ingreso, mensaje = servicio.registrar_urgencia(
           cuil=request.cuil,
           enfermera=enfermera,
           informe=request.informe,
           nivel_emergencia=nivel_enum,
           temperatura=request.temperatura,
           # ...
       )
       
       return IngresoResponse(id=ingreso.id, ...)
   ```

---

#### Paso 7: Servicio Ejecuta Lógica de Negocio

```python
# servicio_emergencias.py
def registrar_urgencia(self, cuil, enfermera, informe, nivel_emergencia, ...):
    # 1. Validar campos mandatorios
    if informe is None:
        raise ValueError("El campo informe es obligatorio")
    
    # 2. Buscar paciente
    paciente = self.pacientes_repo.obtener_paciente_por_cuil(cuil)
    
    if paciente is None:
        # 3. Paciente no existe → Crear si hay datos
        if nombre and apellido:
            paciente = Paciente(nombre, apellido, cuil, domicilio, ...)
            self.pacientes_repo.guardar_paciente(paciente)
            mensaje = "Paciente creado automáticamente"
        else:
            raise Exception("Paciente no existe y faltan datos")
    
    # 4. Crear Value Objects (validan datos)
    temp = Temperatura(temperatura)  # ValueError si < 0
    fc = FrecuenciaCardiaca(frecuencia_cardiaca)  # ValueError si < 0
    fr = FrecuenciaRespiratoria(frecuencia_respiratoria)
    ta = TensionArterial(frecuencia_sistolica, frecuencia_diastolica)
    
    # 5. Crear ingreso
    ingreso = Ingreso(
        cuil_paciente=cuil,
        enfermera=enfermera,
        informe=informe,
        nivel_emergencia=nivel_emergencia,
        temperatura=temp,
        frecuencia_cardiaca=fc,
        frecuencia_respiratoria=fr,
        tension_arterial=ta
    )
    
    # 6. Insertar ordenado en lista de pendientes
    self._insertar_ordenado(ingreso)
    
    return ingreso, mensaje
```

---

#### Paso 8: Algoritmo de Priorización

```python
def _insertar_ordenado(self, nuevo_ingreso):
    """
    Inserta manteniendo orden:
    1. Por nivel de emergencia (menor nivel = más urgente)
    2. Por fecha de ingreso (FIFO como desempate)
    """
    
    for i, ingreso_existente in enumerate(self._ingresos_pendientes):
        # Comparar nivel
        if nuevo_ingreso.nivel_emergencia.value["nivel"] < ingreso_existente.nivel_emergencia.value["nivel"]:
            # Más urgente → insertar antes
            self._ingresos_pendientes.insert(i, nuevo_ingreso)
            return
        
        # Mismo nivel → comparar fecha
        elif nuevo_ingreso.nivel_emergencia == ingreso_existente.nivel_emergencia:
            if nuevo_ingreso.fecha_ingreso < ingreso_existente.fecha_ingreso:
                # Llegó antes → insertar antes
                self._ingresos_pendientes.insert(i, nuevo_ingreso)
                return
    
    # Si no se insertó, agregar al final
    self._ingresos_pendientes.append(nuevo_ingreso)
```

**Ejemplo:**

Lista actual:
1. Juan (Urgencia Menor, 10:00)
2. Pedro (Sin Urgencia, 10:05)

Ingresa: María (Emergencia, 10:10)

Resultado:
1. **María (Emergencia, 10:10)** ← Insertada al inicio
2. Juan (Urgencia Menor, 10:00)
3. Pedro (Sin Urgencia, 10:05)

---

#### Paso 9: Respuesta al Frontend

1. **Backend** construye respuesta:
   ```json
   {
     "id": "abc-123",
     "cuil_paciente": "20-12345678-9",
     "nivel_emergencia": "EMERGENCIA",
     "estado": "PENDIENTE",
     "fecha_ingreso": "2025-12-07T10:15:00",
     "mensaje_advertencia": null
   }
   ```
2. **FastAPI** serializa a JSON y envía

---

#### Paso 10: Frontend Actualiza UI

1. **Axios recibe** respuesta exitosa (status 201)
2. **Hook** `useUrgencias` resuelve Promise
3. **Componente** `FormularioAdmision`:
   ```tsx
   setSuccess("Ingreso registrado exitosamente");
   onSuccess();  // Callback
   ```
4. **Página** `UrgenciasPage`:
   ```tsx
   const handleIngresoSuccess = () => {
     setRefreshTrigger(prev => prev + 1);  // Incrementa trigger
   };
   ```
5. **Componente** `ListaEspera` detecta cambio en `refreshTrigger`:
   ```tsx
   useEffect(() => {
     cargarIngresos();
   }, [refreshTrigger]);  // ← Se re-ejecuta
   ```
6. **Lista se actualiza** mostrando el nuevo paciente en su posición correcta

---

## 🩺 Caso: **Médico Reclama Paciente**

#### Paso 1: Médico Hace Login

Similar al caso anterior, pero con rol `MEDICO`.

---

#### Paso 2: Ver Lista de Espera

1. **Médico ve** `<ListaEspera>` con botón "Reclamar Siguiente"
2. Lista muestra:
   ```
   Posición | CUIL          | Paciente       | Nivel      | Fecha
   1        | 20-12345678-9 | Juan Gonzalez  | Emergencia | 10:15
   2        | 27-98765432-1 | María López    | Urgencia   | 10:20
   ```

---

#### Paso 3: Reclamar Paciente

1. **Click "Reclamar Siguiente"**
2. **Frontend** llama:
   ```typescript
   const response = await reclamarPaciente();
   ```
3. **Backend** (`urgencias.py`):
   ```python
   @router.post("/ingresos/reclamar")
   def reclamar(medico: Doctor = Depends(get_current_medico)):
       ingreso = servicio.reclamar_siguiente_paciente(medico)
       
       return ReclamarResponse(
           id=ingreso.id,
           cuil_paciente=ingreso.cuil_paciente,
           nombre_paciente=...,
           mensaje=f"Paciente {nombre} reclamado"
       )
   ```

---

#### Paso 4: Servicio Mueve Paciente

```python
def reclamar_siguiente_paciente(self, medico: Doctor) -> Ingreso:
    # 1. Verificar que haya pacientes pendientes
    if not self._ingresos_pendientes:
        raise Exception("No hay pacientes en espera")
    
    # 2. Sacar el primero (más urgente / llegó antes)
    ingreso = self._ingresos_pendientes.pop(0)
    
    # 3. Cambiar estado
    ingreso.estado = EstadoIngreso.EN_PROCESO
    
    # 4. Crear atención
    atencion = Atencion(medico, ingreso)
    ingreso.atencion = atencion
    
    # 5. Mover a lista "en proceso"
    self._ingresos_en_proceso.append(ingreso)
    
    return ingreso
```

---

#### Paso 5: Redirigir a Revisión

1. **Frontend** recibe respuesta
2. **Navega** a `/urgencias/revision/{id}`
3. **Página** `RevisionPacientePage` muestra:
   - Datos del paciente
   - Signos vitales
   - Formulario para diagnostico/tratamiento

---

#### Paso 6: Finalizar Atención

1. **Médico completa**:
   - Diagnóstico: "Infarto agudo de miocardio"
   - Tratamiento: "Angioplastia + medicación"
2. **Click "Finalizar Atención"**
3. **Backend**:
   ```python
   def finalizar_atencion(ingreso_id, diagnostico, tratamiento):
       ingreso = self._buscar_ingreso_en_proceso(ingreso_id)
       ingreso.atencion.diagnostico = diagnostico
       ingreso.atencion.tratamiento = tratamiento
       ingreso.estado = EstadoIngreso.FINALIZADO
       
       # Mover a finalizados
       self._ingresos_en_proceso.remove(ingreso)
       self._ingresos_finalizados.append(ingreso)
   ```
4. **Frontend** redirige a `/urgencias`

---

## 🧪 Testing: Validación Automática

### Tests Unitarios (pytest)

```python
# test_servicio_emergencias.py
def test_prioriza_correctamente():
    # ARRANGE
    servicio = ServicioEmergencias(repo)
    
    # Registrar paciente de baja prioridad
    servicio.registrar_urgencia(
        cuil="20-11111111-1",
        nivel_emergencia=NivelEmergencia.URGENCIA_MENOR,
        ...
    )
    
    # ACT: Registrar paciente de alta prioridad
    servicio.registrar_urgencia(
        cuil="20-22222222-2",
        nivel_emergencia=NivelEmergencia.EMERGENCIA,
        ...
    )
    
    # ASSERT: El de alta prioridad debe estar primero
    pendientes = servicio.obtener_ingresos_pendientes()
    assert pendientes[0].cuil_paciente == "20-22222222-2"
    assert pendientes[1].cuil_paciente == "20-11111111-1"
```

---

### Tests BDD (Behave)

```gherkin
Scenario: Ingreso de paciente con mayor prioridad
  Given que hay pacientes en espera:
    | CUIL          | Nivel           |
    | 20-11111111-1 | Urgencia Menor  |
  When ingresa un paciente con nivel "Emergencia"
  Then el nuevo paciente debe estar primero en la lista
```

**Implementación:**
```python
@when('ingresa un paciente con nivel "{nivel}"')
def step_impl(context, nivel):
    nivel_enum = NivelEmergencia[nivel.upper()]
    servicio.registrar_urgencia(
        cuil="20-22222222-2",
        nivel_emergencia=nivel_enum,
        ...
    )

@then('el nuevo paciente debe estar primero en la lista')
def step_impl(context):
    pendientes = servicio.obtener_ingresos_pendientes()
    assert pendientes[0].cuil_paciente == "20-22222222-2"
```

---

### CI/CD: Ejecución Automática

**GitHub Actions** ejecuta tests en cada push:

```yaml
- name: Ejecutar tests
  run: pytest backend/app/test/ -v

- name: Ejecutar BDD
  run: behave features/
```

Si los tests fallan → ❌ El push es rechazado

---

## 🔒 Seguridad: JWT

### ¿Cómo funciona?

1. **Login exitoso** → Backend genera JWT:
   ```python
   token = jwt.encode({
       "email": "medico@hospital.com",
       "rol": "MEDICO",
       "matricula": "12345",
       "exp": datetime.utcnow() + timedelta(hours=24)
   }, SECRET_KEY, algorithm="HS256")
   ```

2. **Frontend guarda** token en `localStorage`

3. **Cada petición** incluye header:
   ```
   Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```

4. **Backend valida** token:
   ```python
   def get_current_user(token: str):
       payload = jwt.decode(token, SECRET_KEY)
       email = payload["email"]
       rol = payload["rol"]
       return Usuario(email, rol)
   ```

5. **Si token inválido/expirado** → 401 Unauthorized

---

## 📊 Tecnologías y Su Rol

| Tecnología | Rol | ¿Por qué? |
|-----------|-----|-----------|
| **Python** | Lenguaje backend | Legible, rápido de desarrollar, gran ecosistema |
| **FastAPI** | Framework web | Rápido, documentación automática, validación de datos |
| **Pydantic** | Validación | Integrado con FastAPI, valida requests automáticamente |
| **JWT** | Autenticación | Stateless (no requiere sesiones en servidor) |
| **bcrypt** | Hash passwords | Algoritmo seguro, resistente a fuerza bruta |
| **pytest** | Testing unitario | Simple, fixtures poderosos, ampliamente usado |
| **Behave** | Testing BDD | Tests en lenguaje natural, trazabilidad requisitos |
| **React** | Framework frontend | Componentes reutilizables, gran comunidad |
| **TypeScript** | Tipado estático | Detecta errores en desarrollo, mejor IDE support |
| **Material-UI** | Componentes UI | Diseño profesional, componentes pre-construidos |
| **Vite** | Build tool | Extremadamente rápido, HMR (Hot Module Replacement) |
| **Axios** | Cliente HTTP | Interceptors, manejo de errores, promesas |
| **GitHub Actions** | CI/CD | Integrado con GitHub, fácil configuración |

---

## 🎯 Patrones de Diseño Utilizados

### 1. **Repository Pattern**
Abstrae acceso a datos.
```python
class PacientesRepo(ABC):
    @abstractmethod
    def guardar_paciente(self, paciente): pass
```

### 2. **Dependency Injection**
FastAPI inyecta dependencias automáticamente.
```python
def registrar_ingreso(
    servicio: ServicioEmergencias = Depends(get_servicio_emergencias)
):
    ...
```

### 3. **Value Objects**
Objetos inmutables con validación.
```python
class FrecuenciaCardiaca:
    def __init__(self, valor: float):
        if valor < 0:
            raise ValueError("No puede ser negativa")
```

### 4. **Clean Architecture**
Separación en capas independientes:
- API → Services → Domain → Data

### 5. **Observer Pattern**
React hooks como `useEffect` observan cambios:
```tsx
useEffect(() => {
  cargarDatos();
}, [refreshTrigger]);  // Re-ejecuta cuando cambia
```

---

## 🚀 ¿Cómo Ejecutar Todo el Sistema?

### 1. Backend

```powershell
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Verificar:** http://localhost:8000/health

---

### 2. Frontend

```powershell
cd frontend
npm install
npm run dev
```

**Verificar:** http://localhost:3000

---

### 3. Tests

**Tests unitarios:**
```powershell
cd backend
pytest app/test/ -v
```

**Tests BDD:**
```powershell
behave features/
```

---

## 🎤 Resumen COMPLETO para Defensa

**Pregunta final:** "Explica el sistema completo, de principio a fin"

**Respuesta:**

> "Desarrollamos un **sistema web de gestión de urgencias hospitalarias** usando una arquitectura **cliente-servidor** moderna.
> 
> **Backend (Python + FastAPI):**
> Implementamos una API REST siguiendo Clean Architecture con separación en capas: API, servicios, dominio y repositorios. La lógica principal está en `ServicioEmergencias` que implementa el algoritmo de priorización: ordena ingresos primero por nivel de emergencia y luego por orden de llegada. Usamos value objects para validar datos (frecuencias no negativas, CUIL con formato correcto) y enums para niveles de emergencia. La autenticación es con JWT tokens que incluyen el rol del usuario (enfermera o médico).
> 
> **Frontend (React + TypeScript):**
> Construimos una SPA (Single Page Application) con componentes reutilizables. Implementamos rutas protegidas que verifican autenticación y roles. La comunicación con el backend es via Axios con interceptors que agregan el token JWT automáticamente. Usamos hooks personalizados para encapsular lógica y Context API para estado global de autenticación.
> 
> **Testing:**
> Implementamos dos niveles de testing: tests unitarios con pytest validando la lógica de negocio, y tests BDD con Behave que validan los criterios de aceptación de las historias de usuario en lenguaje natural. Esto nos da cobertura completa y trazabilidad entre requisitos y código.
> 
> **CI/CD:**
> Configuramos GitHub Actions para ejecutar tests automáticamente en cada push. Si los tests fallan, el código no se puede integrar a main. Esto garantiza calidad continua.
> 
> **Flujo típico:**
> Una enfermera hace login, busca al paciente por CUIL, completa signos vitales y nivel de emergencia, envía el registro. El backend valida datos, crea el ingreso y lo inserta en la lista ordenada. El frontend actualiza la tabla automáticamente. Cuando un médico reclama un paciente, el sistema lo saca de pendientes y lo mueve a en proceso, permitiéndole completar diagnóstico y tratamiento."

---

## 📚 Glosario Completo

| Término | Significado |
|---------|-------------|
| **API REST** | Interfaz web que usa HTTP (GET, POST, PUT, DELETE) |
| **JWT** | Token firmado que contiene datos del usuario |
| **BDD** | Desarrollo guiado por comportamiento (tests legibles) |
| **CI/CD** | Integración y despliegue continuo (automatización) |
| **Clean Architecture** | Arquitectura en capas independientes |
| **Component** | Pieza reutilizable de UI en React |
| **Dependency Injection** | Patrón donde se inyectan dependencias automáticamente |
| **Enum** | Tipo de dato con valores fijos predefinidos |
| **Hook** | Función que engancha funcionalidades de React |
| **Interceptor** | Función que modifica requests/responses HTTP |
| **Repository** | Patrón que abstrae acceso a datos |
| **SPA** | Single Page Application (una sola página HTML) |
| **Value Object** | Objeto inmutable con validaciones |
| **State** | Datos que causan re-renderizado en React |
| **Props** | Parámetros pasados a componentes React |

---

## ✅ Checklist Final de Conocimientos

Para defender con confianza, debes poder explicar:

### Backend:
- ✅ ¿Qué es FastAPI y por qué lo usamos?
- ✅ ¿Cómo funciona la arquitectura por capas?
- ✅ ¿Qué son los Value Objects y por qué los usamos?
- ✅ ¿Cómo funciona el algoritmo de priorización?
- ✅ ¿Qué es un repositorio y por qué abstraemos datos?

### Frontend:
- ✅ ¿Qué es React y qué son componentes?
- ✅ ¿Qué es TypeScript y por qué agregamos tipos?
- ✅ ¿Cómo se comunica el frontend con el backend?
- ✅ ¿Qué son hooks y para qué sirven?
- ✅ ¿Cómo funcionan las rutas protegidas?

### Seguridad:
- ✅ ¿Qué es JWT y cómo funciona?
- ✅ ¿Dónde se guarda el token?
- ✅ ¿Cómo se envía el token en cada petición?
- ✅ ¿Qué pasa si el token expira?

### Testing:
- ✅ ¿Qué es BDD y Gherkin?
- ✅ ¿Cómo se conectan los tests con el código?
- ✅ ¿Qué diferencia hay entre tests unitarios y BDD?
- ✅ ¿Qué es CI/CD y cómo lo implementaron?

### General:
- ✅ ¿Por qué hay `__init__.py` en cada carpeta?
- ✅ ¿Qué hace `requirements.txt` y `package.json`?
- ✅ ¿Cómo se ejecuta el sistema completo?
- ✅ ¿Qué pasa cuando un usuario registra un ingreso?

---

## 🎉 ¡Felicidades!

Ahora tienes **7 guías completas** que explican:
1. ✅ Carpeta `.cursor`
2. ✅ Carpeta `.github` (CI/CD)
3. ✅ Carpeta `backend` (Python/FastAPI)
4. ✅ Carpeta `docs`
5. ✅ Carpeta `features` (BDD)
6. ✅ Carpeta `frontend` (React/TypeScript)
7. ✅ **Integración completa**

**Estudia estas guías, practica explicar cada parte, y estarás listo para defender como un profesional.** 🚀

¡Mucha suerte en tu defensa! 💪
