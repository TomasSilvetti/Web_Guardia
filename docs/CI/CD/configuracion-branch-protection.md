# Configuración de Branch Protection Rules

## 📋 Objetivo

Configurar reglas de protección para la rama `main` que aseguren que:
- ✅ Todos los tests pasen antes de mergear
- ✅ Se requiera revisión de código
- ✅ No se pueda hacer push directo a `main`
- ✅ El código en `main` siempre sea estable

---

## 🔒 ¿Qué son Branch Protection Rules?

Las Branch Protection Rules son reglas que GitHub aplica a ramas específicas para:
- Prevenir cambios accidentales o no autorizados
- Asegurar calidad del código mediante checks automáticos
- Requerir revisiones de código antes de mergear
- Mantener un historial de commits limpio

---

## 🚀 Paso a Paso: Configuración

### Paso 1: Acceder a Settings

1. Ve a tu repositorio en GitHub
2. Haz clic en **"Settings"** en la barra superior
3. **Nota**: Necesitas permisos de administrador del repositorio

### Paso 2: Ir a Branches

1. En el sidebar izquierdo, busca la sección **"Code and automation"**
2. Haz clic en **"Branches"**

### Paso 3: Agregar Regla de Protección

1. En la sección "Branch protection rules", haz clic en **"Add rule"** o **"Add branch protection rule"**

### Paso 4: Configurar Branch Name Pattern

En el campo **"Branch name pattern"**, escribe:

```
main
```

**Nota**: También puedes usar patrones como:
- `main` - Solo la rama main
- `master` - Solo la rama master
- `release/*` - Todas las ramas que empiecen con release/
- `*` - Todas las ramas (no recomendado)

### Paso 5: Configurar Reglas Recomendadas

Marca las siguientes opciones:

#### ✅ Require a pull request before merging

**Qué hace**: Previene push directo a `main`. Todo cambio debe pasar por un Pull Request.

**Configuración recomendada**:
- ✅ **Require approvals**: Marca esta opción
  - **Required number of approvals before merging**: `1`
  - Para equipos grandes: `2` o más
- ✅ **Dismiss stale pull request approvals when new commits are pushed**
  - Si se agregan nuevos commits, se requiere nueva aprobación
- ⚠️ **Require review from Code Owners** (opcional)
  - Solo si tienes un archivo CODEOWNERS configurado

**Beneficio**: Asegura que al menos otra persona revise el código.

#### ✅ Require status checks to pass before merging

**Qué hace**: Requiere que todos los checks (como nuestro workflow de tests) pasen antes de permitir el merge.

**Configuración**:
1. ✅ Marca **"Require status checks to pass before merging"**
2. ✅ Marca **"Require branches to be up to date before merging"**
   - Asegura que el PR tenga los últimos cambios de main
3. En el campo de búsqueda, busca: **"Backend Tests"**
4. Haz clic en **"Backend Tests"** para agregarlo como check requerido

**Nota**: El check "Backend Tests" solo aparecerá después de que el workflow se haya ejecutado al menos una vez.

**Beneficio**: Garantiza que el código en main siempre pase todos los tests.

#### ✅ Require conversation resolution before merging

**Qué hace**: Requiere que todos los comentarios en el PR sean resueltos antes de mergear.

**Beneficio**: Asegura que todas las discusiones y sugerencias sean atendidas.

#### ⚠️ Require signed commits (opcional)

**Qué hace**: Requiere que todos los commits estén firmados con GPG.

**Cuándo usar**: Para proyectos con altos requisitos de seguridad.

**Beneficio**: Verifica la identidad del autor del commit.

#### ⚠️ Require linear history (opcional)

**Qué hace**: Previene merge commits, solo permite squash o rebase.

**Beneficio**: Mantiene un historial de commits más limpio y lineal.

#### ✅ Do not allow bypassing the above settings

**Qué hace**: Ni siquiera los administradores pueden saltarse estas reglas.

**Configuración recomendada**:
- Para equipos grandes: ✅ Habilitar
- Para equipos pequeños o desarrollo personal: ⚠️ Opcional

**Beneficio**: Asegura que las reglas se apliquen consistentemente a todos.

#### ⚠️ Allow force pushes (NO recomendado)

**Qué hace**: Permite force push a la rama protegida.

**Recomendación**: ❌ **Dejar desmarcado**

**Por qué**: Force push puede sobrescribir el historial y causar pérdida de código.

