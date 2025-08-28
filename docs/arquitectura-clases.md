# Diagrama de Clases - Sistema Biblioteca Liskov

## Descripción General

Este diagrama representa la arquitectura del Sistema de Gestión de Biblioteca Liskov siguiendo los principios de **Arquitectura Limpia (Clean Architecture)** y **Hexagonal Architecture**, organizando las clases por capas y responsabilidades.

## Arquitectura por Capas

### 🎯 **Capa de Dominio** (`src/domain/`)
Contiene las entidades de negocio puras, independientes de frameworks y tecnologías externas.

#### Entidades de Dominio
- **Usuario**: Representa usuarios del sistema (Alumnos, Docentes, Bibliotecarios)
- **ItemBiblioteca**: Materiales disponibles en la biblioteca
- **Prestamo**: Transacciones de préstamo de items
- **Reserva**: Sistema de reservas para items no disponibles
- **Multa**: Penalizaciones por retrasos o daños

#### Enumeraciones
- **TipoUsuario**: ALUMNO, DOCENTE, BIBLIOTECARIO
- **EstadoItem**: DISPONIBLE, PRESTADO, EN_REPARACION, PERDIDO
- **CategoriaItem**: LIBRO, REVISTA, DVD, CD, AUDIOBOOK, OTRO

### 🏢 **Capa de Aplicación** (`src/application/`)
Contiene los casos de uso, servicios de aplicación e interfaces que definen los contratos que necesita la aplicación.

#### Servicios de Aplicación
- **UsuarioService**: Casos de uso relacionados con usuarios
- **ItemBibliotecaService**: Casos de uso para gestión de items
- **PrestamoService**: Lógica de préstamos y devoluciones
- **ReservaService**: Gestión de reservas
- **MultaService**: Administración de multas

#### Interfaces de Repositorio (Contratos)
- **IUsuarioRepository**: Define operaciones para gestión de usuarios
- **IItemBibliotecaRepository**: Define operaciones para gestión de items
- **IPrestamoRepository**: Define operaciones para gestión de préstamos
- **IReservaRepository**: Define operaciones para gestión de reservas
- **IMultaRepository**: Define operaciones para gestión de multas

### 🏗️ **Capa de Infraestructura** (`src/infrastructure/`)
Implementaciones concretas de tecnologías específicas.

#### Base de Datos
- **DatabaseConnection**: Manejo de conexiones SQLite
- **ORM**: Mapeo objeto-relacional simplificado

#### Repositorios Concretos
- **SQLiteUsuarioRepository**: Implementación SQLite para usuarios
- **SQLiteItemBibliotecaRepository**: Implementación SQLite para items
- **SQLitePrestamoRepository**: Implementación SQLite para préstamos
- **SQLiteReservaRepository**: Implementación SQLite para reservas
- **SQLiteMultaRepository**: Implementación SQLite para multas

### 🎨 **Capa de Presentación** (`src/presentation/`)
Interfaz de usuario y controladores.

#### Interfaces de Usuario
- **ConsoleUI**: Interfaz de línea de comandos con menús interactivos

### 🔧 **Capa Compartida** (`src/shared/`)
Utilidades y componentes reutilizables.

#### Utilidades Comunes
- **Logger**: Sistema de logging
- **Config**: Configuración del sistema
- **Exceptions**: Excepciones personalizadas
- **MenuUtils**: Utilidades para menús desplegables interactivos

#### Componentes de Interfaz
- **MenuItem**: Elemento de menú con valor y descripción
- **DropdownMenu**: Menú desplegable navegable con teclas

### ⚙️ **Configuración e Inyección** (`src/`)
- **Container**: Contenedor de inyección de dependencias
- **Main**: Punto de entrada de la aplicación

## Diagrama Mermaid

