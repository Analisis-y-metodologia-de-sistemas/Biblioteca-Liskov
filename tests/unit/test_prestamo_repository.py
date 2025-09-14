import unittest
from datetime import datetime
from unittest.mock import Mock

from src.domain.entities import CategoriaItem, ItemBiblioteca, Prestamo, TipoUsuario, Usuario
from src.infrastructure.database import ORM
from src.infrastructure.repositories import PrestamoRepository


class TestPrestamoRepository(unittest.TestCase):

    def setUp(self):
        self.orm_mock = Mock(spec=ORM)
        self.repository = PrestamoRepository(self.orm_mock)

        self.prestamo_data = {
            "id": 1,
            "usuario_id": 1,
            "item_id": 1,
            "empleado_id": 0,
            "fecha_prestamo": "2023-01-01T00:00:00",
            "fecha_devolucion_esperada": "2023-01-15T00:00:00",
            "fecha_devolucion_real": None,
            "observaciones": None,
            "activo": True,
        }

        self.usuario = Usuario(
            id=1,
            nombre="Juan",
            apellido="Pérez",
            email="juan@example.com",
            tipo=TipoUsuario.ALUMNO,
            numero_identificacion="12345678",
        )

        self.item = ItemBiblioteca(id=1, titulo="El Quijote", categoria=CategoriaItem.LIBRO, autor="Cervantes")

        self.prestamo = Prestamo(
            id=1, usuario_id=1, item_id=1, fecha_prestamo=datetime(2023, 1, 1), fecha_devolucion_esperada=datetime(2023, 1, 15)
        )

    def test_crear_prestamo(self):
        self.orm_mock.insert.return_value = 1
        prestamo_sin_id = Prestamo(
            usuario_id=1, item_id=1, fecha_prestamo=datetime(2023, 1, 1), fecha_devolucion_esperada=datetime(2023, 1, 15)
        )

        resultado = self.repository.crear(prestamo_sin_id)

        self.orm_mock.insert.assert_called_once()
        self.assertEqual(resultado.id, 1)
        self.assertEqual(resultado.usuario_id, 1)
        self.assertEqual(resultado.item_id, 1)

    def test_obtener_por_id_existente(self):
        self.orm_mock.select.return_value = [self.prestamo_data]

        resultado = self.repository.obtener_por_id(1)

        self.orm_mock.select.assert_called_once_with("prestamos", "id = ?", (1,))
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.id, 1)
        self.assertEqual(resultado.usuario_id, 1)
        self.assertEqual(resultado.item_id, 1)

    def test_obtener_por_id_no_existente(self):
        self.orm_mock.select.return_value = []

        resultado = self.repository.obtener_por_id(999)

        self.assertIsNone(resultado)

    def test_listar_prestamos_activos(self):
        self.orm_mock.select.return_value = [self.prestamo_data]

        resultado = self.repository.listar_prestamos_activos()

        self.orm_mock.select.assert_called_once_with("prestamos", "activo = ?", (True,))
        self.assertEqual(len(resultado), 1)
        self.assertTrue(resultado[0].activo)

    def test_listar_por_usuario(self):
        self.orm_mock.select.return_value = [self.prestamo_data]

        resultado = self.repository.listar_por_usuario(1)

        self.orm_mock.select.assert_called_once_with("prestamos", "usuario_id = ?", (1,))
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].usuario_id, 1)

    def test_actualizar_prestamo(self):
        self.orm_mock.update.return_value = None

        resultado = self.repository.actualizar(self.prestamo)

        self.orm_mock.update.assert_called_once()
        self.assertEqual(resultado, self.prestamo)

    def test_entity_to_dict_conversion(self):
        resultado = self.repository._entity_to_dict(self.prestamo)

        expected_keys = ["usuario_id", "item_id", "empleado_id", "fecha_prestamo", "fecha_devolucion_esperada", "activo"]
        for key in expected_keys:
            self.assertIn(key, resultado)

        self.assertEqual(resultado["usuario_id"], 1)
        self.assertEqual(resultado["item_id"], 1)
        self.assertEqual(resultado["empleado_id"], 0)
        self.assertTrue(resultado["activo"])


if __name__ == "__main__":
    unittest.main()
