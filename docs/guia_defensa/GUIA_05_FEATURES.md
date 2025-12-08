# GUÍA 05: Carpeta `features` - Testing BDD con Behave

## 🎯 ¿Qué es BDD?

**BDD** = Behavior-Driven Development (Desarrollo Guiado por Comportamiento)

Es una metodología donde escribes **tests en lenguaje natural** que describen cómo debe comportarse el sistema.

### Ventajas:
- ✅ **Legibles**: Los no-programadores pueden entenderlos
- ✅ **Documentación viva**: Los tests describen el sistema
- ✅ **Comunicación**: Todos hablan el mismo idioma
- ✅ **Trazabilidad**: Conectan requisitos con código

---

## 📁 Estructura

```
features/
├── environment.py              # Configuración de Behave
├── Modulo-urgencias.feature    # Escenarios de prueba en Gherkin
└── steps/
    └── modulo_urgencias_steps.py  # Implementación de los pasos
```

---

## 🔧 Herramienta: Behave

**Behave** es el framework de BDD para Python (como Cucumber para Java).

**¿Cómo funciona?**

1. Escribes escenarios en **Gherkin** (`.feature`)
2. Implementas los pasos en **Python** (`.py`)
3. Ejecutas: `behave`
4. Behave conecta cada línea del escenario con su código correspondiente

---

## 📄 Archivo: `Modulo-urgencias.feature`

Este archivo contiene los **escenarios de prueba** para el módulo de urgencias.

### Estructura de un Feature File

```gherkin
Feature: Modulo de Urgencias
    Esta feature esta relacionada al registro de ingresos de pacientes
    en la sala de urgencias respetando su nivel de prioridad...
```

**Feature**: Describe la funcionalidad general que se está probando.

---

### Background (Contexto Común)

```gherkin
Background:
    Given que la siguiente enfermera esta registrada:
        | Nombre | Apellido |
        | Maria  | Lopez    |
```

**¿Qué es un Background?**
- Pasos que se ejecutan **antes de cada escenario**
- Evita repetir código
- En este caso: Siempre hay una enfermera llamada María López registrada

---

### Escenario 1: Paciente Existente

```gherkin
Scenario: Ingreso de un paciente que existe en el sistema
    Given que estan registrados los siguientes pacientes:
        | Cuil          | Apellido | Nombre | Obra Social |
        | 20-12345678-9 | Gonzalez | Juan   | OSDE        |
    When Ingresan a urgencias los siguientes pacientes:
        | Cuil          | Informe                | Nivel de Emergencia | Temperatura | ... |
        | 20-12345678-9 | Dolor toracico intenso | Emergencia          | 37.5        | ... |
    Then La lista de espera esta ordenada por cuil de la siguiente manera:
        | Cuil          |
        | 20-12345678-9 |
    And el ingreso del paciente con cuil "20-12345678-9" queda registrado con estado "PENDIENTE"
```

**Traducción paso a paso:**

1. **Given** (Precondición): Ya existe un paciente en el sistema
2. **When** (Acción): Se registra un ingreso de urgencia para ese paciente
3. **Then** (Verificación): El paciente está en la lista de espera
4. **And** (Verificación adicional): Su estado es PENDIENTE

---

### Escenario 2: Paciente Nuevo (No Existente)

```gherkin
Scenario: Ingreso de un paciente que no existe en el sistema
    Given que no hay pacientes registrados en el sistema
    When se intenta ingresar a urgencias el siguiente paciente:
        | Cuil          | Apellido | Nombre | Obra Social   | ... |
        | 27-98765432-1 | Martinez | Sofia  | Swiss Medical | ... |
    Then se muestra un mensaje de error indicando que el paciente no existe...
    And el paciente con cuil "27-98765432-1" es creado en el sistema...
    And La lista de espera esta ordenada por cuil de la siguiente manera:
        | Cuil          |
        | 27-98765432-1 |
```

**Comportamiento esperado:**
- ⚠️ Sistema detecta que el paciente no existe
- ✅ Crea el paciente automáticamente con los datos del ingreso
- ✅ Registra el ingreso
- ⚠️ Muestra advertencia

---

### Escenario 3: Validación - Dato Mandatorio Faltante

