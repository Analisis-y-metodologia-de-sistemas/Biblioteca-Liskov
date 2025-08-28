# Componentes Reutilizables - Sistema Biblioteca Liskov

## Descripción General

Este documento detalla los componentes reutilizables del sistema, organizados por carpetas y funcionalidades. Estos componentes están diseñados para ser independientes, modulares y fácilmente extensibles.

## 🔧 Componentes por Carpeta

### 📁 `src/shared/` - Utilidades Compartidas

#### **Logger (`logger.py`)**
**Ubicación**: `src/shared/logger.py`

```python
# Uso básico
from src.shared.logger import get_logger

logger = get_logger()
logger.info("Operación exitosa")
logger.error("Error en la operación")
logger.warning("Advertencia")
```

**Funcionalidades**:
- ✅ Logging configurado con rotación de archivos
- ✅ Diferentes niveles (INFO, ERROR, WARNING, DEBUG)
- ✅ Formato estandarizado con timestamps
- ✅ Almacenamiento en archivos por fecha

**Reutilización**:
- Cualquier módulo del sistema puede usarlo
- Configuración centralizada
- Fácil cambio de nivel de logging

#### **MenuUtils (`menu_utils.py`)**
**Ubicación**: `src/shared/menu_utils.py`

```python
# Menú desplegable básico
from src.shared.menu_utils import select_from_list

usuarios = [user1, user2, user3]
usuario_seleccionado = select_from_list(
    title="Seleccione usuario",
    items=usuarios,
    display_func=lambda u: f"{u.nombre} ({u.email})",
    description_func=lambda u: f"Tipo: {u.tipo.value}",
    allow_cancel=True
)

# Confirmación de acciones
from src.shared.menu_utils import confirm_action

if confirm_action("¿Eliminar usuario?", default=False):
    # Proceder con eliminación
    pass

# Mensajes estilizados
from src.shared.menu_utils import show_success, show_error, show_warning

show_success("Usuario creado exitosamente")
show_error("Error al conectar con la base de datos")
show_warning("El usuario ya existe")
```

**Funcionalidades**:
- ✅ **Menús desplegables navegables** con teclas ↑↓
- ✅ **Selección por número directo** (1-9)
- ✅ **Cancelación** con ESC/Q
- ✅ **Descripciones contextuales** de elementos
- ✅ **Confirmaciones interactivas** (Sí/No)
- ✅ **Mensajes estilizados** con colores
- ✅ **Funciones de visualización** customizables

**Reutilización**:
- Cualquier interfaz de consola
- Sistemas de administración CLI
- Scripts de configuración interactivos
- Herramientas de desarrollo

#### **Config (`config.py`)**
**Ubicación**: `src/shared/config.py`

```python
# Configuración centralizada
from src.shared.config import DATABASE_PATH, LOG_LEVEL

# Usar en otros módulos
conn = sqlite3.connect(DATABASE_PATH)
```

**Funcionalidades**:
- ✅ Variables de configuración centralizadas
- ✅ Fácil modificación sin tocar código
- ✅ Valores por defecto sensatos

**Reutilización**:
- Todos los módulos del sistema
- Tests unitarios con configuración diferente
- Entornos de desarrollo/producción

#### **Exceptions (`exceptions.py`)**
**Ubicación**: `src/shared/exceptions.py`

```python
# Excepciones específicas del dominio
from src.shared.exceptions import BibliotecaException, UsuarioNoEncontradoException

try:
    usuario = buscar_usuario(email)
    if not usuario:
        raise UsuarioNoEncontradoException(f"No existe usuario con email: {email}")
except BibliotecaException as e:
    logger.error(f"Error de biblioteca: {e}")
```

**Funcionalidades**:
- ✅ Jerarquía de excepciones del dominio
- ✅ Mensajes de error contextuales
- ✅ Códigos de error consistentes

**Reutilización**:
- Manejo de errores en toda la aplicación
- APIs y servicios web
- Sistemas de logging estructurado

### 📁 `src/domain/` - Núcleo del Dominio

#### **Entidades (`entities.py`)**
**Ubicación**: `src/domain/entities.py`

```python
# Entidades reutilizables con dataclasses
from src.domain.entities import Usuario, ItemBiblioteca, TipoUsuario

# Crear usuario
usuario = Usuario(
    nombre="Juan",
    apellido="Pérez", 
    email="juan@email.com",
    tipo=TipoUsuario.ALUMNO
)

# Usar enums
if usuario.tipo == TipoUsuario.DOCENTE:
    dias_prestamo = 30
else:
    dias_prestamo = 15
```

