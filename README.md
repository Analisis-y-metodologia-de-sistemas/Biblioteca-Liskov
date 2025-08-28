# Sistema de Gestión Bibliotecaria - Biblioteca Liskov

## Descripción Técnica y Arquitectura

Sistema de gestión bibliotecaria implementado siguiendo principios de **Clean Architecture** y patrones de diseño enterprise. El sistema demuestra la aplicación práctica de los principios SOLID, patrones de diseño GoF, y arquitectura hexagonal en un dominio de negocio real.

## Patrones de Diseño y Principios Aplicados

### 🏗️ Arquitectura Hexagonal (Ports & Adapters Pattern)

**Implementación**: El sistema está estructurado en capas concéntricas donde el dominio es independiente de los detalles de infraestructura.

**Componentes**:
- **Puertos (Interfaces)**: `src/domain/repositories.py` - Define contratos de acceso a datos
- **Adaptadores**: `src/infrastructure/repositories.py` - Implementaciones concretas
- **Núcleo**: `src/domain/entities.py` - Lógica de negocio pura

**Beneficio**: Permite intercambiar implementaciones (SQLite → PostgreSQL) sin afectar la lógica de negocio.

### 🎯 Principios SOLID

#### S - Single Responsibility Principle
- **AuthService** (`src/application/auth_service.py`): Solo maneja autenticación
- **PrestamoService** (`src/application/services.py`): Solo gestiona préstamos
- **Cada Entity**: Una responsabilidad de negocio específica

#### O - Open/Closed Principle
- **Repository Interfaces**: Abiertas para extensión via herencia
- **Service Layer**: Nuevos servicios sin modificar existentes
- **Entity Validation**: Extensible via decoradores

#### L - Liskov Substitution Principle
- **Repository Implementations**: Intercambiables sin afectar comportamiento
- **Service Interfaces**: Cualquier implementación mantiene el contrato
- **Entity Hierarchies**: Subclases mantienen invariantes del padre

#### I - Interface Segregation Principle
- **Repositories específicos**: `UsuarioRepository`, `ItemRepository`, etc.
- **Service Interfaces**: Separadas por dominio de responsabilidad
- **No fat interfaces**: Cada interfaz define solo lo necesario

#### D - Dependency Inversion Principle
- **Services dependen de abstracciones**: `AuthService(usuario_repo: UsuarioRepository)`
- **Infrastructure depende de Domain**: Repository implementa interface del dominio
- **Injection via Constructor**: Dependencias inyectadas, no instanciadas

### 🏭 Patrones de Diseño GoF

#### Repository Pattern

**¿Qué es?**: Patrón que encapsula la lógica de acceso a datos y centraliza las consultas comunes. Actúa como una colección en memoria de objetos del dominio.

**¿Por qué usarlo?**: 
- Separa la lógica de negocio de la persistencia
- Facilita testing mediante mocks/stubs
- Permite cambiar el almacén de datos sin afectar la lógica de negocio
- Centraliza consultas complejas

**Principios involucrados**:
- **Single Responsibility**: Cada repository maneja un solo agregado
- **Dependency Inversion**: Domain define la interfaz, Infrastructure la implementa
- **Open/Closed**: Extensible para nuevas consultas sin modificar existentes

```python
# Interface (Puerto) - Dominio define el contrato
class UsuarioRepository(ABC):
    @abstractmethod
    def obtener_por_email(self, email: str) -> Optional[Usuario]:
        """Busca usuario por email único"""
        pass
    
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Usuario]:
        """Busca usuario por ID"""
        pass
    
    @abstractmethod
    def crear(self, usuario: Usuario) -> Usuario:
        """Persiste nuevo usuario"""
        pass

# Implementación (Adaptador) - Infrastructure implementa el contrato
class SQLiteUsuarioRepository(UsuarioRepository):
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection
    
    def obtener_por_email(self, email: str) -> Optional[Usuario]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
        row = cursor.fetchone()
        return self._map_to_entity(row) if row else None
    
    def _map_to_entity(self, row) -> Usuario:
        # Mapeo de datos de BD a entidad de dominio
        return Usuario(id=row[0], nombre=row[1], email=row[2])
```

**Ubicación**: `src/domain/repositories.py` (interfaces), `src/infrastructure/repositories.py` (implementaciones)
**Beneficio**: Domain layer no conoce detalles de SQLite, MongoDB, o cualquier BD específica

#### Service Layer Pattern

**¿Qué es?**: Capa que define las operaciones disponibles en la aplicación y coordina la respuesta de la aplicación para cada operación. Encapsula la lógica de aplicación.

**¿Por qué usarlo?**:
- Mantiene transaccionalidad entre múltiples operaciones
- Coordina múltiples objetos de dominio
- Proporciona una API clara para casos de uso
- Maneja la lógica de aplicación (no de dominio)

**Principios involucrados**:
- **Single Responsibility**: Cada servicio maneja un área funcional específica
- **Dependency Inversion**: Depende de interfaces, no implementaciones concretas
- **Interface Segregation**: Servicios específicos por dominio funcional

