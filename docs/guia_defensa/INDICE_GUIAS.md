# 📚 ÍNDICE COMPLETO - Guías del Proyecto Web_Guardia

## 🎯 Objetivo

Estas guías te permitirán **entender completamente** el proyecto y **defenderlo como un profesional**, incluso si no participaste en su desarrollo.

---

## 📖 Guías Disponibles

### 1. [GUIA_01_CURSOR.md](./GUIA_01_CURSOR.md)
**Tema:** Carpeta `.cursor` - Planes de Desarrollo

**Aprenderás:**
- ¿Qué es la carpeta `.cursor`?
- Para qué sirven los planes de desarrollo
- Cómo demostrar planificación profesional

**Tiempo estimado:** 5 minutos

---

### 2. [GUIA_02_GITHUB_ACTIONS.md](./GUIA_02_GITHUB_ACTIONS.md)
**Tema:** Carpeta `.github` - CI/CD y GitHub Actions

**Aprenderás:**
- ¿Qué es CI/CD?
- Cómo funcionan los workflows de GitHub Actions
- Por qué automatizar tests es importante
- Cómo se ejecutan tests en cada push

**Tiempo estimado:** 10 minutos

---

### 3. [GUIA_03_BACKEND.md](./GUIA_03_BACKEND.md) ⭐ **MÁS IMPORTANTE**
**Tema:** Carpeta `backend` - API REST con Python y FastAPI

**Aprenderás:**
- ¿Por qué hay `__init__.py` en cada carpeta?
- Arquitectura por capas (API, Servicios, Domelos, Repositorios)
- Qué es FastAPI y cómo funciona
- Value Objects, Enums, Entidades
- Algoritmo de priorización de urgencias
- Autenticación con JWT
- Cómo funciona cada archivo y carpeta

**Tiempo estimado:** 30-40 minutos

---

### 4. [GUIA_04_DOCS.md](./GUIA_04_DOCS.md)
**Tema:** Carpeta `docs` - Documentación del Proyecto

**Aprenderás:**
- ¿Qué son las Historias de Usuario?
- Criterios de aceptación
- Qué es BDD y Gherkin
- Documentación de CI/CD
- Branch protection

**Tiempo estimado:** 10 minutos

---

### 5. [GUIA_05_FEATURES.md](./GUIA_05_FEATURES.md)
**Tema:** Carpeta `features` - Testing BDD con Behave

**Aprenderás:**
- ¿Qué es BDD (Behavior-Driven Development)?
- Lenguaje Gherkin (Given/When/Then)
- Cómo funcionan los tests automatizados
- Conexión entre escenarios y código Python
- Validación de requisitos

**Tiempo estimado:** 15 minutos

---

### 6. [GUIA_06_FRONTEND.md](./GUIA_06_FRONTEND.md) ⭐ **MÁS IMPORTANTE**
**Tema:** Carpeta `frontend` - Interfaz Web con React y TypeScript

**Aprenderás:**
- ¿Qué es React y TypeScript?
- Componentes, Props, State, Hooks
- Comunicación con el backend (Axios)
- Context API (estado global)
- Rutas protegidas
- Material-UI para la interfaz
- Cómo funciona cada componente

**Tiempo estimado:** 30-40 minutos

---

### 7. [GUIA_07_INTEGRACION.md](./GUIA_07_INTEGRACION.md) ⭐ **FUNDAMENTAL**
**Tema:** Integración Completa - Cómo Funciona Todo el Sistema

**Aprenderás:**
- Flujo completo: desde que el usuario hace login hasta registrar un ingreso
- Cómo se comunican frontend y backend
- Algoritmo de priorización en acción
- Seguridad con JWT explicada paso a paso
- Resumen de todas las tecnologías
- Patrones de diseño utilizados
- Checklist de conocimientos para la defensa

**Tiempo estimado:** 30 minutos

---

## 🎓 Plan de Estudio Recomendado

### Opción 1: Estudio Intensivo (2-3 horas)
**Para defensa inminente:**

1. **Empieza aquí:** GUIA_07_INTEGRACION.md (30 min)
   - Te da la visión general del sistema completo
   
2. **Profundiza backend:** GUIA_03_BACKEND.md (40 min)
   - Es la parte más técnica y compleja
   
3. **Profundiza frontend:** GUIA_06_FRONTEND.md (40 min)
   - Entenderás la interfaz de usuario
   
4. **Testing:** GUIA_05_FEATURES.md (15 min)
   - Importante para demostrar validación
   
5. **Repaso rápido:** Guías 1, 2 y 4 (20 min)
   - Contexto complementario

---

### Opción 2: Estudio Completo (4-5 horas)
**Para entendimiento profundo:**

1. GUIA_01_CURSOR.md
2. GUIA_02_GITHUB_ACTIONS.md
3. GUIA_04_DOCS.md
4. GUIA_03_BACKEND.md ⭐
5. GUIA_05_FEATURES.md
6. GUIA_06_FRONTEND.md ⭐
7. GUIA_07_INTEGRACION.md ⭐

---

### Opción 3: Repaso Pre-Defensa (30 min)
**Si ya estudiaste todo:**

1. Lee el "Resumen para tu Defensa" de cada guía
2. Revisa el "Checklist de Conocimientos" en GUIA_07
3. Practica explicar el flujo completo en voz alta

