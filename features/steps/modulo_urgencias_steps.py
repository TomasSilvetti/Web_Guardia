from behave import *
from backend.app.models.models import Enfermera, Paciente, NivelEmergencia
from backend.app.services.servicio_emergencias import ServicioEmergencias
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
        cuil = row['Cuil'] if row['Cuil'].strip() else None
        informe = row['Informe'] if row['Informe'].strip() else None
        nivel_emergencia_str = row['Nivel de Emergencia']

        # Convertir campos numéricos solo si no están vacíos
        temperatura_str = row['Temperatura'].strip()
        temperatura = float(temperatura_str) if temperatura_str else None

        frecuencia_cardiaca_str = row['Frecuencia Cardiaca'].strip()
        frecuencia_cardiaca = float(frecuencia_cardiaca_str) if frecuencia_cardiaca_str else None

        frecuencia_respiratoria_str = row['Frecuencia Respiratoria'].strip()
        frecuencia_respiratoria = float(frecuencia_respiratoria_str) if frecuencia_respiratoria_str else None

        tension_arterial_str = row['Tension Arterial'].strip()

        # Leer campos opcionales si están presentes en la tabla
        nombre_valor = row.get('nombre') or row.get('Nombre') or ''
        apellido_valor = row.get('apellido') or row.get('Apellido') or ''
        obra_social_valor = row.get('obra social') or row.get('Obra Social') or ''

        nombre = nombre_valor.strip() if nombre_valor.strip() else None
        apellido = apellido_valor.strip() if apellido_valor.strip() else None
        obra_social = obra_social_valor.strip() if obra_social_valor.strip() else None

        # Parse tension arterial (format: "120/80") solo si no está vacío
        frecuencia_sistolica = None
        frecuencia_diastolica = None
        if tension_arterial_str:
            tension_parts = tension_arterial_str.split('/')
            if len(tension_parts) == 2:
                frecuencia_sistolica = float(tension_parts[0])
                frecuencia_diastolica = float(tension_parts[1])

        # Find the corresponding NivelEmergencia enum solo si no está vacío
        nivel_emergencia = None
        if nivel_emergencia_str.strip():
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
                frecuencia_diastolica=frecuencia_diastolica,
                nombre=nombre,
                apellido=apellido,
                obra_social=obra_social
            )
        except Exception as e:
            excepcion_esperada = e
            break
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

    # Debug print
    print(f"\n[DEBUG] CUILs esperados: {cuils_esperados}")
    print(f"[DEBUG] CUILs actuales: {cuils_actuales}")
    print(f"[DEBUG] Total ingresos pendientes: {len(cuils_actuales)}")

    # Assert the lists match
    assert len(cuils_actuales) == len(cuils_esperados), \
        f"Expected {len(cuils_esperados)} entries, but got {len(cuils_actuales)}. Actual: {cuils_actuales}"

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
    global db_mockeada, servicio_urgencias
    # Asegurar que la base de datos mockeada esté vacía antes del escenario
    if db_mockeada is None:
        db_mockeada = DBPacientes()
    else:
        # limpiar el diccionario interno
        try:
            db_mockeada._pacientes.clear()
        except Exception:
            # si no tiene el atributo, reinstanciamos
            db_mockeada = DBPacientes()

    # Asegurar que el servicio use la misma instancia de DB
    servicio_urgencias = ServicioEmergencias(db_mockeada)


