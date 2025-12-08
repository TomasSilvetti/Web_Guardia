"""Schemas para request/response de la API"""
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


# ============= Auth Schemas =============

@dataclass
class LoginRequest:
    """Schema para request de login"""
    email: str
    password: str


@dataclass
class RegisterRequest:
    """Schema para request de registro"""
    email: str
    password: str
    rol: str
    matricula: str


@dataclass
class UserInfo:
    """Información del usuario para incluir en el token"""
    email: str
    rol: str
    matricula: str


@dataclass
class TokenResponse:
    """Schema para response de autenticación"""
    access_token: str
    token_type: str
    user_info: UserInfo


# ============= Urgencias Schemas =============

@dataclass
class DomicilioRequest:
    """Schema para domicilio del paciente"""
    calle: str
    numero: int
    localidad: str
    ciudad: str
    provincia: str
    pais: str


@dataclass
class DomicilioResponse:
    """Schema para domicilio en respuesta"""
    calle: str
    numero: int
    localidad: str
    ciudad: str
    provincia: str
    pais: str


@dataclass
class PacienteResponse:
    """Schema para respuesta de búsqueda de paciente"""
    cuil: str
    nombre: str
    apellido: str
    obra_social: Optional[str]
    domicilio: DomicilioResponse


@dataclass
class IngresoUrgenciaRequest:
    """Schema para request de registro de ingreso a urgencias"""
    cuil: str
    informe: str
    nivel_emergencia: str
    temperatura: float
    frecuencia_cardiaca: float
    frecuencia_respiratoria: float
    frecuencia_sistolica: float
    frecuencia_diastolica: float
    # Campos opcionales para crear paciente si no existe
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    obra_social: Optional[str] = None
    numero_afiliado: Optional[str] = None
    domicilio: Optional[DomicilioRequest] = None


@dataclass
class IngresoResponse:
    """Schema para response de ingreso registrado"""
    id: str
    cuil_paciente: str
    nivel_emergencia: str
    estado: str
    fecha_ingreso: str
    mensaje_advertencia: Optional[str] = None


@dataclass
class IngresoListItem:
    """Schema para item de lista de ingresos pendientes"""
    id: str
    cuil_paciente: str
    nombre_paciente: str
    apellido_paciente: str
    nivel_emergencia: str
    nivel_emergencia_nombre: str
    estado: str
    fecha_ingreso: str
    temperatura: float
    frecuencia_cardiaca: float
    frecuencia_respiratoria: float
    frecuencia_sistolica: float
    frecuencia_diastolica: float


@dataclass
class NivelEmergenciaItem:
    """Schema para item de nivel de emergencia"""
    valor: str
    nombre: str
    nivel: int
    duracion_max_espera_minutos: int


@dataclass
class ErrorResponse:
    """Schema para respuestas de error"""
    detail: str


# ============= Reclamo y Atención Schemas =============

@dataclass
class ReclamarResponse:
    """Schema para response al reclamar un paciente"""
    id: str
    cuil_paciente: str
    nombre_paciente: str
    apellido_paciente: str
    nivel_emergencia: str
    estado: str
    mensaje: str


@dataclass
class AtencionRequest:
    """Schema para request de registro de atención"""
    ingreso_id: str
    informe: str


@dataclass
class AtencionResponse:
    """Schema para response de atención registrada"""
    ingreso_id: str
    estado: str
    mensaje: str


@dataclass
class IngresoDetalleResponse:
    """Schema para detalle completo de un ingreso"""
    id: str
    # Datos del paciente
    cuil_paciente: str
    nombre_paciente: str
    apellido_paciente: str
    # Datos del ingreso
    nivel_emergencia: str
    nivel_emergencia_nombre: str
    estado: str
    fecha_ingreso: str
    descripcion: str
    # Signos vitales
    temperatura: float
    frecuencia_cardiaca: float
    frecuencia_respiratoria: float
    frecuencia_sistolica: float
    frecuencia_diastolica: float
    # Datos de enfermera
    enfermera_nombre: str
    enfermera_apellido: str
    # Atención (si existe)
    atencion_informe: Optional[str] = None
    atencion_doctor_nombre: Optional[str] = None
    atencion_doctor_apellido: Optional[str] = None


# ============= Health Check Schema =============

@dataclass
class HealthResponse:
    """Schema para health check"""
    status: str
    timestamp: str
    version: str

