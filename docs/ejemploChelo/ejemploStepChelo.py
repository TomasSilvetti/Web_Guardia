from behave import *
from models.models import Enfermera, Paciente, NivelEmergencia
from service import ServicioEmergencias
from interfaces import PacientesRepo

from test.mocks import DBPacientes


enfermera: Enfermera | None = None
db_mockeada: PacientesRepo | None = None
servicio_urgencias: ServicioEmergencias | None = None
excepcion_esperada = None


@given("que la siguiente enfermera esta registrada:")
def step_impl(context):
    global enfermera, db_mockeada, servicio_urgencias
    
    nombre_enfermera = context.table[0]['Nombre']
    apellido_enfermera = context.table[0]['Apellido']

    enfermera = Enfermera(nombre_enfermera, apellido_enfermera)
    
    # Initialize the mock database and service
    db_mockeada = DBPacientes()
    servicio_urgencias = ServicioEmergencias(db_mockeada)


@given("que estan registrados los siguientes pacientes:")
def step_impl(context):
    global db_mockeada
    
    for row in context.table:
        cuil = row['Cuil']
        nombre = row['Nombre']
        apellido = row['Apellido']
        obra_social = row['Obra Social']
        
        paciente = Paciente(nombre, apellido, cuil, obra_social)
        db_mockeada.guardar_paciente(paciente)


@when("Ingresan a urgencias los siguientes pacientes:")
def step_impl(context):
    global enfermera, servicio_urgencias, excepcion_esperada
    
    excepcion_esperada = None
    
    for row in context.table:
        cuil = row['Cuil']
        informe = row['Informe']
        nivel_emergencia_str = row['Nivel de Emergencia']
        temperatura = float(row['Temperatura'])
        frecuencia_cardiaca = float(row['Frecuencia Cardiaca'])
        frecuencia_respiratoria = float(row['Frecuencia Respiratoria'])
        tension_arterial_str = row['Tension Arterial']
        
        # Parse tension arterial (format: "120/80")
        tension_parts = tension_arterial_str.split('/')
        frecuencia_sistolica = float(tension_parts[0])
        frecuencia_diastolica = float(tension_parts[1])
        
        # Find the corresponding NivelEmergencia enum
        nivel_emergencia = None
        for nivel in NivelEmergencia:
            if nivel.value['nombre'] == nivel_emergencia_str:
                nivel_emergencia = nivel
                break
        
        if nivel_emergencia is None:
            raise ValueError(f"Nivel de emergencia desconocido: {nivel_emergencia_str}")
        
        try:
            servicio_urgencias.registrar_urgencia(
                cuil=cuil,
                enfermera=enfermera,
                informe=informe,
                nivel_emergencia=nivel_emergencia,
                temperatura=temperatura,
                frecuencia_cardiaca=frecuencia_cardiaca,
                frecuencia_respiratoria=frecuencia_respiratoria,
                frecuencia_sistolica=frecuencia_sistolica,
                frecuencia_diastolica=frecuencia_diastolica
            )
        except Exception as e:
            excepcion_esperada = e
            break


@then("La lista de espera esta ordenada por cuil de la siguiente manera:")
def step_impl(context):
    global servicio_urgencias
    
    # Get the expected CUILs from the table
    cuils_esperados = [row['Cuil'] for row in context.table]
    
    # Get the actual pending entries
    ingresos_pendientes = servicio_urgencias.obtener_ingresos_pendientes()
    cuils_actuales = [ingreso.cuil_paciente for ingreso in ingresos_pendientes]
    
    # Assert the lists match
    assert len(cuils_actuales) == len(cuils_esperados), \
        f"Expected {len(cuils_esperados)} entries, but got {len(cuils_actuales)}"

    for expected, actual in zip(cuils_esperados, cuils_actuales):
        assert expected == actual, f"Expected CUIL {expected}, but got {actual}"
    

@then('el sistema muestra el siguiente error: "{mensaje}"')
def step_impl(context, mensaje: str):
    global excepcion_esperada
    
    assert excepcion_esperada is not None, "Expected an exception but none was raised"
    assert str(excepcion_esperada) == mensaje, \
        f"Expected error message '{mensaje}', but got '{str(excepcion_esperada)}'"