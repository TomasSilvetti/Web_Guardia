"""Rutas de urgencias"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime

from backend.app.api.schemas import (
    IngresoUrgenciaRequest,
    IngresoResponse,
    IngresoListItem,
    NivelEmergenciaItem
)
from backend.app.api.dependencies import (
    get_servicio_emergencias,
    get_current_user,
    get_current_enfermera
)
from backend.app.services.servicio_emergencias import ServicioEmergencias
from backend.app.models.models import NivelEmergencia, Enfermera, Usuario


router = APIRouter(tags=["urgencias"])


@router.post("/ingresos", response_model=IngresoResponse, status_code=status.HTTP_201_CREATED)
def registrar_ingreso(
    request: IngresoUrgenciaRequest,
    enfermera: Enfermera = Depends(get_current_enfermera),
    servicio: ServicioEmergencias = Depends(get_servicio_emergencias)
):
    """
    Registra un nuevo ingreso de urgencia.
    
    Requiere autenticación y que el usuario sea enfermera.
    
    Args:
        request: Datos del ingreso a registrar
        enfermera: Enfermera autenticada (obtenida del token)
        servicio: Servicio de emergencias
        
    Returns:
        Información del ingreso registrado
        
    Raises:
        HTTPException 400: Si los datos son inválidos
        HTTPException 401: Si el token es inválido
        HTTPException 403: Si el usuario no es enfermera
        HTTPException 500: Si ocurre un error inesperado
    """
    try:
        # Convertir string de nivel_emergencia a enum
        try:
            nivel_enum = NivelEmergencia[request.nivel_emergencia.upper()]
        except KeyError:
            raise ValueError(f"Nivel de emergencia inválido: {request.nivel_emergencia}")
        
        # Registrar urgencia
        ingreso, mensaje_advertencia = servicio.registrar_urgencia(
            cuil=request.cuil,
            enfermera=enfermera,
            informe=request.informe,
            nivel_emergencia=nivel_enum,
            temperatura=request.temperatura,
            frecuencia_cardiaca=request.frecuencia_cardiaca,
            frecuencia_respiratoria=request.frecuencia_respiratoria,
            frecuencia_sistolica=request.frecuencia_sistolica,
            frecuencia_diastolica=request.frecuencia_diastolica,
            nombre=request.nombre,
            apellido=request.apellido,
            obra_social=request.obra_social,
            domicilio=request.domicilio.__dict__ if request.domicilio else None
        )
        
        # Preparar respuesta
        return IngresoResponse(
            id=ingreso.id,
            cuil_paciente=ingreso.cuil_paciente,
            nivel_emergencia=ingreso.nivel_emergencia.name,
            estado=ingreso.estado,
            fecha_ingreso=ingreso.fecha_ingreso.isoformat(),
            mensaje_advertencia=mensaje_advertencia
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al registrar ingreso: {str(e)}"
        )


@router.get("/ingresos/pendientes", response_model=List[IngresoListItem])
def listar_ingresos_pendientes(
    current_user: Usuario = Depends(get_current_user),
    servicio: ServicioEmergencias = Depends(get_servicio_emergencias)
):
    """
    Lista todos los ingresos pendientes ordenados por prioridad.
    
    Requiere autenticación.
    
    Args:
        current_user: Usuario autenticado
        servicio: Servicio de emergencias
        
    Returns:
        Lista de ingresos pendientes
        
    Raises:
        HTTPException 401: Si el token es inválido
    """
    try:
        ingresos = servicio.obtener_ingresos_pendientes()
        
        # Convertir a schema de respuesta
        items = []
        for ingreso in ingresos:
            item = IngresoListItem(
                id=ingreso.id,
                cuil_paciente=ingreso.cuil_paciente,
                nombre_paciente=ingreso.paciente.nombre,
                apellido_paciente=ingreso.paciente.apellido,
                nivel_emergencia=ingreso.nivel_emergencia.name,
                nivel_emergencia_nombre=ingreso.nivel_emergencia.value['nombre'],
                estado=ingreso.estado,
                fecha_ingreso=ingreso.fecha_ingreso.isoformat(),
                temperatura=ingreso.temperatura.valor,
                frecuencia_cardiaca=ingreso.frecuencia_cardiaca.valor,
                frecuencia_respiratoria=ingreso.frecuencia_respiratoria.valor,
                frecuencia_sistolica=ingreso.tension_arterial.frecuencia_sistolica,
                frecuencia_diastolica=ingreso.tension_arterial.frecuencia_diastolica
            )
            items.append(item)
        
        return items
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener ingresos pendientes: {str(e)}"
        )


@router.get("/niveles-emergencia", response_model=List[NivelEmergenciaItem])
def listar_niveles_emergencia():
    """
    Lista todos los niveles de emergencia disponibles.
    
    Endpoint público (no requiere autenticación).
    
    Returns:
        Lista de niveles de emergencia con sus características
    """
    niveles = []
    for nivel in NivelEmergencia:
        item = NivelEmergenciaItem(
            valor=nivel.name,
            nombre=nivel.value['nombre'],
            nivel=nivel.value['nivel'],
            duracion_max_espera_minutos=int(nivel.value['duracionMaxEspera'].total_seconds() / 60)
        )
        niveles.append(item)
    
    # Ordenar por nivel (menor número = mayor prioridad)
    niveles.sort(key=lambda x: x.nivel)
    
    return niveles

