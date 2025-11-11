import unittest
from ..services.auth_service import register, login, InMemoryUserRepo
from ..models.models import Rol
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


class TestAuthService(unittest.TestCase):

    def setUp(self):
        self.repo = InMemoryUserRepo()

    def test_registro_exitoso(self):
        logger.info("\n=== TEST: test_registro_exitoso ===")
        logger.info("DATOS DE ENTRADA:")
        logger.info(f"  - Email: 'medico@test.com'")
        logger.info(f"  - Password: 'strongpass1'")
        logger.info(f"  - Rol: {Rol.MEDICO}")

        u = register("medico@test.com", "strongpass1", Rol.MEDICO, repo=self.repo)

        logger.info("DATOS OBTENIDOS DEL RETORNO:")
        logger.info(f"  - Email: '{u.email}'")
        logger.info(f"  - Rol: {u.rol}")
        logger.info(f"  - ID: {u.id}")
        logger.info(f"  - Password hasheado: {'***' if u.password else 'None'}")

        logger.info("ASSERTS:")
        logger.info(f"  - Email esperado: 'medico@test.com'")
        logger.info(f"  - Email actual: '{u.email}'")
        logger.info(f"  - Rol esperado: {Rol.MEDICO}")
        logger.info(f"  - Rol actual: {u.rol}")

        self.assertEqual(u.email, "medico@test.com")
        self.assertEqual(u.rol, Rol.MEDICO)
        logger.info("✓ Asserts de email y rol pasados correctamente\n")

    def test_registro_faltante_rol(self):
        logger.info("\n=== TEST: test_registro_faltante_rol ===")
        logger.info("DATOS DE ENTRADA:")
        logger.info(f"  - Email: 'u@test.com'")
        logger.info(f"  - Password: 'strongpass1'")
        logger.info(f"  - Rol: {None}")

        logger.info("ASSERT: Se espera que se lance ValueError")
        with self.assertRaises(ValueError) as context:
            register("u@test.com", "strongpass1", None, repo=self.repo)
        logger.info(f"✓ Excepción lanzada correctamente: {context.exception}")

    def test_registro_contrasena_corta(self):
        logger.info("\n=== TEST: test_registro_contrasena_corta ===")
        logger.info("DATOS DE ENTRADA:")
        logger.info(f"  - Email: 'u2@test.com'")
        logger.info(f"  - Password: 'short'")
        logger.info(f"  - Rol: {Rol.ENFERMERA}")

        logger.info("ASSERT: Se espera que se lance ValueError por contraseña corta")
        with self.assertRaises(ValueError) as context:
            register("u2@test.com", "short", Rol.ENFERMERA, repo=self.repo)
        logger.info(f"✓ Excepción lanzada correctamente: {context.exception}")

    def test_registro_email_invalido(self):
        logger.info("\n=== TEST: test_registro_email_invalido ===")
        logger.info("DATOS DE ENTRADA:")
        logger.info(f"  - Email: 'not-an-email'")
        logger.info(f"  - Password: 'strongpass1'")
        logger.info(f"  - Rol: {Rol.MEDICO}")

        logger.info("ASSERT: Se espera que se lance ValueError por email inválido")
        with self.assertRaises(ValueError) as context:
            register("not-an-email", "strongpass1", Rol.MEDICO, repo=self.repo)
        logger.info(f"✓ Excepción lanzada correctamente: {context.exception}")

    def test_login_satisfactorio(self):
        logger.info("\n=== TEST: test_login_satisfactorio ===")
        logger.info("PASO 1: Registro de usuario")
        logger.info("DATOS DE ENTRADA REGISTRO:")
        logger.info(f"  - Email: 'login@test.com'")
        logger.info(f"  - Password: 'strongpass1'")
        logger.info(f"  - Rol: {Rol.MEDICO}")

        register("login@test.com", "strongpass1", Rol.MEDICO, repo=self.repo)
        logger.info("✓ Usuario registrado exitosamente")

        logger.info("\nPASO 2: Login de usuario")
        logger.info("DATOS DE ENTRADA LOGIN:")
        logger.info(f"  - Email: 'login@test.com'")
        logger.info(f"  - Password: 'strongpass1'")

        u = login("login@test.com", "strongpass1", repo=self.repo)

        logger.info("DATOS OBTENIDOS DEL RETORNO LOGIN:")
        logger.info(f"  - Email: '{u.email}'")
        logger.info(f"  - Rol: {u.rol}")
        logger.info(f"  - ID: {u.id}")

        logger.info("ASSERTS:")
        logger.info(f"  - Email esperado: 'login@test.com'")
        logger.info(f"  - Email actual: '{u.email}'")

        self.assertEqual(u.email, "login@test.com")
        logger.info("✓ Assert de email pasado correctamente\n")

    def test_login_fallo_contrasena_incorrecta(self):
        logger.info("\n=== TEST: test_login_fallo_contrasena_incorrecta ===")
        logger.info("PASO 1: Registro de usuario")
        logger.info("DATOS DE ENTRADA REGISTRO:")
        logger.info(f"  - Email: 'login2@test.com'")
        logger.info(f"  - Password: 'strongpass1'")
        logger.info(f"  - Rol: {Rol.MEDICO}")

        register("login2@test.com", "strongpass1", Rol.MEDICO, repo=self.repo)
        logger.info("✓ Usuario registrado exitosamente")

        logger.info("\nPASO 2: Login con contraseña incorrecta")
        logger.info("DATOS DE ENTRADA LOGIN:")
        logger.info(f"  - Email: 'login2@test.com'")
        logger.info(f"  - Password: 'badpass' (incorrecta)")

        logger.info("ASSERT: Se espera que se lance ValueError")
        logger.info("Mensaje esperado: 'Usuario o contraseña inválidos'")

        with self.assertRaises(ValueError) as context:
            login("login2@test.com", "badpass", repo=self.repo)
        logger.info(f"✓ Excepción lanzada correctamente")
        logger.info(f"  - Mensaje recibido: '{str(context.exception)}'")
        logger.info(f"  - Mensaje esperado: 'Usuario o contraseña inválidos'")
        self.assertEqual(str(context.exception), "Usuario o contraseña inválidos")
        logger.info("✓ Mensaje de error coincide con el esperado\n")

    def test_login_fallo_usuario_inexistente(self):
        logger.info("\n=== TEST: test_login_fallo_usuario_inexistente ===")
        logger.info("DATOS DE ENTRADA LOGIN:")
        logger.info(f"  - Email: 'noexist@test.com' (no existe)")
        logger.info(f"  - Password: 'whatever'")

        logger.info("ASSERT: Se espera que se lance ValueError")
        logger.info("Mensaje esperado: 'Usuario o contraseña inválidos'")

        with self.assertRaises(ValueError) as context:
            login("noexist@test.com", "whatever", repo=self.repo)
        logger.info(f"✓ Excepción lanzada correctamente")
        logger.info(f"  - Mensaje recibido: '{str(context.exception)}'")
        logger.info(f"  - Mensaje esperado: 'Usuario o contraseña inválidos'")
        self.assertEqual(str(context.exception), "Usuario o contraseña inválidos")
        logger.info("✓ Mensaje de error coincide con el esperado\n")


if __name__ == '__main__':
    unittest.main()
