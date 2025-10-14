from behave import *
from backend.app.models.models import Enfermera, Paciente, NivelEmergencia
from backend.app.services.servicio_emergencias import ServicioEmergencias
from backend.app.interfaces.pacientes_repo import PacientesRepo
from backend.app.test.mocks import DBPacientes


enfermera: Enfermera | None = None
db_mockeada: PacientesRepo | None = None
servicio_urgencias: ServicioEmergencias | None = None
excepcion_esperada = None
mensaje_advertencia: str | None = None
datos_paciente_nuevo: dict | None = None


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
            ingreso, mensaje = servicio_urgencias.registrar_urgencia(
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


@then('el ingreso del paciente con cuil "{cuil}" queda registrado con estado "{estado}"')
def step_impl(context, cuil: str, estado: str):
    global servicio_urgencias

    # Get the patient's ingreso
    ingresos_pendientes = servicio_urgencias.obtener_ingresos_pendientes()

    # Find the ingreso for the specified CUIL
    ingreso_encontrado = None
    for ingreso in ingresos_pendientes:
        if ingreso.cuil_paciente == cuil:
            ingreso_encontrado = ingreso
            break

    assert ingreso_encontrado is not None, \
        f"No se encontro ningun ingreso para el paciente con CUIL {cuil}"

    assert ingreso_encontrado.estado == estado, \
        f"Expected estado '{estado}', but got '{ingreso_encontrado.estado}'"


@then('el sistema muestra el siguiente error: "{mensaje}"')
def step_impl(context, mensaje: str):
    global excepcion_esperada

    assert excepcion_esperada is not None, "Expected an exception but none was raised"
    assert str(excepcion_esperada) == mensaje, \
        f"Expected error message '{mensaje}', but got '{str(excepcion_esperada)}'"


@given("que no hay pacientes registrados en el sistema")
def step_impl(context):
    global db_mockeada
    # La base de datos va a estar vacia
    pass


@when("se intenta ingresar a urgencias el siguiente paciente:")
def step_impl(context):
    global enfermera, servicio_urgencias, excepcion_esperada, db_mockeada, mensaje_advertencia, datos_paciente_nuevo

    excepcion_esperada = None
    mensaje_advertencia = None
    datos_paciente_nuevo = None

    row = context.table[0]
    cuil = row['Cuil']
    apellido = row['Apellido']
    nombre = row['Nombre']
    obra_social = row['Obra Social']
    informe = row['Informe']
    nivel_emergencia_str = row['Nivel de Emergencia']
    temperatura = float(row['Temperatura'])
    frecuencia_cardiaca = float(row['Frecuencia Cardiaca'])
    frecuencia_respiratoria = float(row['Frecuencia Respiratoria'])
    tension_arterial_str = row['Tension Arterial']

    # Parse tension arterial (formato: "120/80")
    tension_parts = tension_arterial_str.split('/')
    frecuencia_sistolica = float(tension_parts[0])
    frecuencia_diastolica = float(tension_parts[1])

    # Encontrar el correspondiente NivelEmergencia enum
    nivel_emergencia = None
    for nivel in NivelEmergencia:
        if nivel.value['nombre'] == nivel_emergencia_str:
            nivel_emergencia = nivel
            break

    if nivel_emergencia is None:
        raise ValueError(f"Nivel de emergencia desconocido: {nivel_emergencia_str}")

    try:
        # Guardar los datos del paciente para verificación posterior
        datos_paciente_nuevo = {
            'nombre': nombre,
            'apellido': apellido,
            'cuil': cuil,
            'obra_social': obra_social
        }

        # Registrar la urgencia usando el servicio (que ahora maneja la creación del paciente)
        ingreso, mensaje_advertencia = servicio_urgencias.registrar_urgencia(
            cuil=cuil,
            enfermera=enfermera,
            informe=informe,
            nivel_emergencia=nivel_emergencia,
            temperatura=temperatura,
            frecuencia_cardiaca=frecuencia_cardiaca,
            frecuencia_respiratoria=frecuencia_respiratoria,
            frecuencia_sistolica=frecuencia_sistolica,
            frecuencia_diastolica=frecuencia_diastolica,
            nombre=nombre,
            apellido=apellido,
            obra_social=obra_social
        )
    except Exception as e:
        excepcion_esperada = e


@then("se muestra un mensaje de error indicando que el paciente no existe y que se debe registrar antes de proceder al ingreso")
def step_impl(context):
    global mensaje_advertencia

    assert mensaje_advertencia is not None, \
        "No se genero ningun mensaje de advertencia"

    assert "no existe" in mensaje_advertencia.lower(), \
        f"El mensaje de advertencia no indica que el paciente no existe: {mensaje_advertencia}"

    assert "registrar" in mensaje_advertencia.lower() or "registrado" in mensaje_advertencia.lower(), \
        f"El mensaje de advertencia no indica que se debe registrar al paciente: {mensaje_advertencia}"


@then('el paciente con cuil "{cuil}" es creado en el sistema con los datos del ingreso')
def step_impl(context, cuil: str):
    global db_mockeada, datos_paciente_nuevo

    # Verificar que el paciente existe en la base de datos
    paciente = db_mockeada.obtener_paciente_por_cuil(cuil)

    assert paciente is not None, \
        f"El paciente con CUIL {cuil} no fue creado en el sistema"

    assert paciente.cuil == cuil, \
        f"Esperado CUIL {cuil}, pero se obtuvo {paciente.cuil}"

    # Verificar que el paciente fue creado con los datos del ingreso
    if datos_paciente_nuevo is not None:
        assert paciente.nombre == datos_paciente_nuevo['nombre'], \
            f"Esperado nombre {datos_paciente_nuevo['nombre']}, pero se obtuvo {paciente.nombre}"

        assert paciente.apellido == datos_paciente_nuevo['apellido'], \
            f"Esperado apellido {datos_paciente_nuevo['apellido']}, pero se obtuvo {paciente.apellido}"

        assert paciente.obra_social.nombre == datos_paciente_nuevo['obra_social'], \
            f"Esperado obra social {datos_paciente_nuevo['obra_social']}, pero se obtuvo {paciente.obra_social.nombre}"
