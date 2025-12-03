from typing import Optional, Dict, List
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

    def get_all(self) -> List[Usuario]:
        """Retorna todos los usuarios almacenados en memoria"""
        return list(self._store.values())

    def get_all_by_rol(self, rol: Rol) -> List[Usuario]:
        """Retorna todos los usuarios de un rol específico (MEDICO o ENFERMERA)"""
        return [user for user in self._store.values() if user.rol == rol]

    def count(self) -> int:
        """Retorna la cantidad total de usuarios en memoria"""
        return len(self._store)

    def print_all_users(self) -> None:
        """Imprime información detallada de todos los usuarios en memoria"""
        if not self._store:
            print("No hay usuarios registrados en memoria.")
            return

        print(f"\n{'='*80}")
        print(f"USUARIOS EN MEMORIA - Total: {len(self._store)}")
        print(f"{'='*80}\n")

        medicos = [u for u in self._store.values() if u.rol == Rol.MEDICO]
        enfermeras = [u for u in self._store.values() if u.rol == Rol.ENFERMERA]

        if medicos:
            print(f"--- MÉDICOS ({len(medicos)}) ---")
            for user in medicos:
                print(f"  📧 Email: {user.email}")
                print(f"     Rol: {user.rol.value}")
                print(f"     ID: {user.id}")
                print(f"     Matrícula: {user.matricula if user.matricula else 'N/A'}")
                print(f"     Password hash: {user.password_hash[:60]}...")
                print(f"     ✅ Contraseña hasheada correctamente (no se guarda en texto plano)")
                print()

        if enfermeras:
            print(f"--- ENFERMERAS ({len(enfermeras)}) ---")
            for user in enfermeras:
                print(f"  📧 Email: {user.email}")
                print(f"     Rol: {user.rol.value}")
                print(f"     ID: {user.id}")
                print(f"     Matrícula: {user.matricula if user.matricula else 'N/A'}")
                print(f"     Password hash: {user.password_hash[:60]}...")
                print(f"     ✅ Contraseña hasheada correctamente (no se guarda en texto plano)")
                print()

        print(f"{'='*80}\n")


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
