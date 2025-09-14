#!/usr/bin/env python3
"""
Tests de integración para el sistema completo
"""

import os
import shutil
import sys
import tempfile
import unittest
from datetime import datetime, timedelta

# Agregar el path del proyecto
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.container import Container
from src.domain.entities import CategoriaItem, EstadoItem, TipoUsuario


class TestSistemaCompleto(unittest.TestCase):

    def setUp(self):
        """Configuración inicial - crear BD temporal para tests"""
        # Crear directorio temporal para la BD de prueba
        self.temp_dir = tempfile.mkdtemp()
        self.temp_db_path = os.path.join(self.temp_dir, "test_biblioteca.db")

        # Configurar container con BD temporal
        self.container = Container()
        self.container._config.database.path = self.temp_db_path
        self.container._db_connection = None  # Forzar recreación con nueva ruta
        self.container._orm = None

        # Obtener servicios
        self.usuario_service = self.container.get_usuario_service()
        self.item_service = self.container.get_item_service()
        self.prestamo_service = self.container.get_prestamo_service()
        self.reserva_service = self.container.get_reserva_service()
        self.multa_service = self.container.get_multa_service()
        self.auth_service = self.container.get_auth_service()

    def tearDown(self):
        """Limpieza después de cada test"""
        # Eliminar BD temporal
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_flujo_completo_prestamo_con_devolucion_tardia(self):
        """Test: Flujo completo desde registro hasta devolución tardía con multa"""

        # 1. Crear empleado para autenticación
        empleado = self.auth_service.crear_empleado(
            nombre="Test",
            apellido="Bibliotecario",
            email="test@biblioteca.com",
            usuario_sistema="testuser",
            password="test123",
            cargo="Bibliotecario",
        )

        # Autenticar empleado
        login_exitoso = self.auth_service.login("testuser", "test123")
        self.assertTrue(login_exitoso)

        empleado_actual = self.auth_service.get_empleado_actual()
        self.assertIsNotNone(empleado_actual)

        # 2. Registrar usuario
        usuario = self.usuario_service.registrar_usuario(
            nombre="Juan",
            apellido="Pérez",
            email="juan.perez@test.com",
            tipo=TipoUsuario.ALUMNO,
            numero_identificacion="12345678",
            telefono="+54-9-11-1234-5678",
        )

        self.assertEqual(usuario.nombre, "Juan")
        self.assertEqual(usuario.email, "juan.perez@test.com")
        self.assertEqual(usuario.tipo, TipoUsuario.ALUMNO)

        # 3. Agregar item
        item = self.item_service.agregar_item(
            titulo="Python Programming",
            categoria="libro",
            autor="Mark Lutz",
            isbn="978-1449355739",
            descripcion="Comprehensive guide to Python",
            ubicacion="Tech-A1",
        )

        self.assertEqual(item.titulo, "Python Programming")
        self.assertEqual(item.estado, EstadoItem.DISPONIBLE)

        # 4. Realizar préstamo
        prestamo = self.prestamo_service.realizar_prestamo(
            usuario_id=usuario.id, item_id=item.id, empleado_id=empleado_actual.id, dias_prestamo=15
        )

        self.assertEqual(prestamo.usuario_id, usuario.id)
        self.assertEqual(prestamo.item_id, item.id)
        self.assertEqual(prestamo.empleado_id, empleado_actual.id)
        self.assertTrue(prestamo.activo)

        # Verificar que el item cambió de estado
        item_actualizado = self.item_service.item_repo.obtener_por_id(item.id)
        self.assertEqual(item_actualizado.estado, EstadoItem.PRESTADO)

        # 5. Simular devolución tardía modificando fecha de vencimiento
        prestamo_repo = self.container.get_prestamo_repository()
        prestamo_bd = prestamo_repo.obtener_por_id(prestamo.id)

        # Modificar fecha de vencimiento para que esté vencido
        prestamo_bd.fecha_devolucion_esperada = datetime.now() - timedelta(days=3)
        prestamo_repo.actualizar(prestamo_bd)

        # 6. Devolver item (tardíamente)
        prestamo_devuelto = self.prestamo_service.devolver_item(prestamo.id, "Devolución tardía")

        self.assertFalse(prestamo_devuelto.activo)
        self.assertIsNotNone(prestamo_devuelto.fecha_devolucion_real)

        # 7. Verificar que se creó la multa automáticamente
        multas_usuario = self.multa_service.listar_multas_usuario(usuario.id)
        self.assertEqual(len(multas_usuario), 1)

        multa = multas_usuario[0]
        self.assertEqual(multa.usuario_id, usuario.id)
        self.assertEqual(multa.prestamo_id, prestamo.id)
        self.assertEqual(multa.empleado_id, empleado_actual.id)
        self.assertFalse(multa.pagada)
        self.assertTrue(multa.monto > 0)  # Debe tener monto por atraso

        # Verificar que el item volvió a estar disponible
        item_final = self.item_service.item_repo.obtener_por_id(item.id)
        self.assertEqual(item_final.estado, EstadoItem.DISPONIBLE)

        # 8. Pagar multa
        multa_pagada = self.multa_service.pagar_multa(multa.id)
        self.assertTrue(multa_pagada.pagada)

        # 9. Verificar que no hay multas pendientes
        multas_pendientes = self.multa_service.listar_multas_pendientes()
        self.assertEqual(len(multas_pendientes), 0)

    def test_flujo_reserva_completo(self):
        """Test: Flujo completo de reservas"""

        # Crear empleado y autenticar
        empleado = self.auth_service.crear_empleado(
            nombre="Test", apellido="Empleado", email="test2@biblioteca.com", usuario_sistema="test2", password="pass123"
        )

        self.auth_service.login("test2", "pass123")
        empleado_actual = self.auth_service.get_empleado_actual()

        # Crear usuario
        usuario = self.usuario_service.registrar_usuario(
            nombre="María",
            apellido="González",
            email="maria@test.com",
            tipo=TipoUsuario.DOCENTE,
            numero_identificacion="87654321",
        )

        # Crear item
        item = self.item_service.agregar_item(titulo="Clean Code", categoria="libro", autor="Robert C. Martin")

        # Cambiar estado del item a prestado (para poder reservar)
        item_prestado = self.item_service.cambiar_estado_item(item.id, EstadoItem.PRESTADO)
        self.assertEqual(item_prestado.estado, EstadoItem.PRESTADO)

        # Realizar reserva
        reserva = self.reserva_service.realizar_reserva(
            usuario_id=usuario.id, item_id=item.id, empleado_id=empleado_actual.id, dias_expiracion=3
        )

        self.assertEqual(reserva.usuario_id, usuario.id)
        self.assertEqual(reserva.item_id, item.id)
        self.assertEqual(reserva.empleado_id, empleado_actual.id)
        self.assertTrue(reserva.activa)

        # Listar reservas activas
        reservas_activas = self.reserva_service.listar_reservas_activas()
        self.assertEqual(len(reservas_activas), 1)
        self.assertEqual(reservas_activas[0].id, reserva.id)

        # Cancelar reserva
        reserva_cancelada = self.reserva_service.cancelar_reserva(reserva.id)
        self.assertFalse(reserva_cancelada.activa)

        # Verificar que no hay reservas activas
        reservas_activas_final = self.reserva_service.listar_reservas_activas()
        self.assertEqual(len(reservas_activas_final), 0)

    def test_busqueda_y_filtros(self):
        """Test: Funcionalidades de búsqueda y filtros"""

        # Crear varios items de diferentes categorías
        libro1 = self.item_service.agregar_item(titulo="Python Crash Course", categoria="libro", autor="Eric Matthes")

        libro2 = self.item_service.agregar_item(
            titulo="JavaScript: The Good Parts", categoria="libro", autor="Douglas Crockford"
        )

        revista = self.item_service.agregar_item(titulo="Scientific American", categoria="revista", autor="Varios")

        dvd = self.item_service.agregar_item(titulo="Cosmos Documentary", categoria="dvd", autor="Neil deGrasse Tyson")

        # Test búsqueda por título
        resultados_python = self.item_service.buscar_por_titulo("Python")
        self.assertEqual(len(resultados_python), 1)
        self.assertEqual(resultados_python[0].titulo, "Python Crash Course")

        # Test búsqueda por autor
        resultados_matthes = self.item_service.buscar_por_autor("Eric Matthes")
        self.assertEqual(len(resultados_matthes), 1)
        self.assertEqual(resultados_matthes[0].autor, "Eric Matthes")

        # Test filtro por categoría
        libros = self.item_service.listar_por_categoria("libro")
        self.assertEqual(len(libros), 2)

        revistas = self.item_service.listar_por_categoria("revista")
        self.assertEqual(len(revistas), 1)
        self.assertEqual(revistas[0].categoria, CategoriaItem.REVISTA)

        dvds = self.item_service.listar_por_categoria("dvd")
        self.assertEqual(len(dvds), 1)
        self.assertEqual(dvds[0].categoria, CategoriaItem.DVD)

        # Test listar items disponibles
        items_disponibles = self.item_service.listar_disponibles()
        self.assertEqual(len(items_disponibles), 4)
        self.assertTrue(all(item.estado == EstadoItem.DISPONIBLE for item in items_disponibles))

    def test_autenticacion_completa(self):
        """Test: Sistema completo de autenticación"""

        # Crear empleado
        empleado = self.auth_service.crear_empleado(
            nombre="Admin",
            apellido="Biblioteca",
            email="admin@biblioteca.com",
            usuario_sistema="admin",
            password="admin123",
            cargo="Bibliotecario Jefe",
        )

        # Verificar que no está logueado inicialmente
        self.assertFalse(self.auth_service.esta_logueado())
        self.assertIsNone(self.auth_service.get_empleado_actual())

        # Login exitoso
        login_result = self.auth_service.login("admin", "admin123")
        self.assertTrue(login_result)

        # Verificar que está logueado
        self.assertTrue(self.auth_service.esta_logueado())
        empleado_logueado = self.auth_service.get_empleado_actual()
        self.assertIsNotNone(empleado_logueado)
        self.assertEqual(empleado_logueado.usuario_sistema, "admin")
        self.assertEqual(empleado_logueado.cargo, "Bibliotecario Jefe")

        # Verificar sesión activa
        sesion = self.auth_service.get_sesion_actual()
        self.assertIsNotNone(sesion)
        self.assertTrue(sesion.activa)

        # Cambiar contraseña
        cambio_exitoso = self.auth_service.cambiar_password(empleado.id, "admin123", "nueva_password")
        self.assertTrue(cambio_exitoso)

        # Logout
        self.auth_service.logout()
        self.assertFalse(self.auth_service.esta_logueado())
        self.assertIsNone(self.auth_service.get_empleado_actual())

        # Login con nueva contraseña
        login_nueva = self.auth_service.login("admin", "nueva_password")
        self.assertTrue(login_nueva)

        # Login fallido con contraseña anterior
        self.auth_service.logout()
        login_fallido = self.auth_service.login("admin", "admin123")
        self.assertFalse(login_fallido)

    def test_validaciones_y_restricciones(self):
        """Test: Validaciones y restricciones del sistema"""

        # Crear empleado para operaciones
        empleado = self.auth_service.crear_empleado(
            nombre="Test", apellido="User", email="test@test.com", usuario_sistema="test", password="test"
        )
        self.auth_service.login("test", "test")
        empleado_actual = self.auth_service.get_empleado_actual()

        # Test: Email duplicado en usuarios
        usuario1 = self.usuario_service.registrar_usuario(
            nombre="User1", apellido="Test", email="duplicate@test.com", tipo=TipoUsuario.ALUMNO, numero_identificacion="123"
        )

        with self.assertRaises(ValueError):
            self.usuario_service.registrar_usuario(
                nombre="User2",
                apellido="Test",
                email="duplicate@test.com",
                tipo=TipoUsuario.DOCENTE,
                numero_identificacion="456",
            )

        # Test: Usuario del sistema duplicado en empleados
        with self.assertRaises(ValueError):
            self.auth_service.crear_empleado(
                nombre="Otro",
                apellido="Empleado",
                email="otro@test.com",
                usuario_sistema="test",
                password="pass",  # Usuario ya existe
            )

        # Test: Préstamo con usuario inexistente
        item = self.item_service.agregar_item(titulo="Test Book", categoria="libro")

        with self.assertRaises(ValueError):
            self.prestamo_service.realizar_prestamo(
                usuario_id=9999, item_id=item.id, empleado_id=empleado_actual.id  # Usuario inexistente
            )

        # Test: Préstamo con item inexistente
        with self.assertRaises(ValueError):
            self.prestamo_service.realizar_prestamo(
                usuario_id=usuario1.id, item_id=9999, empleado_id=empleado_actual.id  # Item inexistente
            )

        # Test: Reserva de item disponible (debe fallar)
        with self.assertRaises(ValueError):
            self.reserva_service.realizar_reserva(
                usuario_id=usuario1.id, item_id=item.id, empleado_id=empleado_actual.id  # Item disponible
            )


if __name__ == "__main__":
    unittest.main()