```python
class PrestamoService:
    def __init__(self, 
                 prestamo_repo: PrestamoRepository, 
                 item_repo: ItemRepository, 
                 usuario_repo: UsuarioRepository,
                 logger: Logger):
        # Inyección de dependencias - NO instanciación
        self.prestamo_repo = prestamo_repo
        self.item_repo = item_repo  
        self.usuario_repo = usuario_repo
        self.logger = logger
    
    def realizar_prestamo(self, usuario_id: int, item_id: int) -> Prestamo:
        """Caso de uso: Realizar préstamo de libro"""
        # 1. Validaciones de negocio
        usuario = self._obtener_usuario_valido(usuario_id)
        item = self._obtener_item_disponible(item_id)
        
        # 2. Aplicar reglas de dominio
        if not usuario.puede_realizar_prestamos():
            raise UsuarioConRestriccionesError("Usuario tiene multas pendientes")
        
        if not item.esta_disponible():
            raise ItemNoDisponibleError("Item sin stock disponible")
        
        # 3. Coordinar operaciones transaccionales
        prestamo = Prestamo(usuario_id=usuario_id, item_id=item_id)
        prestamo_creado = self.prestamo_repo.crear(prestamo)
        item.reducir_disponibilidad()
        self.item_repo.actualizar(item)
        
        # 4. Logging de auditoria
        self.logger.info(f"Préstamo realizado: {prestamo_creado.id}")
        
        return prestamo_creado
    
    def _obtener_usuario_valido(self, usuario_id: int) -> Usuario:
        """Helper method - Validación común"""
        usuario = self.usuario_repo.obtener_por_id(usuario_id)
        if not usuario:
            raise UsuarioNoEncontradoError(f"Usuario {usuario_id} no existe")
        return usuario
```

**Ubicación**: `src/application/services.py`
**Beneficio**: Separa lógica de aplicación (orquestación) de lógica de dominio (reglas de negocio)

#### Domain Model Pattern
```python
class Usuario:
    def puede_realizar_prestamos(self) -> bool:
        return self.activo and len(self.multas_pendientes) == 0
    
    def obtener_limite_prestamos(self) -> int:
        return self.tipo_usuario.limite_prestamos
```

**Ubicación**: `src/domain/entities.py`
**Propósito**: Encapsula lógica de negocio en las entidades

#### Factory Pattern
```python
# En container.py - Service Locator/Factory hybrid
class Container:
    def get_auth_service(self) -> AuthService:
        return AuthService(self.get_usuario_repository())
```

**Ubicación**: `src/container.py`
**Propósito**: Centraliza creación y configuración de objetos

#### Command Pattern (Implícito)
```python
class PrestamoService:
    def realizar_prestamo(self, usuario_id: int, item_id: int) -> Prestamo:
        # Comando que encapsula toda la operación
```

**Ubicación**: Métodos de servicios en `src/application/services.py`
**Propósito**: Encapsula operaciones complejas como comandos ejecutables

### 🔧 Patrones Arquitectónicos Adicionales

#### Dependency Injection Container
**Implementación**: `src/container.py`
```python
class Container:
    def __init__(self):
        self._database = DatabaseConnection()
    
    def get_prestamo_service(self) -> PrestamoService:
        return PrestamoService(
            self.get_prestamo_repository(),
            self.get_item_repository(), 
            self.get_usuario_repository()
        )
```

#### Data Transfer Object (DTO) Pattern
**Uso implícito**: Las entidades actúan como DTOs entre capas
**Beneficio**: Datos estructurados sin lógica de persistencia

#### Unit of Work Pattern (Simplificado)

**¿Qué es?**: Patrón que mantiene una lista de objetos afectados por una transacción de negocio y coordina la escritura de cambios y resolución de problemas de concurrencia.

**¿Por qué usarlo?**:
- Garantiza atomicidad en operaciones complejas
- Maneja transacciones de base de datos
- Evita inconsistencias parciales
- Centraliza control de transacciones

**Principios involucrados**:
- **Atomicity**: Todo se ejecuta o nada se ejecuta
- **Consistency**: Mantiene invariantes del dominio
- **Single Responsibility**: Se encarga solo de coordinar transacciones

**Implementación en el proyecto**:
```python
class PrestamoService:
    def realizar_prestamo(self, usuario_id: int, item_id: int) -> Prestamo:
        """Unit of Work implícito - Operación transaccional completa"""
        try:
            # BEGIN TRANSACTION (implícita)
            
            # 1. Validar estado inicial
            usuario = self.usuario_repo.obtener_por_id(usuario_id)
            item = self.item_repo.obtener_por_id(item_id)
            self._validar_prestamo_posible(usuario, item)
            
            # 2. Realizar cambios coordinados
            prestamo = Prestamo(usuario_id=usuario_id, item_id=item_id)
            prestamo_creado = self.prestamo_repo.crear(prestamo)
            
            # 3. Actualizar estado del item
            item.reducir_disponibilidad()  # Modifica el aggregate
            self.item_repo.actualizar(item)  # Persiste el cambio
            
            # 4. Log de auditoria
            self.logger.info(f"Préstamo {prestamo_creado.id} completado")
            
            # COMMIT TRANSACTION (implícita)
            return prestamo_creado
            
        except Exception as e:
            # ROLLBACK TRANSACTION (implícita)
            self.logger.error(f"Error en préstamo: {e}")
            raise PrestamoFailedError("No se pudo completar el préstamo") from e

# Implementación más explícita con contexto de transacción
class TransactionalPrestamoService:
    def __init__(self, unit_of_work: UnitOfWork):
        self.uow = unit_of_work
    
    def realizar_prestamo(self, usuario_id: int, item_id: int) -> Prestamo:
        with self.uow:  # Context manager para transacciones
            # Todas las operaciones dentro del contexto son transaccionales
            usuario = self.uow.usuarios.obtener_por_id(usuario_id)
            item = self.uow.items.obtener_por_id(item_id)
            
            prestamo = Prestamo(usuario_id=usuario_id, item_id=item_id)
            self.uow.prestamos.crear(prestamo)
            
            item.reducir_disponibilidad()
            self.uow.items.actualizar(item)
            
            # Commit automático al salir del context manager
            return prestamo
```

