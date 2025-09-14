#!/usr/bin/env python3
"""
Tests unitarios para PrestamoService
"""

import os
import sys
import unittest
from datetime import datetime, timedelta
from unittest.mock import Mock

# Agregar el path del proyecto
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.application.interfaces import IItemBibliotecaRepository, IMultaRepository, IPrestamoRepository, IUsuarioRepository
from src.application.services import PrestamoService
from src.domain.entities import CategoriaItem, EstadoItem, ItemBiblioteca, Multa, Prestamo, TipoUsuario, Usuario


class TestPrestamoService(unittest.TestCase):

    def setUp(self):
        """Configuración inicial para cada test"""
        self.mock_prestamo_repo = Mock(spec=IPrestamoRepository)
        self.mock_item_repo = Mock(spec=IItemBibliotecaRepository)
        self.mock_usuario_repo = Mock(spec=IUsuarioRepository)
        self.mock_multa_repo = Mock(spec=IMultaRepository)

        self.prestamo_service = PrestamoService(
            self.mock_prestamo_repo, self.mock_item_repo, self.mock_usuario_repo, self.mock_multa_repo
        )

    def test_realizar_prestamo_exitoso(self):
        """Test: Realizar préstamo exitosamente"""
        # Arrange
        usuario = Usuario(
            id=1,
            nombre="Juan",
            apellido="Pérez",
            email="juan@test.com",
            tipo=TipoUsuario.ALUMNO,
            numero_identificacion="12345",
        )

        item = ItemBiblioteca(id=1, titulo="Python Programming", categoria=CategoriaItem.LIBRO, estado=EstadoItem.DISPONIBLE)

        prestamo_esperado = Prestamo(
            id=1,
            usuario_id=1,
            item_id=1,
            empleado_id=1,
            fecha_prestamo=datetime.now(),
            fecha_devolucion_esperada=datetime.now() + timedelta(days=15),
            activo=True,
        )

        self.mock_usuario_repo.obtener_por_id.return_value = usuario
        self.mock_item_repo.obtener_por_id.return_value = item
        self.mock_prestamo_repo.crear.return_value = prestamo_esperado
        self.mock_item_repo.actualizar.return_value = item

        # Act
        resultado = self.prestamo_service.realizar_prestamo(1, 1, 1, 15)

        # Assert
        self.assertEqual(resultado.usuario_id, 1)
        self.assertEqual(resultado.item_id, 1)
        self.assertEqual(resultado.empleado_id, 1)
        self.assertTrue(resultado.activo)

        self.mock_usuario_repo.obtener_por_id.assert_called_once_with(1)
        self.mock_item_repo.obtener_por_id.assert_called_once_with(1)
        self.mock_prestamo_repo.crear.assert_called_once()
        self.mock_item_repo.actualizar.assert_called_once()

    def test_realizar_prestamo_usuario_inexistente(self):
        """Test: Error con usuario inexistente"""
        # Arrange
        self.mock_usuario_repo.obtener_por_id.return_value = None

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.prestamo_service.realizar_prestamo(999, 1, 1)

        self.assertIn("No se encontró el usuario con ID: 999", str(context.exception))
        self.mock_prestamo_repo.crear.assert_not_called()

    def test_realizar_prestamo_item_inexistente(self):
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
            self.prestamo_service.realizar_prestamo(1, 999, 1)

        self.assertIn("No se encontró el item con ID: 999", str(context.exception))
        self.mock_prestamo_repo.crear.assert_not_called()

    def test_realizar_prestamo_item_no_disponible(self):
        """Test: Error con item no disponible"""
        # Arrange
        usuario = Usuario(
            id=1,
            nombre="Juan",
            apellido="Pérez",
            email="juan@test.com",
            tipo=TipoUsuario.ALUMNO,
            numero_identificacion="12345",
        )

        item = ItemBiblioteca(id=1, titulo="Python Programming", categoria=CategoriaItem.LIBRO, estado=EstadoItem.PRESTADO)

        self.mock_usuario_repo.obtener_por_id.return_value = usuario
        self.mock_item_repo.obtener_por_id.return_value = item

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.prestamo_service.realizar_prestamo(1, 1, 1)

        self.assertIn("no está disponible", str(context.exception))
        self.mock_prestamo_repo.crear.assert_not_called()

    def test_devolver_item_exitoso(self):
        """Test: Devolución exitosa sin atraso"""
        # Arrange
        prestamo = Prestamo(
            id=1,
            usuario_id=1,
            item_id=1,
            empleado_id=1,
            fecha_prestamo=datetime.now() - timedelta(days=10),
            fecha_devolucion_esperada=datetime.now() + timedelta(days=5),
            activo=True,
        )

        item = ItemBiblioteca(id=1, titulo="Test Book", categoria=CategoriaItem.LIBRO, estado=EstadoItem.PRESTADO)

        prestamo_devuelto = Prestamo(
            id=1,
            usuario_id=1,
            item_id=1,
            empleado_id=1,
            fecha_prestamo=prestamo.fecha_prestamo,
            fecha_devolucion_esperada=prestamo.fecha_devolucion_esperada,
            fecha_devolucion_real=datetime.now(),
            activo=False,
        )

        self.mock_prestamo_repo.obtener_por_id.return_value = prestamo
        self.mock_item_repo.obtener_por_id.return_value = item
        self.mock_prestamo_repo.actualizar.return_value = prestamo_devuelto

        # Act
        resultado = self.prestamo_service.devolver_item(1, "Buen estado")

        # Assert
        self.assertFalse(resultado.activo)
        self.assertIsNotNone(resultado.fecha_devolucion_real)

        self.mock_prestamo_repo.obtener_por_id.assert_called_once_with(1)
        self.mock_item_repo.actualizar.assert_called_once()
        self.mock_prestamo_repo.actualizar.assert_called_once()
        self.mock_multa_repo.crear.assert_not_called()  # No debe crear multa

    def test_devolver_item_con_atraso(self):
        """Test: Devolución con atraso genera multa"""
        # Arrange
        prestamo = Prestamo(
            id=1,
            usuario_id=1,
            item_id=1,
            empleado_id=1,
            fecha_prestamo=datetime.now() - timedelta(days=20),
            fecha_devolucion_esperada=datetime.now() - timedelta(days=3),  # Vencido hace 3 días
            activo=True,
        )

        item = ItemBiblioteca(id=1, titulo="Test Book", categoria=CategoriaItem.LIBRO, estado=EstadoItem.PRESTADO)

        prestamo_devuelto = Prestamo(
            id=1,
            usuario_id=1,
            item_id=1,
            empleado_id=1,
            fecha_prestamo=prestamo.fecha_prestamo,
            fecha_devolucion_esperada=prestamo.fecha_devolucion_esperada,
            fecha_devolucion_real=datetime.now(),
            activo=False,
        )

        multa_esperada = Multa(
            id=1,
            usuario_id=1,
            prestamo_id=1,
            empleado_id=1,
            monto=150.0,  # 3 días * $50
            descripcion="Devolución tardía: 3 días de atraso",
        )

        self.mock_prestamo_repo.obtener_por_id.return_value = prestamo
        self.mock_item_repo.obtener_por_id.return_value = item
        self.mock_prestamo_repo.actualizar.return_value = prestamo_devuelto
        self.mock_multa_repo.crear.return_value = multa_esperada

        # Act
        resultado = self.prestamo_service.devolver_item(1)

        # Assert
        self.assertFalse(resultado.activo)
        self.mock_multa_repo.crear.assert_called_once()  # Debe crear multa

        # Verificar que se llamó con los parámetros correctos
        call_args = self.mock_multa_repo.crear.call_args[0][0]
        self.assertEqual(call_args.usuario_id, 1)
        self.assertEqual(call_args.prestamo_id, 1)
        self.assertEqual(call_args.empleado_id, 1)
        self.assertTrue(call_args.monto > 0)  # Debe tener monto de multa

    def test_devolver_item_inexistente(self):
        """Test: Error al devolver préstamo inexistente"""
        # Arrange
        self.mock_prestamo_repo.obtener_por_id.return_value = None

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.prestamo_service.devolver_item(999)

        self.assertIn("No se encontró el préstamo con ID: 999", str(context.exception))
        self.mock_prestamo_repo.actualizar.assert_not_called()

    def test_devolver_item_ya_devuelto(self):
        """Test: Error al devolver préstamo ya devuelto"""
        # Arrange
        prestamo_devuelto = Prestamo(
            id=1,
            usuario_id=1,
            item_id=1,
            empleado_id=1,
            fecha_prestamo=datetime.now() - timedelta(days=10),
            fecha_devolucion_esperada=datetime.now() - timedelta(days=5),
            fecha_devolucion_real=datetime.now() - timedelta(days=2),
            activo=False,
        )

        self.mock_prestamo_repo.obtener_por_id.return_value = prestamo_devuelto

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.prestamo_service.devolver_item(1)

        self.assertIn("ya fue devuelto", str(context.exception))
        self.mock_prestamo_repo.actualizar.assert_not_called()

    def test_listar_prestamos_activos(self):
        """Test: Listar préstamos activos"""
        # Arrange
        prestamos_esperados = [
            Prestamo(id=1, usuario_id=1, item_id=1, empleado_id=1, activo=True),
            Prestamo(id=2, usuario_id=2, item_id=2, empleado_id=1, activo=True),
        ]

        self.mock_prestamo_repo.listar_activos.return_value = prestamos_esperados

        # Act
        resultado = self.prestamo_service.listar_prestamos_activos()

        # Assert
        self.assertEqual(resultado, prestamos_esperados)
        self.assertEqual(len(resultado), 2)
        self.mock_prestamo_repo.listar_activos.assert_called_once()

    def test_listar_prestamos_usuario(self):
        """Test: Listar préstamos de un usuario"""
        # Arrange
        prestamos_esperados = [
            Prestamo(id=1, usuario_id=1, item_id=1, empleado_id=1, activo=True),
            Prestamo(id=2, usuario_id=1, item_id=2, empleado_id=1, activo=False),
        ]

        self.mock_prestamo_repo.listar_por_usuario.return_value = prestamos_esperados

        # Act
        resultado = self.prestamo_service.listar_prestamos_usuario(1)

        # Assert
        self.assertEqual(resultado, prestamos_esperados)
        self.assertEqual(len(resultado), 2)
        self.mock_prestamo_repo.listar_por_usuario.assert_called_once_with(1)


if __name__ == "__main__":
    unittest.main()
