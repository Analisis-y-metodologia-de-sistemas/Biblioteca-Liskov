import unittest
from datetime import datetime
from unittest.mock import Mock

from src.domain.entities import CategoriaItem, EstadoItem, ItemBiblioteca
from src.infrastructure.database import ORM
from src.infrastructure.repositories import ItemBibliotecaRepository


class TestItemBibliotecaRepository(unittest.TestCase):

    def setUp(self):
        self.orm_mock = Mock(spec=ORM)
        self.repository = ItemBibliotecaRepository(self.orm_mock)

        self.item_data = {
            "id": 1,
            "titulo": "El Quijote",
            "categoria": "libro",
            "autor": "Cervantes",
            "isbn": "978-1234567890",
            "descripcion": "Obra clásica",
            "estado": "disponible",
            "ubicacion": "A1-B2",
            "valor_reposicion": 25000.0,
            "fecha_adquisicion": "2023-01-01T12:00:00",
        }

        self.item = ItemBiblioteca(
            id=1,
            titulo="El Quijote",
            categoria=CategoriaItem.LIBRO,
            autor="Cervantes",
            isbn="978-1234567890",
            descripcion="Obra clásica",
            estado=EstadoItem.DISPONIBLE,
            ubicacion="A1-B2",
            valor_reposicion=25000.0,
            fecha_adquisicion=datetime(2023, 1, 1, 12, 0, 0),
        )

    def test_crear_item(self):
        self.orm_mock.insert.return_value = 1
        item_sin_id = ItemBiblioteca(titulo="El Quijote", categoria=CategoriaItem.LIBRO, autor="Cervantes")

        resultado = self.repository.crear(item_sin_id)

        self.orm_mock.insert.assert_called_once()
        self.assertEqual(resultado.id, 1)
        self.assertEqual(resultado.titulo, "El Quijote")

    def test_obtener_por_id_existente(self):
        self.orm_mock.select.return_value = [self.item_data]

        resultado = self.repository.obtener_por_id(1)

        self.orm_mock.select.assert_called_once_with("items_biblioteca", "id = ?", (1,))
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.id, 1)
        self.assertEqual(resultado.titulo, "El Quijote")

    def test_obtener_por_id_no_existente(self):
        self.orm_mock.select.return_value = []

        resultado = self.repository.obtener_por_id(999)

        self.assertIsNone(resultado)

    def test_buscar_por_titulo(self):
        self.orm_mock.select.return_value = [self.item_data]

        resultado = self.repository.buscar_por_titulo("Quijote")

        self.orm_mock.select.assert_called_once()
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].titulo, "El Quijote")

    def test_buscar_por_autor(self):
        self.orm_mock.select.return_value = [self.item_data]

        resultado = self.repository.buscar_por_autor("Cervantes")

        self.orm_mock.select.assert_called_once()
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].autor, "Cervantes")

    def test_buscar_por_categoria(self):
        self.orm_mock.select.return_value = [self.item_data]

        resultado = self.repository.buscar_por_categoria(CategoriaItem.LIBRO)

        self.orm_mock.select.assert_called_once()
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].categoria, CategoriaItem.LIBRO)

    def test_listar_disponibles(self):
        self.orm_mock.select.return_value = [self.item_data]

        resultado = self.repository.listar_disponibles()

        self.orm_mock.select.assert_called_once_with("items_biblioteca", "estado = ?", ("disponible",))
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].estado, EstadoItem.DISPONIBLE)

    def test_actualizar_item(self):
        self.orm_mock.update.return_value = None

        resultado = self.repository.actualizar(self.item)

        self.orm_mock.update.assert_called_once()
        self.assertEqual(resultado, self.item)

    def test_eliminar_item(self):
        self.orm_mock.delete.return_value = 1

        resultado = self.repository.eliminar(1)

        self.orm_mock.delete.assert_called_once_with("items_biblioteca", "id = ?", (1,))
        self.assertTrue(resultado)

    def test_row_to_entity_conversion(self):
        resultado = self.repository._row_to_entity(self.item_data)

        self.assertEqual(resultado.id, 1)
        self.assertEqual(resultado.titulo, "El Quijote")
        self.assertEqual(resultado.categoria, CategoriaItem.LIBRO)
        self.assertEqual(resultado.autor, "Cervantes")
        self.assertEqual(resultado.isbn, "978-1234567890")
        self.assertEqual(resultado.estado, EstadoItem.DISPONIBLE)
        self.assertEqual(resultado.ubicacion, "A1-B2")
        self.assertEqual(resultado.valor_reposicion, 25000.0)

    def test_entity_to_dict_conversion(self):
        resultado = self.repository._entity_to_dict(self.item)

        self.assertIn("titulo", resultado)
        self.assertIn("categoria", resultado)
        self.assertIn("autor", resultado)
        self.assertEqual(resultado["titulo"], "El Quijote")
        self.assertEqual(resultado["categoria"], "libro")
        self.assertEqual(resultado["estado"], "disponible")


if __name__ == "__main__":
    unittest.main()