**Ubicación**: Implementación simplificada en servicios de `src/application/services.py`
**Beneficio avanzado**: Una implementación completa incluiría un UnitOfWork explicit con context managers para manejo de transacciones más robusto

### 🏛️ Layered Architecture (Arquitectura en Capas)

**¿Qué es?**: Patrón arquitectónico que organiza el sistema en capas horizontales, donde cada capa solo puede comunicarse con la capa inmediatamente inferior.

**¿Por qué usarla?**:
- **Separación de responsabilidades**: Cada capa tiene un propósito específico
- **Reutilización**: Capas inferiores pueden ser reutilizadas por múltiples capas superiores  
- **Testabilidad**: Cada capa puede ser probada independientemente
- **Mantenibilidad**: Cambios en una capa no afectan otras capas

**Principios involucrados**:
- **Single Responsibility**: Cada capa tiene una responsabilidad específica
- **Dependency Rule**: Las dependencias apuntan hacia adentro (hacia el dominio)
- **Abstraction**: Capas superiores no conocen detalles de implementación de capas inferiores

#### Capas del Sistema Biblioteca Liskov:

```python
# 🎭 PRESENTATION LAYER (Capa de Presentación)
# Responsabilidad: Interfaz de usuario y formateo de datos
# Ubicación: src/presentation/
class ConsoleUI:
    def __init__(self, auth_service: AuthService, prestamo_service: PrestamoService):
        # Depende SOLO de Application Layer
        self.auth_service = auth_service
        self.prestamo_service = prestamo_service
    
    def mostrar_menu_principal(self):
        """Lógica de presentación - formateo y navegación"""
        opciones = self._formatear_opciones()
        seleccion = self._obtener_seleccion_usuario()
        self._procesar_seleccion(seleccion)

# 🧠 APPLICATION LAYER (Capa de Aplicación) 
# Responsabilidad: Casos de uso y orquestación de dominio
# Ubicación: src/application/
class PrestamoService:
    def __init__(self, prestamo_repo: PrestamoRepository):
        # Depende SOLO de Domain Layer (interfaces)
        self.prestamo_repo = prestamo_repo
    
    def realizar_prestamo(self, usuario_id: int, item_id: int) -> Prestamo:
        """Caso de uso: coordina objetos de dominio"""
        # Orquesta sin lógica de negocio - eso es responsabilidad del dominio

# 💎 DOMAIN LAYER (Capa de Dominio)
# Responsabilidad: Lógica de negocio y reglas empresariales  
# Ubicación: src/domain/
class Usuario:
    def puede_realizar_prestamos(self) -> bool:
        """Regla de negocio encapsulada en la entidad"""
        return self.activo and not self.tiene_multas_pendientes()
    
    def obtener_limite_prestamos(self) -> int:
        """Lógica de dominio basada en tipo de usuario"""
        return self.tipo_usuario.limite_prestamos

# 🔧 INFRASTRUCTURE LAYER (Capa de Infraestructura)
# Responsabilidad: Detalles técnicos y acceso a recursos externos
# Ubicación: src/infrastructure/
class SQLiteUsuarioRepository:
    def __init__(self, connection: sqlite3.Connection):
        # Implementa interfaces definidas en Domain Layer
        self.connection = connection
    
    def obtener_por_id(self, id: int) -> Optional[Usuario]:
        """Detalle de implementación - SQL específico"""
        # Conoce detalles de SQLite, mapeo de datos, etc.
```

#### Flujo de Dependencias (Dependency Rule):

```
🎭 Presentation Layer
    ↓ (depende de)
🧠 Application Layer  
    ↓ (depende de)
💎 Domain Layer
    ↑ (implementa interfaces de)
🔧 Infrastructure Layer
```

**Regla fundamental**: Las dependencias apuntan hacia adentro. El Domain Layer no conoce nada sobre capas exteriores.

#### Beneficios Específicos en Biblioteca Liskov:

1. **Presentation Independence**: 
   - Podemos cambiar de Console UI a Web UI sin afectar lógica de negocio
   - Diferentes formatos de salida (JSON, XML, HTML) sin cambios en Application Layer

