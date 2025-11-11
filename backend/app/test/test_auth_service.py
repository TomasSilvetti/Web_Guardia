import unittest
from ..services.auth_service import register, login, InMemoryUserRepo
from ..models.models import Rol


class TestAuthService(unittest.TestCase):

    def setUp(self):
        self.repo = InMemoryUserRepo()

    def test_registro_exitoso(self):
        u = register("medico@test.com", "strongpass1", Rol.MEDICO, repo=self.repo)
        self.assertEqual(u.email, "medico@test.com")
        self.assertEqual(u.rol, Rol.MEDICO)

    def test_registro_faltante_rol(self):
        with self.assertRaises(ValueError):
            register("u@test.com", "strongpass1", None, repo=self.repo)

    def test_registro_contrasena_corta(self):
        with self.assertRaises(ValueError):
            register("u2@test.com", "short", Rol.ENFERMERA, repo=self.repo)

    def test_registro_email_invalido(self):
        with self.assertRaises(ValueError):
            register("not-an-email", "strongpass1", Rol.MEDICO, repo=self.repo)

    def test_login_satisfactorio(self):
        register("login@test.com", "strongpass1", Rol.MEDICO, repo=self.repo)
        u = login("login@test.com", "strongpass1", repo=self.repo)
        self.assertEqual(u.email, "login@test.com")

    def test_login_fallo_contrasena_incorrecta(self):
        register("login2@test.com", "strongpass1", Rol.MEDICO, repo=self.repo)
        with self.assertRaises(ValueError) as cm:
            login("login2@test.com", "badpass", repo=self.repo)
        self.assertEqual(str(cm.exception), "Usuario o contraseña inválidos")

    def test_login_fallo_usuario_inexistente(self):
        with self.assertRaises(ValueError) as cm:
            login("noexist@test.com", "whatever", repo=self.repo)
        self.assertEqual(str(cm.exception), "Usuario o contraseña inválidos")


if __name__ == '__main__':
    unittest.main()
