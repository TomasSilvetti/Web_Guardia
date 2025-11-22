"""Implementación en memoria del repositorio de pacientes"""
from typing import Dict, Optional
from backend.app.interfaces.pacientes_repo import PacientesRepo
from backend.app.models.models import Paciente


class InMemoryPacientesRepo(PacientesRepo):
    """Repositorio en memoria para pacientes"""
    
    def __init__(self):
        self._pacientes: Dict[str, Paciente] = {}
    
    def guardar_paciente(self, paciente: Paciente) -> None:
        """
        Guarda un paciente en el repositorio.
        
        Args:
            paciente: Paciente a guardar
        """
        self._pacientes[paciente.cuil] = paciente
    
    def obtener_paciente_por_cuil(self, cuil: str) -> Optional[Paciente]:
        """
        Obtiene un paciente por su CUIL.
        
        Args:
            cuil: CUIL del paciente
            
        Returns:
            Paciente si existe, None en caso contrario
        """
        return self._pacientes.get(cuil)
    
    def existe_paciente(self, cuil: str) -> bool:
        """
        Verifica si existe un paciente con el CUIL dado.
        
        Args:
            cuil: CUIL del paciente
            
        Returns:
            True si existe, False en caso contrario
        """
        return cuil in self._pacientes

