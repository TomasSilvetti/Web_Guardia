from typing import List, Optional, Tuple
import uuid
from backend.app.models.models import (
    Enfermera,
    Paciente,
    NivelEmergencia,
    Temperatura,
    FrecuenciaCardiaca,
    FrecuenciaRespiratoria,
    TensionArterial,
    Ingreso,
    Doctor,
    Atencion,
    EstadoIngreso
)
from backend.app.interfaces.pacientes_repo import PacientesRepo


class ServicioEmergencias:
    """Servicio para gestionar el módulo de urgencias"""
    
    def __init__(self, pacientes_repo: PacientesRepo):
        self.pacientes_repo = pacientes_repo
        self._ingresos_pendientes: List[Ingreso] = []
        self._ingresos_en_proceso: List[Ingreso] = []
        self._ingresos_finalizados: List[Ingreso] = []
    
    def registrar_urgencia(
        self,
        cuil: Optional[str],
        enfermera: Enfermera,
        informe: Optional[str],
        nivel_emergencia: Optional[NivelEmergencia],
        temperatura: Optional[float],
        frecuencia_cardiaca: Optional[float],
        frecuencia_respiratoria: Optional[float],
        frecuencia_sistolica: Optional[float],
        frecuencia_diastolica: Optional[float],
        nombre: Optional[str],
        apellido: Optional[str],
        obra_social: Optional[str],
        domicilio: Optional[dict] = None
    ) -> Tuple[Ingreso, Optional[str]]:
        """
        Registra un ingreso de urgencia de un paciente.

        Valida que el paciente exista en el sistema y crea los value objects necesarios.
        Si el paciente no existe y se proporcionan los datos necesarios (nombre, apellido, obra_social),
        se crea el paciente automáticamente y se retorna un mensaje de advertencia.
        Luego crea el ingreso y lo agrega a la lista de ingresos pendientes
        ordenada por prioridad (nivel) y hora de llegada.

        Args:
            cuil: CUIL del paciente
            enfermera: Enfermera que registra el ingreso
            informe: Informe médico del ingreso (descripción)
            nivel_emergencia: Nivel de emergencia del paciente
            temperatura: Temperatura corporal
            frecuencia_cardiaca: Frecuencia cardíaca
            frecuencia_respiratoria: Frecuencia respiratoria
            frecuencia_sistolica: Presión arterial sistólica
            frecuencia_diastolica: Presión arterial diastólica
            nombre: Nombre del paciente (requerido si el paciente no existe)
            apellido: Apellido del paciente (requerido si el paciente no existe)
            obra_social: Obra social del paciente (requerido si el paciente no existe)
            domicilio: Domicilio del paciente (requerido si el paciente no existe)

        Returns:
            Tupla (ingreso_creado, mensaje_advertencia)
            - ingreso_creado: El ingreso creado
            - mensaje_advertencia: Mensaje de advertencia si el paciente fue creado, None en caso contrario

        Raises:
            ValueError: Si los signos vitales son inválidos o si faltan campos mandatorios
            Exception: Si el paciente no existe y no se proporcionan los datos necesarios para crearlo
        """
        # Validar campos mandatorios básicos
        if cuil is None:
            raise ValueError("El campo cuil es obligatorio")

        if informe is None:
            raise ValueError("El campo informe es obligatorio")

        if nivel_emergencia is None:
            raise ValueError("El campo nivel de emergencia es obligatorio")

        if temperatura is None:
            raise ValueError("El campo temperatura es obligatorio")

        if frecuencia_cardiaca is None:
            raise ValueError("El campo frecuencia cardiaca es obligatorio")

        if frecuencia_respiratoria is None:
            raise ValueError("El campo frecuencia respiratoria es obligatorio")

        if frecuencia_sistolica is None or frecuencia_diastolica is None:
            raise ValueError("El campo tension arterial es obligatorio")

        mensaje_advertencia = None

        # Verificar que el paciente existe
        paciente = self.pacientes_repo.obtener_paciente_por_cuil(cuil)

        if paciente is None:
            # Validar campos necesarios para crear el paciente
            if nombre is None:
                raise ValueError("El campo nombre es obligatorio")

            if apellido is None:
                raise ValueError("El campo apellido es obligatorio")

            if obra_social is None:
                raise ValueError("El campo obra social es obligatorio")

            if domicilio is None:
                raise ValueError("El campo domicilio es obligatorio para crear un paciente nuevo")

            # Crear el paciente automáticamente
            mensaje_advertencia = "El paciente no existe en el sistema y debe ser registrado antes de proceder al ingreso"
            
            # Crear objeto Domicilio
            from backend.app.models.models import Domicilio, ObraSocial, Afiliado
            domicilio_obj = Domicilio(
                calle=domicilio.get('calle'),
                numero=domicilio.get('numero'),
                localidad=domicilio.get('localidad'),
                ciudad=domicilio.get('ciudad'),
                provincia=domicilio.get('provincia'),
                pais=domicilio.get('pais')
            )
            
            # Crear obra social y afiliado si se proporcionó
            afiliado = None
            if obra_social:
                obra_social_obj = ObraSocial(obra_social)
                afiliado = Afiliado(obra_social_obj, "000000")  # número de afiliado temporal
            
            paciente = Paciente(nombre, apellido, cuil, domicilio_obj, afiliado)
            self.pacientes_repo.guardar_paciente(paciente)

        # Crear value objects (aquí se validan los valores)
        temp = Temperatura(temperatura)
        fc = FrecuenciaCardiaca(frecuencia_cardiaca)
        fr = FrecuenciaRespiratoria(frecuencia_respiratoria)
        ta = TensionArterial(frecuencia_sistolica, frecuencia_diastolica)

        # Generar UUID para el ingreso
        ingreso_id = str(uuid.uuid4())

        # Crear el ingreso
        ingreso = Ingreso(
            id_uuid=ingreso_id,
            paciente=paciente,
            enfermera=enfermera,
            nivel_emergencia=nivel_emergencia,
            descripcion=informe,
            temperatura=temp,
            frecuencia_cardiaca=fc,
            frecuencia_respiratoria=fr,
            tension_arterial=ta
        )

        # Agregar a la lista de ingresos pendientes
        self._ingresos_pendientes.append(ingreso)

        # Ordenar por prioridad (nivel, menor número = mayor prioridad) y por fecha/hora de llegada
        self._ingresos_pendientes.sort(
            key=lambda x: (x.nivel_emergencia.value['nivel'], x.fecha_ingreso)
        )

        return ingreso, mensaje_advertencia
    
    def obtener_ingresos_pendientes(self) -> List[Ingreso]:
        """
        Obtiene la lista de ingresos pendientes ordenados por prioridad y hora de llegada.
        
        Returns:
            Lista de ingresos pendientes ordenados
        """
        return self._ingresos_pendientes.copy()
    
    def atender_siguiente(self) -> Ingreso:
        """
        Atiende al siguiente paciente en la cola de urgencias.
        
        Returns:
            El ingreso atendido
            
        Raises:
            Exception: Si no hay pacientes pendientes
        """
        if not self._ingresos_pendientes:
            raise Exception("No hay pacientes pendientes para atender")
        
        ingreso = self._ingresos_pendientes.pop(0)
        ingreso.estado_ingreso = ingreso.estado_ingreso.__class__.EN_PROCESO
        return ingreso
    
    def reclamar_siguiente_paciente(self, doctor: Doctor) -> Ingreso:
        """
        Reclama el siguiente paciente en la lista de espera para ser atendido por un médico.
        
        Cambia el estado del ingreso de PENDIENTE a EN_PROCESO y lo mueve a la lista
        de ingresos en proceso.
        
        Args:
            doctor: Médico que reclama el paciente
            
        Returns:
            El ingreso reclamado
            
        Raises:
            ValueError: Si no hay pacientes en la lista de espera o si el doctor ya tiene un paciente en revisión
        """
        if not doctor:
            raise ValueError("El doctor es obligatorio")
        
        # Verificar que el doctor no tenga otro paciente en proceso
        for ingreso in self._ingresos_en_proceso:
            if ingreso.doctor_asignado and ingreso.doctor_asignado.email == doctor.email:
                raise ValueError(
                    f"El doctor ya tiene un paciente en revisión. "
                    f"Debe finalizar la atención del paciente {ingreso.paciente.nombre} "
                    f"{ingreso.paciente.apellido} antes de reclamar otro."
                )
        
        if not self._ingresos_pendientes:
            raise ValueError("No hay pacientes en la lista de espera")
        
        # Obtener el primer paciente (mayor prioridad)
        ingreso = self._ingresos_pendientes.pop(0)
        
        # Cambiar estado a EN_PROCESO
        ingreso.estado_ingreso = EstadoIngreso.EN_PROCESO
        
        # Asignar doctor al ingreso
        ingreso.doctor_asignado = doctor
        
        # Agregar a lista de ingresos en proceso
        self._ingresos_en_proceso.append(ingreso)
        
        return ingreso
    
    def obtener_ingresos_en_proceso(self) -> List[Ingreso]:
        """
        Obtiene la lista de ingresos que están siendo atendidos (estado EN_PROCESO).
        
        Returns:
            Lista de ingresos en proceso
        """
        return self._ingresos_en_proceso.copy()
    
    def registrar_atencion(self, ingreso_id: str, doctor: Doctor, informe: str) -> Atencion:
        """
        Registra la atención médica de un paciente y finaliza el ingreso.
        
        Valida que el informe no esté vacío, crea la atención asociada al doctor
        e ingreso, cambia el estado del ingreso a FINALIZADO y lo mueve a la lista
        de ingresos finalizados.
        
        Args:
            ingreso_id: ID del ingreso a atender
            doctor: Médico que registra la atención
            informe: Informe de atención (mandatorio)
            
        Returns:
            La atención creada
            
        Raises:
            ValueError: Si el informe está vacío o el ingreso no existe/no está en proceso
        """
        if not informe or not informe.strip():
            raise ValueError("El informe del paciente se ha omitido")
        
        if not doctor:
            raise ValueError("El doctor es obligatorio")
        
        # Buscar el ingreso en la lista de ingresos en proceso
        ingreso = None
        for ing in self._ingresos_en_proceso:
            if ing.id == ingreso_id:
                ingreso = ing
                break
        
        if not ingreso:
            raise ValueError("El ingreso no existe o no está en proceso")
        
        # Crear la atención
        atencion = Atencion(doctor=doctor, informe=informe, ingreso=ingreso)
        
        # Asociar la atención al ingreso
        ingreso.atencion = atencion
        
        # Cambiar estado a FINALIZADO
        ingreso.estado_ingreso = EstadoIngreso.FINALIZADO
        
        # Mover de en_proceso a finalizados
        self._ingresos_en_proceso.remove(ingreso)
        self._ingresos_finalizados.append(ingreso)
        
        return atencion
    
    def obtener_ingreso_por_id(self, ingreso_id: str) -> Optional[Ingreso]:
        """
        Obtiene un ingreso por su ID, buscando en todas las listas.
        
        Args:
            ingreso_id: ID del ingreso a buscar
            
        Returns:
            El ingreso encontrado o None si no existe
        """
        # Buscar en pendientes
        for ingreso in self._ingresos_pendientes:
            if ingreso.id == ingreso_id:
                return ingreso
        
        # Buscar en proceso
        for ingreso in self._ingresos_en_proceso:
            if ingreso.id == ingreso_id:
                return ingreso
        
        # Buscar en finalizados
        for ingreso in self._ingresos_finalizados:
            if ingreso.id == ingreso_id:
                return ingreso
        
        return None
