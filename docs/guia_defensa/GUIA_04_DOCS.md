# GUÍA 04: Carpeta `docs` - Documentación del Proyecto

## 🎯 Propósito

La carpeta `docs/` contiene toda la **documentación** del proyecto: historias de usuario, pruebas, guías de CI/CD, y más.

```
docs/
├── PRUEBAS_HU003_HU004.md          # Pruebas de historias 003 y 004
├── CI/
│   └── CD/
│       ├── configuracion-branch-protection.md
│       ├── guia-implementacion-cicd.md
│       ├── README.md
│       └── resumen-ejecutivo.md
├── ejemploChelo/
│   ├── Ejemplo-gherkin-Chelo.feature
│   └── ejemploStepChelo.py
└── HistoriasDeUsuario/
    ├── CosasPorArreglar.md
    ├── IS2025-001 Módulo de urgencias.md
    ├── IS2025-002_RegistroPacientes.md
    ├── IS2025-003.md
    └── IS2025-004.md
```

---

## 📂 Subcarpeta: `HistoriasDeUsuario/`

### ¿Qué es una Historia de Usuario?

Es una descripción en **lenguaje natural** de una funcionalidad desde la perspectiva del usuario.

**Formato estándar:**
```
Como [tipo de usuario]
Quiero [realizar acción]
Para [obtener beneficio]
```

**Ejemplo de tu proyecto:**
```
Como enfermera
Quiero poder registrar las admisiones de los pacientes a urgencias
Para determinar qué pacientes tienen mayor prioridad de atención
```

### Historias en tu proyecto:

#### 📄 `IS2025-001 Módulo de urgencias.md`

**Tema:** Registro de ingresos a urgencias

**Datos del ingreso:**
- Fecha de ingreso (automática)
- Informe (mandatorio)
- Nivel de emergencia (mandatorio)
- Estado (PENDIENTE, EN_PROCESO, FINALIZADO)
- Signos vitales:
  - Temperatura (°C)
  - Frecuencia cardíaca (lpm)
  - Frecuencia respiratoria (rpm)
  - Tensión arterial (mmHg, formato: 120/80)

**Niveles de emergencia:**

| Nivel | Color | Tiempo máximo espera |
|-------|-------|---------------------|
| Crítica | Rojo | 5 minutos |
| Emergencia | Naranja | 10-30 minutos |
| Urgencia | Amarillo | 60 minutos |
| Urgencia Menor | Verde | 2 horas |
| Sin Urgencia | Azul | 4 horas |

**Orden de atención:**
1. **Prioridad principal**: Nivel de emergencia (Crítica antes que Emergencia, etc.)
2. **Desempate**: Hora de llegada (el que llegó primero)

**Criterios de Aceptación:**

1. ✅ **Paciente existente**: Se registra el ingreso y entra a la cola
2. ✅ **Paciente nuevo**: Se crea automáticamente y se registra
3. ❌ **Falta dato mandatorio**: Error indicando qué falta
4. ❌ **Valores negativos**: Error indicando que no pueden ser negativos
5. ✅ **Priorización correcta**: Paciente más urgente va primero
6. ✅ **Mismo nivel**: Se atiende al que llegó primero

---

#### 📄 `IS2025-002_RegistroPacientes.md`

**Tema:** Registro de pacientes en el sistema

**Datos del paciente:**
- **CUIL** (mandatorio, formato: XX-XXXXXXXX-X)
- **Apellido** (mandatorio)
- **Nombre** (mandatorio)
- **Domicilio** (mandatorio):
  - Calle
  - Número
  - Localidad
  - Ciudad, Provincia, País
- **Obra social** (opcional):
  - Nombre de la obra social
  - Número de afiliado

**Validaciones:**
- La obra social debe existir en el sistema
- El paciente debe estar afiliado a esa obra social
- No se puede duplicar pacientes (mismo CUIL)

**Criterios de Aceptación:**

1. ✅ **Con obra social existente**: Registro exitoso
2. ✅ **Sin obra social**: Registro exitoso
3. ❌ **Obra social inexistente**: Error
4. ❌ **No afiliado**: Error
5. ❌ **Falta dato mandatorio**: Error específico

---

#### 📄 `IS2025-003.md` y `IS2025-004.md`

Estas historias cubren funcionalidades adicionales del sistema (probablemente atención médica, finalizacion de casos, etc.)

---

## 📂 Subcarpeta: `CI/CD/`

Contiene guías sobre el proceso de **Integración y Despliegue Continuos**.

### 📄 `guia-implementacion-cicd.md`

**Qué explica:**
- Cómo configurar GitHub Actions
- Qué workflows crear
- Cómo funcionan los tests automáticos
- Configuración de secrets (variables secretas)

### 📄 `configuracion-branch-protection.md`

**Qué explica:**
- Cómo proteger la rama `main`
- Reglas de protección:
  - ✅ Requiere aprobación de PR
  - ✅ Tests deben pasar antes de mergear
  - ✅ No se puede hacer push directo a `main`

