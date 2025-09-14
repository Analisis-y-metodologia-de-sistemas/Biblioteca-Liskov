import unittest
from datetime import datetime
from unittest.mock import Mock

from src.domain.entities import TipoUsuario, Usuario
from src.infrastructure.database import ORM
from src.infrastructure.repositories import UsuarioRepository


class TestUsuarioRepository(unittest.TestCase):

    def setUp(self):
        self.orm_mock = Mock(spec=ORM)
        self.repository = UsuarioRepository(self.orm_mock)

        self.usuario_data = {
            "id": 1,
            "nombre": "Juan",
            "apellido": "Pérez",
            "email": "juan@example.com",
            "tipo": "alumno",
            "numero_identificacion": "12345678",
            "telefono": "555-1234",
            "activo": True,
            "fecha_registro": "2023-01-01T12:00:00",
        }

        self.usuario = Usuario(
            id=1,
            nombre="Juan",
            apellido="Pérez",
            email="juan@example.com",
            tipo=TipoUsuario.ALUMNO,
            numero_identificacion="12345678",
            telefono="555-1234",
            activo=True,
            fecha_registro=datetime(2023, 1, 1, 12, 0, 0),
        )

    def test_crear_usuario(self):
        self.orm_mock.insert.return_value = 1
        usuario_sin_id = Usuario(
            nombre="Juan",
            apellido="Pérez",
            email="juan@example.com",
            tipo=TipoUsuario.ALUMNO,
            numero_identificacion="12345678",
        )

        resultado = self.repository.crear(usuario_sin_id)

        self.orm_mock.insert.assert_called_once()
        self.assertEqual(resultado.id, 1)
        self.assertEqual(resultado.nombre, "Juan")

    def test_obtener_por_id_existente(self):
        self.orm_mock.select.return_value = [self.usuario_data]

        resultado = self.repository.obtener_por_id(1)

        self.orm_mock.select.assert_called_once_with("usuarios", "id = ?", (1,))
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.id, 1)
        self.assertEqual(resultado.nombre, "Juan")

    def test_obtener_por_id_no_existente(self):
        self.orm_mock.select.return_value = []

        resultado = self.repository.obtener_por_id(999)

        self.orm_mock.select.assert_called_once_with("usuarios", "id = ?", (999,))
        self.assertIsNone(resultado)

    def test_obtener_por_email_existente(self):
        self.orm_mock.select.return_value = [self.usuario_data]

        resultado = self.repository.obtener_por_email("juan@example.com")

        self.orm_mock.select.assert_called_once_with("usuarios", "email = ?", ("juan@example.com",))
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.email, "juan@example.com")

    def test_obtener_por_email_no_existente(self):
        self.orm_mock.select.return_value = []

        resultado = self.repository.obtener_por_email("noexiste@example.com")

        self.assertIsNone(resultado)

    def test_listar_todos(self):
        self.orm_mock.select.return_value = [self.usuario_data, {**self.usuario_data, "id": 2, "email": "otro@example.com"}]

        resultado = self.repository.listar_todos()

        self.orm_mock.select.assert_called_once_with("usuarios")
        self.assertEqual(len(resultado), 2)
        self.assertEqual(resultado[0].id, 1)
        self.assertEqual(resultado[1].id, 2)

    def test_actualizar_usuario(self):
        self.orm_mock.update.return_value = None

        resultado = self.repository.actualizar(self.usuario)

        self.orm_mock.update.assert_called_once()
        self.assertEqual(resultado, self.usuario)

    def test_eliminar_usuario(self):
        self.orm_mock.delete.return_value = 1

        resultado = self.repository.eliminar(1)

        self.orm_mock.delete.assert_called_once_with("usuarios", "id = ?", (1,))
        self.assertTrue(resultado)

    def test_row_to_entity_conversion(self):
        resultado = self.repository._row_to_entity(self.usuario_data)

        self.assertEqual(resultado.id, 1)
        self.assertEqual(resultado.nombre, "Juan")
        self.assertEqual(resultado.apellido, "Pérez")
        self.assertEqual(resultado.email, "juan@example.com")
        self.assertEqual(resultado.tipo, TipoUsuario.ALUMNO)
        self.assertEqual(resultado.numero_identificacion, "12345678")
        self.assertEqual(resultado.telefono, "555-1234")
        self.assertTrue(resultado.activo)

    def test_entity_to_dict_conversion(self):
        resultado = self.repository._entity_to_dict(self.usuario)

        expected = {
            "nombre": "Juan",
            "apellido": "Pérez",
            "email": "juan@example.com",
            "tipo": "alumno",
            "numero_identificacion": "12345678",
            "telefono": "555-1234",
            "activo": True,
        }
        self.assertEqual(resultado, expected)


if __name__ == "__main__":
    unittest.main()
