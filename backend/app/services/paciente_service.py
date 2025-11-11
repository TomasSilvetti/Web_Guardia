from typing import Optional, Dict
from ..models.models import Paciente, Domicilio, ObraSocial, Afiliado


class InMemoryPacienteRepo:
    """Repositorio simple en memoria para pacientes, clave por CUIL."""
    def __init__(self):
        self._pacientes: Dict[str, Paciente] = {}
        self._obras_sociales: Dict[str, ObraSocial] = {}
        self._afiliaciones: Dict[str, set] = {}  # cuil -> set de nombres de obras sociales

    def get(self, cuil: str) -> Optional[Paciente]:
        """Obtiene un paciente por su CUIL"""
        return self._pacientes.get(cuil)

    def save(self, paciente: Paciente) -> None:
        """Guarda un paciente en el repositorio"""
        self._pacientes[paciente.cuil] = paciente

    def existe_obra_social(self, nombre: str) -> bool:
        """Verifica si existe una obra social con el nombre dado"""
        return nombre in self._obras_sociales

    def registrar_obra_social(self, obra_social: ObraSocial) -> None:
        """Registra una obra social en el sistema"""
        self._obras_sociales[obra_social.nombre] = obra_social

    def esta_afiliado(self, cuil: str, nombre_obra_social: str) -> bool:
        """Verifica si un paciente está afiliado a una obra social"""
        if cuil not in self._afiliaciones:
            return False
        return nombre_obra_social in self._afiliaciones[cuil]

    def registrar_afiliacion(self, cuil: str, nombre_obra_social: str) -> None:
        """Registra la afiliación de un paciente a una obra social"""
        if cuil not in self._afiliaciones:
            self._afiliaciones[cuil] = set()
        self._afiliaciones[cuil].add(nombre_obra_social)


def registrar_paciente(
    cuil: str,
    apellido: str,
    nombre: str,
    domicilio: Domicilio,
    afiliado: Optional[Afiliado] = None,
    repo: Optional[InMemoryPacienteRepo] = None
) -> Paciente:
    """Registra un nuevo paciente. Valida todos los campos mandatorios.

    Lanza ValueError en caso de datos inválidos o si la obra social no existe/no está afiliado.
    """
    if repo is None:
        repo = InMemoryPacienteRepo()

    # Validar campos mandatorios
    if not cuil or not isinstance(cuil, str):
        raise ValueError("El campo 'cuil' es obligatorio")
    
    if not apellido or not isinstance(apellido, str):
        raise ValueError("El campo 'apellido' es obligatorio")
    
    if not nombre or not isinstance(nombre, str):
        raise ValueError("El campo 'nombre' es obligatorio")
    
    if not domicilio:
        raise ValueError("El campo 'domicilio' es obligatorio")
    
    # Validar campos del domicilio
    if not domicilio.calle or not isinstance(domicilio.calle, str):
        raise ValueError("El campo 'domicilio.calle' es obligatorio")
    
    if not domicilio.numero or not isinstance(domicilio.numero, int):
        raise ValueError("El campo 'domicilio.numero' es obligatorio")
    
    if not domicilio.localidad or not isinstance(domicilio.localidad, str):
        raise ValueError("El campo 'domicilio.localidad' es obligatorio")

    # Si tiene afiliado, validar obra social
    if afiliado is not None:
        nombre_obra_social = afiliado.obra_social.nombre
        
        # Verificar que la obra social existe
        if not repo.existe_obra_social(nombre_obra_social):
            raise ValueError(f"No se puede registrar al paciente con una obra social inexistente")
        
        # Verificar que el paciente está afiliado
        if not repo.esta_afiliado(cuil, nombre_obra_social):
            raise ValueError(f"No se puede registrar el paciente dado que no está afiliado a la obra social")

    # Crear el paciente (esto también valida el formato del CUIL)
    paciente = Paciente(
        nombre=nombre,
        apellido=apellido,
        cuil=cuil,
        domicilio=domicilio,
        afiliado=afiliado
    )

    # Verificar si el paciente ya existe
    if repo.get(paciente.cuil) is not None:
        raise ValueError("El paciente ya existe")

    repo.save(paciente)
    return paciente