2. **Database Independence**: 
   - Migrar de SQLite a PostgreSQL solo requiere nueva implementación de Repository
   - Domain Layer permanece inalterado

3. **Framework Independence**:
   - No dependemos de frameworks específicos en el core del sistema
   - Frameworks viven en Infrastructure Layer

4. **Testability**:
   - Domain Layer: Tests unitarios puros sin dependencias externas
   - Application Layer: Tests con mocks de repositories
   - Integration Tests: Solo en Infrastructure Layer

#### Ejemplo de Violación vs Cumplimiento:

```python
# ❌ VIOLACIÓN - Domain Layer conociendo Infrastructure
class Usuario:
    def guardar_en_base(self):
        # ¡MAL! Domain no debe conocer detalles de persistencia
        connection = sqlite3.connect("biblioteca.db")
        connection.execute("INSERT INTO usuarios...")

# ✅ CORRECTO - Domain puro, Infrastructure separada  
class Usuario:
    def puede_realizar_prestamos(self) -> bool:
        # ✓ BIEN - Solo lógica de negocio
        return self.activo and not self.tiene_multas_pendientes()

class SQLiteUsuarioRepository:
    def crear(self, usuario: Usuario) -> Usuario:
        # ✓ BIEN - Infrastructure maneja persistencia
        connection = sqlite3.connect("biblioteca.db")
        # ... implementación específica de SQLite
```

### 📐 Domain-Driven Design (DDD) Concepts

#### Entities vs Value Objects
- **Entities**: `Usuario`, `Item`, `Prestamo` (tienen identidad)
- **Value Objects**: `TipoUsuario`, `EstadoPrestamo` (definidos por valor)

#### Aggregate Roots
- **Usuario**: Agrega sus préstamos, reservas y multas
- **Item**: Agrega su disponibilidad y reservas
- **Prestamo**: Agrega sus multas asociadas

#### Domain Services
```python
class MultaService:
    def generar_multas_por_retraso(self):
        # Lógica de dominio que no pertenece a una entidad específica
```

### 🔒 Principios de Seguridad y Robustez

#### Fail-Fast Principle
```python
def realizar_prestamo(self, usuario_id: int, item_id: int) -> Prestamo:
    usuario = self.usuario_repo.obtener_por_id(usuario_id)
    if not usuario:
        raise UsuarioNoEncontradoError(f"Usuario {usuario_id} no existe")
```

#### Exception Handling Strategy
**Ubicación**: `src/shared/exceptions.py`
```python
class BibliotecaBaseException(Exception):
    """Base exception para errores del dominio"""

class UsuarioNoEncontradoError(BibliotecaBaseException):
    """Usuario específico no encontrado"""
```

#### Logging Strategy
**Implementación**: `src/shared/logger.py`
- **Audit Trail**: Todas las operaciones críticas se registran
- **Error Tracking**: Excepciones capturadas y loggeadas
- **Performance Monitoring**: Tiempos de operación registrados

## Ventajas de la Implementación

### ✅ Mantenibilidad
- **Bajo acoplamiento**: Cambios en UI no afectan lógica de negocio
- **Alta cohesión**: Cada componente tiene responsabilidad clara
- **Testabilidad**: Dependencias mockeable via interfaces

### ✅ Extensibilidad  
- **Nuevos adaptadores**: Fácil agregar REST API, GraphQL
- **Nuevas reglas de negocio**: Extensibles via herencia o composición
- **Nuevos tipos de usuario**: Polimorfismo via enum/inheritance

### ✅ Robustez
- **Validación en capas**: Domain, Application y Presentation
- **Transaccionalidad**: Operaciones atómicas a nivel servicio
- **Error handling**: Estrategia consistente de manejo de errores

## 🛠️ Características Principales

- 🏗️ **Arquitectura Hexagonal**: Separación clara entre dominio, aplicación e infraestructura
- 👥 **Gestión de Usuarios**: Alumnos, docentes y empleados con diferentes privilegios
- 📚 **Catálogo de Libros**: Gestión completa del inventario
- 🔄 **Sistema de Préstamos**: Control de préstamos y devoluciones
- 💰 **Gestión de Multas**: Cálculo automático y seguimiento
- 📅 **Sistema de Reservas**: Reserva de libros no disponibles
- 🧪 **Testing Completo**: Tests unitarios e integración

## Arquitectura del Sistema

### Arquitectura Hexagonal (Ports & Adapters)

