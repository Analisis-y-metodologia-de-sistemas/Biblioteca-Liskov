import unittest
from datetime import date, datetime
from unittest.mock import Mock

from src.domain.entities import CategoriaItem, ItemBiblioteca, Multa, Prestamo, TipoUsuario, Usuario
from src.infrastructure.database import ORM
from src.infrastructure.repositories import MultaRepository


class TestMultaRepository(unittest.TestCase):

    def setUp(self):
        self.orm_mock = Mock(spec=ORM)
        self.repository = MultaRepository(self.orm_mock)

        self.multa_data = {
            "id": 1,
            "usuario_id": 1,
            "prestamo_id": 1,
            "empleado_id": 0,
            "monto": 5000.0,
            "descripcion": "Retraso en devolución",
            "fecha_multa": "2023-01-16T00:00:00",
            "pagada": False,
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

        self.multa = Multa(
            id=1,
            usuario_id=1,
            prestamo_id=1,
            monto=5000.0,
            descripcion="Retraso en devolución",
            fecha_multa=datetime(2023, 1, 16),
        )

    def test_crear_multa(self):
        self.orm_mock.insert.return_value = 1
        multa_sin_id = Multa(
            usuario_id=1, prestamo_id=1, monto=5000.0, descripcion="Retraso en devolución", fecha_multa=datetime(2023, 1, 16)
        )

        resultado = self.repository.crear(multa_sin_id)

        self.orm_mock.insert.assert_called_once()
        self.assertEqual(resultado.id, 1)
        self.assertEqual(resultado.monto, 5000.0)
        self.assertEqual(resultado.descripcion, "Retraso en devolución")

    def test_obtener_por_id_existente(self):
        self.orm_mock.select.return_value = [self.multa_data]

        resultado = self.repository.obtener_por_id(1)

        self.orm_mock.select.assert_called_once_with("multas", "id = ?", (1,))
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.id, 1)
        self.assertEqual(resultado.monto, 5000.0)
        self.assertEqual(resultado.usuario_id, 1)
        self.assertEqual(resultado.prestamo_id, 1)

    def test_obtener_por_id_no_existente(self):
        self.orm_mock.select.return_value = []

        resultado = self.repository.obtener_por_id(999)

        self.assertIsNone(resultado)

    def test_listar_multas_pendientes(self):
        self.orm_mock.select.return_value = [self.multa_data]

        resultado = self.repository.listar_multas_pendientes()

        self.orm_mock.select.assert_called_once_with("multas", "pagada = ?", (False,))
        self.assertEqual(len(resultado), 1)
        self.assertFalse(resultado[0].pagada)
        self.assertEqual(resultado[0].monto, 5000.0)

    def test_listar_por_usuario(self):
        self.orm_mock.select.return_value = [self.multa_data]

        resultado = self.repository.listar_por_usuario(1)

        self.orm_mock.select.assert_called_once_with("multas", "usuario_id = ?", (1,))
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].usuario_id, 1)
        self.assertEqual(resultado[0].prestamo_id, 1)

    def test_marcar_como_pagada(self):
        self.orm_mock.update.return_value = None
        fecha_pago = date.today()

        self.repository.marcar_como_pagada(1, fecha_pago)

        self.orm_mock.update.assert_called_once_with(
            "multas", {"pagada": True, "fecha_pago": fecha_pago.isoformat()}, "id = ?", (1,)
        )

    def test_actualizar_multa(self):
        self.orm_mock.update.return_value = None

        resultado = self.repository.actualizar(self.multa)

        self.orm_mock.update.assert_called_once()
        self.assertEqual(resultado, self.multa)

    def test_entity_to_dict_conversion(self):
        resultado = self.repository._entity_to_dict(self.multa)

        expected_keys = ["usuario_id", "prestamo_id", "empleado_id", "monto", "fecha_multa", "descripcion", "pagada"]
        for key in expected_keys:
            self.assertIn(key, resultado)

        self.assertEqual(resultado["usuario_id"], 1)
        self.assertEqual(resultado["prestamo_id"], 1)
        self.assertEqual(resultado["empleado_id"], 0)
        self.assertEqual(resultado["monto"], 5000.0)
        self.assertEqual(resultado["descripcion"], "Retraso en devolución")
        self.assertFalse(resultado["pagada"])


if __name__ == "__main__":
    unittest.main()
