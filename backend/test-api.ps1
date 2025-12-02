# Script completo para probar la API REST - Módulo de Urgencias

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  Prueba de API REST - Módulo de Urgencias" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# 1. Registrar enfermera
Write-Host "`n1. Registrando enfermera..." -ForegroundColor Cyan
$registerBody = @{
    email = "enfermera.test@hospital.com"
    password = "password123"
    rol = "Enfermera"
    matricula = "ENF-99999"
} | ConvertTo-Json

try {
    $registerResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/auth/register" `
        -Method POST `
        -Body $registerBody `
        -ContentType "application/json"
    Write-Host "   ✓ Enfermera registrada: $($registerResponse.email)" -ForegroundColor Green
} catch {
    Write-Host "   ⚠ Usuario ya existe o error en registro" -ForegroundColor Yellow
}

# 2. Login
Write-Host "`n2. Iniciando sesión..." -ForegroundColor Cyan
$loginBody = @{
    email = "enfermera.test@hospital.com"
    password = "password123"
} | ConvertTo-Json

try {
    $loginResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/auth/login" `
        -Method POST `
        -Body $loginBody `
        -ContentType "application/json"

    $token = $loginResponse.access_token
    Write-Host "   ✓ Token obtenido" -ForegroundColor Green
    Write-Host "     Usuario: $($loginResponse.user_info.email)" -ForegroundColor Gray
    Write-Host "     Rol: $($loginResponse.user_info.rol)" -ForegroundColor Gray
    Write-Host "     Matrícula: $($loginResponse.user_info.matricula)" -ForegroundColor Gray
} catch {
    Write-Host "   ✗ Error en login: $_" -ForegroundColor Red
    exit 1
}