```mermaid
graph TB
    subgraph "Presentation Layer"
        UI[Console UI]
        API[API Interface]
    end
    
    subgraph "Application Layer"
        AS[Auth Service]
        US[Usuario Service]
        IS[Item Service]
        PS[Prestamo Service]
        RS[Reserva Service]
        MS[Multa Service]
    end
    
    subgraph "Domain Layer"
        E[Entities]
        R[Repository Interfaces]
        V[Value Objects]
    end
    
    subgraph "Infrastructure Layer"
        DB[(SQLite Database)]
        REPO[Repository Implementations]
        LOG[Logger]
    end
    
    UI --> AS
    UI --> US
    UI --> IS
    UI --> PS
    UI --> RS
    UI --> MS
    
    AS --> E
    US --> E
    IS --> E
    PS --> E
    RS --> E
    MS --> E
    
    AS --> R
    US --> R
    IS --> R
    PS --> R
    RS --> R
    MS --> R
    
    R --> REPO
    REPO --> DB
    
    style E fill:#4a90e2,stroke:#2171b5,stroke-width:2px,color:#fff
    style R fill:#7b68ee,stroke:#5a4fcf,stroke-width:2px,color:#fff
    style AS fill:#5cb85c,stroke:#449d44,stroke-width:2px,color:#fff
    style US fill:#5cb85c,stroke:#449d44,stroke-width:2px,color:#fff
    style IS fill:#5cb85c,stroke:#449d44,stroke-width:2px,color:#fff
    style PS fill:#5cb85c,stroke:#449d44,stroke-width:2px,color:#fff
    style RS fill:#5cb85c,stroke:#449d44,stroke-width:2px,color:#fff
    style MS fill:#5cb85c,stroke:#449d44,stroke-width:2px,color:#fff
    style UI fill:#f0ad4e,stroke:#ec971f,stroke-width:2px,color:#fff
    style API fill:#f0ad4e,stroke:#ec971f,stroke-width:2px,color:#fff
    style DB fill:#d9534f,stroke:#c9302c,stroke-width:2px,color:#fff
    style REPO fill:#d9534f,stroke:#c9302c,stroke-width:2px,color:#fff
    style LOG fill:#d9534f,stroke:#c9302c,stroke-width:2px,color:#fff
    style V fill:#4a90e2,stroke:#2171b5,stroke-width:2px,color:#fff
```

## Arquitectura C4

### Nivel 1: Contexto del Sistema

```mermaid
graph TB
    subgraph "Biblioteca Universitaria"
        SGB[Sistema de Gestión<br/>de Biblioteca]
    end
    
    subgraph "Actores"
        A[👨‍🎓 Alumno]
        D[👨‍🏫 Docente]
        E[👩‍💼 Empleado]
    end
    
    subgraph "Sistemas Externos"
        SE[📧 Sistema de<br/>Notificaciones]
    end
    
    A -->|Consulta catálogo<br/>Realiza préstamos<br/>Gestiona reservas| SGB
    D -->|Consulta catálogo<br/>Realiza préstamos<br/>Gestiona reservas| SGB
    E -->|Administra usuarios<br/>Gestiona inventario<br/>Procesa multas| SGB
    
    SGB -->|Envía notificaciones<br/>de vencimientos| SE
    
    style SGB fill:#4a90e2,stroke:#2171b5,stroke-width:3px,color:#fff
    style A fill:#5cb85c,stroke:#449d44,stroke-width:2px,color:#fff
    style D fill:#5cb85c,stroke:#449d44,stroke-width:2px,color:#fff
    style E fill:#f0ad4e,stroke:#ec971f,stroke-width:2px,color:#fff
    style SE fill:#d9534f,stroke:#c9302c,stroke-width:2px,color:#fff
```

### Nivel 2: Contenedores

```mermaid
graph TB
    subgraph "Sistema de Gestión de Biblioteca"
        subgraph "Aplicación"
            UI[🖥️ Interfaz de Usuario<br/>Console Application<br/>Python]
            API[🔌 API Layer<br/>Application Services<br/>Python]
        end
        
        subgraph "Datos"
            DB[(🗄️ Base de Datos<br/>SQLite<br/>Almacena usuarios,<br/>libros, préstamos)]
        end
        
        subgraph "Logging"
            LOG[📝 Sistema de Logs<br/>Python Logging<br/>Auditoria del sistema]
        end
    end
    
    subgraph "Usuarios"
        U[👥 Usuarios del Sistema<br/>Alumnos, Docentes, Empleados]
    end
    
    U -->|Interactúa con| UI
    UI -->|Llama a| API
    API -->|Lee/Escribe| DB
    API -->|Registra eventos| LOG
    
    style UI fill:#f0ad4e,stroke:#ec971f,stroke-width:2px,color:#fff
    style API fill:#5cb85c,stroke:#449d44,stroke-width:2px,color:#fff
    style DB fill:#d9534f,stroke:#c9302c,stroke-width:2px,color:#fff
    style LOG fill:#7b68ee,stroke:#5a4fcf,stroke-width:2px,color:#fff
    style U fill:#4a90e2,stroke:#2171b5,stroke-width:2px,color:#fff
```

### Nivel 3: Componentes

