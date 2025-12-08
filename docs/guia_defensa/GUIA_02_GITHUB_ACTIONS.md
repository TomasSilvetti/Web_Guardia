# GUÍA 02: Carpeta `.github` - CI/CD y GitHub Actions

## ¿Qué es la carpeta `.github`?

La carpeta `.github` es una carpeta especial de **GitHub** que contiene configuraciones para automatizar procesos del proyecto. En tu caso, contiene **workflows** (flujos de trabajo automatizados).

## Estructura en tu proyecto

```
.github/
  └── workflows/
      └── backend-tests.yml
```

## ¿Qué es CI/CD?

**CI/CD** significa:
- **CI (Continuous Integration)** = Integración Continua
- **CD (Continuous Deployment)** = Despliegue Continuo

Es una práctica de ingeniería donde **automatizas** la ejecución de tests y validaciones cada vez que alguien hace cambios al código.

### Analogía simple:
Imagina que cada vez que guardas un cambio en GitHub, un "robot" automáticamente:
1. ✅ Descarga tu código
2. ✅ Instala las dependencias
3. ✅ Ejecuta todos los tests
4. ✅ Te avisa si algo está roto

Eso es **CI/CD**.

---

## Archivo: `backend-tests.yml`

Este archivo define un **workflow de GitHub Actions** (el "robot" que ejecuta tests automáticamente).

### ¿Cuándo se ejecuta?

```yaml
on:
  pull_request:
    branches: [main]
    paths: ['backend/**']
  
  push:
    branches: [main]
    paths: ['backend/**']
```

**Traducción:** El workflow se ejecuta cuando:
- ✅ Alguien hace un **Pull Request** hacia la rama `main`
- ✅ Alguien hace **push** a la rama `main`
- ✅ **SOLO** si los cambios afectan archivos en la carpeta `backend/`

**¿Por qué es inteligente esto?**
- Si solo cambias el frontend, NO se ejecutan los tests del backend (ahorra tiempo y recursos)

---

## ¿Qué hace el workflow paso a paso?

```yaml
jobs:
  test:
    name: Ejecutar Tests del Backend
    runs-on: ubuntu-latest  # ← Usa una máquina virtual con Linux
```

### Paso 1: Descargar el código
```yaml
- name: Checkout código
  uses: actions/checkout@v4
```
**Traducción:** Descarga el código del repositorio.

### Paso 2: Instalar Python
```yaml
- name: Configurar Python 3.11
  uses: actions/setup-python@v4
  with:
    python-version: '3.11'
    cache: 'pip'  # ← Cachea dependencias para ir más rápido
```
**Traducción:** Instala Python 3.11 en la máquina virtual.

### Paso 3: Instalar dependencias
```yaml
- name: Instalar dependencias
  run: |
    python -m pip install --upgrade pip
    pip install -r backend/requirements.txt
```
**Traducción:** Instala todas las librerías que necesita el backend (FastAPI, pytest, etc.)

### Paso 4: Ejecutar tests
```yaml
- name: Ejecutar tests
  run: |
    cd backend
    python -m pytest app/test/ -v --tb=short
```
**Traducción:** Corre todos los tests que están en `backend/app/test/` con **pytest**.

**Flags importantes:**
- `-v` = verbose (muestra detalles)
- `--tb=short` = traceback corto (si hay error, muestra info resumida)

### Paso 5: Cobertura de código
```yaml
- name: Generar reporte de cobertura
  if: always()  # ← Se ejecuta incluso si los tests fallan
  run: |
    pip install pytest-cov
    python -m pytest app/test/ --cov=app --cov-report=term-missing
```
**Traducción:** Genera un reporte que dice qué porcentaje del código está cubierto por tests.

**¿Qué es cobertura?**
- Si tienes 100 líneas de código y los tests ejecutan 80, tienes **80% de cobertura**

---

## ¿Por qué es importante tener CI/CD?

### Beneficios para tu proyecto:

1. **Calidad asegurada**: No puedes romper el código sin que nadie se entere
2. **Feedback rápido**: Sabes en 2-3 minutos si tus cambios funcionan
3. **Profesionalismo**: Es lo que se usa en empresas reales
4. **Colaboración**: Si varios programan, evitas conflictos

---

## Resumen para tu defensa

**Pregunta del profesor:** "¿Qué es GitHub Actions y para qué lo usaron?"

**Tu respuesta:**
> "GitHub Actions es una herramienta de CI/CD que automatiza la ejecución de tests. Configuramos un workflow en `.github/workflows/backend-tests.yml` que se ejecuta automáticamente cada vez que hay cambios en el backend. Esto nos permitió detectar errores temprano y asegurar que todos los tests pasen antes de integrar código a la rama principal. El workflow instala Python 3.11, las dependencias del proyecto, ejecuta pytest, y genera reportes de cobertura de código. Esto es una buena práctica de ingeniería de software moderna."

**Puntos clave para memorizar:**
- 📌 **CI/CD** = Automatización de tests
- 📌 **GitHub Actions** = Herramienta de GitHub para CI/CD
- 📌 **Workflow** = Secuencia de pasos automatizados
- 📌 **pytest** = Framework de testing de Python
- 📌 Se ejecuta en **Linux (ubuntu-latest)** en servidores de GitHub

---

## Tecnologías mencionadas

| Tecnología | ¿Qué es? |
|-----------|----------|
| **GitHub Actions** | Sistema de CI/CD de GitHub |
| **YAML** | Lenguaje para escribir configuraciones (como `.yml`) |
| **pytest** | Framework para escribir y ejecutar tests en Python |
| **pytest-cov** | Plugin para medir cobertura de código |
| **ubuntu-latest** | Sistema operativo Linux donde se ejecutan los tests |

---

**Siguiente:** Ahora que entiendes la automatización, pasemos al **backend** donde está la lógica real del sistema. 🚀
