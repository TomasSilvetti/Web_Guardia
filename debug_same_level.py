from backend.app.test.mocks import DBPacientes
from backend.app.services.servicio_emergencias import ServicioEmergencias
from backend.app.models.models import Enfermera, Paciente, NivelEmergencia

# Setup
print('Setting up DB and service')
db = DBPacientes()
serv = ServicioEmergencias(db)
enf = Enfermera('Maria','Lopez')

# Patient A in waiting (already exists)
cuil_a = '20-12345678-9'
p_a = Paciente('Juan','Gonzalez', cuil_a, 'OSDE')
db.guardar_paciente(p_a)
# Register ingreso A (Emergencia)
nivel_em = None
for n in NivelEmergencia:
    if n.value['nombre'] == 'Emergencia':
        nivel_em = n
        break
print('Registering ingreso A')
try:
    ingreso_a, _ = serv.registrar_urgencia(cuil=cuil_a, enfermera=enf, informe='Dolor leve tobillo', nivel_emergencia=nivel_em, temperatura=36.5, frecuencia_cardiaca=75, frecuencia_respiratoria=16, frecuencia_sistolica=120, frecuencia_diastolica=80, nombre=None, apellido=None, obra_social=None)
    print('Ingreso A id:', ingreso_a.id)
except Exception as e:
    print('Ingreso A exception:', e)

# Patient B incoming with same level
cuil_b = '27-98765432-1'
print('Registering ingreso B (same level)')
try:
    ingreso_b, msg = serv.registrar_urgencia(cuil=cuil_b, enfermera=enf, informe='Dolor toracico', nivel_emergencia=nivel_em, temperatura=36.5, frecuencia_cardiaca=80, frecuencia_respiratoria=18, frecuencia_sistolica=120, frecuencia_diastolica=80, nombre='Sofia', apellido='Martinez', obra_social='Swiss Medical')
    print('Ingreso B id:', ingreso_b.id, 'msg:', msg)
except Exception as e:
    print('Ingreso B exception:', e)

# Print pending ingresos
print('Pending ingresos CUILs:', [ing.cuil_paciente for ing in serv.obtener_ingresos_pendientes()])
for ing in serv.obtener_ingresos_pendientes():
    print(' -', ing.cuil_paciente, ing.nivel_emergencia.value['nombre'], ing.fecha_ingreso)
