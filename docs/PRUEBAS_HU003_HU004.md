# Pruebas Manuales - HU-003 y HU-004

## Historia de Usuario 003: Módulo de Reclamo de Paciente

### Objetivo
Permitir a los médicos reclamar el próximo paciente en la lista de espera y moverlo a estado EN_PROCESO.

### Casos de Prueba

#### CP-003-01: Médico reclama paciente exitosamente
**Precondiciones:**
- Usuario autenticado como médico
- Al menos un paciente en lista de espera (estado PENDIENTE)

**Pasos:**
1. Iniciar sesión como médico
2. Navegar a la página de urgencias
3. Verificar que aparece la lista de espera con pacientes
4. Hacer clic en el botón "Reclamar Paciente" del primer paciente

**Resultado Esperado:**
- El paciente desaparece de la lista de espera
- El paciente aparece en la lista "Revisión en Progreso"
- El estado del ingreso cambia de PENDIENTE a EN_PROCESO
- Se muestra un mensaje de éxito
- Se redirige automáticamente a la página de revisión del paciente

#### CP-003-02: Médico intenta reclamar sin pacientes en espera
**Precondiciones:**
- Usuario autenticado como médico
- No hay pacientes en lista de espera

**Pasos:**
1. Iniciar sesión como médico
2. Navegar a la página de urgencias
3. Verificar que la lista de espera está vacía

**Resultado Esperado:**
- No se muestra ningún botón de "Reclamar Paciente"
- Se muestra mensaje "No hay pacientes en espera en este momento"

#### CP-003-03: Enfermera no puede ver botón de reclamar
**Precondiciones:**
- Usuario autenticado como enfermera
- Al menos un paciente en lista de espera

**Pasos:**
1. Iniciar sesión como enfermera
2. Navegar a la página de urgencias
3. Verificar la lista de espera

**Resultado Esperado:**
- Los pacientes se muestran en la lista
- NO aparece el botón "Reclamar Paciente"
- Solo las enfermeras pueden registrar nuevos ingresos

#### CP-003-04: Médico continúa revisión de paciente en proceso
**Precondiciones:**
- Usuario autenticado como médico
- Al menos un paciente en estado EN_PROCESO

**Pasos:**
1. Iniciar sesión como médico
2. Navegar a la página de urgencias
3. Verificar la lista "Revisión en Progreso"
4. Hacer clic en "Continuar Revisión"

**Resultado Esperado:**
- Se redirige a la página de revisión del paciente
- Se muestra toda la información del ingreso

---

## Historia de Usuario 004: Módulo de Creación de Atención

### Objetivo
Permitir a los médicos registrar un informe de atención para un paciente reclamado y finalizar el ingreso.

### Casos de Prueba

#### CP-004-01: Médico registra atención con informe completo
**Precondiciones:**
- Usuario autenticado como médico
- Paciente en estado EN_PROCESO
- Navegado a la página de revisión del paciente

**Pasos:**
1. Verificar que se muestra toda la información del paciente:
   - Datos personales (nombre, apellido, CUIL)
   - Nivel de emergencia
   - Signos vitales (temperatura, FC, FR, TA)
   - Descripción del ingreso (de la enfermera)
2. Completar el campo "Informe de Atención" con texto válido
3. Hacer clic en "Finalizar Atención"

**Resultado Esperado:**
- Se registra la atención exitosamente
- El estado del ingreso cambia de EN_PROCESO a FINALIZADO
- El paciente desaparece de la lista "Revisión en Progreso"
- Se muestra mensaje de éxito
- Se redirige a la página de urgencias después de 2 segundos

#### CP-004-02: Médico intenta registrar atención sin informe
**Precondiciones:**
- Usuario autenticado como médico
- Paciente en estado EN_PROCESO
- Navegado a la página de revisión del paciente

**Pasos:**
1. Dejar el campo "Informe de Atención" vacío
2. Hacer clic en "Finalizar Atención"