```gherkin
Scenario: Registrar ingreso omitiendo dato mandatorio
    Given que estan registrados los siguientes pacientes:
        | Cuil          | ... |
        | 20-12345678-9 | ... |
    When Ingresan a urgencias los siguientes pacientes:
        | Cuil          | Informe | ... |
        | 20-12345678-8 |         | ... |  # ← Informe vacío
    Then el sistema muestra el siguiente error: "El campo informe es obligatorio"
```

**Comportamiento esperado:**
- ❌ Ingreso rechazado
- 📢 Error específico indicando qué falta

---

### Escenario 4 y 5: Validación - Valores Negativos

```gherkin
Scenario: Registrar ingreso con valores negativos en Frecuencia Cardiaca
    ...
    When Ingresan a urgencias los siguientes pacientes:
        | ... | Frecuencia Cardiaca | ... |
        | ... | -95                 | ... |  # ← Valor negativo
    Then el sistema muestra el siguiente error: "La Frecuencia Cardiaca no puede ser negativa"
```

**Comportamiento esperado:**
- ❌ Value Object `FrecuenciaCardiaca` lanza excepción
- 📢 Error claro y específico

---

### Escenario 6: Priorización - Mayor Prioridad

```gherkin
Scenario: Ingreso de un paciente con mayor prioridad que otro en espera
    Given que estan registrados los siguientes pacientes:
        | Cuil          | ... |
        | 20-12345678-9 | ... |  # Juan
        | 27-98765432-1 | ... |  # Sofia
    And que hay pacientes en espera:
        | Cuil          | Nivel de Emergencia | ... |
        | 20-12345678-9 | Urgencia Menor      | ... |  # Juan (baja prioridad)
    When Ingresan a urgencias los siguientes pacientes:
        | Cuil          | Nivel de Emergencia | ... |
        | 27-98765432-1 | Emergencia          | ... |  # Sofia (alta prioridad)
    Then La lista de espera esta ordenada por cuil de la siguiente manera:
        | Cuil          |
        | 27-98765432-1 |  # ← Sofia primero (Emergencia)
        | 20-12345678-9 |  # ← Juan segundo (Urgencia Menor)
```

**Regla de negocio testeada:**
- 📍 Paciente con mayor prioridad va primero
- 📍 Emergencia (nivel 1) > Urgencia Menor (nivel 3)

---

### Escenario 7: Priorización - Mismo Nivel

```gherkin
Scenario: Ingreso de paciente con mismo nivel de emergencia...
    Given que hay pacientes en espera:
        | Cuil          | Nivel de Emergencia | ... |
        | 20-12345678-9 | Emergencia         | ... |  # Juan (llegó primero)
    When se ingresa a urgencias el siguiente paciente con el mismo nivel de emergencia:
        | Cuil          | Nivel de Emergencia | ... |
        | 27-98765432-1 | Emergencia         | ... |  # Sofia (llegó después)
    Then La lista de espera queda ordenada por prioridad de llegada:
        | Cuil          |
        | 20-12345678-9 |  # ← Juan primero (mismo nivel, llegó antes)
        | 27-98765432-1 |  # ← Sofia segunda
```

**Regla de negocio testeada:**
- 📍 Mismo nivel de emergencia → orden de llegada
- 📍 FIFO (First In, First Out) como desempate

---

## 🐍 Archivo: `steps/modulo_urgencias_steps.py`

Este archivo **implementa** cada paso (Given/When/Then) en Python.

### Decoradores de Behave

```python
@given("que la siguiente enfermera esta registrada:")
def step_impl(context):
    global enfermera, db_mockeada, servicio_urgencias
    
    nombre_enfermera = context.table[0]['Nombre']
    apellido_enfermera = context.table[0]['Apellido']
    
    enfermera = Enfermera(nombre_enfermera, apellido_enfermera)
    
    # Inicializar base de datos mock y servicio
    db_mockeada = DBPacientes()
    servicio_urgencias = ServicioEmergencias(db_mockeada)
```

**¿Qué hace?**
1. Lee la tabla del escenario (`context.table`)
2. Crea un objeto `Enfermera`
3. Inicializa la base de datos en memoria
4. Crea el servicio de emergencias

---

### Step: Registrar Pacientes

```python
@given("que estan registrados los siguientes pacientes:")
def step_impl(context):
    global db_mockeada
    
    for row in context.table:
        cuil = row['Cuil']
        nombre = row['Nombre']
        apellido = row['Apellido']
        obra_social = row['Obra Social']
        
        paciente = Paciente(nombre, apellido, cuil, obra_social)
        db_mockeada.guardar_paciente(paciente)
```

