from backend.app.test.mocks import DBPacientes
from backend.app.services.servicio_emergencias import ServicioEmergencias
from backend.app.models.models import Enfermera, NivelEmergencia

# Setup
db = DBPacientes()
serv = ServicioEmergencias(db)
enf = Enfermera('Maria','Lopez')

# Add patient in waiting: 20-12345678-9 (Urgencia)
cuil1 = '20-12345678-9'
# create patient
from backend.app.models.models import Paciente
p1 = Paciente('Juan','Gonzalez', cuil1, 'OSDE')
db.guardar_paciente(p1)
# register ingreso for p1
nivel1 = None
for n in NivelEmergencia:
    if n.value['nombre'] == 'Urgencia':
        nivel1 = n
        break
serv.registrar_urgencia(cuil=cuil1, enfermera=enf, informe='Dolor leve tobillo', nivel_emergencia=nivel1, temperatura=36.5, frecuencia_cardiaca=75, frecuencia_respiratoria=16, frecuencia_sistolica=120, frecuencia_diastolica=80, nombre=None, apellido=None, obra_social=None)

# Now try to register new patient 27-98765432-1 with Emergencia
cuil2 = '27-98765432-1'
# Ensure patient 27 exists? Comment out to simulate not existing
# p2 = Paciente('Sofia','Martinez', cuil2, 'Swiss Medical')
# db.guardar_paciente(p2)

nivel2 = None
for n in NivelEmergencia:
    if n.value['nombre'] == 'Emergencia':
        nivel2 = n
        break

try:
    serv.registrar_urgencia(cuil=cuil2, enfermera=enf, informe='Dolor toracico', nivel_emergencia=nivel2, temperatura=36.5, frecuencia_cardiaca=80, frecuencia_respiratoria=18, frecuencia_sistolica=120, frecuencia_diastolica=80, nombre='Sofia', apellido='Martinez', obra_social=None)
    print('Registro OK')
except Exception as e:
    print('Registro raised:', e)

# Print pending cuils
print('Ingresos pendientes:', [ing.cuil_paciente for ing in serv.obtener_ingresos_pendientes()])