**Funcionalidades**:
- ✅ **Dataclasses** con validación automática
- ✅ **Enums tipados** para estados y categorías
- ✅ **Campos opcionales** con valores por defecto
- ✅ **Inmutabilidad** cuando es necesaria

**Reutilización**:
- APIs REST (serialización JSON automática)
- Interfaces gráficas
- Sistemas de reportes
- Integraciones con otros sistemas

#### **Interfaces de Repositorio (`repositories.py`)**
**Ubicación**: `src/domain/repositories.py`

```python
# Contratos claros para persistencia
from src.domain.repositories import IUsuarioRepository
from abc import ABC, abstractmethod

class MongoUsuarioRepository(IUsuarioRepository):
    """Implementación para MongoDB"""
    
    def crear(self, usuario: Usuario) -> Usuario:
        # Implementación específica de MongoDB
        pass
    
    def obtener_por_email(self, email: str) -> Usuario:
        # Implementación específica de MongoDB
        pass

# En servicios de aplicación
class UsuarioService:
    def __init__(self, repo: IUsuarioRepository):  # Acepta cualquier implementación
        self.repo = repo
```

**Funcionalidades**:
- ✅ **Contratos claros** con ABC
- ✅ **Intercambio fácil** de implementaciones
- ✅ **Testing** simplificado con mocks
- ✅ **Múltiples fuentes de datos**

**Reutilización**:
- Cambio de SQLite a PostgreSQL/MongoDB
- Implementaciones para testing
- Cacheo de datos
- APIs externas como fuente de datos

### 📁 `src/infrastructure/` - Infraestructura Técnica

#### **DatabaseConnection (`database.py`)**
**Ubicación**: `src/infrastructure/database.py`

```python
# Conexión reutilizable a base de datos
from src.infrastructure.database import DatabaseConnection

class MiRepositorio:
    def __init__(self):
        self.db = DatabaseConnection("mi_base.db")
    
    def obtener_datos(self):
        return self.db.execute_query(
            "SELECT * FROM tabla WHERE condicion = ?",
            (valor,)
        )
```

**Funcionalidades**:
- ✅ **Gestión automática** de conexiones
- ✅ **Manejo de transacciones**
- ✅ **Queries parametrizadas** (seguridad)
- ✅ **Pool de conexiones** implícito

**Reutilización**:
- Múltiples bases de datos SQLite
- Sistemas de auditoría
- Módulos de reportes
- Scripts de migración

#### **ORM Simple (`database.py`)**
**Ubicación**: `src/infrastructure/database.py`

```python
# ORM simplificado reutilizable
from src.infrastructure.database import ORM

orm = ORM(db_connection)

# Operaciones CRUD genéricas
id_usuario = orm.insert("usuarios", {
    "nombre": "Juan",
    "email": "juan@email.com"
})

usuarios = orm.select("usuarios", "activo = ?", (True,))

orm.update("usuarios", {"activo": False}, "id = ?", (id_usuario,))
```

**Funcionalidades**:
- ✅ **Operaciones CRUD genéricas**
- ✅ **Queries dinámicas**
- ✅ **Parámetros seguros**
- ✅ **Manejo de tipos automático**

**Reutilización**:
- Prototipos rápidos
- Sistemas administrativos
- Scripts de migración de datos
- Herramientas de testing

### 📁 `src/application/` - Lógica de Aplicación

#### **Servicios de Aplicación (`services.py`)**
**Ubicación**: `src/application/services.py`

```python
# Patrón de servicio reutilizable
from src.application.services import UsuarioService

# Extensión para nuevos casos de uso
class UsuarioAdvancedService(UsuarioService):
    def __init__(self, usuario_repo, email_service):
        super().__init__(usuario_repo)
        self.email_service = email_service
    
    def registrar_y_notificar(self, datos_usuario):
        usuario = self.registrar_usuario(**datos_usuario)
        self.email_service.enviar_bienvenida(usuario.email)
        return usuario
```

**Funcionalidades**:
- ✅ **Casos de uso bien definidos**
- ✅ **Inyección de dependencias**
- ✅ **Validaciones de negocio**
- ✅ **Transacciones coordinadas**

**Reutilización**:
- APIs REST como controllers
- Interfaces gráficas
- Sistemas batch
- Integraciones con sistemas externos