**¿Qué hace?**
- Itera sobre cada fila de la tabla
- Crea objetos `Paciente`
- Los guarda en la BD mock

---

### Step: Registrar Ingresos

```python
@when("Ingresan a urgencias los siguientes pacientes:")
def step_impl(context):
    global enfermera, servicio_urgencias, excepcion_esperada
    
    excepcion_esperada = None
    
    for row in context.table:
        cuil = row['Cuil'] if row['Cuil'].strip() else None
        informe = row['Informe'] if row['Informe'].strip() else None
        
        # Parsear temperatura
        temperatura = float(row['Temperatura']) if row['Temperatura'].strip() else None
        
        # Parsear frecuencia cardíaca (puede ser negativa para test)
        frecuencia_cardiaca = float(row['Frecuencia Cardiaca']) if row['Frecuencia Cardiaca'].strip() else None
        
        # Parsear tensión arterial ("120/80")
        tension_arterial_str = row['Tension Arterial'].strip()
        frecuencia_sistolica = None
        frecuencia_diastolica = None
        if tension_arterial_str:
            partes = tension_arterial_str.split('/')
            frecuencia_sistolica = float(partes[0])
            frecuencia_diastolica = float(partes[1])
        
        # Convertir string a enum
        nivel_emergencia_str = row['Nivel de Emergencia']
        nivel_emergencia = None
        for nivel in NivelEmergencia:
            if nivel.value['nombre'] == nivel_emergencia_str:
                nivel_emergencia = nivel
                break
        
        try:
            ingreso, mensaje = servicio_urgencias.registrar_urgencia(
                cuil=cuil,
                enfermera=enfermera,
                informe=informe,
                nivel_emergencia=nivel_emergencia,
                temperatura=temperatura,
                frecuencia_cardiaca=frecuencia_cardiaca,
                # ... más parámetros
            )
        except Exception as e:
            excepcion_esperada = e
```

**¿Qué hace?**
1. Lee cada fila de la tabla
2. Parsea los datos (convierte strings a números, etc.)
3. Convierte el nivel de emergencia de string a enum
4. Llama a `servicio_urgencias.registrar_urgencia()`
5. Si hay error, lo guarda en `excepcion_esperada`

---

### Step: Verificar Lista Ordenada

```python
@then("La lista de espera esta ordenada por cuil de la siguiente manera:")
def step_impl(context):
    global servicio_urgencias
    
    ingresos_pendientes = servicio_urgencias.obtener_ingresos_pendientes()
    
    # Verificar que el orden coincide
    for i, row in enumerate(context.table):
        cuil_esperado = row['Cuil']
        cuil_actual = ingresos_pendientes[i].cuil_paciente
        
        assert cuil_actual == cuil_esperado, \
            f"Posición {i}: esperado {cuil_esperado}, actual {cuil_actual}"
```

**¿Qué hace?**
1. Obtiene la lista de ingresos pendientes
2. Verifica que estén en el orden correcto
3. Compara cada posición con lo esperado
4. Si no coincide, lanza error con mensaje descriptivo

---

### Step: Verificar Error

```python
@then('el sistema muestra el siguiente error: "{mensaje_error}"')
def step_impl(context, mensaje_error):
    global excepcion_esperada
    
    assert excepcion_esperada is not None, "Se esperaba una excepción pero no ocurrió"
    
    assert str(excepcion_esperada) == mensaje_error, \
        f"Mensaje de error incorrecto. Esperado: '{mensaje_error}', Actual: '{str(excepcion_esperada)}'"
```

**¿Qué hace?**
1. Verifica que se haya lanzado una excepción
2. Verifica que el mensaje sea exactamente el esperado

---

## ⚙️ Archivo: `environment.py`

Este archivo define **hooks** (funciones que se ejecutan en momentos específicos).

```python
def before_scenario(context, scenario):
    """
    Hook que se ejecuta ANTES de cada escenario.
    Reinicializa las variables globales para estado limpio.
    """
    import features.steps.modulo_urgencias_steps as steps_module
    
    # Reinicializar todas las variables globales
    steps_module.enfermera = None
    steps_module.db_mockeada = None
    steps_module.servicio_urgencias = None
    steps_module.excepcion_esperada = None
    steps_module.mensaje_advertencia = None
    steps_module.datos_paciente_nuevo = None
```