@when("se intenta ingresar a urgencias el siguiente paciente:")
def step_impl(context):
    global enfermera, servicio_urgencias, excepcion_esperada, db_mockeada, mensaje_advertencia, datos_paciente_nuevo

    excepcion_esperada = None
    mensaje_advertencia = None
    datos_paciente_nuevo = None

    row = context.table[0]
    cuil = row['Cuil'] if row['Cuil'].strip() else None
    apellido = row['Apellido'] if row['Apellido'].strip() else None
    nombre = row['Nombre'] if row['Nombre'].strip() else None
    obra_social = row['Obra Social'] if row['Obra Social'].strip() else None
    informe = row['Informe'] if row['Informe'].strip() else None
    nivel_emergencia_str = row['Nivel de Emergencia']

    # Convertir campos numéricos solo si no están vacíos
    temperatura_str = row['Temperatura'].strip()
    temperatura = float(temperatura_str) if temperatura_str else None

    frecuencia_cardiaca_str = row['Frecuencia Cardiaca'].strip()
    frecuencia_cardiaca = float(frecuencia_cardiaca_str) if frecuencia_cardiaca_str else None

    frecuencia_respiratoria_str = row['Frecuencia Respiratoria'].strip()
    frecuencia_respiratoria = float(frecuencia_respiratoria_str) if frecuencia_respiratoria_str else None

    tension_arterial_str = row['Tension Arterial'].strip()

    # Parse tension arterial (formato: "120/80") solo si no está vacío
    frecuencia_sistolica = None
    frecuencia_diastolica = None
    if tension_arterial_str:
        tension_parts = tension_arterial_str.split('/')
        if len(tension_parts) == 2:
            frecuencia_sistolica = float(tension_parts[0])
            frecuencia_diastolica = float(tension_parts[1])

    # Encontrar el correspondiente NivelEmergencia enum solo si no está vacío
    nivel_emergencia = None
    if nivel_emergencia_str.strip():
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


@when("se ingresa a urgencias el siguiente paciente:")
def step_impl(context):
    """Compatibilidad con el wording de la feature: recibir una tabla con un solo paciente y registrarlo."""
    global enfermera, servicio_urgencias, excepcion_esperada

    excepcion_esperada = None

    # Reusar la lógica de parsing (adaptada para una sola fila)
    for row in context.table:
        cuil = row.get('Cuil', '').strip() or None
        informe = row.get('Informe', '').strip() or None
        nivel_emergencia_str = row.get('Nivel de Emergencia', '')

        temperatura = None
        temperatura_str = row.get('Temperatura', '')
        temperatura = float(temperatura_str) if temperatura_str and temperatura_str.strip() else None

        frecuencia_cardiaca = None
        frecuencia_cardiaca_str = row.get('Frecuencia Cardiaca', '')
        frecuencia_cardiaca = float(frecuencia_cardiaca_str) if frecuencia_cardiaca_str and frecuencia_cardiaca_str.strip() else None

        frecuencia_respiratoria = None
        frecuencia_respiratoria_str = row.get('Frecuencia Respiratoria', '')
        frecuencia_respiratoria = float(frecuencia_respiratoria_str) if frecuencia_respiratoria_str and frecuencia_respiratoria_str.strip() else None

        tension_arterial_str = row.get('Tension Arterial', '')
        frecuencia_sistolica = None
        frecuencia_diastolica = None
        if tension_arterial_str and tension_arterial_str.strip():
            parts = tension_arterial_str.split('/')
            if len(parts) == 2:
                frecuencia_sistolica = float(parts[0])
                frecuencia_diastolica = float(parts[1])

        # buscar el enum
        nivel_emergencia = None
        if nivel_emergencia_str and nivel_emergencia_str.strip():
            for nivel in NivelEmergencia:
                if nivel.value['nombre'] == nivel_emergencia_str:
                    nivel_emergencia = nivel
                    break
            if nivel_emergencia is None:
                raise ValueError(f"Nivel de emergencia desconocido: {nivel_emergencia_str}")

        nombre = row.get('Nombre') or row.get('nombre') or None
        apellido = row.get('Apellido') or row.get('apellido') or None
        obra_social = row.get('Obra Social') or row.get('obra social') or None

        # Si no se provee obra social y el paciente no existe, usar un valor por defecto
        try:
            paciente_existente = db_mockeada.obtener_paciente_por_cuil(cuil) if db_mockeada is not None and cuil is not None else None
        except Exception:
            paciente_existente = None

        if obra_social is None and paciente_existente is None:
            obra_social = "OSDE"

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
                frecuencia_diastolica=frecuencia_diastolica,
                nombre=nombre,
                apellido=apellido,
                obra_social=obra_social
            )
        except Exception as e:
            excepcion_esperada = e
            break


