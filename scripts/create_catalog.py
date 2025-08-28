#!/usr/bin/env python3
"""
Script para crear un catálogo extenso de libros divididos en categorías
"""

import sys
import os

# Agregar el path del proyecto al sistema
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.container import Container
from datetime import datetime


def main():
    print("📚 Creando catálogo extenso de libros por categorías...")
    
    try:
        container = Container()
        item_service = container.get_item_service()
        
        # Catálogo extenso organizado por categorías
        catalogo = {
            "libro": [
                # Programación y Tecnología
                {"titulo": "Python Crash Course", "autor": "Eric Matthes", "isbn": "978-1593279288", "descripcion": "Introducción práctica a Python", "ubicacion": "Tech-A1"},
                {"titulo": "JavaScript: The Good Parts", "autor": "Douglas Crockford", "isbn": "978-0596517748", "descripcion": "Las mejores características de JavaScript", "ubicacion": "Tech-A2"},
                {"titulo": "Clean Architecture", "autor": "Robert C. Martin", "isbn": "978-0134494166", "descripcion": "Guía para crear software mantenible", "ubicacion": "Tech-A3"},
                {"titulo": "Design Patterns", "autor": "Gang of Four", "isbn": "978-0201633612", "descripcion": "Patrones de diseño reutilizables", "ubicacion": "Tech-A4"},
                {"titulo": "The Pragmatic Programmer", "autor": "Andrew Hunt", "isbn": "978-0135957059", "descripcion": "De aprendiz a maestro", "ubicacion": "Tech-A5"},
                {"titulo": "Cracking the Coding Interview", "autor": "Gayle McDowell", "isbn": "978-0984782857", "descripcion": "189 preguntas de programación", "ubicacion": "Tech-A6"},
                {"titulo": "System Design Interview", "autor": "Alex Xu", "isbn": "978-1736049112", "descripcion": "Guía paso a paso", "ubicacion": "Tech-A7"},
                {"titulo": "Effective Java", "autor": "Joshua Bloch", "isbn": "978-0134685991", "descripcion": "Mejores prácticas en Java", "ubicacion": "Tech-A8"},
                
                # Ciencias y Matemáticas  
                {"titulo": "Cálculo de una Variable", "autor": "James Stewart", "isbn": "978-1285740621", "descripcion": "Fundamentos del cálculo", "ubicacion": "Math-B1"},
                {"titulo": "Álgebra Lineal", "autor": "Gilbert Strang", "isbn": "978-0980232776", "descripcion": "Introducción al álgebra lineal", "ubicacion": "Math-B2"},
                {"titulo": "Probabilidad y Estadística", "autor": "Sheldon Ross", "isbn": "978-0123948113", "descripcion": "Fundamentos estadísticos", "ubicacion": "Math-B3"},
                {"titulo": "Física Universitaria", "autor": "Hugh Young", "isbn": "978-0321973610", "descripcion": "Física con aplicaciones modernas", "ubicacion": "Sci-B4"},
                {"titulo": "Química General", "autor": "Raymond Chang", "isbn": "978-0073402680", "descripcion": "Principios de química", "ubicacion": "Sci-B5"},
                {"titulo": "Biología Molecular", "autor": "Bruce Alberts", "isbn": "978-0815344322", "descripcion": "La célula como unidad básica", "ubicacion": "Sci-B6"},
                
                # Literatura y Humanidades
                {"titulo": "Cien Años de Soledad", "autor": "Gabriel García Márquez", "isbn": "978-0307389732", "descripcion": "Realismo mágico latinoamericano", "ubicacion": "Lit-C1"},
                {"titulo": "Don Quijote de la Mancha", "autor": "Miguel de Cervantes", "isbn": "978-8424116781", "descripcion": "Clásico de la literatura española", "ubicacion": "Lit-C2"},
                {"titulo": "1984", "autor": "George Orwell", "isbn": "978-0451524935", "descripcion": "Distopía totalitaria", "ubicacion": "Lit-C3"},
                {"titulo": "El Gran Gatsby", "autor": "F. Scott Fitzgerald", "isbn": "978-0743273565", "descripcion": "La era del jazz americano", "ubicacion": "Lit-C4"},
                {"titulo": "Orgullo y Prejuicio", "autor": "Jane Austen", "isbn": "978-0141439518", "descripcion": "Romance victoriano", "ubicacion": "Lit-C5"},
                {"titulo": "Rayuela", "autor": "Julio Cortázar", "isbn": "978-8437604572", "descripcion": "Novela experimental argentina", "ubicacion": "Lit-C6"},
                {"titulo": "La Metamorfosis", "autor": "Franz Kafka", "isbn": "978-0486290300", "descripcion": "Alegoría existencial", "ubicacion": "Lit-C7"},
                
                # Historia y Filosofía
                {"titulo": "Sapiens", "autor": "Yuval Noah Harari", "isbn": "978-0062316097", "descripcion": "Breve historia de la humanidad", "ubicacion": "Hist-D1"},
                {"titulo": "El Arte de la Guerra", "autor": "Sun Tzu", "isbn": "978-1590302255", "descripcion": "Estrategia militar antigua", "ubicacion": "Hist-D2"},
                {"titulo": "Historia del Tiempo", "autor": "Stephen Hawking", "isbn": "978-0553380163", "descripcion": "Del Big Bang a los agujeros negros", "ubicacion": "Hist-D3"},
                {"titulo": "El Mundo de Sofía", "autor": "Jostein Gaarder", "isbn": "978-8478442355", "descripcion": "Historia de la filosofía", "ubicacion": "Phil-D4"},
                {"titulo": "Más Platón y Menos Prozac", "autor": "Lou Marinoff", "isbn": "978-8466318846", "descripcion": "Filosofía para la vida cotidiana", "ubicacion": "Phil-D5"},
                
                # Economía y Negocios
                {"titulo": "Padre Rico, Padre Pobre", "autor": "Robert Kiyosaki", "isbn": "978-1612680194", "descripcion": "Educación financiera", "ubicacion": "Biz-E1"},
                {"titulo": "El Inversor Inteligente", "autor": "Benjamin Graham", "isbn": "978-0060555665", "descripcion": "Principios de inversión", "ubicacion": "Biz-E2"},
                {"titulo": "Freakonomics", "autor": "Steven Levitt", "isbn": "978-0060731335", "descripcion": "Economía de lo inesperado", "ubicacion": "Biz-E3"},
                {"titulo": "Good to Great", "autor": "Jim Collins", "isbn": "978-0066620992", "descripcion": "Por qué algunas empresas destacan", "ubicacion": "Biz-E4"},
                {"titulo": "The Lean Startup", "autor": "Eric Ries", "isbn": "978-0307887894", "descripcion": "Innovación empresarial", "ubicacion": "Biz-E5"},
            ],
            
            "revista": [
                {"titulo": "National Geographic Español", "autor": "Varios", "isbn": "ISSN-1138-1434", "descripcion": "Revista de geografía y naturaleza", "ubicacion": "Rev-F1"},
                {"titulo": "Scientific American", "autor": "Varios", "isbn": "ISSN-0036-8733", "descripcion": "Divulgación científica", "ubicacion": "Rev-F2"},
                {"titulo": "IEEE Computer", "autor": "Varios", "isbn": "ISSN-0018-9162", "descripcion": "Revista de tecnología", "ubicacion": "Rev-F3"},
                {"titulo": "Harvard Business Review", "autor": "Varios", "isbn": "ISSN-0017-8012", "descripcion": "Gestión empresarial", "ubicacion": "Rev-F4"},
            ],
            
            "cd": [
                {"titulo": "Curso de Python Completo", "autor": "MIT OpenCourseWare", "isbn": "CD-001", "descripcion": "Curso completo de programación", "ubicacion": "CD-G1"},
                {"titulo": "Matemáticas Aplicadas", "autor": "Khan Academy", "isbn": "CD-002", "descripcion": "Ejercicios interactivos", "ubicacion": "CD-G2"},
                {"titulo": "Historia Universal", "autor": "BBC Learning", "isbn": "CD-003", "descripcion": "Documentales educativos", "ubicacion": "CD-G3"},
            ],
            
            "dvd": [
                {"titulo": "Cosmos: Una Odisea Espacial", "autor": "Neil deGrasse Tyson", "isbn": "DVD-001", "descripcion": "Serie documental científica", "ubicacion": "DVD-H1"},
                {"titulo": "Planet Earth", "autor": "BBC", "isbn": "DVD-002", "descripcion": "Documental sobre la naturaleza", "ubicacion": "DVD-H2"},
                {"titulo": "The Code", "autor": "BBC", "isbn": "DVD-003", "descripcion": "Matemáticas en la naturaleza", "ubicacion": "DVD-H3"},
            ]
        }
        
        items_creados = 0
        items_por_categoria = {}
        
        for categoria, items in catalogo.items():
            items_por_categoria[categoria] = 0
            print(f"\\n📖 Creando items de categoría: {categoria.upper()}")
            
            for datos in items:
                try:
                    item = item_service.agregar_item(
                        titulo=datos["titulo"],
                        autor=datos["autor"],
                        categoria=categoria,
                        isbn=datos["isbn"],
                        descripcion=datos["descripcion"],
                        ubicacion=datos["ubicacion"]
                    )
                    
                    print(f"✅ {item.titulo} - {item.autor}")
                    items_creados += 1
                    items_por_categoria[categoria] += 1
                    
                except Exception as e:
                    if "unique constraint" in str(e).lower() or "ya existe" in str(e):
                        print(f"⚠️  Item ya existe: {datos['titulo']}")
                    else:
                        print(f"❌ Error: {datos['titulo']} - {str(e)}")
        
        print(f"\\n🎉 CATÁLOGO CREADO EXITOSAMENTE!")
        print("=" * 50)
        print(f"📊 Total de items creados: {items_creados}")
        print("\\n📋 Items por categoría:")
        
        for categoria, cantidad in items_por_categoria.items():
            emoji = {"libro": "📚", "revista": "📰", "cd": "💿", "dvd": "📀"}.get(categoria, "📄")
            print(f"  {emoji} {categoria.capitalize()}: {cantidad} items")
        
        # Verificar total en base de datos
        todos_los_items = item_service.item_repo.orm.db.execute_query("SELECT COUNT(*) as total FROM items_biblioteca")
        total_db = todos_los_items[0]['total']
        print(f"\\n💾 Total en base de datos: {total_db} items")
        
        print("\\n💡 Usa el sistema para navegar por categorías:")
        print("   Menú Items → Buscar por categoría")
        
    except Exception as e:
        print(f"❌ Error crítico: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()