from enum import Enum
from datetime import datetime, timedelta
from typing import Optional
import re

import bcrypt


# ============= Value Objects =============

class Frecuencia:
    """Clase base para value objects de frecuencia"""
    def __init__(self, valor: float):
        if valor < 0:
            raise ValueError(f"La {self.__class__.__name__} no puede ser negativa")
        self.valor = valor


class Temperatura(Frecuencia):
    """Value object para temperatura corporal"""
    pass


class FrecuenciaCardiaca(Frecuencia):
    """Value object para frecuencia cardíaca"""
    def __init__(self, valor: float):
        if valor < 0:
            raise ValueError("La Frecuencia Cardiaca no puede ser negativa")
        self.valor = valor


class FrecuenciaRespiratoria(Frecuencia):
    """Value object para frecuencia respiratoria"""
    def __init__(self, valor: float):
        if valor < 0:
            raise ValueError("La Frecuencia Respiratoria no puede ser negativa")
        self.valor = valor


class TensionArterial:
    """Value object para tensión arterial (sistólica/diastólica)"""
    def __init__(self, frecuencia_sistolica: float, frecuencia_diastolica: float):
        if frecuencia_sistolica < 0:
            raise ValueError("La Frecuencia Sistolica no puede ser negativa")
        if frecuencia_diastolica < 0:
            raise ValueError("La Frecuencia Diastolica no puede ser negativa")
        self.frecuencia_sistolica = frecuencia_sistolica
        self.frecuencia_diastolica = frecuencia_diastolica


# ============= Enums =============

class NivelEmergencia(Enum):
    """Enum para los niveles de emergencia según protocolo de triaje"""
    CRITICA = {
        "nivel": 0,
        "nombre": "Critica",
        "duracionMaxEspera": timedelta(minutes=5)
    }
    EMERGENCIA = {
        "nivel": 1,
        "nombre": "Emergencia",
        "duracionMaxEspera": timedelta(minutes=30)
    }
    URGENCIA = {
        "nivel": 2,
        "nombre": "Urgencia",
        "duracionMaxEspera": timedelta(hours=1)
    }
    URGENCIA_MENOR = {
        "nivel": 3,
        "nombre": "Urgencia Menor",
        "duracionMaxEspera": timedelta(hours=2)
    }
    SIN_URGENCIA = {
        "nivel": 4,
        "nombre": "Sin Urgencia",
        "duracionMaxEspera": timedelta(hours=4)
    }


class EstadoIngreso(Enum):
    """Enum para los estados de un ingreso"""
    EN_PROCESO = "EN_PROCESO"
    FINALIZADO = "FINALIZADO"
    PENDIENTE = "PENDIENTE"


# ============= Entidades =============

class ObraSocial:
    """Entidad para obra social"""
    def __init__(self, nombre: str):
        self.nombre = nombre


class Afiliado:
    """Entidad para afiliación de paciente a obra social"""
    def __init__(self, obra_social: ObraSocial, numero_afiliado: str):
        if not obra_social:
            raise ValueError("La obra social es obligatoria")
        if not numero_afiliado or not isinstance(numero_afiliado, str):
            raise ValueError("El número de afiliado es obligatorio")
        self.obra_social = obra_social
        self.numero_afiliado = numero_afiliado


class Domicilio:
    """Entidad para domicilio"""
    def __init__(self, calle: str, numero: int, localidad: str, ciudad: str, provincia: str, pais: str):
        self.calle = calle
        self.numero = numero
        self.localidad = localidad
        self.ciudad = ciudad
        self.provincia = provincia
        self.pais = pais


class Persona:
    """Clase base para personas en el sistema"""
    def __init__(self, cuil: str, nombre: str, apellido: str, email: str = ""):
        self.cuil = cuil
        self.nombre = nombre
        self.apellido = apellido
        self.email = email

    def __str__(self):
        return f"{self.nombre} {self.apellido} (CUIL: {self.cuil})"


class Paciente(Persona):
    """Entidad para paciente"""
    def __init__(
        self,
        nombre: str,
        apellido: str,
        cuil: str,
        domicilio: Domicilio,
        afiliado: Optional['Afiliado'] = None,
        email: str = ""
    ):
        # Validar formato CUIL (XX-XXXXXXXX-X)
        if not cuil or not isinstance(cuil, str):
            raise ValueError("El CUIL es obligatorio")
        
        # Eliminar guiones para validar
        cuil_limpio = cuil.replace("-", "")
        if not cuil_limpio.isdigit() or len(cuil_limpio) != 11:
            raise ValueError("El CUIL debe tener el formato XX-XXXXXXXX-X (11 dígitos)")
        
        super().__init__(cuil, nombre, apellido, email)
        
        if not domicilio:
            raise ValueError("El domicilio es obligatorio")
        
        self.domicilio = domicilio
        self.afiliado = afiliado


