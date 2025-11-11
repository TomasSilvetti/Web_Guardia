from typing import Optional, Dict
from ..models.models import Usuario, Rol


class AuthError(Exception):
    pass


class InMemoryUserRepo:
    """Repositorio simple en memoria para usuarios, clave por email."""
    def __init__(self):
        self._store: Dict[str, Usuario] = {}

    def get(self, email: str) -> Optional[Usuario]:
        return self._store.get(email)

    def save(self, user: Usuario) -> None:
        self._store[user.email] = user


def register(email: str, password: str, rol, repo: Optional[InMemoryUserRepo] = None) -> Usuario:
    """Registra un nuevo usuario. Valida email, contraseña y rol.

    Lanza ValueError en caso de datos inválidos o si el usuario ya existe.
    """
    if repo is None:
        repo = InMemoryUserRepo()

    
    user = Usuario(email, password)  
    
    user.set_rol(rol)

    
    if repo.get(user.email) is not None:
        raise ValueError("Usuario ya existe")

    repo.save(user)
    return user


def login(email: str, password: str, repo: Optional[InMemoryUserRepo] = None) -> Usuario:
    """Autentica al usuario. En caso de fallo, lanza ValueError con el mensaje
    exacto: 'Usuario o contraseña inválidos' (no revelar si el usuario existe).
    """
    if repo is None:
        repo = InMemoryUserRepo()

    user = repo.get(email)
  
    if user is None or not user.verificar_password(password):
        raise ValueError("Usuario o contraseña inválidos")

    return user
