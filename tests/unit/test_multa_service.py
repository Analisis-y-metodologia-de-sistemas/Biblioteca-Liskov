#!/usr/bin/env python3
"""
Tests unitarios para MultaService
"""

import os
import sys
import unittest
from datetime import datetime
from unittest.mock import Mock

# Agregar el path del proyecto
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.application.interfaces import IMultaRepository, IUsuarioRepository
from src.application.services import MultaService
from src.domain.entities import Multa


class TestMultaService(unittest.TestCase):

    def setUp(self):
        """Configuración inicial para cada test"""
        self.mock_multa_repo = Mock(spec=IMultaRepository)
        self.mock_usuario_repo = Mock(spec=IUsuarioRepository)

        self.multa_service = MultaService(self.mock_multa_repo, self.mock_usuario_repo)

    def test_pagar_multa_exitoso(self):
        """Test: Pagar multa exitosamente"""
        # Arrange
        multa = Multa(
            id=1,
            usuario_id=1,
            prestamo_id=1,
            empleado_id=1,
            monto=150.0,
            descripcion="Devolución tardía: 3 días de atraso",
            fecha_multa=datetime.now(),
            pagada=False,
        )

        multa_pagada = Multa(
            id=1,
            usuario_id=1,
            prestamo_id=1,
            empleado_id=1,
            monto=150.0,
            descripcion="Devolución tardía: 3 días de atraso",
            fecha_multa=multa.fecha_multa,
            pagada=True,
        )

        self.mock_multa_repo.obtener_por_id.return_value = multa
        self.mock_multa_repo.actualizar.return_value = multa_pagada

        # Act
        resultado = self.multa_service.pagar_multa(1)

        # Assert
        self.assertTrue(resultado.pagada)
        self.mock_multa_repo.obtener_por_id.assert_called_once_with(1)
        self.mock_multa_repo.actualizar.assert_called_once()

    def test_pagar_multa_inexistente(self):
        """Test: Error al pagar multa inexistente"""
        # Arrange
        self.mock_multa_repo.obtener_por_id.return_value = None

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.multa_service.pagar_multa(999)

        self.assertIn("No se encontró la multa con ID: 999", str(context.exception))
        self.mock_multa_repo.actualizar.assert_not_called()

    def test_pagar_multa_ya_pagada(self):
        """Test: Error al pagar multa ya pagada"""
        # Arrange
        multa_ya_pagada = Multa(
            id=1,
            usuario_id=1,
            prestamo_id=1,
            empleado_id=1,
            monto=150.0,
            descripcion="Devolución tardía",
            fecha_multa=datetime.now(),
            pagada=True,  # Ya está pagada
        )

        self.mock_multa_repo.obtener_por_id.return_value = multa_ya_pagada

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.multa_service.pagar_multa(1)

        self.assertIn("ya fue pagada", str(context.exception))
        self.mock_multa_repo.actualizar.assert_not_called()

    def test_listar_multas_pendientes(self):
        """Test: Listar multas pendientes (no pagadas)"""
        # Arrange
        multas_esperadas = [
            Multa(id=1, usuario_id=1, monto=100.0, pagada=False),
            Multa(id=2, usuario_id=2, monto=200.0, pagada=False),
        ]

        self.mock_multa_repo.listar_no_pagadas.return_value = multas_esperadas

        # Act
        resultado = self.multa_service.listar_multas_pendientes()

        # Assert
        self.assertEqual(resultado, multas_esperadas)
        self.assertEqual(len(resultado), 2)
        self.assertTrue(all(not multa.pagada for multa in resultado))
        self.mock_multa_repo.listar_no_pagadas.assert_called_once()

    def test_listar_multas_usuario(self):
        """Test: Listar multas de un usuario específico"""
        # Arrange
        multas_esperadas = [
            Multa(id=1, usuario_id=1, monto=100.0, pagada=False),
            Multa(id=2, usuario_id=1, monto=150.0, pagada=True),
            Multa(id=3, usuario_id=1, monto=75.0, pagada=False),
        ]

        self.mock_multa_repo.listar_por_usuario.return_value = multas_esperadas

        # Act
        resultado = self.multa_service.listar_multas_usuario(1)

        # Assert
        self.assertEqual(resultado, multas_esperadas)
        self.assertEqual(len(resultado), 3)
        self.assertTrue(all(multa.usuario_id == 1 for multa in resultado))
        self.mock_multa_repo.listar_por_usuario.assert_called_once_with(1)

    def test_listar_multas_usuario_sin_multas(self):
        """Test: Listar multas de usuario sin multas"""
        # Arrange
        self.mock_multa_repo.listar_por_usuario.return_value = []

        # Act
        resultado = self.multa_service.listar_multas_usuario(1)

        # Assert
        self.assertEqual(resultado, [])
        self.mock_multa_repo.listar_por_usuario.assert_called_once_with(1)


if __name__ == "__main__":
    unittest.main()
