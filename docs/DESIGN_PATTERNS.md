# 🎯 Patrones de Diseño - Biblioteca Liskov

## Índice

1. [Principios SOLID](#principios-solid)
2. [Patrones de Diseño GoF](#patrones-de-diseño-gof)
3. [Patrones Arquitectónicos](#patrones-arquitectónicos)
4. [Domain-Driven Design](#domain-driven-design)
5. [Principios de Seguridad](#principios-de-seguridad)

## Principios SOLID

### S - Single Responsibility Principle

**Definición**: Cada clase debe tener una única razón para cambiar.

**Implementación en el proyecto**:
- **AuthService** (`src/application/auth_service.py`): Solo maneja autenticación
- **PrestamoService** (`src/application/services.py`): Solo gestiona préstamos
- **Cada Entity**: Una responsabilidad de negocio específica

```python
# ✅ CORRECTO - Una sola responsabilidad
class AuthService:
    def __init__(self, usuario_repo: UsuarioRepository):
        self.usuario_repo = usuario_repo
    
    def autenticar(self, email: str) -> Usuario:
        """Solo se encarga de autenticación"""
        return self.usuario_repo.obtener_por_email(email)
    
    def registrar_usuario(self, nombre: str, email: str, tipo: TipoUsuario) -> Usuario:
        """Solo se encarga de registro"""
        usuario = Usuario(nombre=nombre, email=email, tipo_usuario=tipo)
        return self.usuario_repo.crear(usuario)

# ❌ INCORRECTO - Múltiples responsabilidades
class AuthAndEmailService:
    def autenticar(self, email: str) -> Usuario:
        # Autenticación
        pass
    
    def enviar_email_bienvenida(self, usuario: Usuario):
        # Envío de emails - DIFERENTE responsabilidad
        pass
    
    def generar_reporte_usuarios(self):
        # Generación de reportes - OTRA responsabilidad diferente
        pass
```

### O - Open/Closed Principle

**Definición**: Las clases deben estar abiertas para extensión pero cerradas para modificación.

```python
# ✅ CORRECTO - Extensible sin modificar
from abc import ABC, abstractmethod

class UsuarioRepository(ABC):
    @abstractmethod
    def obtener_por_email(self, email: str) -> Optional[Usuario]:
        pass
    
    @abstractmethod
    def crear(self, usuario: Usuario) -> Usuario:
        pass

# Extensión para SQLite - NO modifica la interfaz
class SQLiteUsuarioRepository(UsuarioRepository):
    def obtener_por_email(self, email: str) -> Optional[Usuario]:
        # Implementación específica SQLite
        pass

# Extensión para MongoDB - NO modifica la interfaz
class MongoUsuarioRepository(UsuarioRepository):
    def obtener_por_email(self, email: str) -> Optional[Usuario]:
        # Implementación específica MongoDB
        pass

# Extensión para nuevos métodos
class ExtendedUsuarioRepository(UsuarioRepository):
    def obtener_por_email(self, email: str) -> Optional[Usuario]:
        pass
    
    def crear(self, usuario: Usuario) -> Usuario:
        pass
    
    # NUEVO método sin modificar la base
    def buscar_por_patron(self, patron: str) -> List[Usuario]:
        pass
```

### L - Liskov Substitution Principle

**Definición**: Los objetos de clases derivadas deben poder reemplazar objetos de la clase base sin alterar el funcionamiento.

```python
# ✅ CORRECTO - Implementaciones intercambiables
class PrestamoService:
    def __init__(self, prestamo_repo: PrestamoRepository):
        # Cualquier implementación de PrestamoRepository funciona
        self.prestamo_repo = prestamo_repo
    
    def realizar_prestamo(self, usuario_id: int, item_id: int) -> Prestamo:
        # Funciona igual con SQLitePrestamoRepository o PostgreSQLPrestamoRepository
        prestamo = Prestamo(usuario_id=usuario_id, item_id=item_id)
        return self.prestamo_repo.crear(prestamo)

# Las implementaciones mantienen el comportamiento esperado
class SQLitePrestamoRepository(PrestamoRepository):
    def crear(self, prestamo: Prestamo) -> Prestamo:
        # Retorna Prestamo con ID asignado - MANTIENE CONTRATO
        # Lanza excepción si falla - MANTIENE CONTRATO
        pass

class PostgreSQLPrestamoRepository(PrestamoRepository):
    def crear(self, prestamo: Prestamo) -> Prestamo:
        # MISMO comportamiento que SQLite - INTERCAMBIABLE
        pass
```

### I - Interface Segregation Principle

**Definición**: Los clientes no deben depender de interfaces que no usan.

```python
# ✅ CORRECTO - Interfaces específicas
class UsuarioRepository(ABC):
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Usuario]:
        pass
    
    @abstractmethod
    def obtener_por_email(self, email: str) -> Optional[Usuario]:
        pass

class ItemRepository(ABC):
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Item]:
        pass
    
    @abstractmethod
    def buscar_por_titulo(self, titulo: str) -> List[Item]:
        pass

class PrestamoRepository(ABC):
    @abstractmethod
    def crear(self, prestamo: Prestamo) -> Prestamo:
        pass
    
    @abstractmethod
    def obtener_por_usuario(self, usuario_id: int) -> List[Prestamo]:
        pass

# Los servicios usan solo las interfaces que necesitan
class PrestamoService:
    def __init__(self, 
                 prestamo_repo: PrestamoRepository,  # Solo métodos de préstamos
                 item_repo: ItemRepository,          # Solo métodos de items
                 usuario_repo: UsuarioRepository):   # Solo métodos de usuarios
        pass

# ❌ INCORRECTO - Fat Interface
class MegaRepository(ABC):
    # Usuario methods
    def obtener_usuario_por_id(self, id: int): pass
    def crear_usuario(self, usuario: Usuario): pass
    
    # Item methods  
    def obtener_item_por_id(self, id: int): pass
    def crear_item(self, item: Item): pass
    
    # Prestamo methods
    def obtener_prestamo_por_id(self, id: int): pass
    def crear_prestamo(self, prestamo: Prestamo): pass
    
    # Los clientes se ven forzados a implementar TODOS los métodos
    # aunque solo necesiten algunos
```

### D - Dependency Inversion Principle

**Definición**: Depender de abstracciones, no de concreciones.

```python
# ✅ CORRECTO - Dependencia de abstracción
class PrestamoService:
    def __init__(self, prestamo_repo: PrestamoRepository):  # ← Interfaz/Abstracción
        self.prestamo_repo = prestamo_repo
    
    def realizar_prestamo(self, usuario_id: int, item_id: int) -> Prestamo:
        # No conoce si es SQLite, PostgreSQL, MongoDB, etc.
        return self.prestamo_repo.crear(prestamo)

# La infraestructura implementa las abstracciones del dominio
class SQLitePrestamoRepository(PrestamoRepository):  # ← Implementa abstracción
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection
    
    def crear(self, prestamo: Prestamo) -> Prestamo:
        # Detalles de implementación específicos
        pass

# ❌ INCORRECTO - Dependencia de concreción
class BadPrestamoService:
    def __init__(self):
        # Dependencia directa de implementación concreta
        self.prestamo_repo = SQLitePrestamoRepository("biblioteca.db")  # ← Concreción
        
    def realizar_prestamo(self, usuario_id: int, item_id: int) -> Prestamo:
        # Acoplado a SQLite - difícil de cambiar y testear
        pass
```

## Patrones de Diseño GoF

### Repository Pattern

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

### Service Layer Pattern

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

### Domain Model Pattern

**¿Qué es?**: Patrón donde las entidades del dominio contienen tanto datos como comportamiento, encapsulando la lógica de negocio.

**¿Por qué usarlo?**:
- La lógica de negocio vive donde conceptualmente pertenece
- Reduce el acoplamiento entre objetos
- Facilita el mantenimiento de reglas complejas
- Hace el código más expresivo y legible

```python
class Usuario:
    def __init__(self, nombre: str, email: str, tipo_usuario: TipoUsuario):
        self.nombre = nombre
        self.email = email
        self.tipo_usuario = tipo_usuario
        self.activo = True
        self.fecha_registro = datetime.now()
        self._multas_pendientes = []
    
    def puede_realizar_prestamos(self) -> bool:
        """Regla de negocio encapsulada en la entidad"""
        return self.activo and not self.tiene_multas_pendientes()
    
    def obtener_limite_prestamos(self) -> int:
        """Lógica de dominio basada en tipo de usuario"""
        limites = {
            TipoUsuario.ALUMNO: 3,
            TipoUsuario.DOCENTE: 5,
            TipoUsuario.EMPLEADO: 10
        }
        return limites.get(self.tipo_usuario, 3)
    
    def tiene_multas_pendientes(self) -> bool:
        """Regla de negocio: usuario con multas no puede hacer préstamos"""
        return len([m for m in self._multas_pendientes if not m.pagada]) > 0
    
    def agregar_multa(self, multa: 'Multa'):
        """Mantiene invariantes del agregado"""
        self._multas_pendientes.append(multa)
        if len(self._multas_pendientes) >= 3:
            self.activo = False  # Regla: 3 multas suspende al usuario

class Item:
    def __init__(self, titulo: str, autor: str, isbn: str, cantidad_total: int):
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.cantidad_total = cantidad_total
        self.cantidad_disponible = cantidad_total
        self.activo = True
    
    def esta_disponible(self) -> bool:
        """Lógica de negocio simple pero importante"""
        return self.activo and self.cantidad_disponible > 0
    
    def reducir_disponibilidad(self):
        """Operación que mantiene invariantes"""
        if not self.esta_disponible():
            raise ItemNoDisponibleError("No hay stock disponible")
        self.cantidad_disponible -= 1
    
    def aumentar_disponibilidad(self):
        """Operación inversa con validación"""
        if self.cantidad_disponible >= self.cantidad_total:
            raise ValueError("No se puede aumentar más allá del total")
        self.cantidad_disponible += 1
```

**Ubicación**: `src/domain/entities.py`

### Factory Pattern

**¿Qué es?**: Patrón que centraliza la creación de objetos complejos y maneja la inyección de dependencias.

**Implementación en Container**:

```python
class Container:
    def __init__(self):
        self._database = None
        self._repositories = {}
        self._services = {}
    
    def get_database_connection(self) -> sqlite3.Connection:
        """Factory para conexión de BD"""
        if not self._database:
            self._database = sqlite3.connect(DATABASE_PATH)
            self._database.row_factory = sqlite3.Row
        return self._database
    
    def get_usuario_repository(self) -> UsuarioRepository:
        """Factory para UsuarioRepository"""
        if 'usuario' not in self._repositories:
            connection = self.get_database_connection()
            self._repositories['usuario'] = SQLiteUsuarioRepository(connection)
        return self._repositories['usuario']
    
    def get_prestamo_service(self) -> PrestamoService:
        """Factory para PrestamoService con todas sus dependencias"""
        if 'prestamo' not in self._services:
            self._services['prestamo'] = PrestamoService(
                prestamo_repo=self.get_prestamo_repository(),
                item_repo=self.get_item_repository(),
                usuario_repo=self.get_usuario_repository(),
                logger=self.get_logger()
            )
        return self._services['prestamo']
```

**Ubicación**: `src/container.py`

### Command Pattern (Implícito)

**¿Qué es?**: Patrón que encapsula una operación completa como un objeto, permitiendo parametrizar, encolar y deshacer operaciones.

```python
class PrestamoService:
    def realizar_prestamo(self, usuario_id: int, item_id: int) -> Prestamo:
        """Comando que encapsula toda la operación de préstamo"""
        # Encapsula:
        # - Validaciones
        # - Lógica de negocio  
        # - Persistencia
        # - Logging
        # Todo como una operación atómica
        
        try:
            # Validar precondiciones
            usuario = self._validar_usuario(usuario_id)
            item = self._validar_item(item_id)
            
            # Ejecutar operación
            prestamo = self._crear_prestamo(usuario, item)
            self._actualizar_inventario(item)
            self._registrar_auditoria(prestamo)
            
            return prestamo
            
        except Exception as e:
            # Rollback implícito en caso de error
            self.logger.error(f"Error en comando realizar_prestamo: {e}")
            raise

# Posible extensión: Comando explícito para operaciones complejas
class RealizarPrestamoCommand:
    def __init__(self, usuario_id: int, item_id: int):
        self.usuario_id = usuario_id
        self.item_id = item_id
        self.executed = False
        self.result = None
    
    def execute(self, prestamo_service: PrestamoService) -> Prestamo:
        if self.executed:
            raise ValueError("Comando ya ejecutado")
        
        self.result = prestamo_service.realizar_prestamo(
            self.usuario_id, 
            self.item_id
        )
        self.executed = True
        return self.result
    
    def undo(self, prestamo_service: PrestamoService):
        if not self.executed or not self.result:
            raise ValueError("No se puede deshacer comando no ejecutado")
        
        prestamo_service.devolver_prestamo(self.result.id)
        self.executed = False
```

## Patrones Arquitectónicos

### Unit of Work Pattern

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

### Dependency Injection Container

**¿Qué es?**: Patrón que centraliza la creación y configuración de objetos, manejando automáticamente las dependencias entre ellos.

```python
class Container:
    def __init__(self):
        self._database = DatabaseConnection()
        self._singletons = {}
    
    def get_prestamo_service(self) -> PrestamoService:
        """Factory con inyección automática de dependencias"""
        if 'prestamo_service' not in self._singletons:
            self._singletons['prestamo_service'] = PrestamoService(
                prestamo_repo=self.get_prestamo_repository(),
                item_repo=self.get_item_repository(), 
                usuario_repo=self.get_usuario_repository(),
                logger=self.get_logger()
            )
        return self._singletons['prestamo_service']
    
    def get_prestamo_repository(self) -> PrestamoRepository:
        return SQLitePrestamoRepository(self._database.get_connection())
    
    def get_logger(self) -> Logger:
        return self._get_configured_logger()
```

### Data Transfer Object (DTO) Pattern

**Uso implícito**: Las entidades actúan como DTOs entre capas, pero mantienen su lógica de negocio en el dominio.

```python
# Las entidades sirven como DTOs entre capas
class Usuario:
    def __init__(self, nombre: str, email: str):
        self.nombre = nombre  # DTO data
        self.email = email    # DTO data
        
    def puede_realizar_prestamos(self) -> bool:
        # Pero también contienen lógica de negocio
        return self.activo and not self.tiene_multas_pendientes()

# Para transferencia pura de datos, se podrían usar dataclasses
from dataclasses import dataclass

@dataclass
class UsuarioDTO:
    id: int
    nombre: str
    email: str
    activo: bool
    
    # Solo datos, sin lógica de negocio
```

## Domain-Driven Design

### Entities vs Value Objects

**Entities**: Objetos con identidad única que persiste a través del tiempo.
- `Usuario`: Identificado por ID, cambia estado pero mantiene identidad
- `Item`: Identificado por ID o ISBN, persiste más allá de cambios
- `Prestamo`: Tiene identidad única, evoluciona en el tiempo

**Value Objects**: Objetos definidos por sus valores, sin identidad única.
- `TipoUsuario`: Enum que representa valores (ALUMNO, DOCENTE, EMPLEADO)
- `EstadoPrestamo`: Enum de estados (ACTIVO, DEVUELTO, VENCIDO)
- `Money`: Para representar montos de multas (si se implementara)

```python
# Entity - Tiene identidad
class Usuario:
    def __init__(self, id: int, nombre: str, email: str):
        self.id = id  # ← Identidad única
        self.nombre = nombre
        self.email = email
    
    def __eq__(self, other):
        # Igualdad basada en identidad, NO en valores
        return isinstance(other, Usuario) and self.id == other.id

# Value Object - Definido por valores
class TipoUsuario(Enum):
    ALUMNO = "alumno"
    DOCENTE = "docente" 
    EMPLEADO = "empleado"
    
    def obtener_limite_prestamos(self) -> int:
        """Comportamiento basado en valor"""
        limits = {
            TipoUsuario.ALUMNO: 3,
            TipoUsuario.DOCENTE: 5,
            TipoUsuario.EMPLEADO: 10
        }
        return limits[self]

# Value Object para dinero (ejemplo)
@dataclass(frozen=True)  # Inmutable
class Money:
    amount: Decimal
    currency: str = "ARS"
    
    def __add__(self, other: 'Money') -> 'Money':
        if self.currency != other.currency:
            raise ValueError("No se pueden sumar monedas de diferentes divisas")
        return Money(self.amount + other.amount, self.currency)
```

### Aggregate Roots

**Definición**: Entidades que controlan el acceso a un conjunto de objetos relacionados, manteniendo invariantes.

```python
class Usuario:  # Aggregate Root
    def __init__(self, nombre: str, email: str):
        self.nombre = nombre
        self.email = email
        self._prestamos = []  # Aggregate interno
        self._multas = []     # Aggregate interno
    
    def realizar_prestamo(self, item: Item) -> Prestamo:
        """Control de invariantes a través del aggregate root"""
        if not self.puede_realizar_prestamos():
            raise UsuarioConRestriccionesError()
        
        if len(self._prestamos) >= self.obtener_limite_prestamos():
            raise LimitePrestamosSuperadoError()
        
        prestamo = Prestamo(self.id, item.id)
        self._prestamos.append(prestamo)  # Mantiene consistencia
        return prestamo
    
    def agregar_multa(self, multa: Multa):
        """Solo el aggregate root puede agregar multas"""
        self._multas.append(multa)
        
        # Invariante: 3 multas = suspensión
        if len([m for m in self._multas if not m.pagada]) >= 3:
            self.activo = False

class Item:  # Aggregate Root
    def __init__(self, titulo: str, cantidad_total: int):
        self.titulo = titulo
        self.cantidad_total = cantidad_total
        self.cantidad_disponible = cantidad_total
        self._reservas = []  # Aggregate interno
    
    def reservar_para_usuario(self, usuario_id: int) -> Reserva:
        """Control de invariantes del aggregate"""
        if self.cantidad_disponible <= 0:
            reserva = Reserva(usuario_id, self.id)
            self._reservas.append(reserva)
            return reserva
        else:
            raise ItemDisponibleError("Item disponible, no requiere reserva")
```

### Domain Services

**¿Cuándo usar?**: Cuando la lógica de negocio no pertenece naturalmente a ninguna entidad específica.

```python
class MultaService:  # Domain Service
    def generar_multas_por_retraso(self):
        """Lógica de dominio que no pertenece a una entidad específica"""
        prestamos_vencidos = self.prestamo_repo.obtener_vencidos()
        
        for prestamo in prestamos_vencidos:
            dias_retraso = self._calcular_dias_retraso(prestamo)
            monto = self._calcular_monto_multa(dias_retraso)
            
            multa = Multa(
                usuario_id=prestamo.usuario_id,
                prestamo_id=prestamo.id,
                monto=monto,
                motivo="Retraso en devolución"
            )
            
            # Utiliza el aggregate root para mantener invariantes
            usuario = self.usuario_repo.obtener_por_id(prestamo.usuario_id)
            usuario.agregar_multa(multa)  # ← A través del aggregate
            
            self.multa_repo.crear(multa)
    
    def _calcular_monto_multa(self, dias_retraso: int) -> Money:
        """Regla de negocio para cálculo de multas"""
        base_amount = Decimal("10.00")  # $10 por día
        return Money(base_amount * dias_retraso)

class ReservaService:  # Domain Service
    def procesar_reservas_expiradas(self):
        """Lógica que coordina múltiples aggregates"""
        reservas_expiradas = self.reserva_repo.obtener_expiradas()
        
        for reserva in reservas_expiradas:
            reserva.marcar_como_expirada()
            self.reserva_repo.actualizar(reserva)
            
            # Notificar próximo en cola
            siguiente_reserva = self.reserva_repo.obtener_siguiente_para_item(
                reserva.item_id
            )
            if siguiente_reserva:
                self._notificar_disponibilidad(siguiente_reserva)
```

## Principios de Seguridad

### Fail-Fast Principle

**Definición**: Fallar rápidamente cuando se detectan condiciones inválidas, en lugar de continuar con estado inconsistente.

```python
def realizar_prestamo(self, usuario_id: int, item_id: int) -> Prestamo:
    """Fail-fast: Validar todo antes de proceder"""
    
    # Fail fast - Usuario debe existir
    usuario = self.usuario_repo.obtener_por_id(usuario_id)
    if not usuario:
        raise UsuarioNoEncontradoError(f"Usuario {usuario_id} no existe")
    
    # Fail fast - Item debe existir
    item = self.item_repo.obtener_por_id(item_id)
    if not item:
        raise ItemNoEncontradoError(f"Item {item_id} no existe")
    
    # Fail fast - Usuario debe estar activo
    if not usuario.es_activo():
        raise UsuarioInactivoError(f"Usuario {usuario_id} está inactivo")
    
    # Fail fast - Item debe estar disponible
    if not item.esta_disponible():
        raise ItemNoDisponibleError(f"Item {item_id} no disponible")
    
    # Fail fast - Usuario no debe tener multas pendientes
    if usuario.tiene_multas_pendientes():
        raise UsuarioConMultasError(f"Usuario {usuario_id} tiene multas pendientes")
    
    # Solo después de todas las validaciones, proceder
    return self._crear_prestamo(usuario, item)
```

### Exception Handling Strategy

**Jerarquía de excepciones del dominio**:

```python
# src/shared/exceptions.py
class BibliotecaBaseException(Exception):
    """Base exception para todos los errores del dominio"""
    pass

# Excepciones de entidades
class UsuarioException(BibliotecaBaseException):
    """Base para errores relacionados con usuarios"""
    pass

class UsuarioNoEncontradoError(UsuarioException):
    """Usuario específico no encontrado"""
    pass

class UsuarioInactivoError(UsuarioException):
    """Usuario está inactivo"""
    pass

class UsuarioConMultasError(UsuarioException):
    """Usuario tiene multas pendientes"""
    pass

# Excepciones de operaciones
class PrestamoException(BibliotecaBaseException):
    """Base para errores de préstamos"""
    pass

class ItemNoDisponibleError(PrestamoException):
    """Item sin stock disponible"""
    pass

class LimitePrestamosSuperadoError(PrestamoException):
    """Usuario superó límite de préstamos"""
    pass

# Uso en servicios
class PrestamoService:
    def realizar_prestamo(self, usuario_id: int, item_id: int) -> Prestamo:
        try:
            # Lógica del préstamo
            pass
        except UsuarioException as e:
            self.logger.warning(f"Error de usuario en préstamo: {e}")
            raise  # Re-raise para que lo maneje la capa superior
        except PrestamoException as e:
            self.logger.error(f"Error en proceso de préstamo: {e}")
            raise
        except Exception as e:
            self.logger.critical(f"Error inesperado en préstamo: {e}")
            raise BibliotecaBaseException("Error interno del sistema") from e
```

### Logging Strategy

```python
# src/shared/logger.py
class BibliotecaLogger:
    def __init__(self):
        self.logger = logging.getLogger('biblioteca')
        self._configure_logger()
    
    def _configure_logger(self):
        handler = logging.FileHandler('logs/biblioteca.log')
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    def log_business_operation(self, operation: str, details: dict):
        """Audit trail para operaciones de negocio"""
        self.logger.info(f"BUSINESS_OP: {operation}", extra=details)
    
    def log_security_event(self, event: str, user_id: int, details: dict):
        """Logging de eventos de seguridad"""
        security_info = {
            'event_type': 'SECURITY',
            'user_id': user_id,
            'timestamp': datetime.now().isoformat(),
            **details
        }
        self.logger.warning(f"SECURITY: {event}", extra=security_info)

# Uso en servicios
class AuthService:
    def autenticar(self, email: str) -> Usuario:
        try:
            usuario = self.usuario_repo.obtener_por_email(email)
            if not usuario:
                self.logger.log_security_event(
                    "FAILED_LOGIN_ATTEMPT", 
                    user_id=0,
                    details={"email": email, "reason": "user_not_found"}
                )
                raise UsuarioNoEncontradoError("Credenciales inválidas")
            
            self.logger.log_business_operation(
                "USER_LOGIN",
                {"user_id": usuario.id, "email": email}
            )
            return usuario
            
        except Exception as e:
            self.logger.error(f"Error en autenticación: {e}")
            raise
```

---

**[⬅️ Volver al README principal](../README.md)**