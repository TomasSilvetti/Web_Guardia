import unittest
from unittest.mock import Mock
from ..services.paciente_service import registrar_paciente
from ..models.models import Domicilio, ObraSocial, Afiliado
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


class TestPacienteService(unittest.TestCase):

    def setUp(self):
        # Crear mock del repositorio para aislar la unidad bajo prueba
        self.repo = Mock()

    def test_registro_exitoso_con_obra_social(self):
        logger.info("TEST: test_registro_exitoso_con_obra_social - Registrar paciente con obra social válida")
        
        # Arrange: configurar datos y mocks
        cuil = "20-12345678-9"
        obra_social = ObraSocial("OSDE")
        domicilio = Domicilio(
            calle="San Martín",
            numero=123,
            localidad="San Miguel de Tucumán",
            ciudad="San Miguel de Tucumán",
            provincia="Tucumán",
            pais="Argentina"
        )
        afiliado = Afiliado(obra_social=obra_social, numero_afiliado="123456")
        
        # Configurar comportamiento del mock
        self.repo.existe_obra_social.return_value = True
        self.repo.esta_afiliado.return_value = True
        self.repo.get.return_value = None  # Paciente no existe previamente
        
        # Act: ejecutar la función bajo prueba
        paciente = registrar_paciente(
            cuil=cuil,
            apellido="González",
            nombre="Juan",
            domicilio=domicilio,
            afiliado=afiliado,
            repo=self.repo
        )

        # Assert: verificar resultados
        self.assertEqual(paciente.cuil, cuil)
        self.assertEqual(paciente.apellido, "González")
        self.assertEqual(paciente.nombre, "Juan")
        self.assertEqual(paciente.domicilio.calle, "San Martín")
        self.assertEqual(paciente.domicilio.localidad, "San Miguel de Tucumán")
        self.assertEqual(paciente.afiliado.obra_social.nombre, "OSDE")
        
        # Verificar interacciones con el repositorio
        self.repo.existe_obra_social.assert_called_once_with("OSDE")
        self.repo.esta_afiliado.assert_called_once_with(cuil, "OSDE")
        self.repo.get.assert_called_once_with(cuil)
        self.repo.save.assert_called_once()
        
        logger.info("✓ Test completado exitosamente")

    def test_registro_exitoso_sin_obra_social(self):
        logger.info("TEST: test_registro_exitoso_sin_obra_social - Registrar paciente sin obra social")
        
        # Arrange: configurar datos y mocks
        cuil = "27-98765432-1"
        domicilio = Domicilio(
            calle="Avenida Mate de Luna",
            numero=456,
            localidad="Yerba Buena",
            ciudad="Yerba Buena",
            provincia="Tucumán",
            pais="Argentina"
        )
        
        # Configurar comportamiento del mock
        self.repo.get.return_value = None  # Paciente no existe previamente

        # Act: ejecutar la función bajo prueba
        paciente = registrar_paciente(
            cuil=cuil,
            apellido="Pérez",
            nombre="María",
            domicilio=domicilio,
            afiliado=None,
            repo=self.repo
        )

        # Assert: verificar resultados
        self.assertEqual(paciente.cuil, cuil)
        self.assertEqual(paciente.apellido, "Pérez")
        self.assertEqual(paciente.nombre, "María")
        self.assertIsNone(paciente.afiliado)
        
        # Verificar interacciones con el repositorio
        self.repo.get.assert_called_once_with(cuil)
        self.repo.save.assert_called_once()
        
        logger.info("✓ Test completado exitosamente")

    def test_registro_obra_social_inexistente(self):
        logger.info("TEST: test_registro_obra_social_inexistente - Rechazar registro con obra social inexistente")
        
        # Arrange: configurar datos y mocks
        cuil = "20-11111111-1"
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
        
        # Configurar comportamiento del mock: obra social NO existe
        self.repo.existe_obra_social.return_value = False

        # Act & Assert: verificar que se lanza la excepción esperada
        with self.assertRaises(ValueError) as context:
            registrar_paciente(
                cuil=cuil,
                apellido="López",
                nombre="Carlos",
                domicilio=domicilio,
                afiliado=afiliado,
                repo=self.repo
            )
        
        self.assertEqual(str(context.exception), "No se puede registrar al paciente con una obra social inexistente")
        
        # Verificar interacciones con el repositorio
        self.repo.existe_obra_social.assert_called_once_with("Swiss Medical")
        
        logger.info("✓ Test completado exitosamente")

    def test_registro_no_afiliado(self):
        logger.info("TEST: test_registro_no_afiliado - Rechazar registro de paciente no afiliado")
        
        # Arrange: configurar datos y mocks
        cuil = "20-22222222-2"
        obra_social = ObraSocial("OSDE")
        domicilio = Domicilio(
            calle="Calle Real",
            numero=789,
            localidad="San Miguel de Tucumán",
            ciudad="San Miguel de Tucumán",
            provincia="Tucumán",
            pais="Argentina"
        )
        afiliado = Afiliado(obra_social=obra_social, numero_afiliado="888888")
        
        # Configurar comportamiento del mock: obra social existe pero paciente NO está afiliado
        self.repo.existe_obra_social.return_value = True
        self.repo.esta_afiliado.return_value = False

        # Act & Assert: verificar que se lanza la excepción esperada
        with self.assertRaises(ValueError) as context:
            registrar_paciente(
                cuil=cuil,
                apellido="Fernández",
                nombre="Ana",
                domicilio=domicilio,
                afiliado=afiliado,
                repo=self.repo
            )
        
        self.assertEqual(str(context.exception), "No se puede registrar el paciente dado que no está afiliado a la obra social")
        
        # Verificar interacciones con el repositorio
        self.repo.existe_obra_social.assert_called_once_with("OSDE")
        self.repo.esta_afiliado.assert_called_once_with(cuil, "OSDE")
        
        logger.info("✓ Test completado exitosamente")

    def test_registro_campo_mandatorio_omitido_cuil(self):
        logger.info("TEST: test_registro_campo_mandatorio_omitido_cuil - Validar campo CUIL obligatorio")
        
        # Arrange: configurar datos con CUIL omitido
        domicilio = Domicilio(
            calle="Calle Test",
            numero=100,
            localidad="San Miguel de Tucumán",
            ciudad="San Miguel de Tucumán",
            provincia="Tucumán",
            pais="Argentina"
        )

        # Act & Assert: verificar que se lanza la excepción esperada
        with self.assertRaises(ValueError) as context:
            registrar_paciente(
                cuil=None,
                apellido="Gómez",
                nombre="Pedro",
                domicilio=domicilio,
                afiliado=None,
                repo=self.repo
            )
        
        self.assertIn("cuil", str(context.exception).lower())
        logger.info("✓ Test completado exitosamente")

    def test_registro_campo_mandatorio_omitido_apellido(self):
        logger.info("TEST: test_registro_campo_mandatorio_omitido_apellido - Validar campo apellido obligatorio")
        
        # Arrange: configurar datos con apellido omitido
        domicilio = Domicilio(
            calle="Calle Test",
            numero=100,
            localidad="San Miguel de Tucumán",
            ciudad="San Miguel de Tucumán",
            provincia="Tucumán",
            pais="Argentina"
        )

        # Act & Assert: verificar que se lanza la excepción esperada
        with self.assertRaises(ValueError) as context:
            registrar_paciente(
                cuil="20-33333333-3",
                apellido=None,
                nombre="Luis",
                domicilio=domicilio,
                afiliado=None,
                repo=self.repo
            )
        
        self.assertIn("apellido", str(context.exception).lower())
        logger.info("✓ Test completado exitosamente")

    def test_registro_campo_mandatorio_omitido_nombre(self):
        logger.info("TEST: test_registro_campo_mandatorio_omitido_nombre - Validar campo nombre obligatorio")
        
        # Arrange: configurar datos con nombre omitido
        domicilio = Domicilio(
            calle="Calle Test",
            numero=100,
            localidad="San Miguel de Tucumán",
            ciudad="San Miguel de Tucumán",
            provincia="Tucumán",
            pais="Argentina"
        )

        # Act & Assert: verificar que se lanza la excepción esperada
        with self.assertRaises(ValueError) as context:
            registrar_paciente(
                cuil="20-44444444-4",
                apellido="Rodríguez",
                nombre=None,
                domicilio=domicilio,
                afiliado=None,
                repo=self.repo
            )
        
        self.assertIn("nombre", str(context.exception).lower())
        logger.info("✓ Test completado exitosamente")

    def test_registro_campo_mandatorio_omitido_domicilio(self):
        logger.info("TEST: test_registro_campo_mandatorio_omitido_domicilio - Validar campo domicilio obligatorio")
        
        # Act & Assert: verificar que se lanza la excepción esperada
        with self.assertRaises(ValueError) as context:
            registrar_paciente(
                cuil="20-55555555-5",
                apellido="Martínez",
                nombre="Laura",
                domicilio=None,
                afiliado=None,
                repo=self.repo
            )
        
        self.assertIn("domicilio", str(context.exception).lower())
        logger.info("✓ Test completado exitosamente")

    def test_registro_campo_mandatorio_omitido_domicilio_calle(self):
        logger.info("TEST: test_registro_campo_mandatorio_omitido_domicilio_calle - Validar campo calle obligatorio")
        
        # Arrange: configurar domicilio con calle omitida
        domicilio = Domicilio(
            calle=None,
            numero=100,
            localidad="San Miguel de Tucumán",
            ciudad="San Miguel de Tucumán",
            provincia="Tucumán",
            pais="Argentina"
        )

        # Act & Assert: verificar que se lanza la excepción esperada
        with self.assertRaises(ValueError) as context:
            registrar_paciente(
                cuil="20-66666666-6",
                apellido="Sánchez",
                nombre="Diego",
                domicilio=domicilio,
                afiliado=None,
                repo=self.repo
            )
        
        self.assertIn("calle", str(context.exception).lower())
        logger.info("✓ Test completado exitosamente")

    def test_registro_campo_mandatorio_omitido_domicilio_numero(self):
        logger.info("TEST: test_registro_campo_mandatorio_omitido_domicilio_numero - Validar campo número obligatorio")
        
        # Arrange: configurar domicilio con número omitido
        domicilio = Domicilio(
            calle="Calle Test",
            numero=None,
            localidad="San Miguel de Tucumán",
            ciudad="San Miguel de Tucumán",
            provincia="Tucumán",
            pais="Argentina"
        )

        # Act & Assert: verificar que se lanza la excepción esperada
        with self.assertRaises(ValueError) as context:
            registrar_paciente(
                cuil="20-77777777-7",
                apellido="Torres",
                nombre="Sofía",
                domicilio=domicilio,
                afiliado=None,
                repo=self.repo
            )
        
        self.assertIn("numero", str(context.exception).lower())
        logger.info("✓ Test completado exitosamente")

    def test_registro_campo_mandatorio_omitido_domicilio_localidad(self):
        logger.info("TEST: test_registro_campo_mandatorio_omitido_domicilio_localidad - Validar campo localidad obligatorio")
        
        # Arrange: configurar domicilio con localidad omitida
        domicilio = Domicilio(
            calle="Calle Test",
            numero=100,
            localidad=None,
            ciudad="San Miguel de Tucumán",
            provincia="Tucumán",
            pais="Argentina"
        )

        # Act & Assert: verificar que se lanza la excepción esperada
        with self.assertRaises(ValueError) as context:
            registrar_paciente(
                cuil="20-88888888-8",
                apellido="Ramírez",
                nombre="Martín",
                domicilio=domicilio,
                afiliado=None,
                repo=self.repo
            )
        
        self.assertIn("localidad", str(context.exception).lower())
        logger.info("✓ Test completado exitosamente")

    def test_registro_cuil_formato_invalido(self):
        logger.info("TEST: test_registro_cuil_formato_invalido - Validar formato de CUIL")
        
        # Arrange: configurar datos con CUIL de formato inválido
        domicilio = Domicilio(
            calle="Calle Test",
            numero=100,
            localidad="San Miguel de Tucumán",
            ciudad="San Miguel de Tucumán",
            provincia="Tucumán",
            pais="Argentina"
        )

        # Act & Assert: verificar que se lanza la excepción esperada
        with self.assertRaises(ValueError) as context:
            registrar_paciente(
                cuil="123",
                apellido="Díaz",
                nombre="Roberto",
                domicilio=domicilio,
                afiliado=None,
                repo=self.repo
            )
        
        self.assertIn("formato", str(context.exception).lower())
        logger.info("✓ Test completado exitosamente")


if __name__ == '__main__':
    unittest.main()

