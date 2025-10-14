from abc import ABC, abstractmethod
from typing import Optional
from backend.app.models.models import Paciente


class PacientesRepo(ABC):
    """Interfaz abstracta para el repositorio de pacientes"""
    
    @abstractmethod
    def guardar_paciente(self, paciente: Paciente) -> None:
        """Guarda un paciente en el repositorio"""
        pass
    
    @abstractmethod
    def obtener_paciente_por_cuil(self, cuil: str) -> Optional[Paciente]:
        """Obtiene un paciente por su CUIL"""
        pass
    
    @abstractmethod
    def existe_paciente(self, cuil: str) -> bool:
        """Verifica si existe un paciente con el CUIL dado"""
        pass

