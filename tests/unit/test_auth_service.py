#!/usr/bin/env python3
"""
Tests unitarios para AuthService
"""

import os
import sys
import unittest
from datetime import datetime
from unittest.mock import MagicMock, Mock

# Agregar el path del proyecto
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.application.auth_service import AuthService
from src.application.interfaces import IEmpleadoRepository
from src.domain.entities import Empleado, SesionEmpleado


class TestAuthService(unittest.TestCase):

    def setUp(self):
        """Configuración inicial para cada test"""
        self.mock_repo = Mock(spec=IEmpleadoRepository)
        self.auth_service = AuthService(self.mock_repo)

    def test_hash_password(self):
        """Test: Hash de contraseña"""
        # Act
        hash1 = self.auth_service.hash_password("test123")
        hash2 = self.auth_service.hash_password("test123")
        hash3 = self.auth_service.hash_password("different")

        # Assert
        self.assertEqual(hash1, hash2)  # Misma contraseña = mismo hash
        self.assertNotEqual(hash1, hash3)  # Diferente contraseña = hash diferente
        self.assertTrue(len(hash1) > 0)  # Hash no vacío

    def test_verificar_password_correcto(self):
        """Test: Verificación correcta de contraseña"""
        # Arrange
        password = "test123"
        hash_password = self.auth_service.hash_password(password)

        # Act
        resultado = self.auth_service.verificar_password(password, hash_password)

        # Assert
        self.assertTrue(resultado)

    def test_verificar_password_incorrecto(self):
        """Test: Verificación incorrecta de contraseña"""
        # Arrange
        password_correcta = "test123"
        password_incorrecta = "wrong"
        hash_password = self.auth_service.hash_password(password_correcta)

        # Act
        resultado = self.auth_service.verificar_password(password_incorrecta, hash_password)

        # Assert
        self.assertFalse(resultado)

    def test_login_exitoso(self):
        """Test: Login exitoso"""
        # Arrange
        empleado = Empleado(
            id=1,
            nombre="Ana",
            apellido="Rodriguez",
            email="ana@biblioteca.com",
            usuario_sistema="arodriguez",
            password_hash=self.auth_service.hash_password("1234"),
            cargo="Bibliotecario Jefe",
            activo=True,
        )

        self.mock_repo.obtener_por_usuario_sistema.return_value = empleado

        # Act
        resultado = self.auth_service.login("arodriguez", "1234")

        # Assert
        self.assertTrue(resultado)
        self.assertIsNotNone(self.auth_service.get_empleado_actual())
        self.assertTrue(self.auth_service.esta_logueado())

        empleado_logueado = self.auth_service.get_empleado_actual()
        self.assertEqual(empleado_logueado.usuario_sistema, "arodriguez")

        self.mock_repo.obtener_por_usuario_sistema.assert_called_once_with("arodriguez")

    def test_login_usuario_inexistente(self):
        """Test: Login con usuario inexistente"""
        # Arrange
        self.mock_repo.obtener_por_usuario_sistema.return_value = None

        # Act
        resultado = self.auth_service.login("inexistente", "1234")

        # Assert
        self.assertFalse(resultado)
        self.assertIsNone(self.auth_service.get_empleado_actual())
        self.assertFalse(self.auth_service.esta_logueado())

    def test_login_usuario_inactivo(self):
        """Test: Login con usuario inactivo"""
        # Arrange
        empleado_inactivo = Empleado(
            id=1,
            nombre="Test",
            apellido="User",
            usuario_sistema="test",
            password_hash=self.auth_service.hash_password("1234"),
            activo=False,  # Inactivo
        )

        self.mock_repo.obtener_por_usuario_sistema.return_value = empleado_inactivo

        # Act
        resultado = self.auth_service.login("test", "1234")

        # Assert
        self.assertFalse(resultado)
        self.assertIsNone(self.auth_service.get_empleado_actual())
        self.assertFalse(self.auth_service.esta_logueado())

    def test_login_password_incorrecta(self):
        """Test: Login con contraseña incorrecta"""
        # Arrange
        empleado = Empleado(
            id=1,
            nombre="Test",
            apellido="User",
            usuario_sistema="test",
            password_hash=self.auth_service.hash_password("1234"),
            activo=True,
        )

        self.mock_repo.obtener_por_usuario_sistema.return_value = empleado

        # Act
        resultado = self.auth_service.login("test", "wrong_password")

        # Assert
        self.assertFalse(resultado)
        self.assertIsNone(self.auth_service.get_empleado_actual())
        self.assertFalse(self.auth_service.esta_logueado())

    def test_logout(self):
        """Test: Logout exitoso"""
        # Arrange - Primero hacer login
        empleado = Empleado(
            id=1,
            nombre="Test",
            apellido="User",
            usuario_sistema="test",
            password_hash=self.auth_service.hash_password("1234"),
            activo=True,
        )

        self.mock_repo.obtener_por_usuario_sistema.return_value = empleado
        self.auth_service.login("test", "1234")

        # Verificar que está logueado
        self.assertTrue(self.auth_service.esta_logueado())

        # Act - Hacer logout
        self.auth_service.logout()

        # Assert
        self.assertFalse(self.auth_service.esta_logueado())
        self.assertIsNone(self.auth_service.get_empleado_actual())
        self.assertIsNone(self.auth_service.get_sesion_actual())

    def test_crear_empleado_exitoso(self):
        """Test: Crear empleado exitosamente"""
        # Arrange
        self.mock_repo.obtener_por_usuario_sistema.return_value = None  # Usuario no existe

        empleado_creado = Empleado(
            id=1,
            nombre="Nuevo",
            apellido="Empleado",
            email="nuevo@biblioteca.com",
            usuario_sistema="nuevo",
            password_hash=self.auth_service.hash_password("password"),
            cargo="Bibliotecario",
        )

        self.mock_repo.crear.return_value = empleado_creado

        # Act
        resultado = self.auth_service.crear_empleado(
            nombre="Nuevo",
            apellido="Empleado",
            email="nuevo@biblioteca.com",
            usuario_sistema="nuevo",
            password="password",
            cargo="Bibliotecario",
        )

        # Assert
        self.assertEqual(resultado.nombre, "Nuevo")
        self.assertEqual(resultado.usuario_sistema, "nuevo")
        self.assertEqual(resultado.cargo, "Bibliotecario")

        self.mock_repo.obtener_por_usuario_sistema.assert_called_once_with("nuevo")
        self.mock_repo.crear.assert_called_once()

    def test_crear_empleado_usuario_existente(self):
        """Test: Error al crear empleado con usuario existente"""
        # Arrange
        empleado_existente = Empleado(id=1, nombre="Existente", usuario_sistema="existente")

        self.mock_repo.obtener_por_usuario_sistema.return_value = empleado_existente

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.auth_service.crear_empleado(
                nombre="Nuevo", apellido="Empleado", email="nuevo@test.com", usuario_sistema="existente", password="password"
            )

        self.assertIn("ya existe", str(context.exception))
        self.mock_repo.crear.assert_not_called()

    def test_cambiar_password_exitoso(self):
        """Test: Cambio de contraseña exitoso"""
        # Arrange
        password_actual = "old_pass"
        password_nuevo = "new_pass"

        empleado = Empleado(
            id=1, nombre="Test", usuario_sistema="test", password_hash=self.auth_service.hash_password(password_actual)
        )

        self.mock_repo.obtener_por_id.return_value = empleado

        # Act
        resultado = self.auth_service.cambiar_password(1, password_actual, password_nuevo)

        # Assert
        self.assertTrue(resultado)
        self.mock_repo.obtener_por_id.assert_called_once_with(1)
        self.mock_repo.actualizar.assert_called_once()

        # Verificar que el hash de contraseña cambió
        args_call = self.mock_repo.actualizar.call_args[0][0]
        self.assertTrue(self.auth_service.verificar_password(password_nuevo, args_call.password_hash))

    def test_cambiar_password_empleado_inexistente(self):
        """Test: Error al cambiar contraseña de empleado inexistente"""
        # Arrange
        self.mock_repo.obtener_por_id.return_value = None

        # Act
        resultado = self.auth_service.cambiar_password(999, "old", "new")

        # Assert
        self.assertFalse(resultado)
        self.mock_repo.actualizar.assert_not_called()

    def test_cambiar_password_actual_incorrecta(self):
        """Test: Error con contraseña actual incorrecta"""
        # Arrange
        empleado = Empleado(id=1, nombre="Test", password_hash=self.auth_service.hash_password("correct_old"))

        self.mock_repo.obtener_por_id.return_value = empleado

        # Act
        resultado = self.auth_service.cambiar_password(1, "wrong_old", "new_pass")

        # Assert
        self.assertFalse(resultado)
        self.mock_repo.actualizar.assert_not_called()

    def test_listar_empleados_activos(self):
        """Test: Listar empleados activos"""
        # Arrange
        empleados_esperados = [Empleado(id=1, nombre="Ana", activo=True), Empleado(id=2, nombre="Carlos", activo=True)]

        self.mock_repo.listar_activos.return_value = empleados_esperados

        # Act
        resultado = self.auth_service.listar_empleados_activos()

        # Assert
        self.assertEqual(resultado, empleados_esperados)
        self.mock_repo.listar_activos.assert_called_once()


if __name__ == "__main__":
    unittest.main()
