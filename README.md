# Sistema de Gestión Bibliotecaria - Biblioteca Liskov

[![CI Pipeline](https://github.com/Analisis-y-metodologia-de-sistemas/Biblioteca-Liskov/actions/workflows/ci.yml/badge.svg)](https://github.com/Analisis-y-metodologia-de-sistemas/Biblioteca-Liskov/actions/workflows/ci.yml)
[![PR Checks](https://github.com/Analisis-y-metodologia-de-sistemas/Biblioteca-Liskov/actions/workflows/pr-checks.yml/badge.svg)](https://github.com/Analisis-y-metodologia-de-sistemas/Biblioteca-Liskov/actions/workflows/pr-checks.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📖 Descripción General

Sistema de gestión bibliotecaria implementado siguiendo principios de **Clean Architecture** y patrones de diseño enterprise. El sistema demuestra la aplicación práctica de los principios SOLID, patrones de diseño GoF, y arquitectura hexagonal en un dominio de negocio real.

## 🚀 Características Principales

- 🏗️ **Arquitectura Hexagonal**: Separación clara entre dominio, aplicación e infraestructura
- 👥 **Gestión de Usuarios**: Alumnos, docentes y empleados con diferentes privilegios
- 📚 **Catálogo de Libros**: Gestión completa del inventario
- 🔄 **Sistema de Préstamos**: Control de préstamos y devoluciones
- 💰 **Gestión de Multas**: Cálculo automático y seguimiento
- 📅 **Sistema de Reservas**: Reserva de libros no disponibles
- 🧪 **Testing Completo**: Tests unitarios e integración

## 📚 Documentación

### 🏗️ [Arquitectura del Sistema](docs/ARCHITECTURE.md)
Descripción detallada de la arquitectura hexagonal, diagramas C4, y estructura de capas del sistema.

### 🎯 [Patrones de Diseño](docs/DESIGN_PATTERNS.md) 
Explicación exhaustiva de todos los patrones implementados: Repository, Service Layer, Unit of Work, y principios SOLID aplicados.

### ⚙️ [Guía de Instalación y Uso](docs/INSTALLATION.md)
Instrucciones paso a paso para instalar, configurar y ejecutar el sistema.

### 🧪 [Guía de Testing](docs/TESTING.md)
Documentación sobre la estrategia de testing, cómo ejecutar tests y escribir nuevos.

### 📋 [Casos de Uso](docs/USE_CASES.md)
Especificación completa de casos de uso por tipo de usuario, con flujos detallados y reglas de negocio.

## 🏛️ Arquitectura en Resumen

```mermaid
graph TB
    subgraph "Presentation Layer"
        UI[Console UI]
    end
    
    subgraph "Application Layer"
        AS[Auth Service]
        PS[Prestamo Service]
        US[Usuario Service]
        MS[Multa Service]
    end
    
    subgraph "Domain Layer"
        E[Entities]
        R[Repository Interfaces]
    end
    
    subgraph "Infrastructure Layer"
        DB[(SQLite Database)]
        REPO[Repository Implementations]
    end
    
    UI --> AS
    UI --> PS
    UI --> US
    UI --> MS
    
    AS --> E
    PS --> E
    US --> E
    MS --> E
    
    AS --> R
    PS --> R
    US --> R
    MS --> R
    
    R --> REPO
    REPO --> DB
    
    style E fill:#4a90e2,stroke:#2171b5,stroke-width:2px,color:#fff
    style R fill:#7b68ee,stroke:#5a4fcf,stroke-width:2px,color:#fff
    style AS fill:#5cb85c,stroke:#449d44,stroke-width:2px,color:#fff
    style PS fill:#5cb85c,stroke:#449d44,stroke-width:2px,color:#fff
    style US fill:#5cb85c,stroke:#449d44,stroke-width:2px,color:#fff
    style MS fill:#5cb85c,stroke:#449d44,stroke-width:2px,color:#fff
    style UI fill:#f0ad4e,stroke:#ec971f,stroke-width:2px,color:#fff
    style DB fill:#d9534f,stroke:#c9302c,stroke-width:2px,color:#fff
    style REPO fill:#d9534f,stroke:#c9302c,stroke-width:2px,color:#fff
```

## 🚀 Inicio Rápido

### Prerrequisitos
- Python 3.11 o superior
- Git

### Instalación
```bash
# Clonar el repositorio
git clone https://github.com/Analisis-y-metodologia-de-sistemas/Biblioteca-Liskov.git
cd Biblioteca-Liskov

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el sistema
python main.py
```

## 👨‍💻 Desarrollo

### Configuración del Entorno de Desarrollo
```bash
# Instalar dependencias de desarrollo
make install-dev

# O manualmente:
pip install -r requirements-dev.txt
pre-commit install
```

### Comandos de Desarrollo
```bash
# Ejecutar tests
make test

# Linting y formateo
make lint
make format

# Verificar arquitectura limpia
make architecture

# Pipeline completo (como CI)
make ci
```

### Flujo de Trabajo
1. **Fork** del repositorio
2. **Crear rama** para feature: `git checkout -b feature/nueva-funcionalidad`
3. **Desarrollar** siguiendo Clean Architecture
4. **Ejecutar tests**: `make test`
5. **Verificar calidad**: `make lint`
6. **Crear Pull Request**

### CI/CD Pipeline
- ✅ **Linting automático** con flake8, black, isort
- ✅ **Tests automáticos** con pytest y coverage
- ✅ **Análisis de seguridad** con bandit
- ✅ **Verificación de arquitectura** limpia
- ✅ **Type checking** con mypy
- ✅ **Dependency scanning** con safety

## 📁 Estructura del Proyecto

```
Biblioteca_Liskov/
├── src/
│   ├── domain/              # 💎 Entidades y lógica de negocio
│   ├── application/         # 🧠 Servicios y casos de uso
│   ├── infrastructure/      # 🔧 Implementaciones técnicas
│   ├── presentation/        # 🎭 Interfaz de usuario
│   └── shared/              # 🔄 Componentes compartidos
├── tests/
│   ├── unit/               # Tests unitarios
│   └── integration/        # Tests de integración
├── docs/                   # 📖 Documentación detallada
├── data/                   # 🗄️ Base de datos
└── scripts/               # 🛠️ Scripts de utilidad
```

## 🛠️ Tecnologías

- **Python 3.11+**: Lenguaje principal
- **SQLite**: Base de datos  
- **Architecture**: Hexagonal (Ports & Adapters)
- **Testing**: unittest + pytest
- **Logging**: Python logging module

## 🤝 Contribuir

1. Fork del proyecto
2. Crear rama para feature (`git checkout -b feature/AmazingFeature`)
3. Commit de cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto es parte del curso de Análisis y Metodología de Sistemas.

## 🔗 Enlaces Útiles

- **[Documentación Completa](docs/)**
- **[Arquitectura Detallada](docs/ARCHITECTURE.md)**
- **[Patrones de Diseño](docs/DESIGN_PATTERNS.md)**
- **[Casos de Uso](docs/USE_CASES.md)**
- **[Tests y Calidad](docs/TESTING.md)**

---

**Desarrollado como ejemplo práctico de aplicación de principios de Clean Architecture y patrones de diseño enterprise.**