```mermaid
graph TB
    subgraph "Presentation Layer"
        UI[Console UI]
        MU[Menu Utils]
    end
    
    subgraph "Application Layer"
        AS[Auth Service]
        PS[Prestamo Service]
        US[Usuario Service]
        IS[Item Service]
        RS[Reserva Service]
        MS[Multa Service]
    end
    
    subgraph "Domain Layer"
        subgraph "Entities"
            UE[Usuario]
            IE[Item]
            PE[Prestamo]
            RE[Reserva]
            ME[Multa]
        end
        
        subgraph "Repository Interfaces"
            URI[Usuario Repository<br/>Interface]
            IRI[Item Repository<br/>Interface]
            PRI[Prestamo Repository<br/>Interface]
            RRI[Reserva Repository<br/>Interface]
            MRI[Multa Repository<br/>Interface]
        end
    end
    
    subgraph "Infrastructure Layer"
        subgraph "Repository Implementations"
            UR[Usuario Repository]
            IR[Item Repository]
            PR[Prestamo Repository]
            RR[Reserva Repository]
            MR[Multa Repository]
        end
        
        subgraph "Data Access"
            DB[(SQLite Database)]
            DBC[Database Connection]
        end
    end
    
    subgraph "Shared"
        CFG[Configuration]
        LOG[Logger]
        EX[Exceptions]
    end
    
    UI --> AS
    UI --> PS
    UI --> US
    UI --> IS
    UI --> RS
    UI --> MS
    UI --> MU
    
    AS --> UE
    PS --> PE
    US --> UE
    IS --> IE
    RS --> RE
    MS --> ME
    
    AS --> URI
    PS --> PRI
    US --> URI
    IS --> IRI
    RS --> RRI
    MS --> MRI
    
    URI --> UR
    IRI --> IR
    PRI --> PR
    RRI --> RR
    MRI --> MR
    
    UR --> DBC
    IR --> DBC
    PR --> DBC
    RR --> DBC
    MR --> DBC
    
    DBC --> DB
    
    AS --> LOG
    PS --> LOG
    US --> LOG
    IS --> LOG
    RS --> LOG
    MS --> LOG
    
    AS --> CFG
    PS --> CFG
    US --> CFG
    IS --> CFG
    RS --> CFG
    MS --> CFG
    
    style UE fill:#4a90e2,stroke:#2171b5,stroke-width:2px,color:#fff
    style IE fill:#4a90e2,stroke:#2171b5,stroke-width:2px,color:#fff
    style PE fill:#4a90e2,stroke:#2171b5,stroke-width:2px,color:#fff
    style RE fill:#4a90e2,stroke:#2171b5,stroke-width:2px,color:#fff
    style ME fill:#4a90e2,stroke:#2171b5,stroke-width:2px,color:#fff
    style URI fill:#7b68ee,stroke:#5a4fcf,stroke-width:2px,color:#fff
    style IRI fill:#7b68ee,stroke:#5a4fcf,stroke-width:2px,color:#fff
    style PRI fill:#7b68ee,stroke:#5a4fcf,stroke-width:2px,color:#fff
    style RRI fill:#7b68ee,stroke:#5a4fcf,stroke-width:2px,color:#fff
    style MRI fill:#7b68ee,stroke:#5a4fcf,stroke-width:2px,color:#fff
    style AS fill:#5cb85c,stroke:#449d44,stroke-width:2px,color:#fff
    style PS fill:#5cb85c,stroke:#449d44,stroke-width:2px,color:#fff
    style US fill:#5cb85c,stroke:#449d44,stroke-width:2px,color:#fff
    style IS fill:#5cb85c,stroke:#449d44,stroke-width:2px,color:#fff
    style RS fill:#5cb85c,stroke:#449d44,stroke-width:2px,color:#fff
    style MS fill:#5cb85c,stroke:#449d44,stroke-width:2px,color:#fff
    style UI fill:#f0ad4e,stroke:#ec971f,stroke-width:2px,color:#fff
    style MU fill:#f0ad4e,stroke:#ec971f,stroke-width:2px,color:#fff
    style DB fill:#d9534f,stroke:#c9302c,stroke-width:2px,color:#fff
    style DBC fill:#d9534f,stroke:#c9302c,stroke-width:2px,color:#fff
    style UR fill:#d9534f,stroke:#c9302c,stroke-width:2px,color:#fff
    style IR fill:#d9534f,stroke:#c9302c,stroke-width:2px,color:#fff
    style PR fill:#d9534f,stroke:#c9302c,stroke-width:2px,color:#fff
    style RR fill:#d9534f,stroke:#c9302c,stroke-width:2px,color:#fff
    style MR fill:#d9534f,stroke:#c9302c,stroke-width:2px,color:#fff
```

## Modelo de Datos

### Diagrama Entidad-Relación

```mermaid
erDiagram
    Usuario {
        int id PK
        string nombre
        string email
        string tipo_usuario
        boolean activo
        datetime fecha_registro
    }
    
    Item {
        int id PK
        string titulo
        string autor
        string isbn
        int cantidad_total
        int cantidad_disponible
        string categoria
        boolean activo
    }
    
    Prestamo {
        int id PK
        int usuario_id FK
        int item_id FK
        date fecha_prestamo
        date fecha_vencimiento
        date fecha_devolucion
        string estado
    }
    
    Reserva {
        int id PK
        int usuario_id FK
        int item_id FK
        datetime fecha_reserva
        date fecha_expiracion
        string estado
    }
    
    Multa {
        int id PK
        int usuario_id FK
        int prestamo_id FK
        decimal monto
        string motivo
        datetime fecha_creacion
        boolean pagada
    }
    
    Usuario ||--o{ Prestamo : "realiza"
    Usuario ||--o{ Reserva : "hace"
    Usuario ||--o{ Multa : "tiene"
    Item ||--o{ Prestamo : "se presta"
    Item ||--o{ Reserva : "se reserva"
    Prestamo ||--o{ Multa : "genera"
```

