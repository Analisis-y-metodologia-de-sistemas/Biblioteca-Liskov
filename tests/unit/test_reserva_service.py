#!/usr/bin/env python3
"""
Tests unitarios para ReservaService
"""

import os
import sys
import unittest
from datetime import datetime, timedelta
from unittest.mock import Mock

# Agregar el path del proyecto
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.application.interfaces import IItemBibliotecaRepository, IReservaRepository, IUsuarioRepository
from src.application.services import ReservaService
from src.domain.entities import CategoriaItem, EstadoItem, ItemBiblioteca, Reserva, TipoUsuario, Usuario


class TestReservaService(unittest.TestCase):

    def setUp(self):
        """Configuración inicial para cada test"""
        self.mock_reserva_repo = Mock(spec=IReservaRepository)
        self.mock_item_repo = Mock(spec=IItemBibliotecaRepository)
        self.mock_usuario_repo = Mock(spec=IUsuarioRepository)

        self.reserva_service = ReservaService(self.mock_reserva_repo, self.mock_item_repo, self.mock_usuario_repo)

    def test_realizar_reserva_exitosa(self):
        """Test: Realizar reserva exitosamente"""
        # Arrange
        usuario = Usuario(
            id=1,
            nombre="Juan",
            apellido="Pérez",
            email="juan@test.com",
            tipo=TipoUsuario.ALUMNO,
            numero_identificacion="12345",
        )

        item = ItemBiblioteca(
            id=1,
            titulo="Python Programming",
            categoria=CategoriaItem.LIBRO,
            estado=EstadoItem.PRESTADO,  # No disponible, por eso se puede reservar
        )

        reserva_esperada = Reserva(
            id=1,
            usuario_id=1,
            item_id=1,
            empleado_id=1,
            fecha_reserva=datetime.now(),
            fecha_expiracion=datetime.now() + timedelta(days=3),
            activa=True,
        )

        self.mock_usuario_repo.obtener_por_id.return_value = usuario
        self.mock_item_repo.obtener_por_id.return_value = item
        self.mock_reserva_repo.crear.return_value = reserva_esperada

        # Act
        resultado = self.reserva_service.realizar_reserva(1, 1, 1, 3)

        # Assert
        self.assertEqual(resultado.usuario_id, 1)
        self.assertEqual(resultado.item_id, 1)
        self.assertEqual(resultado.empleado_id, 1)
        self.assertTrue(resultado.activa)

        self.mock_usuario_repo.obtener_por_id.assert_called_once_with(1)
        self.mock_item_repo.obtener_por_id.assert_called_once_with(1)
        self.mock_reserva_repo.crear.assert_called_once()

    def test_realizar_reserva_usuario_inexistente(self):
        """Test: Error con usuario inexistente"""
        # Arrange
        self.mock_usuario_repo.obtener_por_id.return_value = None

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.reserva_service.realizar_reserva(999, 1, 1)

        self.assertIn("No se encontró el usuario con ID: 999", str(context.exception))
        self.mock_reserva_repo.crear.assert_not_called()

    def test_realizar_reserva_item_inexistente(self):
        """Test: Error con item inexistente"""
        # Arrange
        usuario = Usuario(
            id=1,
            nombre="Juan",
            apellido="Pérez",
            email="juan@test.com",
            tipo=TipoUsuario.ALUMNO,
            numero_identificacion="12345",
        )

        self.mock_usuario_repo.obtener_por_id.return_value = usuario
        self.mock_item_repo.obtener_por_id.return_value = None

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.reserva_service.realizar_reserva(1, 999, 1)

        self.assertIn("No se encontró el item con ID: 999", str(context.exception))
        self.mock_reserva_repo.crear.assert_not_called()

    def test_realizar_reserva_item_disponible(self):
        """Test: Error al reservar item disponible"""
        # Arrange
        usuario = Usuario(
            id=1,
            nombre="Juan",
            apellido="Pérez",
            email="juan@test.com",
            tipo=TipoUsuario.ALUMNO,
            numero_identificacion="12345",
        )

        item = ItemBiblioteca(
            id=1,
            titulo="Python Programming",
            categoria=CategoriaItem.LIBRO,
            estado=EstadoItem.DISPONIBLE,  # Disponible, no necesita reserva
        )

        self.mock_usuario_repo.obtener_por_id.return_value = usuario
        self.mock_item_repo.obtener_por_id.return_value = item

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.reserva_service.realizar_reserva(1, 1, 1)

        self.assertIn("está disponible, no necesita reserva", str(context.exception))
        self.mock_reserva_repo.crear.assert_not_called()

    def test_cancelar_reserva_exitosa(self):
        """Test: Cancelar reserva exitosamente"""
        # Arrange
        reserva = Reserva(
            id=1,
            usuario_id=1,
            item_id=1,
            empleado_id=1,
            fecha_reserva=datetime.now(),
            fecha_expiracion=datetime.now() + timedelta(days=3),
            activa=True,
        )

        reserva_cancelada = Reserva(
            id=1,
            usuario_id=1,
            item_id=1,
            empleado_id=1,
            fecha_reserva=reserva.fecha_reserva,
            fecha_expiracion=reserva.fecha_expiracion,
            activa=False,
        )

        self.mock_reserva_repo.obtener_por_id.return_value = reserva
        self.mock_reserva_repo.actualizar.return_value = reserva_cancelada

        # Act
        resultado = self.reserva_service.cancelar_reserva(1)

        # Assert
        self.assertFalse(resultado.activa)
        self.mock_reserva_repo.obtener_por_id.assert_called_once_with(1)
        self.mock_reserva_repo.actualizar.assert_called_once()

    def test_cancelar_reserva_inexistente(self):
        """Test: Error al cancelar reserva inexistente"""
        # Arrange
        self.mock_reserva_repo.obtener_por_id.return_value = None

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.reserva_service.cancelar_reserva(999)

        self.assertIn("No se encontró la reserva con ID: 999", str(context.exception))
        self.mock_reserva_repo.actualizar.assert_not_called()

    def test_listar_reservas_activas(self):
        """Test: Listar reservas activas"""
        # Arrange
        reservas_esperadas = [
            Reserva(id=1, usuario_id=1, item_id=1, empleado_id=1, activa=True),
            Reserva(id=2, usuario_id=2, item_id=2, empleado_id=1, activa=True),
        ]

        self.mock_reserva_repo.listar_activas.return_value = reservas_esperadas

        # Act
        resultado = self.reserva_service.listar_reservas_activas()

        # Assert
        self.assertEqual(resultado, reservas_esperadas)
        self.assertEqual(len(resultado), 2)
        self.mock_reserva_repo.listar_activas.assert_called_once()


if __name__ == "__main__":
    unittest.main()
