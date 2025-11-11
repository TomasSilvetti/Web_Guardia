import unittest
from ..models.models import Usuario, Rol
import bcrypt

class TestAuthModule(unittest.TestCase):

    def setUp(self):
        """Se ejecuta antes de cada test"""
        self.usuario_name = "usuario@test.com"
        self.password = "contraseña123"
        self.usuario = Usuario(self.usuario_name, self.password)

    def test_password_hashing(self):
        """Verificar que la contraseña se guarda hasheada y no en texto plano"""
        self.assertNotEqual(self.usuario.password_hash, self.password)
        self.assertTrue(bcrypt.checkpw(self.password.encode('utf-8'),
                                       self.usuario.password_hash.encode('utf-8')))

    def test_login_correcto(self):
        """Login con contraseña correcta"""
        self.assertTrue(self.usuario.verificar_password(self.password))

    def test_login_incorrecto(self):
        """Login con contraseña incorrecta"""
        self.assertFalse(self.usuario.verificar_password("password_incorrecto"))
