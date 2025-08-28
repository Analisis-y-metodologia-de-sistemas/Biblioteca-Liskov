#!/usr/bin/env python3
"""
Tests unitarios para UsuarioService
"""

import sys
import os
import unittest
from unittest.mock import Mock, MagicMock
from datetime import datetime

# Agregar el path del proyecto
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.domain.entities import Usuario, TipoUsuario
from src.application.services import UsuarioService
from src.application.interfaces import IUsuarioRepository


class TestUsuarioService(unittest.TestCase):
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.mock_repo = Mock(spec=IUsuarioRepository)
        self.usuario_service = UsuarioService(self.mock_repo)
        
    def test_registrar_usuario_exitoso(self):
        """Test: Registro exitoso de usuario"""
        # Arrange
        self.mock_repo.obtener_por_email.return_value = None
        
        usuario_esperado = Usuario(
            id=1,
            nombre="Juan",
            apellido="Pérez",
            email="juan.perez@test.com",
            tipo=TipoUsuario.ALUMNO,
            numero_identificacion="12345678",
            telefono="+54-9-11-1234-5678"
        )
        
        self.mock_repo.crear.return_value = usuario_esperado
        
        # Act
        resultado = self.usuario_service.registrar_usuario(
            nombre="Juan",
            apellido="Pérez", 
            email="juan.perez@test.com",
            tipo=TipoUsuario.ALUMNO,
            numero_identificacion="12345678",
            telefono="+54-9-11-1234-5678"
        )
        
        # Assert
        self.assertEqual(resultado.nombre, "Juan")
        self.assertEqual(resultado.email, "juan.perez@test.com")
        self.assertEqual(resultado.tipo, TipoUsuario.ALUMNO)
        self.mock_repo.obtener_por_email.assert_called_once_with("juan.perez@test.com")
        self.mock_repo.crear.assert_called_once()
        
    def test_registrar_usuario_email_duplicado(self):
        """Test: Error al registrar usuario con email duplicado"""
        # Arrange
        usuario_existente = Usuario(
            id=1,
            nombre="Existente",
            apellido="Usuario",
            email="juan.perez@test.com",
            tipo=TipoUsuario.DOCENTE,
            numero_identificacion="87654321"
        )
        self.mock_repo.obtener_por_email.return_value = usuario_existente
        
        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.usuario_service.registrar_usuario(
                nombre="Juan",
                apellido="Pérez",
                email="juan.perez@test.com",
                tipo=TipoUsuario.ALUMNO,
                numero_identificacion="12345678"
            )
        
        self.assertIn("Ya existe un usuario con el email", str(context.exception))
        self.mock_repo.crear.assert_not_called()
        
    def test_buscar_usuario_por_email_encontrado(self):
        """Test: Búsqueda exitosa de usuario por email"""
        # Arrange
        usuario_esperado = Usuario(
            id=1,
            nombre="Juan",
            apellido="Pérez",
            email="juan.perez@test.com",
            tipo=TipoUsuario.ALUMNO,
            numero_identificacion="12345678"
        )
        self.mock_repo.obtener_por_email.return_value = usuario_esperado
        
        # Act
        resultado = self.usuario_service.buscar_usuario_por_email("juan.perez@test.com")
        
        # Assert
        self.assertEqual(resultado, usuario_esperado)
        self.mock_repo.obtener_por_email.assert_called_once_with("juan.perez@test.com")
        
    def test_buscar_usuario_por_email_no_encontrado(self):
        """Test: Usuario no encontrado por email"""
        # Arrange
        self.mock_repo.obtener_por_email.return_value = None
        
        # Act
        resultado = self.usuario_service.buscar_usuario_por_email("inexistente@test.com")
        
        # Assert
        self.assertIsNone(resultado)
        self.mock_repo.obtener_por_email.assert_called_once_with("inexistente@test.com")
        
    def test_listar_usuarios(self):
        """Test: Listar todos los usuarios"""
        # Arrange
        usuarios_esperados = [
            Usuario(id=1, nombre="Juan", apellido="Pérez", email="juan@test.com", 
                   tipo=TipoUsuario.ALUMNO, numero_identificacion="12345"),
            Usuario(id=2, nombre="María", apellido="González", email="maria@test.com",
                   tipo=TipoUsuario.DOCENTE, numero_identificacion="67890")
        ]
        self.mock_repo.listar_todos.return_value = usuarios_esperados
        
        # Act
        resultado = self.usuario_service.listar_usuarios()
        
        # Assert
        self.assertEqual(resultado, usuarios_esperados)
        self.assertEqual(len(resultado), 2)
        self.mock_repo.listar_todos.assert_called_once()
        
    def test_actualizar_usuario(self):
        """Test: Actualización de usuario"""
        # Arrange
        usuario = Usuario(
            id=1,
            nombre="Juan",
            apellido="Pérez",
            email="juan.perez@test.com",
            tipo=TipoUsuario.ALUMNO,
            numero_identificacion="12345678"
        )
        self.mock_repo.actualizar.return_value = usuario
        
        # Act
        resultado = self.usuario_service.actualizar_usuario(usuario)
        
        # Assert
        self.assertEqual(resultado, usuario)
        self.mock_repo.actualizar.assert_called_once_with(usuario)


if __name__ == '__main__':
    unittest.main()