@then("La lista de espera esta ordenada por prioridad de emergencia de la siguiente manera:")
def step_impl(context):
    """Verifica que la lista de espera esté ordenada según la prioridad (nivel_emergencia) y hora de llegada."""
    global servicio_urgencias

    cuils_esperados = [row['Cuil'] for row in context.table]

    ingresos_pendientes = servicio_urgencias.obtener_ingresos_pendientes()
    cuils_actuales = [ingreso.cuil_paciente for ingreso in ingresos_pendientes]

    # Debug
    print(f"\n[DEBUG - prioridad] Esperado: {cuils_esperados}")
    print(f"[DEBUG - prioridad] Actual:   {cuils_actuales}")

    assert len(cuils_actuales) == len(cuils_esperados), \
        f"Expected {len(cuils_esperados)} entries, but got {len(cuils_actuales)}. Actual: {cuils_actuales}"

    for expected, actual in zip(cuils_esperados, cuils_actuales):
        assert expected == actual, f"Expected CUIL {expected}, but got {actual}"


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


@then('se muestra un error de validacion indicando que "{campo}" no puede ser negativo')
def step_impl(context, campo: str):
    global excepcion_esperada

    assert excepcion_esperada is not None, \
        f"Se esperaba una excepcion de validacion pero no se lanzo ninguna"

    mensaje_esperado = f"La {campo} no puede ser negativa"
    mensaje_obtenido = str(excepcion_esperada)

    assert mensaje_esperado == mensaje_obtenido, \
        f"Se esperaba el mensaje de error: '{mensaje_esperado}'\nPero se obtuvo: '{mensaje_obtenido}'"


@given("que hay pacientes en espera:")
def step_impl(context):
    """
    Registra pacientes que ya están en la lista de espera de urgencias.
    Este step se utiliza para configurar un estado inicial donde ya hay pacientes esperando atención.
    """
    global enfermera, servicio_urgencias

    # Iterar sobre cada fila de la tabla del contexto
    for row in context.table:
        # Extraer los datos del paciente
        cuil = row['Cuil']
        informe = row['Informe']
        nivel_emergencia_str = row['Nivel de Emergencia']

        # Convertir campos numéricos
        temperatura = float(row['Temperatura'])
        frecuencia_cardiaca = float(row['Frecuencia Cardiaca'])
        frecuencia_respiratoria = float(row['Frecuencia Respiratoria'])

        # Parse tensión arterial (formato: "120/80")
        tension_arterial_str = row['Tension Arterial']
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

        # Extraer nombre/apellido/obra social si están presentes en la tabla
        nombre_row = (row.get('Nombre') or row.get('nombre') or '').strip() or None
        apellido_row = (row.get('Apellido') or row.get('apellido') or '').strip() or None
        obra_social_row = (row.get('Obra Social') or row.get('obra social') or '').strip() or None

        # Si el paciente no existe en la DB mock, crearlo allí para poder registrar el ingreso sin que el servicio tenga que crear al paciente
        try:
            paciente_existente = db_mockeada.obtener_paciente_por_cuil(cuil)
        except Exception:
            paciente_existente = None

        if paciente_existente is None:
            # Si no tenemos obra social en la tabla, usar un valor por defecto para crear el paciente
            obra_social_para_crear = obra_social_row if obra_social_row is not None else "OSDE"
            if nombre_row is None or apellido_row is None:
                # Si faltan nombre/apellido, no podemos crear el paciente; lanzar error claro
                raise ValueError(f"Faltan datos para crear paciente en 'que hay pacientes en espera' para CUIL {cuil}")

            paciente = Paciente(nombre_row, apellido_row, cuil, obra_social_para_crear)
            db_mockeada.guardar_paciente(paciente)

        # Llamar al servicio para registrar la urgencia; pasar nombre/apellido/obra_social como None porque el paciente ya existe
        servicio_urgencias.registrar_urgencia(
            cuil=cuil,
            enfermera=enfermera,
            informe=informe,
            nivel_emergencia=nivel_emergencia,
            temperatura=temperatura,
            frecuencia_cardiaca=frecuencia_cardiaca,
            frecuencia_respiratoria=frecuencia_respiratoria,
            frecuencia_sistolica=frecuencia_sistolica,
            frecuencia_diastolica=frecuencia_diastolica,
            nombre=None,
            apellido=None,
            obra_social=None
        )
@when('se ingresa un paciente "{nombre}" con nivel de emergencia "{nivel_ingreso}"')
def step_impl(context, nombre, nivel_ingreso):
    global servicio_urgencias, enfermera, excepcion_esperada

    excepcion_esperada = None

    row = context.table[0] if hasattr(context, 'table') and context.table else None

    # Extraer CUIL desde la tabla si se pasó, sino generamos un valor ficticio
    cuil = row['Cuil'] if row and 'Cuil' in row else "00-00000000-0"
    apellido = row['Apellido'] if row and 'Apellido' in row else "ApellidoFicticio"
    obra_social = row['Obra Social'] if row and 'Obra Social' in row else "OSDE"
    informe = row['Informe'] if row and 'Informe' in row else "Informe de prueba"

    # Buscar el enum correspondiente al nivel de emergencia
    nivel_emergencia = None
    for nivel in NivelEmergencia:
        if nivel.value['nombre'] == nivel_ingreso:
            nivel_emergencia = nivel
            break
    if nivel_emergencia is None:
        raise ValueError(f"Nivel de emergencia desconocido: {nivel_ingreso}")

    try:
        servicio_urgencias.registrar_urgencia(
            cuil=cuil,
            enfermera=enfermera,
            informe=informe,
            nivel_emergencia=nivel_emergencia,
            temperatura=36.5,
            frecuencia_cardiaca=80,
            frecuencia_respiratoria=18,
            frecuencia_sistolica=120,
            frecuencia_diastolica=80,
            nombre=nombre,
            apellido=apellido,
            obra_social=obra_social
        )
    except Exception as e:
        excepcion_esperada = e


@when('se ingresa a urgencias el siguiente paciente con el mismo nivel de emergencia:')
def step_impl(context):
    """Registrar un paciente (tabla de una fila) que tiene el mismo nivel de emergencia que otro en espera."""
    global servicio_urgencias, enfermera, excepcion_esperada

    excepcion_esperada = None
    # Reusar el paso 'se ingresa a urgencias el siguiente paciente' existente
    for row in context.table:
        # delegar a la implementación ya existente
        cuil = row.get('Cuil', '').strip() or None
        informe = row.get('Informe', '').strip() or None
        nivel_emergencia_str = row.get('Nivel de Emergencia', '')

        temperatura = None
        temperatura_str = row.get('Temperatura', '')
        temperatura = float(temperatura_str) if temperatura_str and temperatura_str.strip() else None

        frecuencia_cardiaca = None
        frecuencia_cardiaca_str = row.get('Frecuencia Cardiaca', '')
        frecuencia_cardiaca = float(frecuencia_cardiaca_str) if frecuencia_cardiaca_str and frecuencia_cardiaca_str.strip() else None

        frecuencia_respiratoria = None
        frecuencia_respiratoria_str = row.get('Frecuencia Respiratoria', '')
        frecuencia_respiratoria = float(frecuencia_respiratoria_str) if frecuencia_respiratoria_str and frecuencia_respiratoria_str.strip() else None

        tension_arterial_str = row.get('Tension Arterial', '')
        frecuencia_sistolica = None
        frecuencia_diastolica = None
        if tension_arterial_str and tension_arterial_str.strip():
            parts = tension_arterial_str.split('/')
            if len(parts) == 2:
                frecuencia_sistolica = float(parts[0])
                frecuencia_diastolica = float(parts[1])

        # buscar el enum
        nivel_emergencia = None
        if nivel_emergencia_str and nivel_emergencia_str.strip():
            for nivel in NivelEmergencia:
                if nivel.value['nombre'] == nivel_emergencia_str:
                    nivel_emergencia = nivel
                    break
            if nivel_emergencia is None:
                raise ValueError(f"Nivel de emergencia desconocido: {nivel_emergencia_str}")

        nombre = row.get('Nombre') or row.get('nombre') or None
        apellido = row.get('Apellido') or row.get('apellido') or None
        obra_social = row.get('Obra Social') or row.get('obra social') or None

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
                frecuencia_diastolica=frecuencia_diastolica,
                nombre=nombre,
                apellido=apellido,
                obra_social=obra_social
            )
            print(f"\n[DEBUG after register] ingreso.id={ingreso.id}, mensaje={mensaje}")
            print(f"[DEBUG after register] pending={[ing.cuil_paciente for ing in servicio_urgencias.obtener_ingresos_pendientes()]}")
        except Exception as e:
            excepcion_esperada = e
            print(f"\n[DEBUG register failed] error={str(e)}")
            raise  # Re-lanzar para que behave muestre el error real
            break  # (unreachable after raise)


