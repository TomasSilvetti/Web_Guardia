# Scripts de Inspección

## inspect_memory.py

Script para inspeccionar el estado actual de la memoria del sistema (usuarios y pacientes).

### Descripción

Este script consulta los repositorios en memoria y muestra todos los usuarios y pacientes que han sido registrados manualmente en el sistema. **No crea datos de ejemplo**, solo inspecciona los datos existentes.

### Uso

```powershell
python backend/app/scripts/inspect_memory.py
```

### Funcionalidad

El script realiza las siguientes acciones:

1. **Inspección de Usuarios**:
   - Lista todos los usuarios registrados
   - Muestra estadísticas por rol (médicos, enfermeras)
   - Verifica que las contraseñas estén correctamente hasheadas

2. **Inspección de Pacientes**:
   - Lista todos los pacientes registrados
   - Muestra información de obras sociales
   - Separa pacientes con y sin obra social

### Comportamiento

- Si **hay datos en memoria**: Muestra toda la información detallada
- Si **NO hay datos**: Muestra un mensaje de error indicando que no hay registros

### Ejemplo de Salida (Sin Datos)

```
================================================================================
🔍 INSPECTOR DE MEMORIA - Sistema de Guardia
================================================================================

================================================================================
📋 INSPECCIÓN DE USUARIOS
================================================================================

❌ ERROR: No hay usuarios registrados en memoria.
   Por favor, registre usuarios antes de ejecutar este script.

================================================================================
📋 INSPECCIÓN DE PACIENTES
================================================================================

❌ ERROR: No hay pacientes registrados en memoria.
   Por favor, registre pacientes antes de ejecutar este script.

================================================================================
⚠️  Inspección completada - No se encontraron datos en memoria

💡 Sugerencia: Ejecute la aplicación y registre usuarios/pacientes
   antes de ejecutar este script de inspección.
================================================================================
```

### Ejemplo de Salida (Con Datos)

```
================================================================================
🔍 INSPECTOR DE MEMORIA - Sistema de Guardia
================================================================================

================================================================================
📋 INSPECCIÓN DE USUARIOS
================================================================================

--- TODOS LOS USUARIOS ---

Usuario: dr.garcia@hospital.com
  Rol: MEDICO
  ID: abc123...

--- CONSULTAS ESPECÍFICAS ---

Total de usuarios: 2
Total de médicos: 1
  • dr.garcia@hospital.com
Total de enfermeras: 1
  • enf.lopez@hospital.com

--- VERIFICACIÓN DE SEGURIDAD ---

Usuario: dr.garcia@hospital.com
  ✅ Password hasheado con bcrypt
  ✅ NO se guarda la contraseña en texto plano
  Hash (primeros 40 caracteres): $2b$12$...

================================================================================
📋 INSPECCIÓN DE PACIENTES
================================================================================

[Similar output para pacientes]

================================================================================
✅ Inspección completada
================================================================================
```

### Notas

- Este script es útil para debugging y verificación del estado del sistema
- Los datos en memoria se pierden al reiniciar la aplicación
- Para tener datos que inspeccionar, primero debe ejecutar la aplicación y registrar usuarios/pacientes manualmente
