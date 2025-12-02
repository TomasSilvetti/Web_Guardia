# Instrucciones para Probar la Integración Frontend-Backend

## Paso 1: Iniciar el Backend

Abre una terminal de PowerShell en la carpeta raíz del proyecto y ejecuta:

```powershell
cd backend
.\start.ps1
```

O alternativamente:

```powershell
cd backend
.\venv\Scripts\Activate.ps1
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

El backend debería estar corriendo en: `http://localhost:8000`

Verifica que esté funcionando accediendo a: `http://localhost:8000/docs`

## Paso 2: Iniciar el Frontend

Abre **otra terminal** de PowerShell en la carpeta raíz del proyecto y ejecuta:

```powershell
cd frontend
npm run dev
```

El frontend debería estar corriendo en: `http://localhost:3000`

## Paso 3: Probar la Aplicación

### 3.1 Registro de Usuario (Enfermera)

1. Abre el navegador en `http://localhost:3000`
2. Serás redirigido automáticamente a `/login`
3. Haz clic en la pestaña "Registrarse"
4. Completa el formulario:
   - **Email**: enfermera@hospital.com
   - **Contraseña**: 123456 (o la que prefieras)
   - **Rol**: Enfermera
   - **Matrícula**: 12345
5. Haz clic en "Registrarse"
6. Deberías ver un mensaje de éxito

### 3.2 Login

1. Cambia a la pestaña "Iniciar Sesión"
2. Ingresa las credenciales que acabas de registrar
3. Haz clic en "Ingresar"
4. Deberías ser redirigido a `/urgencias`

### 3.3 Registrar un Ingreso de Urgencia

En la página de urgencias verás dos paneles:

#### Panel Izquierdo: Formulario de Admisión

1. **CUIL del Paciente**: Ingresa un CUIL de 11 dígitos (ej: 20-12345678-9)
2. Haz clic en "Buscar" (simulará que el paciente no existe)
3. Completa los campos adicionales:
   - **Nombre**: Juan
   - **Apellido**: Pérez
   - **Obra Social**: OSDE
4. **Nivel de Emergencia**: Selecciona uno (ej: Crítica - Rojo)
5. **Informe**: Describe el motivo de consulta (ej: "Dolor torácico intenso")
6. **Signos Vitales**:
   - Temperatura: 37.5
   - Frecuencia Cardíaca: 110
   - Frecuencia Respiratoria: 22
   - Tensión Sistólica: 140
   - Tensión Diastólica: 90
7. Haz clic en "Registrar Ingreso"

#### Panel Derecho: Lista de Espera

- Deberías ver el paciente recién registrado aparecer en la lista
- La lista está ordenada por prioridad (nivel de emergencia) y hora de llegada
- Cada tarjeta muestra:
  - Nombre y CUIL del paciente
  - Nivel de emergencia con color
  - Signos vitales
  - Tiempo de espera

### 3.4 Registrar Múltiples Pacientes

Registra varios pacientes con diferentes niveles de emergencia para ver cómo se ordenan:

**Paciente 2** (Urgencia Menor - Verde):
- CUIL: 27-87654321-3
- Nombre: María, Apellido: González
- Obra Social: Swiss Medical
- Nivel: Urgencia Menor
- Informe: "Control de presión arterial"
- Signos vitales normales

**Paciente 3** (Emergencia - Naranja):
- CUIL: 23-11223344-5
- Nombre: Carlos, Apellido: López
- Obra Social: Galeno
- Nivel: Emergencia
- Informe: "Fractura expuesta en brazo"
- Signos vitales con frecuencia cardíaca elevada

Verifica que la lista se ordene correctamente:
1. Crítica (Rojo) - Juan Pérez
2. Emergencia (Naranja) - Carlos López
3. Urgencia Menor (Verde) - María González

### 3.5 Validaciones a Probar

#### Campos Obligatorios
- Intenta registrar sin completar algún campo obligatorio
- Deberías ver mensajes de error específicos

#### Valores Negativos
- Intenta ingresar valores negativos en frecuencias
- Deberías ver: "El valor no puede ser negativo"

#### CUIL Inválido
- Intenta ingresar un CUIL con menos de 11 dígitos
- Deberías ver: "El CUIL debe tener 11 dígitos"

#### Temperatura Inválida
- Intenta ingresar temperatura < 30 o > 45
- Deberías ver: "La temperatura debe estar entre 30 y 45 °C"

### 3.6 Funcionalidades Adicionales

- **Auto-refresh**: La lista de espera se actualiza automáticamente cada 30 segundos
- **Botón Actualizar**: Puedes refrescar manualmente la lista
- **Limpiar Formulario**: Botón para resetear todos los campos
- **Logout**: En el navbar, haz clic en el ícono de usuario y selecciona "Cerrar Sesión"

## Verificación de Criterios de Aceptación

### ✅ Criterio 1: Paciente existe en el sistema
- Actualmente todos los pacientes se crean automáticamente (IS2025-002 pendiente)

### ✅ Criterio 2: Paciente no existe
- Se muestran campos adicionales para crear el paciente
- Se muestra mensaje de advertencia

### ✅ Criterio 3: Datos mandatorios omitidos
- Validación en tiempo real
- Mensajes de error específicos por campo

### ✅ Criterio 4: Valores negativos
- Validación de frecuencias
- Mensaje de error claro

### ✅ Criterio 5, 6, 7: Ordenamiento por prioridad
- Lista ordenada por nivel (menor número = mayor prioridad)
- Mismo nivel: ordenado por fecha/hora de ingreso

## Endpoints del Backend Utilizados

- `POST /api/auth/register` - Registro de usuarios
- `POST /api/auth/login` - Login y obtención de JWT
- `POST /api/urgencias/ingresos` - Registro de ingreso
- `GET /api/urgencias/ingresos/pendientes` - Lista de ingresos pendientes
- `GET /api/urgencias/niveles-emergencia` - Niveles disponibles

## Notas Importantes

1. **CORS**: El backend está configurado para aceptar peticiones desde `http://localhost:3000`
2. **JWT**: El token se guarda en `localStorage` y se envía automáticamente en cada petición
3. **Proxy**: Vite está configurado para hacer proxy de `/api` a `http://localhost:8000`
4. **Persistencia**: Los datos se mantienen en memoria mientras el backend esté corriendo

## Problemas Comunes

### Backend no responde
- Verifica que el backend esté corriendo en el puerto 8000
- Accede a `http://localhost:8000/docs` para verificar

### Error de CORS
- Asegúrate de que el frontend esté en `http://localhost:3000`
- Verifica la configuración en `backend/app/core/config.py`

### Token inválido
- Cierra sesión y vuelve a iniciar sesión
- Limpia el localStorage del navegador (F12 > Application > Local Storage)

### Lista no se actualiza
- Haz clic en el botón "Actualizar"
- Verifica que el backend esté respondiendo correctamente

## Próximos Pasos

Una vez que hayas probado todas las funcionalidades, el módulo de urgencias está completo según la historia de usuario IS2025-001. 

Para implementar la búsqueda real de pacientes, se necesitará completar la historia IS2025-002.

