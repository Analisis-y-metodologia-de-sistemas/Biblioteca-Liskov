#!/usr/bin/env python3
"""
Tests simplificados para todos los repositorios
"""

import os
import sys
import unittest
from datetime import date, datetime
from unittest.mock import MagicMock, Mock

# Agregar el path del proyecto
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.domain.entities import (
    CategoriaItem,
    Empleado,
    EstadoItem,
    ItemBiblioteca,
    Multa,
    Prestamo,
    Reserva,
    TipoUsuario,
    Usuario,
)
from src.infrastructure.database import ORM
from src.infrastructure.repositories import (
    EmpleadoRepository,
    ItemBibliotecaRepository,
    MultaRepository,
    PrestamoRepository,
    ReservaRepository,
    UsuarioRepository,
)


class TestAllRepositories(unittest.TestCase):

    def setUp(self):
        """Configuración inicial para cada test"""
        self.orm_mock = Mock(spec=ORM)

        # Repositorios
        self.usuario_repo = UsuarioRepository(self.orm_mock)
        self.item_repo = ItemBibliotecaRepository(self.orm_mock)
        self.prestamo_repo = PrestamoRepository(self.orm_mock)
        self.reserva_repo = ReservaRepository(self.orm_mock)
        self.multa_repo = MultaRepository(self.orm_mock)
        self.empleado_repo = EmpleadoRepository(self.orm_mock)

    def test_usuario_repository_crear(self):
        """Test crear usuario"""
        self.orm_mock.insert.return_value = 1

        usuario = Usuario(
            nombre="Juan", apellido="Pérez", email="juan@test.com", tipo=TipoUsuario.ALUMNO, numero_identificacion="12345678"
        )

        resultado = self.usuario_repo.crear(usuario)

        self.orm_mock.insert.assert_called_once()
        self.assertEqual(resultado.id, 1)
        self.assertEqual(resultado.nombre, "Juan")

    def test_item_repository_crear(self):
        """Test crear item"""
        self.orm_mock.insert.return_value = 1

        item = ItemBiblioteca(titulo="El Quijote", categoria=CategoriaItem.LIBRO, autor="Cervantes")

        resultado = self.item_repo.crear(item)

        self.orm_mock.insert.assert_called_once()
        self.assertEqual(resultado.id, 1)
        self.assertEqual(resultado.titulo, "El Quijote")

    def test_empleado_repository_crear(self):
        """Test crear empleado"""
        self.orm_mock.insert.return_value = 1

        empleado = Empleado(
            nombre="Ana", apellido="García", email="ana@test.com", usuario_sistema="agarcia", password_hash="hash123"
        )

        resultado = self.empleado_repo.crear(empleado)

        self.orm_mock.insert.assert_called_once()
        self.assertEqual(resultado.id, 1)
        self.assertEqual(resultado.nombre, "Ana")

    def test_prestamo_repository_crear(self):
        """Test crear préstamo"""
        self.orm_mock.insert.return_value = 1

        prestamo = Prestamo(usuario_id=1, item_id=1, fecha_prestamo=datetime.now(), fecha_devolucion_esperada=datetime.now())

        resultado = self.prestamo_repo.crear(prestamo)

        self.orm_mock.insert.assert_called_once()
        self.assertEqual(resultado.id, 1)
        self.assertEqual(resultado.usuario_id, 1)

    def test_reserva_repository_crear(self):
        """Test crear reserva"""
        self.orm_mock.insert.return_value = 1

        reserva = Reserva(usuario_id=1, item_id=1, fecha_reserva=datetime.now(), fecha_expiracion=datetime.now())

        resultado = self.reserva_repo.crear(reserva)

        self.orm_mock.insert.assert_called_once()
        self.assertEqual(resultado.id, 1)
        self.assertEqual(resultado.usuario_id, 1)

    def test_multa_repository_crear(self):
        """Test crear multa"""
        self.orm_mock.insert.return_value = 1

        multa = Multa(
            usuario_id=1, prestamo_id=1, monto=5000.0, descripcion="Retraso en devolución", fecha_multa=datetime.now()
        )

        resultado = self.multa_repo.crear(multa)

        self.orm_mock.insert.assert_called_once()
        self.assertEqual(resultado.id, 1)
        self.assertEqual(resultado.monto, 5000.0)

    def test_repositories_obtener_por_id_inexistente(self):
        """Test obtener por ID inexistente en todos los repositorios"""
        self.orm_mock.select.return_value = []

        # Todos los repositorios deben retornar None si no existe el ID
        self.assertIsNone(self.usuario_repo.obtener_por_id(999))
        self.assertIsNone(self.item_repo.obtener_por_id(999))
        self.assertIsNone(self.prestamo_repo.obtener_por_id(999))
        self.assertIsNone(self.reserva_repo.obtener_por_id(999))
        self.assertIsNone(self.multa_repo.obtener_por_id(999))
        self.assertIsNone(self.empleado_repo.obtener_por_id(999))

    def test_repositories_actualizar(self):
        """Test actualizar entidades"""
        self.orm_mock.update.return_value = None

        # Crear entidades de test
        usuario = Usuario(id=1, nombre="Juan", email="juan@test.com")
        item = ItemBiblioteca(id=1, titulo="Test Book")
        empleado = Empleado(id=1, nombre="Ana", email="ana@test.com")
        prestamo = Prestamo(id=1, usuario_id=1, item_id=1)
        reserva = Reserva(id=1, usuario_id=1, item_id=1)
        multa = Multa(id=1, usuario_id=1, prestamo_id=1, monto=100.0)

        # Actualizar todas las entidades
        self.usuario_repo.actualizar(usuario)
        self.item_repo.actualizar(item)
        self.empleado_repo.actualizar(empleado)
        self.prestamo_repo.actualizar(prestamo)
        self.reserva_repo.actualizar(reserva)
        self.multa_repo.actualizar(multa)

        # Verificar que se llamó update 6 veces
        self.assertEqual(self.orm_mock.update.call_count, 6)


if __name__ == "__main__":
    unittest.main()
