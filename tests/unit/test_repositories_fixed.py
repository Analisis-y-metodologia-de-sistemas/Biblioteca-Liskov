#!/usr/bin/env python3
"""
Tests corregidos para repositorios con relaciones complejas
"""

import os
import sys
import unittest
from datetime import datetime
from unittest.mock import Mock

# Agregar el path del proyecto
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.domain.entities import CategoriaItem, EstadoItem, ItemBiblioteca, Multa, Prestamo, Reserva
from src.infrastructure.database import ORM
from src.infrastructure.repositories import ItemBibliotecaRepository, MultaRepository, PrestamoRepository, ReservaRepository


class TestRepositoriesFixed(unittest.TestCase):

    def setUp(self):
        """Configuración inicial para cada test"""
        self.orm_mock = Mock(spec=ORM)

        # Repositorios
        self.prestamo_repo = PrestamoRepository(self.orm_mock)
        self.reserva_repo = ReservaRepository(self.orm_mock)
        self.multa_repo = MultaRepository(self.orm_mock)
        self.item_repo = ItemBibliotecaRepository(self.orm_mock)

    def test_prestamo_repository_operations(self):
        """Test operaciones básicas PrestamoRepository"""
        # Datos de test
        prestamo_data = {
            "id": 1,
            "usuario_id": 1,
            "item_id": 1,
            "empleado_id": 1,
            "fecha_prestamo": "2023-01-01T00:00:00",
            "fecha_devolucion_esperada": "2023-01-15T00:00:00",
            "fecha_devolucion_real": None,
            "observaciones": None,
            "activo": True,
        }

        # Test crear
        self.orm_mock.insert.return_value = 1
        prestamo = Prestamo(usuario_id=1, item_id=1, fecha_prestamo=datetime.now())
        resultado = self.prestamo_repo.crear(prestamo)
        self.assertEqual(resultado.id, 1)
        self.orm_mock.insert.assert_called()

        # Test obtener por id
        self.orm_mock.select.return_value = [prestamo_data]
        resultado = self.prestamo_repo.obtener_por_id(1)
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.usuario_id, 1)

        # Test listar activos
        self.orm_mock.select.return_value = [prestamo_data]
        resultado = self.prestamo_repo.listar_activos()
        self.assertEqual(len(resultado), 1)

        # Test actualizar
        self.orm_mock.update.return_value = None
        prestamo_actualizado = Prestamo(id=1, usuario_id=1, item_id=1)
        resultado = self.prestamo_repo.actualizar(prestamo_actualizado)
        self.assertEqual(resultado, prestamo_actualizado)

    def test_reserva_repository_operations(self):
        """Test operaciones básicas ReservaRepository"""
        # Datos de test
        reserva_data = {
            "id": 1,
            "usuario_id": 1,
            "item_id": 1,
            "empleado_id": 1,
            "fecha_reserva": "2023-01-01T00:00:00",
            "fecha_expiracion": "2023-01-08T00:00:00",
            "activa": True,
        }

        # Test crear
        self.orm_mock.insert.return_value = 1
        reserva = Reserva(usuario_id=1, item_id=1, fecha_reserva=datetime.now())
        resultado = self.reserva_repo.crear(reserva)
        self.assertEqual(resultado.id, 1)

        # Test obtener por id
        self.orm_mock.select.return_value = [reserva_data]
        resultado = self.reserva_repo.obtener_por_id(1)
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.usuario_id, 1)

        # Test listar activas
        self.orm_mock.select.return_value = [reserva_data]
        resultado = self.reserva_repo.listar_activas()
        self.assertEqual(len(resultado), 1)

        # Test cancelar reserva
        self.orm_mock.update.return_value = None
        self.reserva_repo.cancelar_reserva(1)
        self.orm_mock.update.assert_called()

    def test_multa_repository_operations(self):
        """Test operaciones básicas MultaRepository"""
        # Datos de test
        multa_data = {
            "id": 1,
            "usuario_id": 1,
            "prestamo_id": 1,
            "empleado_id": 1,
            "monto": 5000.0,
            "descripcion": "Retraso en devolución",
            "fecha_multa": "2023-01-16T00:00:00",
            "pagada": False,
        }

        # Test crear
        self.orm_mock.insert.return_value = 1
        multa = Multa(usuario_id=1, prestamo_id=1, monto=5000.0, descripcion="Test")
        resultado = self.multa_repo.crear(multa)
        self.assertEqual(resultado.id, 1)

        # Test obtener por id
        self.orm_mock.select.return_value = [multa_data]
        resultado = self.multa_repo.obtener_por_id(1)
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.monto, 5000.0)

        # Test listar no pagadas
        self.orm_mock.select.return_value = [multa_data]
        resultado = self.multa_repo.listar_no_pagadas()
        self.assertEqual(len(resultado), 1)
        self.assertFalse(resultado[0].pagada)

        # Test marcar como pagada
        self.orm_mock.update.return_value = None
        from datetime import date

        self.multa_repo.marcar_como_pagada(1, date.today())
        self.orm_mock.update.assert_called()

    def test_item_repository_operations(self):
        """Test operaciones básicas ItemBibliotecaRepository"""
        # Datos de test
        item_data = {
            "id": 1,
            "titulo": "El Quijote",
            "categoria": "libro",
            "autor": "Cervantes",
            "isbn": "978-1234567890",
            "descripcion": "Obra clásica",
            "estado": "disponible",
            "ubicacion": "A1-B2",
            "valor_reposicion": 25000.0,
            "fecha_adquisicion": "2023-01-01T12:00:00",
        }

        # Test crear
        self.orm_mock.insert.return_value = 1
        item = ItemBiblioteca(titulo="Test Book", categoria=CategoriaItem.LIBRO)
        resultado = self.item_repo.crear(item)
        self.assertEqual(resultado.id, 1)

        # Test obtener por id
        self.orm_mock.select.return_value = [item_data]
        resultado = self.item_repo.obtener_por_id(1)
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.titulo, "El Quijote")

        # Test buscar por título
        self.orm_mock.select.return_value = [item_data]
        resultado = self.item_repo.buscar_por_titulo("Quijote")
        self.assertEqual(len(resultado), 1)

        # Test buscar por categoría
        self.orm_mock.select.return_value = [item_data]
        resultado = self.item_repo.buscar_por_categoria(CategoriaItem.LIBRO)
        self.assertEqual(len(resultado), 1)

        # Test listar disponibles
        self.orm_mock.select.return_value = [item_data]
        resultado = self.item_repo.listar_disponibles()
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].estado, EstadoItem.DISPONIBLE)

    def test_entity_to_dict_conversions(self):
        """Test conversiones entity to dict"""
        # Prestamo
        prestamo = Prestamo(id=1, usuario_id=1, item_id=1, fecha_prestamo=datetime.now())
        resultado = self.prestamo_repo._entity_to_dict(prestamo)
        self.assertIn("usuario_id", resultado)
        self.assertIn("item_id", resultado)
        self.assertIn("fecha_prestamo", resultado)

        # Reserva
        reserva = Reserva(id=1, usuario_id=1, item_id=1, fecha_reserva=datetime.now())
        resultado = self.reserva_repo._entity_to_dict(reserva)
        self.assertIn("usuario_id", resultado)
        self.assertIn("item_id", resultado)
        self.assertIn("fecha_reserva", resultado)

        # Multa
        multa = Multa(id=1, usuario_id=1, prestamo_id=1, monto=100.0, fecha_multa=datetime.now())
        resultado = self.multa_repo._entity_to_dict(multa)
        self.assertIn("usuario_id", resultado)
        self.assertIn("prestamo_id", resultado)
        self.assertIn("monto", resultado)
        self.assertIn("fecha_multa", resultado)

        # Item
        item = ItemBiblioteca(id=1, titulo="Test", categoria=CategoriaItem.LIBRO)
        resultado = self.item_repo._entity_to_dict(item)
        self.assertIn("titulo", resultado)
        self.assertIn("categoria", resultado)


if __name__ == "__main__":
    unittest.main()