## Diagramas de Clases por Módulos

### Módulo Domain - Entidades

```mermaid
classDiagram
    class Usuario {
        -int id
        -str nombre
        -str email
        -TipoUsuario tipo_usuario
        -bool activo
        -datetime fecha_registro
        +__init__(nombre, email, tipo_usuario)
        +es_activo() bool
        +puede_realizar_prestamos() bool
        +obtener_limite_prestamos() int
    }
    
    class Item {
        -int id
        -str titulo
        -str autor
        -str isbn
        -int cantidad_total
        -int cantidad_disponible
        -str categoria
        -bool activo
        +__init__(titulo, autor, isbn, cantidad_total)
        +esta_disponible() bool
        +reducir_disponibilidad()
        +aumentar_disponibilidad()
    }
    
    class TipoUsuario {
        <<enumeration>>
        ALUMNO
        DOCENTE
        EMPLEADO
    }
    
    Usuario --> TipoUsuario
```

### Módulo Domain - Operaciones

```mermaid
classDiagram
    class Prestamo {
        -int id
        -int usuario_id
        -int item_id
        -date fecha_prestamo
        -date fecha_vencimiento
        -date fecha_devolucion
        -EstadoPrestamo estado
        +__init__(usuario_id, item_id)
        +esta_vencido() bool
        +devolver()
        +calcular_dias_retraso() int
    }
    
    class Reserva {
        -int id
        -int usuario_id
        -int item_id
        -datetime fecha_reserva
        -date fecha_expiracion
        -EstadoReserva estado
        +__init__(usuario_id, item_id)
        +esta_expirada() bool
        +activar()
        +cancelar()
    }
    
    class Multa {
        -int id
        -int usuario_id
        -int prestamo_id
        -decimal monto
        -str motivo
        -datetime fecha_creacion
        -bool pagada
        +__init__(usuario_id, prestamo_id, monto, motivo)
        +marcar_como_pagada()
        +esta_pagada() bool
    }
    
    class EstadoPrestamo {
        <<enumeration>>
        ACTIVO
        DEVUELTO
        VENCIDO
    }
    
    class EstadoReserva {
        <<enumeration>>
        ACTIVA
        EXPIRADA
        CANCELADA
        COMPLETADA
    }
    
    Prestamo --> EstadoPrestamo
    Reserva --> EstadoReserva
```

### Módulo Application - Servicios

```mermaid
classDiagram
    class AuthService {
        -UsuarioRepository usuario_repo
        +__init__(usuario_repo)
        +autenticar(email: str) Usuario
        +registrar_usuario(nombre, email, tipo) Usuario
    }
    
    class PrestamoService {
        -PrestamoRepository prestamo_repo
        -ItemRepository item_repo
        -UsuarioRepository usuario_repo
        +__init__(repos)
        +realizar_prestamo(usuario_id, item_id) Prestamo
        +devolver_prestamo(prestamo_id) bool
        +listar_prestamos_usuario(usuario_id) List[Prestamo]
        +listar_prestamos_vencidos() List[Prestamo]
    }
    
    class MultaService {
        -MultaRepository multa_repo
        -PrestamoRepository prestamo_repo
        +__init__(repos)
        +generar_multas_por_retraso()
        +pagar_multa(multa_id) bool
        +obtener_multas_usuario(usuario_id) List[Multa]
    }
    
    class ReservaService {
        -ReservaRepository reserva_repo
        -ItemRepository item_repo
        +__init__(repos)
        +crear_reserva(usuario_id, item_id) Reserva
        +procesar_reservas_expiradas()
        +cancelar_reserva(reserva_id) bool
    }
```

## Diagramas de Secuencia

### Proceso de Préstamo

```mermaid
sequenceDiagram
    participant U as Usuario
    participant UI as Console UI
    participant PS as PrestamoService
    participant IR as ItemRepository
    participant PR as PrestamoRepository
    participant DB as Database
    
    U->>UI: Solicitar préstamo
    UI->>PS: realizar_prestamo(usuario_id, item_id)
    
    PS->>IR: obtener_por_id(item_id)
    IR->>DB: SELECT * FROM items WHERE id = ?
    DB-->>IR: item_data
    IR-->>PS: Item
    
    alt Item disponible
        PS->>PR: crear_prestamo(prestamo)
        PR->>DB: INSERT INTO prestamos
        DB-->>PR: prestamo_id
        
        PS->>IR: reducir_disponibilidad(item_id)
        IR->>DB: UPDATE items SET cantidad_disponible = ?
        
        PR-->>PS: Prestamo
        PS-->>UI: Prestamo exitoso
        UI-->>U: Confirmación de préstamo
    else Item no disponible
        PS-->>UI: Error - Item no disponible
        UI-->>U: Mensaje de error
    end
```

### Proceso de Devolución con Multa

