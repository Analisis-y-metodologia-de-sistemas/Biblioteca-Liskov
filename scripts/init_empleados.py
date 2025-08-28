#!/usr/bin/env python3
"""
Script para inicializar empleados en la base de datos
Crea empleados de prueba para el sistema de biblioteca
"""

import sys
import os

# Agregar el path del proyecto al sistema
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.container import Container


def main():
    print("🔧 Inicializando empleados en la base de datos...")
    
    try:
        container = Container()
        auth_service = container.get_auth_service()
        
        # Empleados iniciales
        empleados_iniciales = [
            {
                "nombre": "Ana",
                "apellido": "Rodriguez",
                "email": "ana.rodriguez@biblioteca.edu",
                "usuario_sistema": "arodriguez",
                "password": "1234",
                "cargo": "Bibliotecario Jefe",
                "turno": "Mañana"
            },
            {
                "nombre": "Carlos",
                "apellido": "Martinez",
                "email": "carlos.martinez@biblioteca.edu",
                "usuario_sistema": "cmartinez",
                "password": "1234",
                "cargo": "Bibliotecario",
                "turno": "Tarde"
            },
            {
                "nombre": "Maria",
                "apellido": "Lopez",
                "email": "maria.lopez@biblioteca.edu",
                "usuario_sistema": "mlopez",
                "password": "1234",
                "cargo": "Bibliotecario",
                "turno": "Noche"
            }
        ]
        
        empleados_creados = 0
        
        for datos_empleado in empleados_iniciales:
            try:
                empleado = auth_service.crear_empleado(
                    nombre=datos_empleado["nombre"],
                    apellido=datos_empleado["apellido"],
                    email=datos_empleado["email"],
                    usuario_sistema=datos_empleado["usuario_sistema"],
                    password=datos_empleado["password"],
                    cargo=datos_empleado["cargo"],
                    turno=datos_empleado["turno"]
                )
                
                print(f"✅ Empleado creado: {empleado.nombre} {empleado.apellido} ({empleado.usuario_sistema})")
                empleados_creados += 1
                
            except ValueError as e:
                if "ya existe" in str(e):
                    print(f"⚠️  El empleado {datos_empleado['usuario_sistema']} ya existe")
                else:
                    print(f"❌ Error al crear empleado {datos_empleado['usuario_sistema']}: {str(e)}")
            except Exception as e:
                print(f"❌ Error inesperado al crear empleado {datos_empleado['usuario_sistema']}: {str(e)}")
        
        print(f"\n🎉 Proceso completado: {empleados_creados} empleados creados/actualizados")
        
        if empleados_creados > 0:
            print("\n📋 Credenciales de acceso:")
            print("=" * 40)
            for datos in empleados_iniciales:
                print(f"Usuario: {datos['usuario_sistema']}")
                print(f"Contraseña: {datos['password']}")
                print(f"Nombre: {datos['nombre']} {datos['apellido']}")
                print("-" * 40)
        
        print("\n🔐 Utilice estas credenciales para acceder al sistema")
        
    except Exception as e:
        print(f"❌ Error crítico: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()