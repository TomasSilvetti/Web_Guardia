# 🔍 Comandos de Inspección de Memoria

## Método 1: Script HTTP (Recomendado) ⭐

### Ejecutar el script de inspección

```powershell
# Asegúrate de estar en el directorio backend con el venv activado
python app\scripts\inspect_memory_http.py
```

Este script consulta los endpoints de la API y muestra:
- ✅ Todos los usuarios registrados (médicos y enfermeras)
- ✅ Todos los pacientes registrados
- ✅ Estadísticas generales
- ✅ Verificación de seguridad (contraseñas hasheadas)

### Requisitos
- El servidor FastAPI debe estar corriendo
- Ejecutar desde el directorio `backend` con el venv activado

---

## Método 2: Endpoints HTTP Directos

También puedes acceder directamente a los endpoints desde tu navegador o con `curl`:

### Ver todos los usuarios
```powershell
# En el navegador:
http://localhost:8000/api/debug/memory/users

# Con curl:
curl http://localhost:8000/api/debug/memory/users
```

### Ver todos los pacientes
```powershell
# En el navegador:
http://localhost:8000/api/debug/memory/pacientes

# Con curl:
curl http://localhost:8000/api/debug/memory/pacientes
```

### Ver resumen general
```powershell
# En el navegador:
http://localhost:8000/api/debug/memory/all

# Con curl:
curl http://localhost:8000/api/debug/memory/all
```

---

## Método 3: Swagger UI (Interfaz Gráfica)

1. Abre tu navegador en: `http://localhost:8000/docs`
2. Busca la sección **"debug"**
3. Prueba los endpoints:
   - `GET /api/debug/memory/users`
   - `GET /api/debug/memory/pacientes`
   - `GET /api/debug/memory/all`

---

## Ejemplo de Uso Completo

```powershell
# 1. Activar el entorno virtual (si no está activado)
.\venv\Scripts\Activate.ps1

# 2. Asegurarse de que el servidor esté corriendo (en otra terminal)
# python start.ps1

# 3. Ejecutar el script de inspección
python app\scripts\inspect_memory_http.py
```

---

## Salida Esperada

Si tienes datos registrados, verás algo como:

```
================================================================================
🔍 INSPECTOR DE MEMORIA - Sistema de Guardia (vía HTTP)
================================================================================

================================================================================
  📊 RESUMEN GENERAL DE MEMORIA
================================================================================

--- ESTADÍSTICAS GENERALES ---
  Total usuarios: 2
    • Médicos: 1
    • Enfermeras: 1
  Total pacientes: 1
    • Con obra social: 0

================================================================================
  📋 INSPECCIÓN DE USUARIOS
================================================================================

✅ Total de usuarios: 2

--- RESUMEN POR ROL ---
  Médicos: 1
  Enfermeras: 1

--- MÉDICOS (1) ---
  📧 enfermera1@gmail.com
     Matrícula: Mat: 11334422

--- ENFERMERAS (1) ---
  📧 doctor1@gmail.com
     Matrícula: 123456

[... más detalles ...]
```

---

## Notas Importantes

⚠️ **El servidor debe estar corriendo**: Este método solo funciona mientras el servidor FastAPI está activo.

⚠️ **Datos en memoria**: Los datos se pierden al reiniciar el servidor.

💡 **Para producción**: Se recomienda usar una base de datos real (PostgreSQL, MySQL, etc.) en lugar de repositorios en memoria.