#### ⚠️ Allow deletions (NO recomendado)

**Qué hace**: Permite eliminar la rama protegida.

**Recomendación**: ❌ **Dejar desmarcado**

**Por qué**: No quieres que alguien elimine accidentalmente la rama main.

### Paso 6: Guardar Cambios

1. Revisa todas las configuraciones
2. Haz clic en **"Create"** o **"Save changes"** al final de la página

---

## ✅ Configuración Recomendada - Resumen

```
Branch name pattern: main

✅ Require a pull request before merging
   ✅ Require approvals (1)
   ✅ Dismiss stale pull request approvals when new commits are pushed

✅ Require status checks to pass before merging
   ✅ Require branches to be up to date before merging
   ✅ Status checks: "Backend Tests"

✅ Require conversation resolution before merging

✅ Do not allow bypassing the above settings (para equipos grandes)

❌ Allow force pushes
❌ Allow deletions
```

---

## 🧪 Verificar la Configuración

### Prueba 1: Intentar Push Directo a Main

```powershell
# Esto debería fallar
git checkout main
git commit --allow-empty -m "test"
git push origin main
```

**Resultado esperado**:
```
remote: error: GH006: Protected branch update failed for refs/heads/main.
remote: error: Changes must be made through a pull request.
```

✅ Si ves este error, la protección funciona correctamente.

### Prueba 2: Crear PR con Tests Fallidos

1. Crea una rama nueva
2. Modifica un test para que falle intencionalmente
3. Haz commit y push
4. Crea un PR hacia `main`

**Resultado esperado**:
- ❌ El check "Backend Tests" falla
- ❌ El botón "Merge pull request" está deshabilitado
- Mensaje: "Merging is blocked - Required status check 'Backend Tests' has not succeeded"

✅ Si no puedes mergear, la protección funciona correctamente.

### Prueba 3: Crear PR con Tests Exitosos

1. Arregla el test
2. Haz commit y push
3. Espera a que el workflow termine

**Resultado esperado**:
- ✅ El check "Backend Tests" pasa
- ✅ El botón "Merge pull request" está habilitado (si tienes aprobaciones)
- Puedes mergear el PR

✅ Si puedes mergear, todo funciona correctamente.

---

## 🔧 Configuraciones Avanzadas

### Configuración para Equipos Pequeños (2-3 personas)

```
✅ Require a pull request before merging
   ✅ Require approvals (1)
   ⚠️ Dismiss stale approvals (opcional)

✅ Require status checks to pass before merging
   ✅ Backend Tests

⚠️ Require conversation resolution (opcional)

❌ Do not allow bypassing (permite flexibilidad)
```

### Configuración para Equipos Grandes (5+ personas)

```
✅ Require a pull request before merging
   ✅ Require approvals (2)
   ✅ Dismiss stale approvals
   ✅ Require review from Code Owners

✅ Require status checks to pass before merging
   ✅ Backend Tests
   ✅ Require branches to be up to date

✅ Require conversation resolution

✅ Do not allow bypassing

⚠️ Require linear history (opcional)
```

### Configuración para Proyectos Open Source

```
✅ Require a pull request before merging
   ✅ Require approvals (1-2)
   ✅ Dismiss stale approvals

✅ Require status checks to pass before merging
   ✅ Backend Tests
   ✅ Require branches to be up to date

✅ Require conversation resolution

✅ Do not allow bypassing

⚠️ Require signed commits (recomendado)
```

---

## 🚨 Casos Especiales

### Hotfix Urgente

Si necesitas hacer un hotfix urgente y los tests están fallando:

**Opción 1: Arreglar los tests (recomendado)**
```powershell
# Arregla el código y los tests
git add .
git commit -m "fix: Arreglar tests"
git push
```

**Opción 2: Deshabilitar temporalmente la protección**
1. Settings → Branches → Edit rule
2. Desmarca temporalmente "Require status checks"
3. Mergea el hotfix
4. ✅ **Importante**: Vuelve a habilitar la protección inmediatamente

**Opción 3: Usar permisos de administrador**
- Si no marcaste "Do not allow bypassing", los admins pueden mergear
- Solo usar en emergencias

### Actualizar la Rama con Main

Si el check "Require branches to be up to date" está bloqueando el merge:

```powershell
# Opción 1: Merge main en tu rama
git checkout tu-rama
git merge main
git push

# Opción 2: Rebase (historial más limpio)
git checkout tu-rama
git rebase main
git push --force-with-lease
```

