import unittest
from datetime import datetime
from unittest.mock import Mock

from src.domain.entities import CategoriaItem, ItemBiblioteca, Reserva, TipoUsuario, Usuario
from src.infrastructure.database import ORM
from src.infrastructure.repositories import ReservaRepository


class TestReservaRepository(unittest.TestCase):

    def setUp(self):
        self.orm_mock = Mock(spec=ORM)
        self.repository = ReservaRepository(self.orm_mock)

        self.reserva_data = {
            "id": 1,
            "usuario_id": 1,
            "item_id": 1,
            "empleado_id": 0,
            "fecha_reserva": "2023-01-01T00:00:00",
            "fecha_expiracion": "2023-01-08T00:00:00",
            "activa": True,
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

        self.reserva = Reserva(
            id=1, usuario_id=1, item_id=1, fecha_reserva=datetime(2023, 1, 1), fecha_expiracion=datetime(2023, 1, 8)
        )

    def test_crear_reserva(self):
        self.orm_mock.insert.return_value = 1
        reserva_sin_id = Reserva(
            usuario_id=1, item_id=1, fecha_reserva=datetime(2023, 1, 1), fecha_expiracion=datetime(2023, 1, 8)
        )

        resultado = self.repository.crear(reserva_sin_id)

        self.orm_mock.insert.assert_called_once()
        self.assertEqual(resultado.id, 1)
        self.assertEqual(resultado.usuario_id, 1)
        self.assertEqual(resultado.item_id, 1)

    def test_obtener_por_id_existente(self):
        self.orm_mock.select.return_value = [self.reserva_data]

        resultado = self.repository.obtener_por_id(1)

        self.orm_mock.select.assert_called_once_with("reservas", "id = ?", (1,))
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.id, 1)
        self.assertEqual(resultado.usuario_id, 1)
        self.assertEqual(resultado.item_id, 1)

    def test_obtener_por_id_no_existente(self):
        self.orm_mock.select.return_value = []

        resultado = self.repository.obtener_por_id(999)

        self.assertIsNone(resultado)

    def test_listar_reservas_activas(self):
        self.orm_mock.select.return_value = [self.reserva_data]

        resultado = self.repository.listar_reservas_activas()

        self.orm_mock.select.assert_called_once_with("reservas", "activa = ?", (True,))
        self.assertEqual(len(resultado), 1)
        self.assertTrue(resultado[0].activa)

    def test_listar_por_usuario(self):
        self.orm_mock.select.return_value = [self.reserva_data]

        resultado = self.repository.listar_por_usuario(1)

        self.orm_mock.select.assert_called_once_with("reservas", "usuario_id = ?", (1,))
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].usuario_id, 1)
        self.assertEqual(resultado[0].item_id, 1)

    def test_listar_por_item(self):
        self.orm_mock.select.return_value = [self.reserva_data]

        resultado = self.repository.listar_por_item(1)

        self.orm_mock.select.assert_called_once_with("reservas", "item_id = ?", (1,))
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].usuario_id, 1)
        self.assertEqual(resultado[0].item_id, 1)

    def test_actualizar_reserva(self):
        self.orm_mock.update.return_value = None

        resultado = self.repository.actualizar(self.reserva)

        self.orm_mock.update.assert_called_once()
        self.assertEqual(resultado, self.reserva)

    def test_cancelar_reserva(self):
        self.orm_mock.update.return_value = None

        self.repository.cancelar_reserva(1)

        self.orm_mock.update.assert_called_once_with("reservas", {"activa": False}, "id = ?", (1,))

    def test_entity_to_dict_conversion(self):
        resultado = self.repository._entity_to_dict(self.reserva)

        expected_keys = ["usuario_id", "item_id", "empleado_id", "fecha_reserva", "fecha_expiracion", "activa"]
        for key in expected_keys:
            self.assertIn(key, resultado)

        self.assertEqual(resultado["usuario_id"], 1)
        self.assertEqual(resultado["item_id"], 1)
        self.assertEqual(resultado["empleado_id"], 0)
        self.assertTrue(resultado["activa"])


if __name__ == "__main__":
    unittest.main()
