# 🏗️ Arquitectura del Sistema - Biblioteca Liskov

## Índice

1. [Arquitectura Hexagonal](#arquitectura-hexagonal)
2. [Arquitectura C4](#arquitectura-c4)
3. [Modelo de Datos](#modelo-de-datos)
4. [Diagramas de Clases](#diagramas-de-clases)
5. [Diagramas de Secuencia](#diagramas-de-secuencia)
6. [Layered Architecture](#layered-architecture)

## Arquitectura Hexagonal

### Arquitectura Hexagonal (Ports & Adapters)

La arquitectura hexagonal permite que el dominio sea independiente de los detalles de infraestructura mediante el uso de puertos (interfaces) y adaptadores (implementaciones).

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

### Componentes Principales

- **Puertos (Interfaces)**: `src/domain/repositories.py` - Define contratos de acceso a datos
- **Adaptadores**: `src/infrastructure/repositories.py` - Implementaciones concretas
- **Núcleo**: `src/domain/entities.py` - Lógica de negocio pura

**Beneficio**: Permite intercambiar implementaciones (SQLite → PostgreSQL) sin afectar la lógica de negocio.

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

## Diagramas de Clases

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

## Layered Architecture

### Flujo de Dependencias (Dependency Rule):

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

### Beneficios de la Arquitectura

- **Presentation Independence**: Cambiar UI sin afectar lógica de negocio
- **Database Independence**: Migrar BD solo requiere nueva implementación de Repository
- **Framework Independence**: No dependencia de frameworks específicos en el core
- **Testability**: Cada capa se puede probar independientemente

---

**[⬅️ Volver al README principal](../README.md)**