### Resolver Conflictos de Merge

```powershell
# Actualizar tu rama con main
git checkout tu-rama
git merge main

# Resolver conflictos manualmente
# Editar archivos con conflictos

# Marcar como resueltos
git add .
git commit -m "fix: Resolver conflictos con main"
git push
```

---

## 📊 Monitoreo y Mantenimiento

### Ver Historial de Protección

1. Settings → Branches
2. Clic en "Edit" en la regla de `main`
3. Scroll hasta el final para ver el historial de cambios

### Auditar Intentos de Bypass

1. Settings → Audit log
2. Buscar eventos relacionados con branch protection

### Actualizar Reglas

Es buena práctica revisar y actualizar las reglas cada:
- ✅ 3-6 meses
- ✅ Cuando el equipo crece
- ✅ Cuando se agregan nuevos workflows

---

## 🎯 Mejores Prácticas

### 1. Empezar Estricto, Aflojar si es Necesario

Es más fácil relajar reglas que endurecerlas después.

### 2. Comunicar Cambios al Equipo

Antes de habilitar branch protection:
- Notifica al equipo
- Explica las nuevas reglas
- Proporciona documentación

### 3. Configurar Notificaciones

Asegúrate de que el equipo reciba notificaciones cuando:
- Un PR necesita revisión
- Los tests fallan
- Hay conflictos

### 4. Usar CODEOWNERS (Opcional)

Crea un archivo `.github/CODEOWNERS`:

```
# Backend
/backend/ @tu-usuario @otro-dev

# Frontend
/frontend/ @frontend-lead

# CI/CD
/.github/ @devops-lead

# Docs
/docs/ @tech-writer
```

### 5. Documentar Excepciones

Si necesitas hacer bypass, documenta:
- Por qué fue necesario
- Quién lo autorizó
- Qué se hizo después para prevenir que vuelva a pasar

---

## ❓ Preguntas Frecuentes

### ¿Puedo proteger múltiples ramas?

Sí, crea una regla para cada rama o usa patrones:
- `main` - Solo main
- `release/*` - Todas las ramas de release
- `feature/*` - Todas las ramas de feature

### ¿Qué pasa si el workflow falla?

No podrás mergear el PR hasta que:
1. Arregles el código y los tests pasen
2. O deshabilites temporalmente la protección (no recomendado)

### ¿Puedo tener diferentes reglas para diferentes ramas?

Sí, crea múltiples reglas con diferentes configuraciones.

### ¿Cómo agrego más checks requeridos?

1. Crea el workflow
2. Ejecuta el workflow al menos una vez
3. Ve a Branch protection → Edit rule
4. Busca el nuevo check y agrégalo

### ¿Qué pasa si elimino el workflow?

El check seguirá siendo requerido pero nunca pasará. Debes:
1. Editar la regla de protección
2. Quitar el check de la lista de checks requeridos

---

## 🔗 Recursos Adicionales

- [GitHub Docs - Branch Protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [GitHub Docs - Required Status Checks](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/collaborating-on-repositories-with-code-quality-features/about-status-checks)
- [GitHub Docs - CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)

---

## ✅ Checklist de Configuración

- [ ] Acceder a Settings → Branches
- [ ] Crear regla para `main`
- [ ] Habilitar "Require a pull request before merging"
- [ ] Configurar número de aprobaciones requeridas
- [ ] Habilitar "Require status checks to pass"
- [ ] Agregar "Backend Tests" como check requerido
- [ ] Habilitar "Require branches to be up to date"
- [ ] Habilitar "Require conversation resolution"
- [ ] Decidir sobre "Do not allow bypassing"
- [ ] Guardar cambios
- [ ] Probar con un PR de prueba
- [ ] Comunicar cambios al equipo
- [ ] Documentar en el README del proyecto

---

## 🎓 Conclusión

Las Branch Protection Rules son una herramienta esencial para:
- ✅ Mantener la calidad del código
- ✅ Prevenir errores en producción
- ✅ Fomentar revisiones de código
- ✅ Asegurar que los tests siempre pasen

**Recuerda**: La configuración debe adaptarse a las necesidades de tu equipo. Empieza con reglas básicas y ajusta según sea necesario.

---

*Última actualización: Diciembre 2024*  
*Versión: 1.0*  
*Mantenido por: Equipo Web_guardia*

