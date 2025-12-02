"""Rutas de autenticación"""
from fastapi import APIRouter, Depends, HTTPException, status
from backend.app.api.schemas import LoginRequest, RegisterRequest, TokenResponse, UserInfo
from backend.app.api.dependencies import get_user_repo
from backend.app.services.auth_service import InMemoryUserRepo, register, login
from backend.app.core.security import create_access_token


router = APIRouter(tags=["auth"])


@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
def register_user(
    request: RegisterRequest,
    user_repo: InMemoryUserRepo = Depends(get_user_repo)
):
    """
    Registra un nuevo usuario en el sistema.
    
    Args:
        request: Datos del usuario a registrar (email, password, rol, matricula)
        user_repo: Repositorio de usuarios
        
    Returns:
        Mensaje de confirmación
        
    Raises:
        HTTPException 400: Si los datos son inválidos o el usuario ya existe
    """
    try:
        user = register(
            email=request.email,
            password=request.password,
            rol=request.rol,
            repo=user_repo
        )
        # Agregar matrícula al usuario
        user.matricula = request.matricula
        
        return {
            "message": "Usuario registrado exitosamente",
            "email": user.email,
            "rol": user.rol.value if user.rol else None
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=TokenResponse)
def login_user(
    request: LoginRequest,
    user_repo: InMemoryUserRepo = Depends(get_user_repo)
):
    """
    Autentica un usuario y retorna un token JWT.
    
    Args:
        request: Credenciales del usuario (email, password)
        user_repo: Repositorio de usuarios
        
    Returns:
        Token JWT y información del usuario
        
    Raises:
        HTTPException 401: Si las credenciales son inválidas
    """
    try:
        user = login(
            email=request.email,
            password=request.password,
            repo=user_repo
        )
        
        # Crear token JWT con información del usuario
        token_data = {
            "email": user.email,
            "rol": user.rol.value if user.rol else None,
            "matricula": user.matricula
        }
        access_token = create_access_token(data=token_data)
        
        # Preparar información del usuario para la respuesta
        user_info = UserInfo(
            email=user.email,
            rol=user.rol.value if user.rol else "",
            matricula=user.matricula
        )
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user_info=user_info
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )

