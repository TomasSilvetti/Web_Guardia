"""Rutas de urgencias"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime

from backend.app.api.schemas import (
    IngresoUrgenciaRequest,
    IngresoResponse,
    IngresoListItem,
    NivelEmergenciaItem,
    ReclamarResponse,
    AtencionRequest,
    AtencionResponse,
    IngresoDetalleResponse,
    PacienteResponse,
    DomicilioResponse
)
from backend.app.api.dependencies import (
    get_servicio_emergencias,
    get_current_user,
    get_current_enfermera,
    get_current_medico
)
from backend.app.services.servicio_emergencias import ServicioEmergencias
from backend.app.models.models import NivelEmergencia, Enfermera, Usuario, Doctor


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


@router.get("/pacientes/{cuil}", response_model=PacienteResponse)
def buscar_paciente(
    cuil: str,
    current_user: Usuario = Depends(get_current_user),
    servicio: ServicioEmergencias = Depends(get_servicio_emergencias)
):
    """
    Busca un paciente por su CUIL.
    
    Requiere autenticación.
    
    Args:
        cuil: CUIL del paciente a buscar
        current_user: Usuario autenticado
        servicio: Servicio de emergencias
        
    Returns:
        Datos del paciente si existe
        
    Raises:
        HTTPException 404: Si el paciente no existe
        HTTPException 401: Si el token es inválido
    """
    try:
        paciente = servicio.pacientes_repo.obtener_paciente_por_cuil(cuil)
        
        if not paciente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paciente no encontrado"
            )
        
        # Construir respuesta de domicilio
        domicilio_response = DomicilioResponse(
            calle=paciente.domicilio.calle,
            numero=paciente.domicilio.numero,
            localidad=paciente.domicilio.localidad,
            ciudad=paciente.domicilio.ciudad if hasattr(paciente.domicilio, 'ciudad') else '',
            provincia=paciente.domicilio.provincia if hasattr(paciente.domicilio, 'provincia') else '',
            pais=paciente.domicilio.pais if hasattr(paciente.domicilio, 'pais') else 'Argentina'
        )
        
        # Construir respuesta de paciente
        obra_social = None
        if paciente.afiliado and paciente.afiliado.obra_social:
            obra_social = paciente.afiliado.obra_social.nombre
        
        return PacienteResponse(
            cuil=paciente.cuil,
            nombre=paciente.nombre,
            apellido=paciente.apellido,
            obra_social=obra_social,
            domicilio=domicilio_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar paciente: {str(e)}"
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


@router.post("/reclamar", response_model=ReclamarResponse, status_code=status.HTTP_200_OK)
def reclamar_paciente(
    doctor: Doctor = Depends(get_current_medico),
    servicio: ServicioEmergencias = Depends(get_servicio_emergencias)
):
    """
    Reclama el siguiente paciente en la lista de espera.
    
    Requiere autenticación y que el usuario sea médico.
    Cambia el estado del ingreso de PENDIENTE a EN_PROCESO.
    
    Args:
        doctor: Médico autenticado (obtenido del token)
        servicio: Servicio de emergencias
        
    Returns:
        Información del paciente reclamado
        
    Raises:
        HTTPException 400: Si no hay pacientes en espera
        HTTPException 401: Si el token es inválido
        HTTPException 403: Si el usuario no es médico
    """
    try:
        ingreso = servicio.reclamar_siguiente_paciente(doctor)
        
        return ReclamarResponse(
            id=ingreso.id,
            cuil_paciente=ingreso.cuil_paciente,
            nombre_paciente=ingreso.paciente.nombre,
            apellido_paciente=ingreso.paciente.apellido,
            nivel_emergencia=ingreso.nivel_emergencia.name,
            estado=ingreso.estado,
            mensaje="Paciente reclamado exitosamente"
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al reclamar paciente: {str(e)}"
        )


@router.get("/ingresos/en-proceso", response_model=List[IngresoListItem])
def listar_ingresos_en_proceso(
    current_user: Usuario = Depends(get_current_user),
    servicio: ServicioEmergencias = Depends(get_servicio_emergencias)
):
    """
    Lista todos los ingresos en proceso (siendo atendidos).
    
    Requiere autenticación.
    
    Args:
        current_user: Usuario autenticado
        servicio: Servicio de emergencias
        
    Returns:
        Lista de ingresos en proceso
        
    Raises:
        HTTPException 401: Si el token es inválido
    """
    try:
        ingresos = servicio.obtener_ingresos_en_proceso()
        
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
            detail=f"Error al obtener ingresos en proceso: {str(e)}"
        )


@router.post("/atencion", response_model=AtencionResponse, status_code=status.HTTP_201_CREATED)
def registrar_atencion(
    request: AtencionRequest,
    doctor: Doctor = Depends(get_current_medico),
    servicio: ServicioEmergencias = Depends(get_servicio_emergencias)
):
    """
    Registra la atención médica de un paciente y finaliza el ingreso.
    
    Requiere autenticación y que el usuario sea médico.
    Cambia el estado del ingreso de EN_PROCESO a FINALIZADO.
    
    Args:
        request: Datos de la atención (ingreso_id, informe)
        doctor: Médico autenticado (obtenido del token)
        servicio: Servicio de emergencias
        
    Returns:
        Confirmación de atención registrada
        
    Raises:
        HTTPException 400: Si el informe está vacío o el ingreso no existe
        HTTPException 401: Si el token es inválido
        HTTPException 403: Si el usuario no es médico
    """
    try:
        servicio.registrar_atencion(
            ingreso_id=request.ingreso_id,
            doctor=doctor,
            informe=request.informe
        )
        
        return AtencionResponse(
            ingreso_id=request.ingreso_id,
            estado="FINALIZADO",
            mensaje="Atención registrada exitosamente"
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al registrar atención: {str(e)}"
        )


@router.get("/ingresos/{ingreso_id}", response_model=IngresoDetalleResponse)
def obtener_detalle_ingreso(
    ingreso_id: str,
    current_user: Usuario = Depends(get_current_user),
    servicio: ServicioEmergencias = Depends(get_servicio_emergencias)
):
    """
    Obtiene el detalle completo de un ingreso.
    
    Requiere autenticación.
    
    Args:
        ingreso_id: ID del ingreso
        current_user: Usuario autenticado
        servicio: Servicio de emergencias
        
    Returns:
        Detalle completo del ingreso
        
    Raises:
        HTTPException 404: Si el ingreso no existe
        HTTPException 401: Si el token es inválido
    """
    try:
        ingreso = servicio.obtener_ingreso_por_id(ingreso_id)
        
        if not ingreso:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ingreso no encontrado"
            )
        
        # Preparar datos de atención si existe
        atencion_informe = None
        atencion_doctor_nombre = None
        atencion_doctor_apellido = None
        
        if ingreso.atencion:
            atencion_informe = ingreso.atencion.informe
            atencion_doctor_nombre = ingreso.atencion.doctor.nombre
            atencion_doctor_apellido = ingreso.atencion.doctor.apellido
        
        return IngresoDetalleResponse(
            id=ingreso.id,
            cuil_paciente=ingreso.cuil_paciente,
            nombre_paciente=ingreso.paciente.nombre,
            apellido_paciente=ingreso.paciente.apellido,
            nivel_emergencia=ingreso.nivel_emergencia.name,
            nivel_emergencia_nombre=ingreso.nivel_emergencia.value['nombre'],
            estado=ingreso.estado,
            fecha_ingreso=ingreso.fecha_ingreso.isoformat(),
            descripcion=ingreso.descripcion,
            temperatura=ingreso.temperatura.valor,
            frecuencia_cardiaca=ingreso.frecuencia_cardiaca.valor,
            frecuencia_respiratoria=ingreso.frecuencia_respiratoria.valor,
            frecuencia_sistolica=ingreso.tension_arterial.frecuencia_sistolica,
            frecuencia_diastolica=ingreso.tension_arterial.frecuencia_diastolica,
            enfermera_nombre=ingreso.enfermera.nombre,
            enfermera_apellido=ingreso.enfermera.apellido,
            atencion_informe=atencion_informe,
            atencion_doctor_nombre=atencion_doctor_nombre,
            atencion_doctor_apellido=atencion_doctor_apellido
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener detalle del ingreso: {str(e)}"
        )