class Doctor(Persona):
    """Entidad para doctor"""
    def __init__(self, cuil: str, nombre: str, apellido: str, matricula: str, email: str = ""):
        super().__init__(cuil, nombre, apellido, email)
        self.matricula = matricula


class Enfermera(Persona):
    """Entidad para enfermera"""
    def __init__(self, nombre: str, apellido: str, matricula: str = "", cuil: str = "", email: str = ""):
        # Para mantener compatibilidad con tests que solo pasan nombre y apellido
        super().__init__(cuil, nombre, apellido, email)
        self.matricula = matricula


class Usuario:
    """Entidad para usuario del sistema

    Ahora el constructor acepta un parámetro opcional `rol` (miembro de `Rol` o `str`).
    """
    def __init__(self, email: str, password: str, rol: Optional[object] = None):
        # Validaciones básicas por historia de usuario IS2025-005
        if not email or not isinstance(email, str):
            raise ValueError("El email es obligatorio")
        # simple validación de formato de email
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            raise ValueError("El email no tiene un formato válido")

        if not password or not isinstance(password, str) or len(password) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")

        self.email = email
        self.password = password
        self.password_hash = self._hash_password(password)
        # rol por defecto no asignado; puede asignarse con set_rol o pasarse al constructor
        self.rol = None
        self.id = None  # ID será asignado por el repositorio
        self.matricula = None
        if rol is not None:
            # delega la validación y normalización a set_rol
            self.set_rol(rol)

    def set_rol(self, rol):
        """Asigna el rol al usuario. Acepta un miembro de `Rol` o un string.

        Ejemplos válidos: Rol.MEDICO, "Medico", "medico", "ENFERMERA".
        """
        if isinstance(rol, Rol):
            self.rol = rol
            return

        if isinstance(rol, str):
            key = rol.strip().lower()
            if key.startswith("med"):
                self.rol = Rol.MEDICO
                return
            if key.startswith("enf"):
                self.rol = Rol.ENFERMERA
                return

        raise ValueError("El rol debe ser un miembro de Rol o una cadena 'Medico'/'Enfermera'")

    def _hash_password(self, password: str) -> str:
        """Hashea la contraseña usando bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


    def verificar_password(self, password: str) -> bool:
        """Verifica si el password coincide con el hash guardado"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

class Rol(Enum):
    MEDICO = "MEDICO"
    ENFERMERA = "ENFERMERA"




class Atencion:
    """Entidad para atención médica"""
    def __init__(self, doctor: Doctor, informe: str, ingreso: Optional['Ingreso'] = None):
        if not doctor:
            raise ValueError("El doctor es obligatorio")
        if not informe or not isinstance(informe, str) or not informe.strip():
            raise ValueError("El informe es obligatorio y no puede estar vacío")
        
        self.doctor = doctor
        self.informe = informe
        self.ingreso = ingreso


class Ingreso:
    """Entidad principal para ingreso a urgencias"""
    def __init__(
        self,
        id_uuid: str,
        paciente: Paciente,
        enfermera: Enfermera,
        nivel_emergencia: NivelEmergencia,
        descripcion: str,
        temperatura: Temperatura,
        frecuencia_cardiaca: FrecuenciaCardiaca,
        frecuencia_respiratoria: FrecuenciaRespiratoria,
        tension_arterial: TensionArterial,
        fecha_ingreso: Optional[datetime] = None,
        atencion: Optional[Atencion] = None,
        doctor_asignado: Optional[Doctor] = None
    ):
        self.id = id_uuid
        self.paciente = paciente
        self.enfermera = enfermera
        self.nivel_emergencia = nivel_emergencia
        self.descripcion = descripcion
        self.temperatura = temperatura
        self.frecuencia_cardiaca = frecuencia_cardiaca
        self.frecuencia_respiratoria = frecuencia_respiratoria
        self.tension_arterial = tension_arterial
        self.fecha_ingreso = fecha_ingreso if fecha_ingreso else datetime.now()
        self.atencion = atencion
        self.estado_ingreso = EstadoIngreso.PENDIENTE
        self.doctor_asignado = doctor_asignado

    @property
    def cuil_paciente(self) -> str:
        """Propiedad para acceder al CUIL del paciente (compatibilidad con tests)"""
        return self.paciente.cuil

    @property
    def estado(self) -> str:
        """Propiedad para acceder al estado como string (compatibilidad con tests)"""
        return self.estado_ingreso.value

    def __str__(self):
        return f"Ingreso {self.id} - {self.paciente.nombre} {self.paciente.apellido} - {self.nivel_emergencia.value['nombre']}"


# Alias para mantener compatibilidad con código existente
IngresoUrgencia = Ingreso
SignosVitales = None  # Ya no se usa como clase separada