## 🎯 Patrones de Reutilización Implementados

### 1. **Dependency Injection**
```python
# Container de dependencias
class Container:
    @staticmethod
    def build_usuario_service():
        db_conn = DatabaseConnection()
        orm = ORM(db_conn)
        repo = SQLiteUsuarioRepository(orm)
        return UsuarioService(repo)
```

### 2. **Repository Pattern**
```python
# Intercambio fácil de implementaciones
def crear_usuario_service(tipo_db="sqlite"):
    if tipo_db == "sqlite":
        repo = SQLiteUsuarioRepository()
    elif tipo_db == "mongo":
        repo = MongoUsuarioRepository()
    else:
        repo = InMemoryUsuarioRepository()
    
    return UsuarioService(repo)
```

### 3. **Strategy Pattern**
```python
# MenuUtils usa strategy para diferentes displays
select_from_list(
    items=usuarios,
    display_func=lambda u: u.email,           # Estrategia simple
    display_func=lambda u: f"{u.nombre} ({u.tipo})",  # Estrategia compleja
    description_func=lambda u: f"ID: {u.id}"  # Estrategia para descripción
)
```

### 4. **Observer Pattern**
```python
# Logger como observer de eventos
class EventLogger:
    def __init__(self, logger):
        self.logger = logger
    
    def on_usuario_creado(self, evento):
        self.logger.info(f"Usuario creado: {evento.usuario.email}")
```

## 🚀 Ejemplos de Extensión

### **Nuevo Sistema de Notificaciones**
```python
# Usar componentes existentes
from src.shared.logger import get_logger
from src.shared.menu_utils import confirm_action, show_success
from src.domain.entities import Usuario

class NotificationService:
    def __init__(self):
        self.logger = get_logger()
    
    def enviar_notificacion(self, usuario: Usuario, mensaje: str):
        if confirm_action(f"¿Enviar notificación a {usuario.email}?"):
            # Lógica de envío
            self.logger.info(f"Notificación enviada a {usuario.email}")
            show_success("Notificación enviada exitosamente")
```

### **Nueva Interfaz Web**
```python
# Reutilizar servicios existentes
from src.application.services import UsuarioService, PrestamoService

class WebController:
    def __init__(self, usuario_service: UsuarioService):
        self.usuario_service = usuario_service  # Mismo servicio, nueva interfaz
    
    def crear_usuario_endpoint(self, datos_json):
        try:
            usuario = self.usuario_service.registrar_usuario(**datos_json)
            return {"success": True, "usuario_id": usuario.id}
        except Exception as e:
            return {"success": False, "error": str(e)}
```

### **Sistema de Reportes**
```python
# Reutilizar repositorios para reportes
from src.domain.repositories import IUsuarioRepository, IPrestamoRepository

class ReportService:
    def __init__(self, usuario_repo: IUsuarioRepository, prestamo_repo: IPrestamoRepository):
        self.usuario_repo = usuario_repo
        self.prestamo_repo = prestamo_repo
    
    def generar_reporte_usuarios_activos(self):
        usuarios = self.usuario_repo.listar_todos()
        activos = [u for u in usuarios if u.activo]
        return {
            "total_usuarios": len(usuarios),
            "usuarios_activos": len(activos),
            "porcentaje_activos": len(activos) / len(usuarios) * 100
        }
```

## 📦 Distribución de Componentes

### **Como Paquete Independiente**
```python
# setup.py para distribuir MenuUtils
from setuptools import setup

setup(
    name="interactive-menu-utils",
    version="1.0.0",
    packages=["menu_utils"],
    install_requires=["colorama"],
    description="Interactive console menus with navigation"
)
```

### **Como Microservicio**
```python
# API REST usando servicios existentes
from flask import Flask, jsonify
from src.application.services import UsuarioService

app = Flask(__name__)
usuario_service = Container.build_usuario_service()

@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = usuario_service.listar_usuarios()
    return jsonify([{
        "id": u.id,
        "nombre": u.nombre,
        "email": u.email
    } for u in usuarios])
```

## ✅ Beneficios de la Reutilización

1. **Desarrollo más rápido**: Componentes probados y listos
2. **Consistencia**: Comportamiento uniforme en toda la aplicación  
3. **Mantenimiento simplificado**: Cambios centralizados
4. **Testing facilitado**: Componentes aislados y mockables
5. **Extensibilidad**: Fácil agregar nuevas funcionalidades
6. **Calidad**: Componentes batalla-probados y refinados