```mermaid
classDiagram
    %% CAPA DE DOMINIO
    namespace Domain {
        class Usuario {
            +int id
            +string nombre
            +string apellido
            +string email
            +TipoUsuario tipo
            +string numero_identificacion
            +string telefono
            +bool activo
            +datetime fecha_registro
        }
        
        class ItemBiblioteca {
            +int id
            +string titulo
            +string autor
            +string isbn
            +CategoriaItem categoria
            +EstadoItem estado
            +string descripcion
            +string ubicacion
            +datetime fecha_adquisicion
            +float valor_reposicion
        }
        
        class Prestamo {
            +int id
            +int usuario_id
            +int item_id
            +datetime fecha_prestamo
            +datetime fecha_devolucion_esperada
            +datetime fecha_devolucion_real
            +string observaciones
            +bool activo
        }
        
        class Reserva {
            +int id
            +int usuario_id
            +int item_id
            +datetime fecha_reserva
            +datetime fecha_expiracion
            +bool activa
        }
        
        class Multa {
            +int id
            +int usuario_id
            +int prestamo_id
            +float monto
            +string descripcion
            +datetime fecha_multa
            +bool pagada
        }
        
        class TipoUsuario {
            <<enumeration>>
            ALUMNO
            DOCENTE
            BIBLIOTECARIO
        }
        
        class EstadoItem {
            <<enumeration>>
            DISPONIBLE
            PRESTADO
            EN_REPARACION
            PERDIDO
        }
        
        class CategoriaItem {
            <<enumeration>>
            LIBRO
            REVISTA
            DVD
            CD
            AUDIOBOOK
            OTRO
        }
        
        class IUsuarioRepository {
            <<interface>>
            +crear(usuario: Usuario) Usuario
            +obtener_por_id(id: int) Usuario
            +obtener_por_email(email: string) Usuario
            +listar_todos() List~Usuario~
            +actualizar(usuario: Usuario) Usuario
            +eliminar(id: int) bool
        }
        
        class IItemBibliotecaRepository {
            <<interface>>
            +crear(item: ItemBiblioteca) ItemBiblioteca
            +obtener_por_id(id: int) ItemBiblioteca
            +buscar_por_titulo(titulo: string) List~ItemBiblioteca~
            +buscar_por_autor(autor: string) List~ItemBiblioteca~
            +listar_por_categoria(categoria: string) List~ItemBiblioteca~
            +listar_todos() List~ItemBiblioteca~
            +actualizar(item: ItemBiblioteca) ItemBiblioteca
            +eliminar(id: int) bool
        }
        
        class IPrestamoRepository {
            <<interface>>
            +crear(prestamo: Prestamo) Prestamo
            +obtener_por_id(id: int) Prestamo
            +listar_por_usuario(usuario_id: int) List~Prestamo~
            +listar_activos() List~Prestamo~
            +actualizar(prestamo: Prestamo) Prestamo
        }
        
        class IReservaRepository {
            <<interface>>
            +crear(reserva: Reserva) Reserva
            +obtener_por_id(id: int) Reserva
            +listar_por_usuario(usuario_id: int) List~Reserva~
            +listar_activas() List~Reserva~
            +actualizar(reserva: Reserva) Reserva
        }
        
        class IMultaRepository {
            <<interface>>
            +crear(multa: Multa) Multa
            +obtener_por_id(id: int) Multa
            +listar_por_usuario(usuario_id: int) List~Multa~
            +listar_no_pagadas() List~Multa~
            +actualizar(multa: Multa) Multa
        }
    }
    
    %% CAPA DE APLICACIÓN
    namespace Application {
        class UsuarioService {
            -IUsuarioRepository usuario_repo
            +registrar_usuario(...) Usuario
            +buscar_usuario_por_email(email: string) Usuario
            +listar_usuarios() List~Usuario~
            +actualizar_usuario(usuario: Usuario) Usuario
        }
        
        class ItemBibliotecaService {
            -IItemBibliotecaRepository item_repo
            +agregar_item(...) ItemBiblioteca
            +buscar_por_titulo(titulo: string) List~ItemBiblioteca~
            +buscar_por_autor(autor: string) List~ItemBiblioteca~
            +listar_por_categoria(categoria: string) List~ItemBiblioteca~
            +listar_disponibles() List~ItemBiblioteca~
            +cambiar_estado_item(item_id: int, estado: EstadoItem) ItemBiblioteca
        }
        
        class PrestamoService {
            -IPrestamoRepository prestamo_repo
            -IItemBibliotecaRepository item_repo
            -IUsuarioRepository usuario_repo
            -IMultaRepository multa_repo
            +realizar_prestamo(usuario_id: int, item_id: int, dias: int) Prestamo
            +devolver_item(prestamo_id: int, observaciones: string) Prestamo
            +listar_prestamos_activos() List~Prestamo~
            +listar_prestamos_usuario(usuario_id: int) List~Prestamo~
        }
        
        class ReservaService {
            -IReservaRepository reserva_repo
            -IItemBibliotecaRepository item_repo
            -IUsuarioRepository usuario_repo
            +realizar_reserva(usuario_id: int, item_id: int, dias: int) Reserva
            +cancelar_reserva(reserva_id: int) Reserva
            +listar_reservas_activas() List~Reserva~
        }
        
        class MultaService {
            -IMultaRepository multa_repo
            -IUsuarioRepository usuario_repo
            +pagar_multa(multa_id: int) Multa
            +listar_multas_pendientes() List~Multa~
            +listar_multas_usuario(usuario_id: int) List~Multa~
        }
    }
    
    %% CAPA DE INFRAESTRUCTURA
    namespace Infrastructure {
        class DatabaseConnection {
            -string db_path
            +get_connection() Connection
            +execute_query(query: string, params: tuple) List~Dict~
            +execute_non_query(query: string, params: tuple) int
            +execute_script(script: string) void
        }
        
        class ORM {
            -DatabaseConnection db
            +create_tables() void
            +insert(table: string, data: Dict) int
            +select(table: string, where: string, params: tuple) List~Dict~
            +update(table: string, data: Dict, where: string, params: tuple) int
            +delete(table: string, where: string, params: tuple) int
        }
        
        class SQLiteUsuarioRepository {
            -ORM orm
            +crear(usuario: Usuario) Usuario
            +obtener_por_id(id: int) Usuario
            +obtener_por_email(email: string) Usuario
            +listar_todos() List~Usuario~
            +actualizar(usuario: Usuario) Usuario
            +eliminar(id: int) bool
        }
        
        class SQLiteItemBibliotecaRepository {
            -ORM orm
            +crear(item: ItemBiblioteca) ItemBiblioteca
            +obtener_por_id(id: int) ItemBiblioteca
            +buscar_por_titulo(titulo: string) List~ItemBiblioteca~
            +buscar_por_autor(autor: string) List~ItemBiblioteca~
            +listar_por_categoria(categoria: string) List~ItemBiblioteca~
            +listar_todos() List~ItemBiblioteca~
            +actualizar(item: ItemBiblioteca) ItemBiblioteca
            +eliminar(id: int) bool
        }
        
        class SQLitePrestamoRepository {
            -ORM orm
            +crear(prestamo: Prestamo) Prestamo
            +obtener_por_id(id: int) Prestamo
            +listar_por_usuario(usuario_id: int) List~Prestamo~
            +listar_activos() List~Prestamo~
            +actualizar(prestamo: Prestamo) Prestamo
        }
        
        class SQLiteReservaRepository {
            -ORM orm
            +crear(reserva: Reserva) Reserva
            +obtener_por_id(id: int) Reserva
            +listar_por_usuario(usuario_id: int) List~Reserva~
            +listar_activas() List~Reserva~
            +actualizar(reserva: Reserva) Reserva
        }
        
        class SQLiteMultaRepository {
            -ORM orm
            +crear(multa: Multa) Multa
            +obtener_por_id(id: int) Multa
            +listar_por_usuario(usuario_id: int) List~Multa~
            +listar_no_pagadas() List~Multa~
            +actualizar(multa: Multa) Multa
        }
    }
    
    %% CAPA DE PRESENTACIÓN
    namespace Presentation {
        class ConsoleUI {
            -UsuarioService usuario_service
            -ItemBibliotecaService item_service
            -PrestamoService prestamo_service
            -ReservaService reserva_service
            -MultaService multa_service
            -Logger logger
            +ejecutar() void
            +mostrar_menu_principal() void
            +registrar_usuario() void
            +agregar_item() void
            +realizar_prestamo() void
            +listar_usuarios() void
            +listar_items_disponibles() void
        }
    }
    
    %% CAPA COMPARTIDA
    namespace Shared {
        class Logger {
            +get_logger() Logger
            +info(message: string) void
            +error(message: string) void
            +warning(message: string) void
        }
        
        class Config {
            +DATABASE_PATH string
            +LOG_LEVEL string
        }
        
        class BibliotecaException {
            +message string
        }
        
        class MenuItem {
            +string text
            +Any value
            +string description
        }
        
        class MenuUtils {
            +select_from_list(...) Any
            +show_dropdown_menu(...) MenuItem
            +confirm_action(message: string, default: bool) bool
            +show_success(message: string) void
            +show_error(message: string) void
            +show_warning(message: string) void
            +show_info(message: string, title: string) void
        }
    }
    
    %% CONFIGURACIÓN
    namespace Root {
        class Container {
            +build_usuario_service() UsuarioService
            +build_item_service() ItemBibliotecaService
            +build_prestamo_service() PrestamoService
            +build_reserva_service() ReservaService
            +build_multa_service() MultaService
        }
        
        class Main {
            +main() void
        }
    }
    
    %% RELACIONES DE COMPOSICIÓN Y DEPENDENCIAS
    Usuario ||--o{ Prestamo
    ItemBiblioteca ||--o{ Prestamo
    Usuario ||--o{ Reserva
    ItemBiblioteca ||--o{ Reserva
    Usuario ||--o{ Multa
    Prestamo ||--o{ Multa
    
    UsuarioService --> IUsuarioRepository
    ItemBibliotecaService --> IItemBibliotecaRepository
    PrestamoService --> IPrestamoRepository
    PrestamoService --> IItemBibliotecaRepository
    PrestamoService --> IUsuarioRepository
    PrestamoService --> IMultaRepository
    ReservaService --> IReservaRepository
    ReservaService --> IItemBibliotecaRepository
    ReservaService --> IUsuarioRepository
    MultaService --> IMultaRepository
    MultaService --> IUsuarioRepository
    
    SQLiteUsuarioRepository ..|> IUsuarioRepository
    SQLiteItemBibliotecaRepository ..|> IItemBibliotecaRepository
    SQLitePrestamoRepository ..|> IPrestamoRepository
    SQLiteReservaRepository ..|> IReservaRepository
    SQLiteMultaRepository ..|> IMultaRepository
    
    SQLiteUsuarioRepository --> ORM
    SQLiteItemBibliotecaRepository --> ORM
    SQLitePrestamoRepository --> ORM
    SQLiteReservaRepository --> ORM
    SQLiteMultaRepository --> ORM
    
    ORM --> DatabaseConnection
    
    ConsoleUI --> UsuarioService
    ConsoleUI --> ItemBibliotecaService
    ConsoleUI --> PrestamoService
    ConsoleUI --> ReservaService
    ConsoleUI --> MultaService
    ConsoleUI --> MenuUtils
    ConsoleUI --> Logger
    
    Container --> UsuarioService
    Container --> ItemBibliotecaService
    Container --> PrestamoService
    Container --> ReservaService
    Container --> MultaService
    
    Main --> Container
    Main --> ConsoleUI
```

## Principios Aplicados

### 🔄 **Inversión de Dependencias**
- Las capas superiores dependen de abstracciones (interfaces)
- Las implementaciones concretas están en la capa de infraestructura

### 🎯 **Separación de Responsabilidades**
- **Dominio**: Lógica de negocio pura
- **Aplicación**: Casos de uso
- **Infraestructura**: Detalles técnicos
- **Presentación**: Interfaz de usuario

### 🧩 **Inyección de Dependencias**
- Container centralizado para crear e inyectar dependencias
- Facilita testing y mantenimiento

### 🔒 **Encapsulación**
- Cada capa tiene responsabilidades bien definidas
- Interfaces públicas claramente definidas

### 🚀 **Extensibilidad**
- Fácil agregar nuevas implementaciones (web UI, REST API)
- Cambio de base de datos sin afectar lógica de negocio
- Nuevos casos de uso sin modificar código existente

## Beneficios de esta Arquitectura

1. **Testabilidad**: Fácil crear unit tests con mocks
2. **Mantenibilidad**: Cambios aislados por capas
3. **Flexibilidad**: Intercambio de implementaciones
4. **Escalabilidad**: Estructura preparada para crecimiento
5. **Independencia**: Lógica de negocio independiente de frameworks