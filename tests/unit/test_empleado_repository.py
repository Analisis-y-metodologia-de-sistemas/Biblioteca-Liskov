import unittest
from unittest.mock import Mock, MagicMock
from datetime import datetime
from src.infrastructure.repositories import EmpleadoRepository
from src.domain.entities import Empleado
from src.infrastructure.database import ORM


class TestEmpleadoRepository(unittest.TestCase):
    
    def setUp(self):
        self.orm_mock = Mock(spec=ORM)
        self.repository = EmpleadoRepository(self.orm_mock)
        
        self.empleado_data = {
            'id': 1,
            'nombre': 'Ana',
            'apellido': 'García',
            'email': 'ana.garcia@biblioteca.com',
            'usuario_sistema': 'agarcia',
            'password_hash': 'hashed_password_123',
            'cargo': 'Bibliotecario',
            'turno': 'mañana',
            'activo': True,
            'fecha_registro': '2023-01-01T09:00:00'
        }
        
        self.empleado = Empleado(
            id=1,
            nombre='Ana',
            apellido='García',
            email='ana.garcia@biblioteca.com',
            usuario_sistema='agarcia',
            password_hash='hashed_password_123',
            cargo='Bibliotecario',
            turno='mañana',
            activo=True,
            fecha_registro=datetime(2023, 1, 1, 9, 0, 0)
        )
    
    def test_crear_empleado(self):
        self.orm_mock.insert.return_value = 1
        empleado_sin_id = Empleado(
            nombre='Ana',
            apellido='García',
            email='ana.garcia@biblioteca.com',
            usuario_sistema='agarcia',
            password_hash='hashed_password_123',
            cargo='Bibliotecario',
            turno='mañana'
        )
        
        resultado = self.repository.crear(empleado_sin_id)
        
        self.orm_mock.insert.assert_called_once()
        self.assertEqual(resultado.id, 1)
        self.assertEqual(resultado.nombre, 'Ana')
        self.assertEqual(resultado.usuario_sistema, 'agarcia')
    
    def test_obtener_por_id_existente(self):
        self.orm_mock.select.return_value = [self.empleado_data]
        
        resultado = self.repository.obtener_por_id(1)
        
        self.orm_mock.select.assert_called_once_with("empleados", "id = ?", (1,))
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.id, 1)
        self.assertEqual(resultado.nombre, 'Ana')
        self.assertEqual(resultado.usuario_sistema, 'agarcia')
    
    def test_obtener_por_id_no_existente(self):
        self.orm_mock.select.return_value = []
        
        resultado = self.repository.obtener_por_id(999)
        
        self.assertIsNone(resultado)
    
    def test_obtener_por_usuario_sistema_existente(self):
        self.orm_mock.select.return_value = [self.empleado_data]
        
        resultado = self.repository.obtener_por_usuario_sistema('agarcia')
        
        self.orm_mock.select.assert_called_once_with("empleados", "usuario_sistema = ?", ('agarcia',))
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.usuario_sistema, 'agarcia')
    
    def test_obtener_por_usuario_sistema_no_existente(self):
        self.orm_mock.select.return_value = []
        
        resultado = self.repository.obtener_por_usuario_sistema('noexiste')
        
        self.assertIsNone(resultado)
    
    def test_eliminar_empleado(self):
        self.orm_mock.delete.return_value = 1
        
        resultado = self.repository.eliminar(1)
        
        self.orm_mock.delete.assert_called_once_with("empleados", "id = ?", (1,))
        self.assertTrue(resultado)
    
    def test_listar_empleados_activos(self):
        self.orm_mock.select.return_value = [self.empleado_data, {**self.empleado_data, 'id': 2, 'usuario_sistema': 'otro'}]
        
        resultado = self.repository.listar_activos()
        
        self.orm_mock.select.assert_called_once_with("empleados", "activo = 1")
        self.assertEqual(len(resultado), 2)
        for empleado in resultado:
            self.assertTrue(empleado.activo)
    
    def test_listar_todos(self):
        self.orm_mock.select.return_value = [
            self.empleado_data, 
            {**self.empleado_data, 'id': 2, 'usuario_sistema': 'otro', 'activo': False}
        ]
        
        resultado = self.repository.listar_todos()
        
        self.orm_mock.select.assert_called_once_with("empleados")
        self.assertEqual(len(resultado), 2)
        self.assertTrue(resultado[0].activo)
        self.assertFalse(resultado[1].activo)
    
    def test_actualizar_empleado(self):
        self.orm_mock.update.return_value = None
        
        resultado = self.repository.actualizar(self.empleado)
        
        self.orm_mock.update.assert_called_once()
        self.assertEqual(resultado, self.empleado)
    
    def test_empleado_activo_desactivo_diferentes(self):
        empleado_activo = self.empleado_data
        empleado_inactivo = {**self.empleado_data, 'id': 2, 'usuario_sistema': 'otro', 'activo': False}
        
        self.orm_mock.select.return_value = [empleado_activo, empleado_inactivo]
        
        resultado = self.repository.listar_todos()
        
        self.assertEqual(len(resultado), 2)
        self.assertTrue(resultado[0].activo)
        self.assertFalse(resultado[1].activo)
    
    def test_row_to_entity_conversion(self):
        resultado = self.repository._row_to_entity(self.empleado_data)
        
        self.assertEqual(resultado.id, 1)
        self.assertEqual(resultado.nombre, 'Ana')
        self.assertEqual(resultado.apellido, 'García')
        self.assertEqual(resultado.email, 'ana.garcia@biblioteca.com')
        self.assertEqual(resultado.usuario_sistema, 'agarcia')
        self.assertEqual(resultado.password_hash, 'hashed_password_123')
        self.assertTrue(resultado.activo)
        self.assertEqual(resultado.fecha_registro, datetime(2023, 1, 1, 9, 0, 0))
    
    def test_entity_to_dict_conversion(self):
        resultado = self.repository._entity_to_dict(self.empleado)
        
        expected_keys = ['nombre', 'apellido', 'email', 'usuario_sistema', 'password_hash', 'activo']
        for key in expected_keys:
            self.assertIn(key, resultado)
        
        self.assertEqual(resultado['nombre'], 'Ana')
        self.assertEqual(resultado['apellido'], 'García')
        self.assertEqual(resultado['email'], 'ana.garcia@biblioteca.com')
        self.assertEqual(resultado['usuario_sistema'], 'agarcia')
        self.assertEqual(resultado['password_hash'], 'hashed_password_123')
        self.assertTrue(resultado['activo'])


if __name__ == '__main__':
    unittest.main()