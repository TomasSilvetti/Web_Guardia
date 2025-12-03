"""Rutas de debug para inspección de memoria"""
from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from backend.app.api.dependencies import get_user_repo, get_pacientes_repo
from backend.app.services.auth_service import InMemoryUserRepo
from backend.app.repositories.paciente_repo_impl import InMemoryPacientesRepo
from backend.app.models.models import Rol


router = APIRouter(tags=["debug"])


@router.get("/memory/users", response_model=Dict[str, Any])
def inspect_users(user_repo: InMemoryUserRepo = Depends(get_user_repo)):
    """
    Inspecciona todos los usuarios en memoria.
    
    Args:
        user_repo: Repositorio de usuarios
        
    Returns:
        Información detallada de todos los usuarios en memoria
    """
    usuarios = user_repo.get_all()
    
    # Agrupar por rol
    medicos = [u for u in usuarios if u.rol == Rol.MEDICO]
    enfermeras = [u for u in usuarios if u.rol == Rol.ENFERMERA]
    
    return {
        "total": len(usuarios),
        "por_rol": {
            "medicos": len(medicos),
            "enfermeras": len(enfermeras)
        },
        "usuarios": [
            {
                "id": u.id,
                "email": u.email,
                "rol": u.rol.value if u.rol else None,
                "matricula": u.matricula,
                "password_hash_preview": u.password_hash[:40] + "..." if u.password_hash else None
            }
            for u in usuarios
        ],
        "medicos": [
            {
                "email": u.email,
                "matricula": u.matricula
            }
            for u in medicos
        ],
        "enfermeras": [
            {
                "email": u.email,
                "matricula": u.matricula
            }
            for u in enfermeras
        ]
    }


@router.get("/memory/pacientes", response_model=Dict[str, Any])
def inspect_pacientes(paciente_repo: InMemoryPacientesRepo = Depends(get_pacientes_repo)):
    """
    Inspecciona todos los pacientes en memoria.
    
    Args:
        paciente_repo: Repositorio de pacientes
        
    Returns:
        Información detallada de todos los pacientes en memoria
    """
    # Acceder al diccionario interno del repositorio
    pacientes = list(paciente_repo._pacientes.values())
    
    # Clasificar pacientes
    con_obra_social = [p for p in pacientes if p.afiliado is not None]
    sin_obra_social = [p for p in pacientes if p.afiliado is None]
    
    return {
        "total": len(pacientes),
        "con_obra_social": len(con_obra_social),
        "sin_obra_social": len(sin_obra_social),
        "pacientes": [
            {
                "nombre": p.nombre,
                "apellido": p.apellido,
                "cuil": p.cuil,
                "email": p.email if p.email else None,
                "domicilio": {
                    "calle": p.domicilio.calle,
                    "numero": p.domicilio.numero,
                    "localidad": p.domicilio.localidad,
                    "ciudad": p.domicilio.ciudad
                } if p.domicilio else None,
                "obra_social": {
                    "nombre": p.afiliado.obra_social.nombre,
                    "numero_afiliado": p.afiliado.numero_afiliado
                } if p.afiliado else None
            }
            for p in pacientes
        ]
    }


@router.get("/memory/all", response_model=Dict[str, Any])
def inspect_all_memory(
    user_repo: InMemoryUserRepo = Depends(get_user_repo),
    paciente_repo: InMemoryPacientesRepo = Depends(get_pacientes_repo)
):
    """
    Inspecciona toda la memoria del sistema (usuarios y pacientes).
    
    Args:
        user_repo: Repositorio de usuarios
        paciente_repo: Repositorio de pacientes
        
    Returns:
        Información completa de la memoria del sistema
    """
    usuarios = user_repo.get_all()
    pacientes = list(paciente_repo._pacientes.values())
    
    return {
        "resumen": {
            "total_usuarios": len(usuarios),
            "total_pacientes": len(pacientes),
            "medicos": len([u for u in usuarios if u.rol == Rol.MEDICO]),
            "enfermeras": len([u for u in usuarios if u.rol == Rol.ENFERMERA]),
            "pacientes_con_obra_social": len([p for p in pacientes if p.afiliado is not None])
        },
        "usuarios": [
            {
                "email": u.email,
                "rol": u.rol.value if u.rol else None,
                "matricula": u.matricula
            }
            for u in usuarios
        ],
        "pacientes": [
            {
                "nombre_completo": f"{p.nombre} {p.apellido}",
                "cuil": p.cuil,
                "tiene_obra_social": p.afiliado is not None
            }
            for p in pacientes
        ]
    }