**¿Por qué proteger ramas?**
- Evita que alguien rompa el código sin revisión
- Garantiza que todo cambio pase por tests
- Workflow profesional de desarrollo

### 📄 `resumen-ejecutivo.md`

**Qué contiene:**
- Resumen del proceso CI/CD implementado
- Beneficios obtenidos
- Métricas (tiempo de ejecución de tests, etc.)

---

## 📂 Subcarpeta: `ejemploChelo/`

Contiene **ejemplos** de cómo escribir tests con Gherkin (lenguaje de BDD).

### 📄 `Ejemplo-gherkin-Chelo.feature`

**Ejemplo de sintaxis Gherkin:**

```gherkin
Feature: Login de usuarios
  Como usuario del sistema
  Quiero poder iniciar sesión
  Para acceder a las funcionalidades

  Scenario: Login exitoso
    Given que existe un usuario con email "test@example.com"
    When intento hacer login con email "test@example.com" y password "123456"
    Then el login es exitoso
    And recibo un token JWT
```

**Palabras clave:**
- **Feature**: Funcionalidad general
- **Scenario**: Caso específico
- **Given**: Estado inicial (precondiciones)
- **When**: Acción que se realiza
- **Then**: Resultado esperado
- **And**: Condición adicional

### 📄 `ejemploStepChelo.py`

Implementación en Python de los pasos del ejemplo:

```python
@given('que existe un usuario con email "{email}"')
def step_impl(context, email):
    # Crear usuario en el sistema
    usuario = Usuario(email, "password")
    context.usuario = usuario

@when('intento hacer login con email "{email}" y password "{password}"')
def step_impl(context, email, password):
    # Intentar login
    context.resultado = login(email, password)

@then('el login es exitoso')
def step_impl(context):
    # Verificar que funcionó
    assert context.resultado is not None
```

---

## 📄 `PRUEBAS_HU003_HU004.md`

Documenta las **pruebas realizadas** para las historias de usuario 003 y 004.

**Contenido típico:**
- Casos de prueba ejecutados
- Resultados obtenidos
- Capturas de pantalla o logs
- Estado: ✅ Pasó / ❌ Falló

---

## 🎓 ¿Por qué es importante la documentación?

### En Ingeniería de Software:

1. **Comunicación**: Todo el equipo entiende qué se está construyendo
2. **Trazabilidad**: Puedes conectar código → tests → requisitos
3. **Mantenimiento**: Nuevos desarrolladores entienden el sistema
4. **Validación**: Los stakeholders pueden revisar y aprobar

### En tu defensa:

Esta carpeta demuestra que:
- ✅ Siguieron **metodologías ágiles** (historias de usuario)
- ✅ Usaron **BDD** (Behavior-Driven Development)
- ✅ Documentaron **procesos** (CI/CD)
- ✅ Trabajaron **profesionalmente**

---

## 🎤 Resumen para tu Defensa

**Pregunta:** "¿Cómo gestionaron los requisitos del proyecto?"

**Respuesta:**
> "Utilizamos **historias de usuario** en formato estándar 'Como [usuario] quiero [acción] para [beneficio]'. Cada historia tiene criterios de aceptación claros que definen cuándo está completa. Por ejemplo, la historia IS2025-001 describe el módulo de urgencias con sus reglas de priorización: primero por nivel de emergencia y luego por orden de llegada.
> 
> También implementamos **BDD (Behavior-Driven Development)** escribiendo escenarios en lenguaje Gherkin que luego se traducen a tests automatizados. Esto asegura que el código cumpla exactamente con los requisitos del negocio.
> 
> Además, documentamos todo el proceso de CI/CD y las configuraciones de protección de ramas para garantizar calidad en el código."

**Puntos clave:**
- 📌 **Historias de usuario**: Requisitos en lenguaje natural
- 📌 **Criterios de aceptación**: Definición de "hecho"
- 📌 **BDD/Gherkin**: Tests legibles por no-programadores
- 📌 **Documentación CI/CD**: Proceso de automatización
- 📌 **Branch protection**: Aseguramiento de calidad

---

## 📚 Conceptos Clave

| Concepto | Explicación |
|----------|-------------|
| **Historia de Usuario** | Requisito descrito desde perspectiva del usuario |
| **Criterios de Aceptación** | Condiciones para considerar completa una historia |
| **BDD** | Behavior-Driven Development (desarrollo guiado por comportamiento) |
| **Gherkin** | Lenguaje para escribir tests legibles (Given/When/Then) |
| **Feature** | Archivo `.feature` con escenarios de prueba |
| **Branch Protection** | Reglas para proteger ramas importantes (ej: main) |
| **Pull Request** | Solicitud para integrar cambios (requiere revisión) |

---

**Siguiente:** Ahora veremos la carpeta `features/` donde están los tests BDD completos. 🚀
