#!/usr/bin/env python3
"""
Script para crear datos de prueba en el sistema
"""

import sys
import os

# Agregar el path del proyecto al sistema
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.container import Container
from datetime import datetime


def main():
    print("🧪 Creando datos de prueba en el sistema...")
    
    try:
        container = Container()
        
        # Servicios
        usuario_service = container.get_usuario_service()
        item_service = container.get_item_service()
        prestamo_service = container.get_prestamo_service()
        reserva_service = container.get_reserva_service()
        auth_service = container.get_auth_service()
        
        print("\n📋 Creando usuarios de prueba...")
        
        # Crear usuarios de prueba
        usuarios_prueba = [
            {
                "nombre": "Juan",
                "apellido": "Pérez",
                "email": "juan.perez@universidad.edu",
                "tipo": "alumno",
                "numero_identificacion": "12345678",
                "telefono": "+54-9-11-1234-5678"
            },
            {
                "nombre": "María",
                "apellido": "González",
                "email": "maria.gonzalez@universidad.edu",
                "tipo": "docente",
                "numero_identificacion": "87654321",
                "telefono": "+54-9-11-8765-4321"
            },
            {
                "nombre": "Pedro",
                "apellido": "López",
                "email": "pedro.lopez@universidad.edu",
                "tipo": "bibliotecario",
                "numero_identificacion": "11223344",
                "telefono": "+54-9-11-1122-3344"
            }
        ]
        
        for datos in usuarios_prueba:
            try:
                from src.domain.entities import TipoUsuario
                tipo_enum = TipoUsuario(datos["tipo"])
                
                usuario = usuario_service.registrar_usuario(
                    nombre=datos["nombre"],
                    apellido=datos["apellido"],
                    email=datos["email"],
                    tipo=tipo_enum,
                    numero_identificacion=datos["numero_identificacion"],
                    telefono=datos["telefono"]
                )
                
                print(f"✅ Usuario creado: {usuario.nombre} {usuario.apellido} ({usuario.tipo.value})")
                
            except Exception as e:
                if "ya existe" in str(e):
                    print(f"⚠️  Usuario {datos['email']} ya existe")
                else:
                    print(f"❌ Error al crear usuario: {str(e)}")
        
        print("\n📚 Creando items de prueba...")
        
        # Crear items de prueba
        items_prueba = [
            {
                "titulo": "Python Programming",
                "autor": "Mark Lutz",
                "categoria": "libro",
                "isbn": "978-1449355739",
                "descripcion": "Comprehensive guide to Python programming",
                "ubicacion": "Estante A-1"
            },
            {
                "titulo": "Clean Code",
                "autor": "Robert C. Martin",
                "categoria": "libro", 
                "isbn": "978-0132350884",
                "descripcion": "A handbook of agile software craftsmanship",
                "ubicacion": "Estante B-2"
            },
            {
                "titulo": "Introduction to Algorithms",
                "autor": "Thomas H. Cormen",
                "categoria": "libro",
                "isbn": "978-0262033848",
                "descripcion": "Comprehensive textbook on algorithms",
                "ubicacion": "Estante C-3"
            }
        ]
        
        for datos in items_prueba:
            try:
                from src.domain.entities import CategoriaItem
                categoria_enum = CategoriaItem(datos["categoria"])
                
                item = item_service.agregar_item(
                    titulo=datos["titulo"],
                    autor=datos["autor"],
                    categoria=datos["categoria"],
                    isbn=datos["isbn"],
                    descripcion=datos["descripcion"],
                    ubicacion=datos["ubicacion"]
                )
                
                print(f"✅ Item creado: {item.titulo} - {item.autor}")
                
            except Exception as e:
                print(f"❌ Error al crear item: {str(e)}")
        
        print("\n🎉 Datos de prueba creados exitosamente!")
        
        # Mostrar resumen
        usuarios = usuario_service.listar_usuarios()
        items = item_service.listar_disponibles()
        
        print(f"\n📊 RESUMEN:")
        print(f"👥 Usuarios registrados: {len(usuarios)}")
        print(f"📚 Items disponibles: {len(items)}")
        print(f"\n💡 Use las credenciales de empleado para probar el sistema:")
        print(f"   Usuario: arodriguez | Contraseña: 1234")
        print(f"   Usuario: cmartinez  | Contraseña: 1234")
        print(f"   Usuario: mlopez     | Contraseña: 1234")
        
    except Exception as e:
        print(f"❌ Error crítico: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()