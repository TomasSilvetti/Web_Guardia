"""Dependencias para inyección en FastAPI"""
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from backend.app.core.security import decode_access_token
from backend.app.models.models import Usuario, Enfermera, Rol
from backend.app.services.auth_service import InMemoryUserRepo
from backend.app.repositories.paciente_repo_impl import InMemoryPacientesRepo
from backend.app.services.servicio_emergencias import ServicioEmergencias


# OAuth2 scheme para autenticación con Bearer token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


# Singletons para desarrollo (en producción usar scope de FastAPI)
_user_repo: Optional[InMemoryUserRepo] = None
_pacientes_repo: Optional[InMemoryPacientesRepo] = None
_servicio_emergencias: Optional[ServicioEmergencias] = None


def get_user_repo() -> InMemoryUserRepo:
    """
    Obtiene el repositorio de usuarios (singleton).
    
    Returns:
        Repositorio de usuarios
    """
    global _user_repo
    if _user_repo is None:
        _user_repo = InMemoryUserRepo()
    return _user_repo


def get_pacientes_repo() -> InMemoryPacientesRepo:
    """
    Obtiene el repositorio de pacientes (singleton).
    
    Returns:
        Repositorio de pacientes
    """
    global _pacientes_repo
    if _pacientes_repo is None:
        _pacientes_repo = InMemoryPacientesRepo()
    return _pacientes_repo


def get_servicio_emergencias(
    pacientes_repo: InMemoryPacientesRepo = Depends(get_pacientes_repo)
) -> ServicioEmergencias:
    """
    Obtiene el servicio de emergencias (singleton).
    
    Args:
        pacientes_repo: Repositorio de pacientes
        
    Returns:
        Servicio de emergencias
    """
    global _servicio_emergencias
    if _servicio_emergencias is None:
        _servicio_emergencias = ServicioEmergencias(pacientes_repo)
    return _servicio_emergencias


def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repo: InMemoryUserRepo = Depends(get_user_repo)
) -> Usuario:
    """
    Extrae y valida el JWT del header Authorization.
    
    Args:
        token: Token JWT del header Authorization
        user_repo: Repositorio de usuarios
        
    Returns:
        Usuario autenticado
        
    Raises:
        HTTPException 401: Si el token es inválido o el usuario no existe
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = decode_access_token(token)
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = user_repo.get(email)
    if user is None:
        raise credentials_exception
    
    return user


def get_current_enfermera(
    current_user: Usuario = Depends(get_current_user)
) -> Enfermera:
    """
    Valida que el usuario autenticado sea una enfermera.
    
    Args:
        current_user: Usuario autenticado
        
    Returns:
        Objeto Enfermera con los datos del usuario
        
    Raises:
        HTTPException 403: Si el usuario no es enfermera
    """
    if current_user.rol != Rol.ENFERMERA:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para realizar esta acción. Solo enfermeras pueden registrar ingresos."
        )
    
    # Crear objeto Enfermera a partir del Usuario
    enfermera = Enfermera(
        nombre=current_user.email.split("@")[0],  # Usar parte del email como nombre temporal
        apellido="",
        matricula=current_user.matricula,
        cuil="",
        email=current_user.email
    )
    
    return enfermera

