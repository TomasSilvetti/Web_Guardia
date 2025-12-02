"""Aplicación FastAPI principal"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from backend.app.core.config import settings
from backend.app.api.routes import auth, urgencias


# Crear instancia de FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API REST para el módulo de urgencias del sistema de gestión hospitalaria"
)


# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Incluir routers
app.include_router(auth.router, prefix=f"{settings.API_PREFIX}/auth", tags=["auth"])
app.include_router(urgencias.router, prefix=f"{settings.API_PREFIX}/urgencias", tags=["urgencias"])


# Endpoints raíz
@app.get("/")
def root():
    """
    Endpoint raíz de la API.
    
    Returns:
        Información básica de la API
    """
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": "API REST para el módulo de urgencias",
        "endpoints": {
            "auth": f"{settings.API_PREFIX}/auth",
            "urgencias": f"{settings.API_PREFIX}/urgencias",
            "health": "/health",
            "docs": "/docs"
        }
    }


@app.get("/health")
def health_check():
    """
    Health check endpoint.
    
    Returns:
        Estado de salud de la API
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.APP_VERSION
    }


# Para ejecutar con uvicorn
# uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