---

## 💡 Consejos para la Defensa

### 1. **Enfoca en conceptos, no en código memorizado**
En vez de memorizar líneas de código, entiende:
- **¿Por qué?** se tomó cada decisión
- **¿Cómo?** se comunican las partes
- **¿Qué problema?** resuelve cada componente

### 2. **Usa analogías**
Ejemplos de esta guía:
- "El backend es como el cerebro, el frontend es la cara"
- "JWT es como un pase VIP que llevas en tu billetera"
- "El repositorio es como un archivador que abstrae dónde guardas"

### 3. **Practica en voz alta**
- Explícale el sistema a alguien que no sepa programar
- Grábate explicando y escúchate
- Si te trabas en algo, vuelve a esa sección

### 4. **Ten respuestas preparadas para preguntas típicas**

**"¿Por qué usaron Python y no otro lenguaje?"**
> "Python por su legibilidad y rapidez de desarrollo. FastAPI porque genera documentación automática y tiene excelente rendimiento."

**"¿Por qué React en vez de Vue o Angular?"**
> "React por su gran comunidad, abundancia de librerías y conceptos fundamentales como componentes reutilizables. TypeScript nos da seguridad de tipos."

**"¿Cómo manejan la concurrencia si múltiples enfermeras registran ingresos?"**
> "Actualmente usamos repositorios en memoria que no son thread-safe. En producción usaríamos una base de datos con transacciones o locks."

**"¿Por qué no usaron base de datos?"**
> "Por simplicidad en el alcance del TFI. La arquitectura con repositorios permite cambiar fácilmente a PostgreSQL o MongoDB sin tocar la lógica de negocio."

---

## 🎯 Preguntas que DEBES poder responder

### Conceptuales:
- ✅ ¿Qué es una API REST?
- ✅ ¿Qué es JWT y cómo funciona?
- ✅ ¿Qué es BDD?
- ✅ ¿Qué es CI/CD?
- ✅ ¿Por qué separar en capas (arquitectura)?

### Específicas del proyecto:
- ✅ ¿Cómo funciona el algoritmo de priorización?
- ✅ ¿Qué pasa cuando un paciente no existe?
- ✅ ¿Cómo se validan los signos vitales?
- ✅ ¿Qué diferencia hay entre enfermera y médico en el sistema?
- ✅ ¿Cómo se protegen las rutas del frontend?

### Técnicas:
- ✅ ¿Para qué sirven los `__init__.py`?
- ✅ ¿Qué son los Value Objects?
- ✅ ¿Qué es dependency injection?
- ✅ ¿Qué hace un interceptor de Axios?
- ✅ ¿Qué es un custom hook en React?

---

## 📊 Resumen Ultra-Compacto

**Sistema:** Gestión de urgencias hospitalarias

**Arquitectura:** Cliente-servidor (SPA + API REST)

**Backend:** 
- Python 3.11 + FastAPI
- Clean Architecture (capas)
- JWT para autenticación
- Algoritmo de priorización (nivel + FIFO)

**Frontend:**
- React 19 + TypeScript
- Material-UI (componentes)
- Axios (HTTP) + JWT automático
- Rutas protegidas por rol

**Testing:**
- pytest (unitarios)
- Behave (BDD/Gherkin)
- GitHub Actions (CI/CD)

**Flujo típico:**
1. Login → JWT
2. Buscar paciente (GET)
3. Registrar ingreso (POST)
4. Backend valida y prioriza
5. Frontend actualiza lista

---

## 🚀 Cómo Ejecutar el Sistema

### Backend:
```powershell
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
**Docs:** http://localhost:8000/docs

### Frontend:
```powershell
cd frontend
npm install
npm run dev
```
**App:** http://localhost:3000

### Tests:
```powershell
# Unitarios
cd backend
pytest app/test/ -v

# BDD
behave features/
```

---

## 📞 Última Recomendación

**Lee las guías en orden recomendado, toma notas de los puntos clave, y practica explicar el sistema en voz alta.**

**Recuerda:** Los profesores valoran más que entiendas **el por qué** de las decisiones que **el código** en sí.

---

## ✅ Checklist Final

Antes de la defensa, verifica que puedas:

- [ ] Explicar la arquitectura completa en 2 minutos
- [ ] Describir el flujo de registro de un ingreso
- [ ] Justificar decisiones tecnológicas (Python, React, JWT)
- [ ] Explicar cómo funcionan los tests (pytest + Behave)
- [ ] Describir el algoritmo de priorización
- [ ] Explicar qué es CI/CD y cómo lo implementaron
- [ ] Responder "¿Por qué hay __init__.py en cada carpeta?"
- [ ] Explicar la diferencia entre Value Objects y Entidades
- [ ] Describir cómo se protegen las rutas
- [ ] Ejecutar el sistema (backend + frontend)

---

## 🎉 ¡Estás listo!

Con estas guías dominarás el proyecto por completo. **¡Mucha suerte en tu defensa!** 💪🚀

---

**Creado:** 7 de diciembre de 2025  
**Proyecto:** Web_Guardia - Sistema de Gestión de Urgencias Hospitalarias  
**Autor de las guías:** GitHub Copilot (Claude Sonnet 4.5)