```mermaid
sequenceDiagram
    participant U as Usuario
    participant UI as Console UI
    participant PS as PrestamoService
    participant MS as MultaService
    participant PR as PrestamoRepository
    participant MR as MultaRepository
    participant DB as Database
    
    U->>UI: Devolver libro
    UI->>PS: devolver_prestamo(prestamo_id)
    
    PS->>PR: obtener_por_id(prestamo_id)
    PR->>DB: SELECT * FROM prestamos WHERE id = ?
    DB-->>PR: prestamo_data
    PR-->>PS: Prestamo
    
    alt Préstamo vencido
        PS->>MS: generar_multa_por_retraso(prestamo)
        MS->>MR: crear_multa(multa)
        MR->>DB: INSERT INTO multas
        DB-->>MR: multa_id
        MR-->>MS: Multa
        MS-->>PS: Multa generada
    end
    
    PS->>PR: marcar_como_devuelto(prestamo_id)
    PR->>DB: UPDATE prestamos SET estado = 'DEVUELTO'
    
    PS-->>UI: Devolución completada
    UI-->>U: Confirmación (+ info de multa si aplica)
```

### Gestión de Reservas

```mermaid
sequenceDiagram
    participant U as Usuario
    participant UI as Console UI
    participant RS as ReservaService
    participant IR as ItemRepository
    participant RR as ReservaRepository
    participant DB as Database
    
    U->>UI: Reservar libro
    UI->>RS: crear_reserva(usuario_id, item_id)
    
    RS->>IR: obtener_por_id(item_id)
    IR->>DB: SELECT * FROM items WHERE id = ?
    DB-->>IR: item_data
    IR-->>RS: Item
    
    alt Item no disponible
        RS->>RR: crear_reserva(reserva)
        RR->>DB: INSERT INTO reservas
        DB-->>RR: reserva_id
        RR-->>RS: Reserva
        RS-->>UI: Reserva creada
        UI-->>U: Confirmación de reserva
    else Item disponible
        RS-->>UI: Item disponible para préstamo directo
        UI-->>U: Sugerir préstamo inmediato
    end
```

## Estructura del Proyecto

```
Biblioteca_Liskov/
├── src/
│   ├── domain/
│   │   ├── entities.py          # Entidades del dominio
│   │   └── repositories.py      # Interfaces de repositorios
│   ├── application/
│   │   ├── services.py          # Servicios de aplicación
│   │   ├── interfaces.py        # Interfaces de servicios
│   │   └── auth_service.py      # Servicio de autenticación
│   ├── infrastructure/
│   │   ├── database.py          # Configuración de base de datos
│   │   └── repositories.py      # Implementación de repositorios
│   ├── presentation/
│   │   └── console_ui.py        # Interfaz de consola
│   └── shared/
│       ├── config.py            # Configuración
│       ├── logger.py            # Sistema de logging
│       ├── exceptions.py        # Excepciones personalizadas
│       └── menu_utils.py        # Utilidades de menú
├── tests/
│   ├── unit/                    # Tests unitarios
│   └── integration/             # Tests de integración
├── data/
│   └── biblioteca.db            # Base de datos SQLite
├── docs/                        # Documentación adicional
├── scripts/                     # Scripts de utilidad
└── main.py                      # Punto de entrada
```

## Tecnologías Utilizadas

- **Python 3.11+**: Lenguaje principal
- **SQLite**: Base de datos
- **Architecture**: Hexagonal (Ports & Adapters)
- **Testing**: unittest (Python estándar)
- **Logging**: Python logging module

## Instalación y Ejecución

### Prerrequisitos
- Python 3.11 o superior

### Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/Analisis-y-metodologia-de-sistemas/Biblioteca-Liskov.git
cd Biblioteca-Liskov
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecutar el sistema:
```bash
python main.py
```

### Ejecutar Tests

```bash
# Tests unitarios
python -m pytest tests/unit/

# Tests de integración
python -m pytest tests/integration/

# Todos los tests
python -m pytest tests/
```

## Casos de Uso Principales

### 1. Gestión de Usuarios
- Registro de nuevos usuarios
- Autenticación de usuarios existentes
- Gestión de permisos por tipo de usuario

### 2. Gestión de Préstamos
- Realizar préstamo de libros
- Devolver libros prestados
- Consultar préstamos activos
- Renovar préstamos

### 3. Gestión de Multas
- Generación automática por retrasos
- Consulta de multas pendientes
- Pago de multas

### 4. Sistema de Reservas
- Reservar libros no disponibles
- Notificación cuando el libro esté disponible
- Cancelación de reservas

## Principios de Diseño Aplicados

### SOLID
- **S**: Cada servicio tiene una responsabilidad específica
- **O**: Las clases están abiertas para extensión, cerradas para modificación
- **L**: Las implementaciones son intercambiables por sus interfaces
- **I**: Interfaces específicas por dominio
- **D**: Dependencia de abstracciones, no de concreciones

### Arquitectura Hexagonal
- **Dominio**: Lógica de negocio pura
- **Aplicación**: Orquestación de casos de uso
- **Infraestructura**: Detalles técnicos
- **Presentation**: Interfaz de usuario

## Contribuir

1. Fork del proyecto
2. Crear rama para feature (`git checkout -b feature/AmazingFeature`)
3. Commit de cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## Licencia

Este proyecto es parte del curso de Análisis y Metodología de Sistemas.