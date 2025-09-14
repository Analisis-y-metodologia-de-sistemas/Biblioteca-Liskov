#!/usr/bin/env python3
"""
Script para cargar datos de demostración en el sistema de biblioteca.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.container import Container
from src.domain.entities import TipoUsuario, CategoriaItem

def cargar_datos_demo():
    print("🔄 Cargando datos de demostración...")
    
    container = Container()
    usuario_service = container.get_usuario_service()
    item_service = container.get_item_service()
    
    try:
        print("👤 Registrando usuarios...")
        usuarios = [
            ("Ana", "García", "ana.garcia@email.com", TipoUsuario.ALUMNO, "12345678", "123456789"),
            ("Carlos", "Martínez", "carlos.martinez@email.com", TipoUsuario.DOCENTE, "87654321", "987654321"),
            ("María", "López", "maria.lopez@email.com", TipoUsuario.BIBLIOTECARIO, "11111111", "111111111"),
            ("Pedro", "Sánchez", "pedro.sanchez@email.com", TipoUsuario.ALUMNO, "22222222", "222222222"),
        ]
        
        for nombre, apellido, email, tipo, num_id, telefono in usuarios:
            try:
                usuario_service.registrar_usuario(nombre, apellido, email, tipo, num_id, telefono)
                print(f"  ✅ {nombre} {apellido}")
            except Exception as e:
                print(f"  ❌ {nombre} {apellido}: {str(e)}")
        
        print("\n📚 Agregando items a la biblioteca...")
        items = [
            ("Introducción a Python", "Mark Lutz", "978-1449355730", CategoriaItem.LIBRO_ALUMNO, "Programación básica en Python", "Estante A-1"),
            ("Django por Ejemplos", "Antonio Melé", "978-1782172950", CategoriaItem.LIBRO_ALUMNO, "Framework web Django", "Estante A-2"),
            ("Algoritmos y Estructuras de Datos", "Robert Sedgewick", "978-0321573513", CategoriaItem.LIBRO_BIBLIOTECARIO, "Referencia avanzada", "Estante B-1"),
            ("Ajedrez para Principiantes", None, None, CategoriaItem.JUEGO_MESA, "Juego de mesa educativo", "Área Recreativa"),
            ("Material de Laboratorio Química", None, None, CategoriaItem.MATERIAL_DIDACTICO, "Kit de experimentos", "Laboratorio"),
            ("Revista National Geographic", None, None, CategoriaItem.REVISTA, "Edición Enero 2024", "Hemeroteca"),
            ("Clean Code", "Robert C. Martin", "978-0132350884", CategoriaItem.LIBRO_ALUMNO, "Principios de programación limpia", "Estante A-3"),
            ("Monopoly Clásico", "Hasbro", None, CategoriaItem.JUEGO_MESA, "Juego de mesa estratégico", "Área Recreativa"),
        ]
        
        for titulo, autor, isbn, categoria, descripcion, ubicacion in items:
            try:
                item_service.agregar_item(titulo, categoria, autor, isbn, descripcion, ubicacion, 50.0)
                print(f"  ✅ {titulo}")
            except Exception as e:
                print(f"  ❌ {titulo}: {str(e)}")
        
        print(f"\n🎉 ¡Datos de demostración cargados exitosamente!")
        print(f"📊 Estadísticas:")
        usuarios_total = len(usuario_service.listar_usuarios())
        items_total = len(item_service.listar_disponibles())
        print(f"  👤 Usuarios: {usuarios_total}")
        print(f"  📚 Items disponibles: {items_total}")
        
    except Exception as e:
        print(f"❌ Error al cargar datos: {str(e)}")


if __name__ == "__main__":
    cargar_datos_demo()