**Resultado Esperado:**
- Se muestra mensaje de error: "El informe del paciente se ha omitido"
- El ingreso NO cambia de estado
- El paciente permanece en la lista "Revisión en Progreso"

#### CP-004-03: Médico cancela registro de atención
**Precondiciones:**
- Usuario autenticado como médico
- Paciente en estado EN_PROCESO
- Navegado a la página de revisión del paciente

**Pasos:**
1. Comenzar a escribir en el campo de informe
2. Hacer clic en "Cancelar"

**Resultado Esperado:**
- Se redirige a la página de urgencias
- El paciente permanece en estado EN_PROCESO
- No se registra ninguna atención

#### CP-004-04: Visualización completa de información del paciente
**Precondiciones:**
- Usuario autenticado como médico
- Navegado a la página de revisión de un paciente

**Pasos:**
1. Verificar que se muestra toda la información:
   - Nombre y apellido del paciente
   - CUIL
   - Fecha y hora de ingreso
   - Nivel de emergencia con color correspondiente
   - Temperatura corporal
   - Frecuencia cardíaca
   - Frecuencia respiratoria
   - Tensión arterial (sistólica/diastólica)
   - Descripción del ingreso
   - Nombre de la enfermera que registró el ingreso

**Resultado Esperado:**
- Toda la información se muestra correctamente
- Los colores del nivel de emergencia coinciden con la lista de espera
- Los datos son legibles y están bien organizados

---

## Flujo Completo de Prueba

### Escenario End-to-End: Ciclo completo de atención

**Actores:**
- Enfermera
- Médico

**Pasos:**

1. **Enfermera registra paciente:**
   - Login como enfermera
   - Registrar nuevo ingreso con todos los datos
   - Verificar que aparece en lista de espera

2. **Médico reclama paciente:**
   - Login como médico
   - Ver paciente en lista de espera con botón "Reclamar"
   - Reclamar paciente
   - Verificar redirección a página de revisión

3. **Médico revisa información:**
   - Verificar que se muestra toda la información del paciente
   - Verificar signos vitales
   - Leer descripción de la enfermera

4. **Médico registra atención:**
   - Completar informe de atención
   - Finalizar atención
   - Verificar mensaje de éxito
   - Verificar redirección a urgencias

5. **Verificación final:**
   - Paciente no aparece en lista de espera
   - Paciente no aparece en lista de revisión en progreso
   - Estado del ingreso es FINALIZADO

---

## Validaciones de Seguridad

### VS-01: Control de acceso por rol
- Enfermeras NO pueden reclamar pacientes
- Enfermeras NO pueden ver botón "Reclamar Paciente"
- Enfermeras NO pueden ver botón "Continuar Revisión"
- Enfermeras NO pueden acceder a /urgencias/revision/:id (403)
- Médicos pueden reclamar pacientes
- Médicos pueden registrar atenciones

### VS-02: Validaciones de datos
- Informe de atención es mandatorio
- Informe no puede ser solo espacios en blanco
- ID de ingreso debe ser válido
- Ingreso debe estar en estado EN_PROCESO para registrar atención

---

## Notas de Implementación

### Backend
- ✅ Modelo Atencion actualizado con validaciones
- ✅ ServicioEmergencias extendido con métodos de reclamo y atención
- ✅ Schemas creados para API
- ✅ Dependency get_current_medico agregado
- ✅ Endpoints creados: /reclamar, /en-proceso, /atencion, /ingresos/{id}

### Frontend
- ✅ Función isMedico agregada
- ✅ Servicios extendidos con nuevas funciones
- ✅ Hook useUrgencias actualizado
- ✅ TarjetaPaciente modificado con botones condicionales
- ✅ ListaRevisionEnProceso creado
- ✅ RevisionPacientePage creado
- ✅ UrgenciasPage actualizado con ambas listas
- ✅ Ruta protegida configurada

### Estados de Ingreso
- PENDIENTE: Paciente en lista de espera
- EN_PROCESO: Paciente reclamado por médico
- FINALIZADO: Atención registrada y completada