@then('La lista de espera queda ordenada por prioridad de llegada de la siguiente manera:')
def step_impl(context):
    """Verifica que la lista de espera con igual nivel de emergencia esté ordenada por fecha de ingreso (FIFO)."""
    global servicio_urgencias

    cuils_esperados = [row['Cuil'] for row in context.table]

    ingresos_pendientes = servicio_urgencias.obtener_ingresos_pendientes()
    cuils_actuales = [ingreso.cuil_paciente for ingreso in ingresos_pendientes]

    # Filtrar sólo los ingresos que aparecen en la tabla esperada (manteniendo su orden actual)
    cuils_actuales_filtrados = [c for c in cuils_actuales if c in cuils_esperados]

    # Debug
    print(f"\n[DEBUG - llegada] Esperado: {cuils_esperados}")
    print(f"[DEBUG - llegada] Actual filtered: {cuils_actuales_filtrados}")

    assert len(cuils_actuales_filtrados) >= len(cuils_esperados), \
        f"Expected at least {len(cuils_esperados)} matching entries, but got {len(cuils_actuales_filtrados)}. Actual: {cuils_actuales_filtrados}"

    # Comprobar que los CUILs esperados están en el mismo orden relativo en la lista actual
    idx = 0
    for expected in cuils_esperados:
        try:
            pos = cuils_actuales_filtrados.index(expected)
        except ValueError:
            raise AssertionError(f"Expected CUIL {expected} not found in actual pending list")
        # ensure ordering: previous expected should be before current
        if pos < idx:
            raise AssertionError(f"Expected CUIL order violated: {cuils_esperados}")
        idx = pos + 1

@then("La lista de espera debe mantener al paciente B antes que el paciente A, aun cuando ambos tengan el mismo nivel de emergencia:")
def step_impl(context):
    global servicio_urgencias

    # Obtener los CUILs esperados de la tabla
    cuils_esperados = [row['Cuil'] for row in context.table]

    # Obtener los ingresos pendientes ordenados por prioridad de emergencia y llegada
    ingresos_pendientes = servicio_urgencias.obtener_ingresos_pendientes()
    cuils_actuales = [ingreso.cuil_paciente for ingreso in ingresos_pendientes]

    # Debug
    print(f"[DEBUG] CUILs esperados: {cuils_esperados}")
    print(f"[DEBUG] CUILs actuales: {cuils_actuales}")

    # Verificar que la lista actual respete el orden esperado
    assert cuils_actuales[:len(cuils_esperados)] == cuils_esperados, (
        f"Se esperaba el orden {cuils_esperados} pero se obtuvo {cuils_actuales}"
    )