**¿Por qué es necesario?**
- Cada escenario debe empezar "limpio"
- Si un escenario deja datos, no debe afectar al siguiente
- Esto asegura que los tests sean **independientes**

---

## 🚀 ¿Cómo ejecutar los tests?

### Opción 1: Todos los tests
```bash
behave
```

### Opción 2: Solo un feature
```bash
behave features/Modulo-urgencias.feature
```

### Opción 3: Solo un escenario
```bash
behave features/Modulo-urgencias.feature:12  # Línea del escenario
```

### Opción 4: Con tags
```gherkin
@wip
Scenario: Mi escenario en desarrollo
```
```bash
behave --tags=wip
```

---

## 📊 Salida de Behave

Cuando ejecutas `behave`, ves algo como:

```
Feature: Modulo de Urgencias

  Background:
    Given que la siguiente enfermera esta registrada  # passed

  Scenario: Ingreso de un paciente que existe en el sistema
    Given que estan registrados los siguientes pacientes  # passed
    When Ingresan a urgencias los siguientes pacientes   # passed
    Then La lista de espera esta ordenada...             # passed
    And el ingreso del paciente... estado "PENDIENTE"    # passed

1 feature passed, 0 failed, 0 skipped
7 scenarios passed, 0 failed, 0 skipped
28 steps passed, 0 failed, 0 skipped
```

**Colores:**
- 🟢 Verde = Paso exitoso
- 🔴 Rojo = Paso fallido
- 🟡 Amarillo = Paso no implementado

---

## 🎯 ¿Por qué usar BDD?

### En tu proyecto:

1. **Validación de requisitos**: Los tests son la especificación
2. **Regresión**: Si cambias código, los tests detectan problemas
3. **Documentación**: Cualquiera puede leer los `.feature` y entender qué hace el sistema
4. **Comunicación**: Cliente/profesor puede revisar escenarios

### En la defensa:

Demuestra que:
- ✅ Probaste **todos los criterios de aceptación**
- ✅ Usaste **metodología profesional** (BDD)
- ✅ Tienes **cobertura de tests**
- ✅ El sistema funciona **según especificaciones**

---

## 🎤 Resumen para tu Defensa

**Pregunta:** "¿Cómo validaron que el sistema cumple con los requisitos?"

**Respuesta:**
> "Implementamos **BDD (Behavior-Driven Development)** usando **Behave**, el framework de Python para escribir tests en lenguaje Gherkin. Los escenarios de prueba están escritos en lenguaje natural en el archivo `Modulo-urgencias.feature`, donde describimos cada caso de uso con el formato Given/When/Then.
> 
> Por ejemplo, probamos que cuando ingresa un paciente con nivel 'Emergencia' y ya hay uno en espera con 'Urgencia Menor', el sistema los ordena correctamente priorizando al más urgente. También validamos que el sistema rechace valores negativos en frecuencia cardíaca y que cree pacientes automáticamente si no existen.
> 
> Cada escenario Gherkin está implementado en Python en el archivo `modulo_urgencias_steps.py`, donde usamos decoradores `@given`, `@when`, `@then` para conectar cada paso con su código correspondiente. Esto nos permitió automatizar la validación de todos los criterios de aceptación de las historias de usuario."

**Puntos clave:**
- 📌 **BDD**: Desarrollo guiado por comportamiento
- 📌 **Gherkin**: Lenguaje natural (Given/When/Then)
- 📌 **Behave**: Framework Python para BDD
- 📌 **Trazabilidad**: Tests → Requisitos → Código
- 📌 **Automatización**: Tests ejecutables y repetibles

---

## 📚 Conceptos Clave

| Concepto | Explicación |
|----------|-------------|
| **BDD** | Metodología de testing con lenguaje natural |
| **Gherkin** | Sintaxis Given/When/Then para escribir escenarios |
| **Behave** | Framework BDD para Python (como Cucumber/Java) |
| **Feature** | Funcionalidad que se está probando |
| **Scenario** | Caso de prueba específico |
| **Background** | Pasos comunes antes de cada escenario |
| **Step Definition** | Implementación en Python de un paso Gherkin |
| **Context** | Objeto que comparte datos entre pasos |
| **Hook** | Función que se ejecuta en momentos específicos |
| **Table** | Datos tabulares en Gherkin (`\| Columna \|`) |

---

**Siguiente:** Ahora veremos el **frontend** (React + TypeScript) y luego la integración completa. 🚀