# 3. Listar niveles de emergencia
Write-Host "`n3. Listando niveles de emergencia..." -ForegroundColor Cyan
try {
    $niveles = Invoke-RestMethod -Uri "http://localhost:8000/api/urgencias/niveles-emergencia" `
        -Method GET

    Write-Host "   ✓ Niveles disponibles:" -ForegroundColor Green
    foreach ($nivel in $niveles) {
        Write-Host "     - $($nivel.nombre) (Espera máx: $($nivel.duracion_max_espera_minutos) min)" -ForegroundColor Gray
    }
} catch {
    Write-Host "   ✗ Error al listar niveles: $_" -ForegroundColor Red
}

# 4. Registrar ingreso de urgencia
Write-Host "`n4. Registrando ingreso de urgencia..." -ForegroundColor Cyan
$headers = @{
    Authorization = "Bearer $token"
}

$ingresoBody = @{
    cuil = "20-98765432-1"
    informe = "Paciente con dolor torácico y dificultad respiratoria"
    nivel_emergencia = "EMERGENCIA"
    temperatura = 38.2
    frecuencia_cardiaca = 110
    frecuencia_respiratoria = 24
    frecuencia_sistolica = 140
    frecuencia_diastolica = 90
    nombre = "María"
    apellido = "González"
    obra_social = "Swiss Medical"
} | ConvertTo-Json

try {
    $ingresoResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/urgencias/ingresos" `
        -Method POST `
        -Headers $headers `
        -Body $ingresoBody `
        -ContentType "application/json"

    Write-Host "   ✓ Ingreso registrado:" -ForegroundColor Green
    Write-Host "     ID: $($ingresoResponse.id)" -ForegroundColor Gray
    Write-Host "     Paciente: $($ingresoResponse.cuil_paciente)" -ForegroundColor Gray
    Write-Host "     Nivel: $($ingresoResponse.nivel_emergencia)" -ForegroundColor Gray
    Write-Host "     Estado: $($ingresoResponse.estado)" -ForegroundColor Gray

    if ($ingresoResponse.mensaje_advertencia) {
        Write-Host "     ⚠ Advertencia: $($ingresoResponse.mensaje_advertencia)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "   ✗ Error al registrar ingreso: $_" -ForegroundColor Red
}

# 5. Registrar otro ingreso con nivel crítico
Write-Host "`n5. Registrando ingreso CRÍTICO..." -ForegroundColor Cyan

$ingresoCriticoBody = @{
    cuil = "27-11223344-5"
    informe = "Paciente inconsciente, traumatismo craneoencefálico severo"
    nivel_emergencia = "CRITICA"
    temperatura = 36.8
    frecuencia_cardiaca = 130
    frecuencia_respiratoria = 28
    frecuencia_sistolica = 90
    frecuencia_diastolica = 60
    nombre = "Carlos"
    apellido = "Rodríguez"
    obra_social = "OSDE"
} | ConvertTo-Json

try {
    $ingresoCriticoResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/urgencias/ingresos" `
        -Method POST `
        -Headers $headers `
        -Body $ingresoCriticoBody `
        -ContentType "application/json"

    Write-Host "   ✓ Ingreso crítico registrado:" -ForegroundColor Green
    Write-Host "     ID: $($ingresoCriticoResponse.id)" -ForegroundColor Gray
    Write-Host "     Paciente: $($ingresoCriticoResponse.cuil_paciente)" -ForegroundColor Gray
    Write-Host "     Nivel: $($ingresoCriticoResponse.nivel_emergencia)" -ForegroundColor Gray
} catch {
    Write-Host "   ✗ Error al registrar ingreso crítico: $_" -ForegroundColor Red
}

# 6. Listar ingresos pendientes
Write-Host "`n6. Listando ingresos pendientes (ordenados por prioridad)..." -ForegroundColor Cyan
try {
    $pendientes = Invoke-RestMethod -Uri "http://localhost:8000/api/urgencias/ingresos/pendientes" `
        -Method GET `
        -Headers $headers

    Write-Host "   ✓ Ingresos pendientes: $($pendientes.Count)" -ForegroundColor Green
    
    $contador = 1
    foreach ($ingreso in $pendientes) {
        Write-Host "`n   [$contador] Paciente: $($ingreso.nombre_paciente) $($ingreso.apellido_paciente)" -ForegroundColor White
        Write-Host "       CUIL: $($ingreso.cuil_paciente)" -ForegroundColor Gray
        Write-Host "       Nivel: $($ingreso.nivel_emergencia_nombre)" -ForegroundColor $(
            switch ($ingreso.nivel_emergencia) {
                "CRITICA" { "Red" }
                "EMERGENCIA" { "Yellow" }
                "URGENCIA" { "Cyan" }
                default { "Gray" }
            }
        )
        Write-Host "       Estado: $($ingreso.estado)" -ForegroundColor Gray
        Write-Host "       Signos vitales:" -ForegroundColor Gray
        Write-Host "         • Temperatura: $($ingreso.temperatura)°C" -ForegroundColor DarkGray
        Write-Host "         • FC: $($ingreso.frecuencia_cardiaca) lpm" -ForegroundColor DarkGray
        Write-Host "         • FR: $($ingreso.frecuencia_respiratoria) rpm" -ForegroundColor DarkGray
        Write-Host "         • TA: $($ingreso.frecuencia_sistolica)/$($ingreso.frecuencia_diastolica) mmHg" -ForegroundColor DarkGray
        $contador++
    }
} catch {
    Write-Host "   ✗ Error al listar ingresos pendientes: $_" -ForegroundColor Red
}

# 7. Health check
Write-Host "`n7. Verificando estado de la API..." -ForegroundColor Cyan
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method GET
    Write-Host "   ✓ API Status: $($health.status)" -ForegroundColor Green
    Write-Host "     Versión: $($health.version)" -ForegroundColor Gray
    Write-Host "     Timestamp: $($health.timestamp)" -ForegroundColor Gray
} catch {
    Write-Host "   ✗ Error en health check: $_" -ForegroundColor Red
}

Write-Host "`n==================================================" -ForegroundColor Cyan
Write-Host "  ✓ Prueba completada exitosamente!" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "`nPara ver la documentación interactiva, visita:" -ForegroundColor White
Write-Host "  http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""

