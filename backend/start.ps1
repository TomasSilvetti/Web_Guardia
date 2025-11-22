# Script de inicio para la API REST
# Uso: .\start.ps1

Write-Host "Iniciando API REST - Módulo de Urgencias..." -ForegroundColor Green

# Verificar si el entorno virtual existe
if (-Not (Test-Path ".\venv\Scripts\Activate.ps1")) {
    Write-Host "Entorno virtual no encontrado. Creando..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "Entorno virtual creado." -ForegroundColor Green
}

# Activar entorno virtual
Write-Host "Activando entorno virtual..." -ForegroundColor Cyan
& .\venv\Scripts\Activate.ps1

# Instalar/actualizar dependencias
Write-Host "Instalando dependencias..." -ForegroundColor Cyan
pip install -r requirements.txt

# Iniciar servidor
Write-Host "`nIniciando servidor en http://localhost:8000" -ForegroundColor Green
Write-Host "Documentación disponible en http://localhost:8000/docs`n" -ForegroundColor Cyan

uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

