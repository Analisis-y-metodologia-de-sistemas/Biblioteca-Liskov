#!/usr/bin/env python3
"""
Tests unitarios para ItemBibliotecaService
"""

import os
import sys
import unittest
from datetime import datetime
from unittest.mock import MagicMock, Mock

# Agregar el path del proyecto
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.application.interfaces import IItemBibliotecaRepository
from src.application.services import ItemBibliotecaService
from src.domain.entities import CategoriaItem, EstadoItem, ItemBiblioteca


class TestItemBibliotecaService(unittest.TestCase):

    def setUp(self):
        """Configuración inicial para cada test"""
        self.mock_repo = Mock(spec=IItemBibliotecaRepository)
        self.item_service = ItemBibliotecaService(self.mock_repo)

    def test_agregar_item_exitoso(self):
        """Test: Agregar item exitosamente"""
        # Arrange
        item_esperado = ItemBiblioteca(
            id=1,
            titulo="Python Programming",
            autor="Mark Lutz",
            isbn="978-1449355739",
            categoria=CategoriaItem.LIBRO,
            estado=EstadoItem.DISPONIBLE,
            descripcion="Comprehensive guide to Python",
            ubicacion="Tech-A1",
        )

        self.mock_repo.crear.return_value = item_esperado

        # Act
        resultado = self.item_service.agregar_item(
            titulo="Python Programming",
            categoria="libro",
            autor="Mark Lutz",
            isbn="978-1449355739",
            descripcion="Comprehensive guide to Python",
            ubicacion="Tech-A1",
        )

        # Assert
        self.assertEqual(resultado.titulo, "Python Programming")
        self.assertEqual(resultado.categoria, CategoriaItem.LIBRO)
        self.assertEqual(resultado.estado, EstadoItem.DISPONIBLE)
        self.mock_repo.crear.assert_called_once()

    def test_agregar_item_categoria_invalida(self):
        """Test: Error con categoría inválida"""
        # Act & Assert
        with self.assertRaises(ValueError):
            self.item_service.agregar_item(titulo="Test Book", categoria="categoria_inexistente", autor="Test Author")

        self.mock_repo.crear.assert_not_called()

    def test_buscar_por_titulo_encontrados(self):
        """Test: Búsqueda exitosa por título"""
        # Arrange
        items_esperados = [
            ItemBiblioteca(
                id=1,
                titulo="Python Programming",
                autor="Mark Lutz",
                categoria=CategoriaItem.LIBRO,
                estado=EstadoItem.DISPONIBLE,
            ),
            ItemBiblioteca(
                id=2,
                titulo="Python Crash Course",
                autor="Eric Matthes",
                categoria=CategoriaItem.LIBRO,
                estado=EstadoItem.DISPONIBLE,
            ),
        ]
        self.mock_repo.buscar_por_titulo.return_value = items_esperados

        # Act
        resultado = self.item_service.buscar_por_titulo("Python")

        # Assert
        self.assertEqual(resultado, items_esperados)
        self.assertEqual(len(resultado), 2)
        self.mock_repo.buscar_por_titulo.assert_called_once_with("Python")

    def test_buscar_por_titulo_no_encontrados(self):
        """Test: Búsqueda sin resultados"""
        # Arrange
        self.mock_repo.buscar_por_titulo.return_value = []

        # Act
        resultado = self.item_service.buscar_por_titulo("Inexistente")

        # Assert
        self.assertEqual(resultado, [])
        self.mock_repo.buscar_por_titulo.assert_called_once_with("Inexistente")

    def test_buscar_por_autor(self):
        """Test: Búsqueda por autor"""
        # Arrange
        items_esperados = [
            ItemBiblioteca(
                id=1,
                titulo="Clean Code",
                autor="Robert C. Martin",
                categoria=CategoriaItem.LIBRO,
                estado=EstadoItem.DISPONIBLE,
            )
        ]
        self.mock_repo.buscar_por_autor.return_value = items_esperados

        # Act
        resultado = self.item_service.buscar_por_autor("Robert C. Martin")

        # Assert
        self.assertEqual(resultado, items_esperados)
        self.mock_repo.buscar_por_autor.assert_called_once_with("Robert C. Martin")

    def test_listar_por_categoria(self):
        """Test: Listar items por categoría"""
        # Arrange
        items_esperados = [
            ItemBiblioteca(id=1, titulo="Scientific American", categoria=CategoriaItem.REVISTA, estado=EstadoItem.DISPONIBLE)
        ]
        self.mock_repo.listar_por_categoria.return_value = items_esperados

        # Act
        resultado = self.item_service.listar_por_categoria("revista")

        # Assert
        self.assertEqual(resultado, items_esperados)
        self.mock_repo.listar_por_categoria.assert_called_once_with("revista")

    def test_listar_disponibles(self):
        """Test: Listar solo items disponibles"""
        # Arrange
        todos_los_items = [
            ItemBiblioteca(id=1, titulo="Disponible", categoria=CategoriaItem.LIBRO, estado=EstadoItem.DISPONIBLE),
            ItemBiblioteca(id=2, titulo="Prestado", categoria=CategoriaItem.LIBRO, estado=EstadoItem.PRESTADO),
            ItemBiblioteca(id=3, titulo="También Disponible", categoria=CategoriaItem.REVISTA, estado=EstadoItem.DISPONIBLE),
        ]
        self.mock_repo.listar_todos.return_value = todos_los_items

        # Act
        resultado = self.item_service.listar_disponibles()

        # Assert
        self.assertEqual(len(resultado), 2)
        self.assertTrue(all(item.estado == EstadoItem.DISPONIBLE for item in resultado))
        self.mock_repo.listar_todos.assert_called_once()

    def test_cambiar_estado_item_exitoso(self):
        """Test: Cambio de estado exitoso"""
        # Arrange
        item_original = ItemBiblioteca(id=1, titulo="Test Book", categoria=CategoriaItem.LIBRO, estado=EstadoItem.DISPONIBLE)

        item_actualizado = ItemBiblioteca(id=1, titulo="Test Book", categoria=CategoriaItem.LIBRO, estado=EstadoItem.PRESTADO)

        self.mock_repo.obtener_por_id.return_value = item_original
        self.mock_repo.actualizar.return_value = item_actualizado

        # Act
        resultado = self.item_service.cambiar_estado_item(1, EstadoItem.PRESTADO)

        # Assert
        self.assertEqual(resultado.estado, EstadoItem.PRESTADO)
        self.mock_repo.obtener_por_id.assert_called_once_with(1)
        self.mock_repo.actualizar.assert_called_once()

    def test_cambiar_estado_item_no_encontrado(self):
        """Test: Error al cambiar estado de item inexistente"""
        # Arrange
        self.mock_repo.obtener_por_id.return_value = None

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.item_service.cambiar_estado_item(999, EstadoItem.PRESTADO)

        self.assertIn("No se encontró el item con ID: 999", str(context.exception))
        self.mock_repo.actualizar.assert_not_called()


if __name__ == "__main__":
    unittest.main()
