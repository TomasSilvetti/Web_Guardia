import unittest
from ..models.models import Usuario, Rol

class TestUsuarioRol(unittest.TestCase):

    def test_set_rol_with_enum(self):
        u = Usuario("usuario1@test.com", "password123")
        u.set_rol(Rol.MEDICO)
        self.assertEqual(u.rol, Rol.MEDICO)

    def test_set_rol_with_string(self):
        u = Usuario("usuario2@test.com", "password123")
        u.set_rol("Medico")
        self.assertEqual(u.rol, Rol.MEDICO)

    def test_constructor_with_role_enum(self):
        u = Usuario("usuario3@test.com", "password123", Rol.ENFERMERA)
        self.assertEqual(u.rol, Rol.ENFERMERA)

    def test_constructor_with_role_str(self):
        u = Usuario("usuario4@test.com", "password123", "enfermera")
        self.assertEqual(u.rol, Rol.ENFERMERA)

    def test_set_rol_invalid(self):
        u = Usuario("usuario5@test.com", "password123")
        with self.assertRaises(ValueError):
            u.set_rol("invalidrole")


if __name__ == '__main__':
    unittest.main()
