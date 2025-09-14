#!/usr/bin/env python3
"""
Script simple para probar la navegación por categorías
"""

import os
import sys

# Agregar el path del proyecto al sistema
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.container import Container


def main():
    print("🧪 Probando navegación por categorías...")

    try:
        container = Container()
        item_service = container.get_item_service()

        # Listar todas las categorías disponibles
        print("\\n📊 RESUMEN DEL CATÁLOGO")
        print("=" * 50)

        from src.domain.entities import CategoriaItem

        categorias_emoji = {
            CategoriaItem.LIBRO: "📚",
            CategoriaItem.REVISTA: "📰",
            CategoriaItem.DVD: "📀",
            CategoriaItem.CD: "💿",
            CategoriaItem.AUDIOBOOK: "🎧",
            CategoriaItem.OTRO: "📄",
        }

        total_items = 0

        for categoria in CategoriaItem:
            items = item_service.listar_por_categoria(categoria.value)
            emoji = categorias_emoji.get(categoria, "📄")
            print(f"{emoji} {categoria.value.capitalize()}: {len(items)} items")
            total_items += len(items)

            # Mostrar algunos ejemplos
            if items and len(items) > 0:
                print(f"   📖 Ejemplos: {items[0].titulo}", end="")
                if len(items) > 1:
                    print(f", {items[1].titulo}", end="")
                if len(items) > 2:
                    print(f", {items[2].titulo}...", end="")
                print()

        print(f"\\n📚 TOTAL: {total_items} items en el catálogo")

        # Mostrar algunos libros por categoría
        print("\\n📚 MUESTRA DE LIBROS:")
        print("-" * 30)

        libros = item_service.listar_por_categoria("libro")
        for i, libro in enumerate(libros[:10]):  # Mostrar primeros 10
            estado_emoji = {"disponible": "✅", "prestado": "📤", "en_reparacion": "🔧", "perdido": "❌"}
            emoji = estado_emoji.get(libro.estado.value, "❓")
            print(f"{i+1:2d}. {emoji} [{libro.id:2d}] {libro.titulo}")
            print(f"    ✍️  {libro.autor or 'Autor no especificado'}")
            print(f"    📍 {libro.ubicacion or 'Ubicación no especificada'}")
            print()

        if len(libros) > 10:
            print(f"... y {len(libros) - 10} libros más")

        print("\\n✅ Sistema listo para usar!")
        print("🚀 Ejecuta 'python main.py' para acceder al sistema completo")
        print("🔐 Usa: arodriguez / 1234 para login")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
