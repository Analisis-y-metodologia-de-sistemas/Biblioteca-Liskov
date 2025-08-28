# 🧪 Guía de Testing - Biblioteca Liskov

## Índice

1. [Estrategia de Testing](#estrategia-de-testing)
2. [Tipos de Tests](#tipos-de-tests)
3. [Ejecutar Tests](#ejecutar-tests)
4. [Escribir Nuevos Tests](#escribir-nuevos-tests)
5. [Coverage y Calidad](#coverage-y-calidad)
6. [Mocking y Stubs](#mocking-y-stubs)

## Estrategia de Testing

### Pirámide de Testing

```
           🔺 E2E Tests (Pocos)
          /                 \
         /   Integration      \
        /      Tests           \
       /    (Algunos)           \
      /                         \
     🔽 Unit Tests (Muchos)      🔽
```

### Principios de Testing

1. **Tests Rápidos**: Unit tests deben ejecutar en milisegundos
2. **Tests Independientes**: Cada test debe ser independiente
3. **Tests Deterministas**: Mismo resultado siempre
4. **Tests Legibles**: Nombre descriptivo y estructura clara
5. **Fail Fast**: Fallar rápido con mensajes claros

## Tipos de Tests

### 1. Unit Tests

**Ubicación**: `tests/unit/`

Testean componentes individuales en aislamiento.

#### Ejemplo: Testing de Entidades

```python
# tests/unit/test_usuario.py
import pytest
from datetime import datetime, date
from src.domain.entities import Usuario, TipoUsuario, Multa

class TestUsuario:
    def setup_method(self):
        """Setup ejecutado antes de cada test"""
        self.usuario = Usuario(
            nombre="Juan Pérez",
            email="juan@universidad.edu",
            tipo_usuario=TipoUsuario.ALUMNO
        )
    
    def test_usuario_creation(self):
        """Test: Usuario se crea correctamente"""
        assert self.usuario.nombre == "Juan Pérez"
        assert self.usuario.email == "juan@universidad.edu"
        assert self.usuario.tipo_usuario == TipoUsuario.ALUMNO
        assert self.usuario.activo is True
        assert isinstance(self.usuario.fecha_registro, datetime)
    
    def test_puede_realizar_prestamos_usuario_activo_sin_multas(self):
        """Test: Usuario activo sin multas puede realizar préstamos"""
        # Arrange - estado inicial correcto
        
        # Act
        result = self.usuario.puede_realizar_prestamos()
        
        # Assert
        assert result is True
    
    def test_no_puede_realizar_prestamos_usuario_inactivo(self):
        """Test: Usuario inactivo NO puede realizar préstamos"""
        # Arrange
        self.usuario.activo = False
        
        # Act
        result = self.usuario.puede_realizar_prestamos()
        
        # Assert
        assert result is False
    
    def test_no_puede_realizar_prestamos_con_multas_pendientes(self):
        """Test: Usuario con multas pendientes NO puede realizar préstamos"""
        # Arrange
        multa = Multa(
            usuario_id=self.usuario.id,
            prestamo_id=1,
            monto=50.0,
            motivo="Libro dañado"
        )
        self.usuario.agregar_multa(multa)
        
        # Act
        result = self.usuario.puede_realizar_prestamos()
        
        # Assert
        assert result is False
    
    def test_limite_prestamos_por_tipo_usuario(self):
        """Test: Límite de préstamos según tipo de usuario"""
        # Test para alumno
        self.usuario.tipo_usuario = TipoUsuario.ALUMNO
        assert self.usuario.obtener_limite_prestamos() == 3
        
        # Test para docente
        self.usuario.tipo_usuario = TipoUsuario.DOCENTE
        assert self.usuario.obtener_limite_prestamos() == 5
        
        # Test para empleado
        self.usuario.tipo_usuario = TipoUsuario.EMPLEADO
        assert self.usuario.obtener_limite_prestamos() == 10
    
    @pytest.mark.parametrize("tipo_usuario,limite_esperado", [
        (TipoUsuario.ALUMNO, 3),
        (TipoUsuario.DOCENTE, 5), 
        (TipoUsuario.EMPLEADO, 10)
    ])
    def test_limite_prestamos_parametrizado(self, tipo_usuario, limite_esperado):
        """Test parametrizado: Límites para diferentes tipos de usuario"""
        # Arrange
        self.usuario.tipo_usuario = tipo_usuario
        
        # Act
        limite = self.usuario.obtener_limite_prestamos()
        
        # Assert
        assert limite == limite_esperado
```

#### Ejemplo: Testing de Servicios con Mocks

```python
# tests/unit/test_prestamo_service.py
import pytest
from unittest.mock import Mock, MagicMock
from src.application.services import PrestamoService
from src.domain.entities import Usuario, Item, Prestamo, TipoUsuario
from src.shared.exceptions import UsuarioNoEncontradoError, ItemNoDisponibleError

class TestPrestamoService:
    def setup_method(self):
        """Setup con mocks de repositorios"""
        self.prestamo_repo_mock = Mock()
        self.item_repo_mock = Mock()
        self.usuario_repo_mock = Mock()
        self.logger_mock = Mock()
        
        self.prestamo_service = PrestamoService(
            prestamo_repo=self.prestamo_repo_mock,
            item_repo=self.item_repo_mock,
            usuario_repo=self.usuario_repo_mock,
            logger=self.logger_mock
        )
    
    def test_realizar_prestamo_exitoso(self):
        """Test: Préstamo exitoso con usuario y libro válidos"""
        # Arrange
        usuario_id = 1
        item_id = 1
        
        usuario_mock = Usuario("Juan", "juan@test.com", TipoUsuario.ALUMNO)
        usuario_mock.id = usuario_id
        
        item_mock = Item("1984", "George Orwell", "123456789", 5)
        item_mock.id = item_id
        
        prestamo_mock = Prestamo(usuario_id=usuario_id, item_id=item_id)
        prestamo_mock.id = 1
        
        # Configurar mocks
        self.usuario_repo_mock.obtener_por_id.return_value = usuario_mock
        self.item_repo_mock.obtener_por_id.return_value = item_mock
        self.prestamo_repo_mock.crear.return_value = prestamo_mock
        
        # Act
        resultado = self.prestamo_service.realizar_prestamo(usuario_id, item_id)
        
        # Assert
        assert resultado == prestamo_mock
        self.usuario_repo_mock.obtener_por_id.assert_called_once_with(usuario_id)
        self.item_repo_mock.obtener_por_id.assert_called_once_with(item_id)
        self.prestamo_repo_mock.crear.assert_called_once()
        self.item_repo_mock.actualizar.assert_called_once_with(item_mock)
        self.logger_mock.info.assert_called()
    
    def test_realizar_prestamo_usuario_no_encontrado(self):
        """Test: Error cuando usuario no existe"""
        # Arrange
        usuario_id = 999  # Usuario inexistente
        item_id = 1
        
        self.usuario_repo_mock.obtener_por_id.return_value = None
        
        # Act & Assert
        with pytest.raises(UsuarioNoEncontradoError, match="Usuario 999 no existe"):
            self.prestamo_service.realizar_prestamo(usuario_id, item_id)
        
        # Verificar que no se llamaron otros métodos
        self.item_repo_mock.obtener_por_id.assert_not_called()
        self.prestamo_repo_mock.crear.assert_not_called()
    
    def test_realizar_prestamo_item_no_disponible(self):
        """Test: Error cuando item no está disponible"""
        # Arrange
        usuario_id = 1
        item_id = 1
        
        usuario_mock = Usuario("Juan", "juan@test.com", TipoUsuario.ALUMNO)
        item_mock = Item("1984", "George Orwell", "123456789", 0)  # Sin stock
        
        self.usuario_repo_mock.obtener_por_id.return_value = usuario_mock
        self.item_repo_mock.obtener_por_id.return_value = item_mock
        
        # Act & Assert
        with pytest.raises(ItemNoDisponibleError):
            self.prestamo_service.realizar_prestamo(usuario_id, item_id)
```

### 2. Integration Tests

**Ubicación**: `tests/integration/`

Testean la interacción entre múltiples componentes.

```python
# tests/integration/test_sistema_completo.py
import pytest
import sqlite3
import tempfile
import os
from src.container import Container
from src.application.services import PrestamoService, AuthService
from src.domain.entities import TipoUsuario

class TestSistemaCompleto:
    def setup_method(self):
        """Setup con base de datos temporal"""
        # Crear base de datos temporal
        self.db_fd, self.db_path = tempfile.mkstemp()
        
        # Configurar container con BD temporal
        self.container = Container()
        self.container._database_path = self.db_path
        
        # Inicializar BD
        self.container.get_database_connection()
        self.container.initialize_database()
        
        # Servicios a testear
        self.auth_service = self.container.get_auth_service()
        self.prestamo_service = self.container.get_prestamo_service()
        self.item_service = self.container.get_item_service()
    
    def teardown_method(self):
        """Cleanup después de cada test"""
        os.close(self.db_fd)
        os.unlink(self.db_path)
    
    def test_flujo_completo_prestamo(self):
        """Test de integración: Flujo completo de préstamo"""
        # 1. Registrar usuario
        usuario = self.auth_service.registrar_usuario(
            nombre="María García",
            email="maria@universidad.edu", 
            tipo=TipoUsuario.ALUMNO
        )
        assert usuario.id is not None
        
        # 2. Agregar libro al catálogo
        item = self.item_service.agregar_item(
            titulo="Clean Code",
            autor="Robert Martin",
            isbn="9780132350884",
            cantidad=3
        )
        assert item.id is not None
        assert item.cantidad_disponible == 3
        
        # 3. Realizar préstamo
        prestamo = self.prestamo_service.realizar_prestamo(
            usuario_id=usuario.id,
            item_id=item.id
        )
        assert prestamo.id is not None
        assert prestamo.usuario_id == usuario.id
        assert prestamo.item_id == item.id
        
        # 4. Verificar que se redujo disponibilidad
        item_actualizado = self.item_service.obtener_por_id(item.id)
        assert item_actualizado.cantidad_disponible == 2
        
        # 5. Listar préstamos del usuario
        prestamos_usuario = self.prestamo_service.listar_prestamos_usuario(usuario.id)
        assert len(prestamos_usuario) == 1
        assert prestamos_usuario[0].id == prestamo.id
    
    def test_prestamo_con_limite_excedido(self):
        """Test: Usuario no puede exceder límite de préstamos"""
        # Arrange: Usuario alumno (límite 3)
        usuario = self.auth_service.registrar_usuario(
            "Test User", "test@test.com", TipoUsuario.ALUMNO
        )
        
        # Crear 4 libros
        items = []
        for i in range(4):
            item = self.item_service.agregar_item(
                f"Libro {i}", f"Autor {i}", f"ISBN{i}", 1
            )
            items.append(item)
        
        # Realizar 3 préstamos (hasta el límite)
        for i in range(3):
            prestamo = self.prestamo_service.realizar_prestamo(
                usuario.id, items[i].id
            )
            assert prestamo is not None
        
        # El 4to préstamo debe fallar
        with pytest.raises(Exception):  # LimitePrestamosSuperadoError
            self.prestamo_service.realizar_prestamo(
                usuario.id, items[3].id
            )
```

### 3. End-to-End Tests

**Ubicación**: `tests/e2e/`

Testean el sistema completo desde la perspectiva del usuario.

```python
# tests/e2e/test_user_scenarios.py
import pytest
from unittest.mock import patch
from io import StringIO
import sys
from src.presentation.console_ui import ConsoleUI
from src.container import Container

class TestUserScenarios:
    def setup_method(self):
        self.container = Container()
        self.console_ui = ConsoleUI(self.container)
    
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_scenario_alumno_consulta_y_prestamo(self, mock_stdout, mock_input):
        """Test E2E: Alumno consulta catálogo y realiza préstamo"""
        # Simular inputs del usuario
        mock_input.side_effect = [
            '1',  # Iniciar sesión
            'alumno@universidad.edu',  # Email
            '1',  # Consultar catálogo
            '2',  # Realizar préstamo  
            '1',  # ID del libro
            '5'   # Salir
        ]
        
        # Ejecutar flujo
        self.console_ui.run()
        
        # Verificar output
        output = mock_stdout.getvalue()
        assert "Catálogo de Libros" in output
        assert "Préstamo realizado exitosamente" in output
```

## Ejecutar Tests

### Comandos Básicos

```bash
# Todos los tests
python -m pytest

# Solo unit tests
python -m pytest tests/unit/

# Solo integration tests  
python -m pytest tests/integration/

# Test específico
python -m pytest tests/unit/test_usuario.py::TestUsuario::test_puede_realizar_prestamos

# Tests con output verbose
python -m pytest -v

# Tests con output de print statements
python -m pytest -s
```

### Tests con Coverage

```bash
# Coverage básico
python -m pytest --cov=src

# Coverage con reporte HTML
python -m pytest --cov=src --cov-report=html

# Coverage con líneas faltantes
python -m pytest --cov=src --cov-report=term-missing

# Coverage mínimo requerido
python -m pytest --cov=src --cov-fail-under=80
```

### Tests Paralelos

```bash
# Instalar pytest-xdist
pip install pytest-xdist

# Ejecutar en paralelo
python -m pytest -n auto
```

## Escribir Nuevos Tests

### Estructura de Test

```python
def test_descripcion_clara_del_comportamiento(self):
    """Test: Descripción de lo que se está probando"""
    # Arrange - Preparar datos y mocks
    usuario = Usuario("Test", "test@test.com", TipoUsuario.ALUMNO)
    
    # Act - Ejecutar la acción a probar
    resultado = usuario.puede_realizar_prestamos()
    
    # Assert - Verificar el resultado esperado
    assert resultado is True
```

### Convenciones de Naming

```python
# Nombre del archivo: test_{modulo}.py
# Clase de test: Test{ClaseAProbar}  
# Método de test: test_{accion}_{condicion}_{resultado_esperado}

class TestPrestamoService:
    def test_realizar_prestamo_usuario_valido_prestamo_exitoso(self):
        pass
    
    def test_realizar_prestamo_usuario_inactivo_lanza_excepcion(self):
        pass
    
    def test_devolver_prestamo_prestamo_vencido_genera_multa(self):
        pass
```

### Fixtures

```python
# conftest.py - Fixtures compartidas
import pytest
from src.domain.entities import Usuario, TipoUsuario, Item

@pytest.fixture
def usuario_alumno():
    """Fixture: Usuario alumno para tests"""
    return Usuario(
        nombre="Test Alumno",
        email="alumno@test.com",
        tipo_usuario=TipoUsuario.ALUMNO
    )

@pytest.fixture
def item_disponible():
    """Fixture: Item con stock disponible"""
    return Item(
        titulo="Test Book",
        autor="Test Author", 
        isbn="123456789",
        cantidad_total=5
    )

@pytest.fixture
def database_temporal():
    """Fixture: Base de datos temporal para integration tests"""
    import tempfile
    import os
    
    fd, path = tempfile.mkstemp()
    
    yield path  # Proporciona el path del archivo
    
    # Cleanup
    os.close(fd)
    os.unlink(path)

# Uso en tests
def test_con_fixtures(usuario_alumno, item_disponible):
    assert usuario_alumno.tipo_usuario == TipoUsuario.ALUMNO
    assert item_disponible.esta_disponible()
```

### Parametrized Tests

```python
@pytest.mark.parametrize("tipo_usuario,limite_esperado", [
    (TipoUsuario.ALUMNO, 3),
    (TipoUsuario.DOCENTE, 5),
    (TipoUsuario.EMPLEADO, 10),
])
def test_limite_prestamos(tipo_usuario, limite_esperado):
    usuario = Usuario("Test", "test@test.com", tipo_usuario)
    assert usuario.obtener_limite_prestamos() == limite_esperado

@pytest.mark.parametrize("dias_retraso,monto_esperado", [
    (1, 10.0),
    (5, 50.0), 
    (10, 100.0),
])
def test_calculo_multa_por_retraso(dias_retraso, monto_esperado):
    multa_service = MultaService()
    monto = multa_service.calcular_monto_por_retraso(dias_retraso)
    assert monto == monto_esperado
```

## Coverage y Calidad

### Configuración de Coverage

```ini
# .coveragerc
[run]
source = src/
omit = 
    */tests/*
    */venv/*
    */__pycache__/*
    */migrations/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:

[html]
directory = htmlcov
```

### Métricas de Calidad

```bash
# Coverage mínimo por módulo
python -m pytest \
    --cov=src/domain --cov-fail-under=90 \
    --cov=src/application --cov-fail-under=85 \
    --cov=src/infrastructure --cov-fail-under=75
```

### Reportes

```bash
# Generar reporte completo
python -m pytest \
    --cov=src \
    --cov-report=html \
    --cov-report=xml \
    --cov-report=term-missing \
    --junit-xml=reports/junit.xml
```

## Mocking y Stubs

### Mock de Repositorios

```python
from unittest.mock import Mock, patch

class TestPrestamoService:
    def setup_method(self):
        # Mock de dependencias externas
        self.prestamo_repo_mock = Mock()
        self.item_repo_mock = Mock()
        self.usuario_repo_mock = Mock()
        
        self.prestamo_service = PrestamoService(
            prestamo_repo=self.prestamo_repo_mock,
            item_repo=self.item_repo_mock,
            usuario_repo=self.usuario_repo_mock
        )
    
    def test_realizar_prestamo_llama_repositorios_correctos(self):
        # Arrange
        usuario_mock = Mock()
        usuario_mock.puede_realizar_prestamos.return_value = True
        self.usuario_repo_mock.obtener_por_id.return_value = usuario_mock
        
        item_mock = Mock() 
        item_mock.esta_disponible.return_value = True
        self.item_repo_mock.obtener_por_id.return_value = item_mock
        
        prestamo_mock = Mock()
        self.prestamo_repo_mock.crear.return_value = prestamo_mock
        
        # Act
        resultado = self.prestamo_service.realizar_prestamo(1, 1)
        
        # Assert - Verificar llamadas
        self.usuario_repo_mock.obtener_por_id.assert_called_once_with(1)
        self.item_repo_mock.obtener_por_id.assert_called_once_with(1)
        self.prestamo_repo_mock.crear.assert_called_once()
        item_mock.reducir_disponibilidad.assert_called_once()
        self.item_repo_mock.actualizar.assert_called_once_with(item_mock)
```

### Mock de Tiempo

```python
from unittest.mock import patch
from datetime import datetime, date

class TestMultaService:
    @patch('src.domain.entities.datetime')
    def test_generar_multa_usa_fecha_actual(self, mock_datetime):
        # Arrange - Mock de fecha fija
        fecha_fija = datetime(2024, 1, 15, 10, 30, 0)
        mock_datetime.now.return_value = fecha_fija
        
        multa_service = MultaService(multa_repo=Mock())
        
        # Act
        multa = multa_service.generar_multa_retraso(prestamo_id=1)
        
        # Assert
        assert multa.fecha_creacion == fecha_fija
        mock_datetime.now.assert_called_once()
```

### Stub de Base de Datos

```python
class FakeUsuarioRepository:
    """Stub repository para tests - implementación en memoria"""
    
    def __init__(self):
        self._usuarios = {}
        self._next_id = 1
    
    def obtener_por_id(self, id: int) -> Optional[Usuario]:
        return self._usuarios.get(id)
    
    def obtener_por_email(self, email: str) -> Optional[Usuario]:
        for usuario in self._usuarios.values():
            if usuario.email == email:
                return usuario
        return None
    
    def crear(self, usuario: Usuario) -> Usuario:
        usuario.id = self._next_id
        self._usuarios[self._next_id] = usuario
        self._next_id += 1
        return usuario

# Uso en tests
class TestAuthService:
    def setup_method(self):
        self.usuario_repo = FakeUsuarioRepository()
        self.auth_service = AuthService(self.usuario_repo)
    
    def test_registrar_usuario_asigna_id(self):
        usuario = self.auth_service.registrar_usuario(
            "Test", "test@test.com", TipoUsuario.ALUMNO
        )
        assert usuario.id == 1
        assert self.usuario_repo.obtener_por_id(1) == usuario
```

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/tests.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        python -m pytest tests/ \
          --cov=src \
          --cov-report=xml \
          --cov-fail-under=80
    
    - name: Upload coverage
      uses: codecov/codecov-action@v1
```

---

**[⬅️ Volver al README principal](../README.md)**