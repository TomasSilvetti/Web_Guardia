# GUÍA 01: Carpeta `.cursor` - Planes de Desarrollo

## ¿Qué es la carpeta `.cursor`?

La carpeta `.cursor` es una carpeta especial creada por el editor **Cursor** (un editor de código basado en VS Code con IA integrada). Esta carpeta NO forma parte del código de tu aplicación, sino que contiene archivos de configuración y planes de trabajo que el equipo usó durante el desarrollo.

## ¿Por qué existe?

Cuando un equipo trabaja con **Cursor AI**, la inteligencia artificial puede generar "planes" de desarrollo que documentan:
- Qué se va a construir
- Cómo se va a estructurar
- Qué pasos seguir

Estos planes quedan guardados en `.cursor/plans/` como referencia.

## ¿Qué contiene en tu proyecto?

En tu caso, hay un archivo:
```
.cursor/
  └── plans/
      └── backend-api-6cc2255c.plan.md
```

### Archivo: `backend-api-6cc2255c.plan.md`

**Propósito:** Es un documento de planificación que describe cómo se construyó la API REST del backend.

**Contenido importante:**

1. **Estructura de archivos a crear**: Lista todas las carpetas y archivos que se necesitan para el backend
2. **Implementación paso a paso**: Describe en qué orden se deben crear las cosas
3. **Tecnologías a usar**: FastAPI, JWT para autenticación, dependencias

**¿Para qué sirve en tu defensa?**

Este archivo demuestra que el equipo:
- ✅ **Planificó antes de codificar** (buena práctica de ingeniería)
- ✅ **Siguió una arquitectura clara** (separación en capas: API, servicios, repositorios)
- ✅ **Documentó decisiones técnicas** (uso de JWT, FastAPI, estructura MVC)

## Resumen para tu defensa

**Pregunta del profesor:** "¿Qué es la carpeta .cursor?"

**Tu respuesta:**
> "La carpeta `.cursor` contiene planes de desarrollo generados durante la fase de diseño del proyecto. En particular, tenemos un plan para el backend API que documenta la arquitectura de capas que decidimos implementar: capa de presentación (API), capa de servicios (lógica de negocio), y capa de datos (repositorios). Esto nos ayudó a mantener el código organizado y seguir buenas prácticas de ingeniería de software como la separación de responsabilidades."

**Puntos clave:**
- 📌 NO es parte del código ejecutable
- 📌 Es documentación de planificación
- 📌 Muestra que siguieron metodología ordenada
- 📌 Pueden borrarse sin afectar la aplicación

---

## Próximos pasos

Ahora que entiendes `.cursor`, continuaremos con:
- `.github/` → Sistema de integración continua (CI/CD)
- `backend/` → La aplicación Python con FastAPI
- Y así sucesivamente...

**¿Listo para la siguiente carpeta?** 🚀
