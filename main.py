#!/usr/bin/env python3
"""
Sistema de Gestión de Biblioteca Liskov
======================================

Un sistema completo de biblioteca que demuestra las capacidades
de Python con arquitectura empresarial, utilizando:

- Arquitectura en capas (Domain, Infrastructure, Application, Presentation)
- Patrón Repository para abstracción de datos
- Inyección de dependencias con contenedor IoC
- ORM personalizado para SQLite
- Logging y manejo de excepciones
- Separación de responsabilidades

Categorías soportadas:
- Libros para alumnos
- Libros para bibliotecarios
- Juegos de mesa
- Material didáctico para docentes
- Revistas y multimedia

Funcionalidades:
- Gestión de usuarios (alumnos, docentes, bibliotecarios)
- Catálogo de items con búsqueda avanzada
- Sistema de préstamos con fechas de devolución
- Reservas y multas automatizadas
- Interfaz de consola amigable

Autor: Sistema Biblioteca Liskov
Versión: 1.0.0
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.container import Container
from src.shared.logger import get_logger


def main() -> None:
    try:
        logger = get_logger()
        logger.info("Iniciando Sistema de Biblioteca Liskov")

        container = Container()
        console_ui = container.get_console_ui()

        console_ui.ejecutar()

    except KeyboardInterrupt:
        print("\n\n👋 Sistema cerrado por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error crítico del sistema: {str(e)}")
        logger = get_logger()
        logger.error(f"Error crítico: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
