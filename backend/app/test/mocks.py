from typing import Dict, Optional
from ..interfaces.pacientes_repo import PacientesRepo
from ..models.models import Paciente


class DBPacientes(PacientesRepo):
    """Mock de base de datos de pacientes para testing"""
    
    def __init__(self):
        self._pacientes: Dict[str, Paciente] = {}
    
    def guardar_paciente(self, paciente: Paciente) -> None:
        """Guarda un paciente en el mock de base de datos"""
        self._pacientes[paciente.cuil] = paciente
    
    def obtener_paciente_por_cuil(self, cuil: str) -> Optional[Paciente]:
        """Obtiene un paciente por su CUIL"""
        return self._pacientes.get(cuil)
    
    def existe_paciente(self, cuil: str) -> bool:
        """Verifica si existe un paciente con el CUIL dado"""
        return cuil in self._pacientes

