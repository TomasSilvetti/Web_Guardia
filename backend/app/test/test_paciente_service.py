import unittest
from ..services.paciente_service import registrar_paciente, InMemoryPacienteRepo
from ..models.models import Domicilio, ObraSocial, Afiliado
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


class TestPacienteService(unittest.TestCase):

    def setUp(self):
        self.repo = InMemoryPacienteRepo()

    def test_registro_exitoso_con_obra_social(self):
        logger.info("\n=== TEST: test_registro_exitoso_con_obra_social ===")
        logger.info("PASO 1: Registrar obra social en el sistema")
        
        obra_social = ObraSocial("OSDE")
        self.repo.registrar_obra_social(obra_social)
        logger.info(f"  - Obra social registrada: '{obra_social.nombre}'")
        
        logger.info("\nPASO 2: Registrar afiliación del paciente")
        cuil = "20-12345678-9"
        self.repo.registrar_afiliacion(cuil, "OSDE")
        logger.info(f"  - CUIL: '{cuil}'")
        logger.info(f"  - Afiliado a: 'OSDE'")
        
        logger.info("\nPASO 3: Crear datos del paciente")
        logger.info("DATOS DE ENTRADA:")
        logger.info(f"  - CUIL: '{cuil}'")
        logger.info(f"  - Apellido: 'González'")
        logger.info(f"  - Nombre: 'Juan'")
        logger.info(f"  - Domicilio:")
        logger.info(f"    - Calle: 'San Martín'")
        logger.info(f"    - Número: 123")
        logger.info(f"    - Localidad: 'San Miguel de Tucumán'")
        logger.info(f"    - Ciudad: 'San Miguel de Tucumán'")
        logger.info(f"    - Provincia: 'Tucumán'")
        logger.info(f"    - País: 'Argentina'")
        logger.info(f"  - Obra Social: 'OSDE'")
        logger.info(f"  - Número de Afiliado: '123456'")

        domicilio = Domicilio(
            calle="San Martín",
            numero=123,
            localidad="San Miguel de Tucumán",
            ciudad="San Miguel de Tucumán",
            provincia="Tucumán",
            pais="Argentina"
        )
        
        afiliado = Afiliado(obra_social=obra_social, numero_afiliado="123456")
        
        logger.info("\nPASO 4: Registrar paciente")
        paciente = registrar_paciente(
            cuil=cuil,
            apellido="González",
            nombre="Juan",
            domicilio=domicilio,
            afiliado=afiliado,
            repo=self.repo
        )

        logger.info("DATOS OBTENIDOS DEL RETORNO:")
        logger.info(f"  - CUIL: '{paciente.cuil}'")
        logger.info(f"  - Apellido: '{paciente.apellido}'")
        logger.info(f"  - Nombre: '{paciente.nombre}'")
        logger.info(f"  - Domicilio.Calle: '{paciente.domicilio.calle}'")
        logger.info(f"  - Domicilio.Localidad: '{paciente.domicilio.localidad}'")
        logger.info(f"  - Afiliado.ObraSocial: '{paciente.afiliado.obra_social.nombre}'")
        logger.info(f"  - Afiliado.NumeroAfiliado: '{paciente.afiliado.numero_afiliado}'")

        logger.info("ASSERTS:")
        logger.info(f"  - CUIL esperado: '{cuil}'")
        logger.info(f"  - CUIL actual: '{paciente.cuil}'")
        logger.info(f"  - Apellido esperado: 'González'")
        logger.info(f"  - Apellido actual: '{paciente.apellido}'")
        logger.info(f"  - Nombre esperado: 'Juan'")
        logger.info(f"  - Nombre actual: '{paciente.nombre}'")

        self.assertEqual(paciente.cuil, cuil)
        self.assertEqual(paciente.apellido, "González")
        self.assertEqual(paciente.nombre, "Juan")
        self.assertEqual(paciente.domicilio.calle, "San Martín")
        self.assertEqual(paciente.domicilio.localidad, "San Miguel de Tucumán")
        self.assertEqual(paciente.afiliado.obra_social.nombre, "OSDE")
        logger.info("✓ Asserts pasados correctamente\n")

    def test_registro_exitoso_sin_obra_social(self):
        logger.info("\n=== TEST: test_registro_exitoso_sin_obra_social ===")
        logger.info("DATOS DE ENTRADA:")
        cuil = "27-98765432-1"
        logger.info(f"  - CUIL: '{cuil}'")
        logger.info(f"  - Apellido: 'Pérez'")
        logger.info(f"  - Nombre: 'María'")
        logger.info(f"  - Domicilio:")
        logger.info(f"    - Calle: 'Avenida Mate de Luna'")
        logger.info(f"    - Número: 456")
        logger.info(f"    - Localidad: 'Yerba Buena'")
        logger.info(f"    - Ciudad: 'Yerba Buena'")
        logger.info(f"    - Provincia: 'Tucumán'")
        logger.info(f"    - País: 'Argentina'")
        logger.info(f"  - Obra Social: None")

        domicilio = Domicilio(
            calle="Avenida Mate de Luna",
            numero=456,
            localidad="Yerba Buena",
            ciudad="Yerba Buena",
            provincia="Tucumán",
            pais="Argentina"
        )

        paciente = registrar_paciente(
            cuil=cuil,
            apellido="Pérez",
            nombre="María",
            domicilio=domicilio,
            afiliado=None,
            repo=self.repo
        )

        logger.info("DATOS OBTENIDOS DEL RETORNO:")
        logger.info(f"  - CUIL: '{paciente.cuil}'")
        logger.info(f"  - Apellido: '{paciente.apellido}'")
        logger.info(f"  - Nombre: '{paciente.nombre}'")
        logger.info(f"  - Afiliado: {paciente.afiliado}")

        logger.info("ASSERTS:")
        self.assertEqual(paciente.cuil, cuil)
        self.assertEqual(paciente.apellido, "Pérez")
        self.assertEqual(paciente.nombre, "María")
        self.assertIsNone(paciente.afiliado)
        logger.info("✓ Asserts pasados correctamente\n")

    def test_registro_obra_social_inexistente(self):
        logger.info("\n=== TEST: test_registro_obra_social_inexistente ===")
        logger.info("PASO 1: NO registrar obra social en el sistema")
        logger.info("  - La obra social 'Swiss Medical' NO existe en el sistema")
        
        logger.info("\nPASO 2: Intentar registrar paciente con obra social inexistente")
        logger.info("DATOS DE ENTRADA:")
        cuil = "20-11111111-1"
        logger.info(f"  - CUIL: '{cuil}'")
        logger.info(f"  - Apellido: 'López'")
        logger.info(f"  - Nombre: 'Carlos'")
        logger.info(f"  - Obra Social: 'Swiss Medical' (NO EXISTE)")

        domicilio = Domicilio(
            calle="Calle Falsa",
            numero=123,
            localidad="San Miguel de Tucumán",
            ciudad="San Miguel de Tucumán",
            provincia="Tucumán",
            pais="Argentina"
        )

        obra_social_inexistente = ObraSocial("Swiss Medical")
        afiliado = Afiliado(obra_social=obra_social_inexistente, numero_afiliado="999999")

        logger.info("ASSERT: Se espera que se lance ValueError")
        logger.info("Mensaje esperado: 'No se puede registrar al paciente con una obra social inexistente'")

        with self.assertRaises(ValueError) as context:
            registrar_paciente(
                cuil=cuil,
                apellido="López",
                nombre="Carlos",
                domicilio=domicilio,
                afiliado=afiliado,
                repo=self.repo
            )
        
        logger.info(f"✓ Excepción lanzada correctamente")
        logger.info(f"  - Mensaje recibido: '{str(context.exception)}'")
        self.assertEqual(str(context.exception), "No se puede registrar al paciente con una obra social inexistente")
        logger.info("✓ Mensaje de error coincide con el esperado\n")

    def test_registro_no_afiliado(self):
        logger.info("\n=== TEST: test_registro_no_afiliado ===")
        logger.info("PASO 1: Registrar obra social en el sistema")
        
        obra_social = ObraSocial("OSDE")
        self.repo.registrar_obra_social(obra_social)
        logger.info(f"  - Obra social registrada: '{obra_social.nombre}'")
        
        logger.info("\nPASO 2: NO registrar afiliación del paciente")
        cuil = "20-22222222-2"
        logger.info(f"  - CUIL: '{cuil}' NO está afiliado a OSDE")
        
        logger.info("\nPASO 3: Intentar registrar paciente sin estar afiliado")
        logger.info("DATOS DE ENTRADA:")
        logger.info(f"  - CUIL: '{cuil}'")
        logger.info(f"  - Apellido: 'Fernández'")
        logger.info(f"  - Nombre: 'Ana'")
        logger.info(f"  - Obra Social: 'OSDE' (existe pero paciente NO afiliado)")

        domicilio = Domicilio(
            calle="Calle Real",
            numero=789,
            localidad="San Miguel de Tucumán",
            ciudad="San Miguel de Tucumán",
            provincia="Tucumán",
            pais="Argentina"
        )

        afiliado = Afiliado(obra_social=obra_social, numero_afiliado="888888")

        logger.info("ASSERT: Se espera que se lance ValueError")
        logger.info("Mensaje esperado: 'No se puede registrar el paciente dado que no está afiliado a la obra social'")

        with self.assertRaises(ValueError) as context:
            registrar_paciente(
                cuil=cuil,
                apellido="Fernández",
                nombre="Ana",
                domicilio=domicilio,
                afiliado=afiliado,
                repo=self.repo
            )
        
        logger.info(f"✓ Excepción lanzada correctamente")
        logger.info(f"  - Mensaje recibido: '{str(context.exception)}'")
        self.assertEqual(str(context.exception), "No se puede registrar el paciente dado que no está afiliado a la obra social")
        logger.info("✓ Mensaje de error coincide con el esperado\n")

    def test_registro_campo_mandatorio_omitido_cuil(self):
        logger.info("\n=== TEST: test_registro_campo_mandatorio_omitido_cuil ===")
        logger.info("DATOS DE ENTRADA:")
        logger.info(f"  - CUIL: None (OMITIDO)")
        logger.info(f"  - Apellido: 'Gómez'")
        logger.info(f"  - Nombre: 'Pedro'")

        domicilio = Domicilio(
            calle="Calle Test",
            numero=100,
            localidad="San Miguel de Tucumán",
            ciudad="San Miguel de Tucumán",
            provincia="Tucumán",
            pais="Argentina"
        )

        logger.info("ASSERT: Se espera que se lance ValueError")
        logger.info("Mensaje esperado: \"El campo 'cuil' es obligatorio\"")

        with self.assertRaises(ValueError) as context:
            registrar_paciente(
                cuil=None,
                apellido="Gómez",
                nombre="Pedro",
                domicilio=domicilio,
                afiliado=None,
                repo=self.repo
            )
        
        logger.info(f"✓ Excepción lanzada correctamente")
        logger.info(f"  - Mensaje recibido: '{str(context.exception)}'")
        self.assertIn("cuil", str(context.exception).lower())
        logger.info("✓ Mensaje de error menciona el campo omitido\n")

    def test_registro_campo_mandatorio_omitido_apellido(self):
        logger.info("\n=== TEST: test_registro_campo_mandatorio_omitido_apellido ===")
        logger.info("DATOS DE ENTRADA:")
        logger.info(f"  - CUIL: '20-33333333-3'")
        logger.info(f"  - Apellido: None (OMITIDO)")
        logger.info(f"  - Nombre: 'Luis'")

        domicilio = Domicilio(
            calle="Calle Test",
            numero=100,
            localidad="San Miguel de Tucumán",
            ciudad="San Miguel de Tucumán",
            provincia="Tucumán",
            pais="Argentina"
        )

        logger.info("ASSERT: Se espera que se lance ValueError")
        logger.info("Mensaje esperado: \"El campo 'apellido' es obligatorio\"")

        with self.assertRaises(ValueError) as context:
            registrar_paciente(
                cuil="20-33333333-3",
                apellido=None,
                nombre="Luis",
                domicilio=domicilio,
                afiliado=None,
                repo=self.repo
            )
        
        logger.info(f"✓ Excepción lanzada correctamente")
        logger.info(f"  - Mensaje recibido: '{str(context.exception)}'")
        self.assertIn("apellido", str(context.exception).lower())
        logger.info("✓ Mensaje de error menciona el campo omitido\n")

    def test_registro_campo_mandatorio_omitido_nombre(self):
        logger.info("\n=== TEST: test_registro_campo_mandatorio_omitido_nombre ===")
        logger.info("DATOS DE ENTRADA:")
        logger.info(f"  - CUIL: '20-44444444-4'")
        logger.info(f"  - Apellido: 'Rodríguez'")
        logger.info(f"  - Nombre: None (OMITIDO)")

        domicilio = Domicilio(
            calle="Calle Test",
            numero=100,
            localidad="San Miguel de Tucumán",
            ciudad="San Miguel de Tucumán",
            provincia="Tucumán",
            pais="Argentina"
        )

        logger.info("ASSERT: Se espera que se lance ValueError")
        logger.info("Mensaje esperado: \"El campo 'nombre' es obligatorio\"")

        with self.assertRaises(ValueError) as context:
            registrar_paciente(
                cuil="20-44444444-4",
                apellido="Rodríguez",
                nombre=None,
                domicilio=domicilio,
                afiliado=None,
                repo=self.repo
            )
        
        logger.info(f"✓ Excepción lanzada correctamente")
        logger.info(f"  - Mensaje recibido: '{str(context.exception)}'")
        self.assertIn("nombre", str(context.exception).lower())
        logger.info("✓ Mensaje de error menciona el campo omitido\n")

    def test_registro_campo_mandatorio_omitido_domicilio(self):
        logger.info("\n=== TEST: test_registro_campo_mandatorio_omitido_domicilio ===")
        logger.info("DATOS DE ENTRADA:")
        logger.info(f"  - CUIL: '20-55555555-5'")
        logger.info(f"  - Apellido: 'Martínez'")
        logger.info(f"  - Nombre: 'Laura'")
        logger.info(f"  - Domicilio: None (OMITIDO)")

        logger.info("ASSERT: Se espera que se lance ValueError")
        logger.info("Mensaje esperado: \"El campo 'domicilio' es obligatorio\"")

        with self.assertRaises(ValueError) as context:
            registrar_paciente(
                cuil="20-55555555-5",
                apellido="Martínez",
                nombre="Laura",
                domicilio=None,
                afiliado=None,
                repo=self.repo
            )
        
        logger.info(f"✓ Excepción lanzada correctamente")
        logger.info(f"  - Mensaje recibido: '{str(context.exception)}'")
        self.assertIn("domicilio", str(context.exception).lower())
        logger.info("✓ Mensaje de error menciona el campo omitido\n")

    def test_registro_campo_mandatorio_omitido_domicilio_calle(self):
        logger.info("\n=== TEST: test_registro_campo_mandatorio_omitido_domicilio_calle ===")
        logger.info("DATOS DE ENTRADA:")
        logger.info(f"  - CUIL: '20-66666666-6'")
        logger.info(f"  - Domicilio.Calle: None (OMITIDO)")

        domicilio = Domicilio(
            calle=None,
            numero=100,
            localidad="San Miguel de Tucumán",
            ciudad="San Miguel de Tucumán",
            provincia="Tucumán",
            pais="Argentina"
        )

        logger.info("ASSERT: Se espera que se lance ValueError")
        logger.info("Mensaje esperado: \"El campo 'domicilio.calle' es obligatorio\"")

        with self.assertRaises(ValueError) as context:
            registrar_paciente(
                cuil="20-66666666-6",
                apellido="Sánchez",
                nombre="Diego",
                domicilio=domicilio,
                afiliado=None,
                repo=self.repo
            )
        
        logger.info(f"✓ Excepción lanzada correctamente")
        logger.info(f"  - Mensaje recibido: '{str(context.exception)}'")
        self.assertIn("calle", str(context.exception).lower())
        logger.info("✓ Mensaje de error menciona el campo omitido\n")

    def test_registro_campo_mandatorio_omitido_domicilio_numero(self):
        logger.info("\n=== TEST: test_registro_campo_mandatorio_omitido_domicilio_numero ===")
        logger.info("DATOS DE ENTRADA:")
        logger.info(f"  - CUIL: '20-77777777-7'")
        logger.info(f"  - Domicilio.Numero: None (OMITIDO)")

        domicilio = Domicilio(
            calle="Calle Test",
            numero=None,
            localidad="San Miguel de Tucumán",
            ciudad="San Miguel de Tucumán",
            provincia="Tucumán",
            pais="Argentina"
        )

        logger.info("ASSERT: Se espera que se lance ValueError")
        logger.info("Mensaje esperado: \"El campo 'domicilio.numero' es obligatorio\"")

        with self.assertRaises(ValueError) as context:
            registrar_paciente(
                cuil="20-77777777-7",
                apellido="Torres",
                nombre="Sofía",
                domicilio=domicilio,
                afiliado=None,
                repo=self.repo
            )
        
        logger.info(f"✓ Excepción lanzada correctamente")
        logger.info(f"  - Mensaje recibido: '{str(context.exception)}'")
        self.assertIn("numero", str(context.exception).lower())
        logger.info("✓ Mensaje de error menciona el campo omitido\n")

    def test_registro_campo_mandatorio_omitido_domicilio_localidad(self):
        logger.info("\n=== TEST: test_registro_campo_mandatorio_omitido_domicilio_localidad ===")
        logger.info("DATOS DE ENTRADA:")
        logger.info(f"  - CUIL: '20-88888888-8'")
        logger.info(f"  - Domicilio.Localidad: None (OMITIDO)")

        domicilio = Domicilio(
            calle="Calle Test",
            numero=100,
            localidad=None,
            ciudad="San Miguel de Tucumán",
            provincia="Tucumán",
            pais="Argentina"
        )

        logger.info("ASSERT: Se espera que se lance ValueError")
        logger.info("Mensaje esperado: \"El campo 'domicilio.localidad' es obligatorio\"")

        with self.assertRaises(ValueError) as context:
            registrar_paciente(
                cuil="20-88888888-8",
                apellido="Ramírez",
                nombre="Martín",
                domicilio=domicilio,
                afiliado=None,
                repo=self.repo
            )
        
        logger.info(f"✓ Excepción lanzada correctamente")
        logger.info(f"  - Mensaje recibido: '{str(context.exception)}'")
        self.assertIn("localidad", str(context.exception).lower())
        logger.info("✓ Mensaje de error menciona el campo omitido\n")

    def test_registro_cuil_formato_invalido(self):
        logger.info("\n=== TEST: test_registro_cuil_formato_invalido ===")
        logger.info("DATOS DE ENTRADA:")
        logger.info(f"  - CUIL: '123' (FORMATO INVÁLIDO)")
        logger.info(f"  - Apellido: 'Díaz'")
        logger.info(f"  - Nombre: 'Roberto'")

        domicilio = Domicilio(
            calle="Calle Test",
            numero=100,
            localidad="San Miguel de Tucumán",
            ciudad="San Miguel de Tucumán",
            provincia="Tucumán",
            pais="Argentina"
        )

        logger.info("ASSERT: Se espera que se lance ValueError")
        logger.info("Mensaje esperado: 'El CUIL debe tener el formato XX-XXXXXXXX-X (11 dígitos)'")

        with self.assertRaises(ValueError) as context:
            registrar_paciente(
                cuil="123",
                apellido="Díaz",
                nombre="Roberto",
                domicilio=domicilio,
                afiliado=None,
                repo=self.repo
            )
        
        logger.info(f"✓ Excepción lanzada correctamente")
        logger.info(f"  - Mensaje recibido: '{str(context.exception)}'")
        self.assertIn("formato", str(context.exception).lower())
        logger.info("✓ Mensaje de error menciona formato inválido\n")


if __name__ == '__main__':
    unittest.main()

