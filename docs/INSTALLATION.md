# ⚙️ Guía de Instalación y Uso - Biblioteca Liskov

## Índice

1. [Prerrequisitos](#prerrequisitos)
2. [Instalación](#instalación)
3. [Configuración](#configuración)
4. [Primera Ejecución](#primera-ejecución)
5. [Guía de Usuario](#guía-de-usuario)
6. [Scripts Disponibles](#scripts-disponibles)
7. [Troubleshooting](#troubleshooting)

## Prerrequisitos

### Software Requerido

- **Python 3.11 o superior**: [Descargar Python](https://www.python.org/downloads/)
- **Git**: Para clonar el repositorio
- **Terminal/CMD**: Para ejecutar comandos

### Verificar Instalación

```bash
# Verificar Python
python --version
# o en algunos sistemas:
python3 --version

# Verificar pip
pip --version
# o:
pip3 --version

# Verificar Git
git --version
```

## Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/Analisis-y-metodologia-de-sistemas/Biblioteca-Liskov.git
cd Biblioteca-Liskov
```

### 2. Crear Entorno Virtual (Recomendado)

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate

# En macOS/Linux:
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
# Instalar dependencias del proyecto
pip install -r requirements.txt
```

### 4. Verificar Instalación

```bash
# Verificar que todo esté instalado correctamente
python -c "import src; print('✅ Instalación correcta')"
```

## Configuración

### 1. Configuración de Base de Datos

El sistema usa SQLite por defecto. La base de datos se crea automáticamente en la primera ejecución.

```bash
# (Opcional) Crear base de datos manualmente
python -c "from src.infrastructure.database import DatabaseConnection; DatabaseConnection().initialize_database()"
```

### 2. Configuración de Logging

Los logs se guardan automáticamente en la carpeta `logs/`. Para personalizar:

```python
# src/shared/config.py
LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR
LOG_FILE = 'logs/biblioteca_{date}.log'
```

### 3. Configuración de Usuarios por Defecto

```bash
# Ejecutar script para crear usuarios de ejemplo
python scripts/init_empleados.py
```

## Primera Ejecución

### 1. Ejecutar el Sistema

```bash
# Ejecutar la aplicación principal
python main.py
```

### 2. Primera Configuración

Al ejecutar por primera vez, el sistema:

1. **Crea la base de datos** automáticamente
2. **Configura las tablas** necesarias
3. **Muestra el menú principal**

### 3. Crear Primer Usuario Empleado

```
=== Sistema de Gestión de Biblioteca ===
1. Iniciar Sesión
2. Registrar Usuario
3. Salir

Seleccione una opción: 2
```

Ingrese los datos del primer empleado del sistema:
- **Nombre**: Administrador
- **Email**: admin@biblioteca.edu
- **Tipo**: Empleado

## Guía de Usuario

### Tipos de Usuario

#### 🎓 **Alumno**
- **Límite de préstamos**: 3 libros
- **Duración del préstamo**: 14 días
- **Funciones**:
  - Consultar catálogo
  - Realizar préstamos
  - Devolver libros
  - Consultar historial
  - Realizar reservas

#### 👨‍🏫 **Docente**  
- **Límite de préstamos**: 5 libros
- **Duración del préstamo**: 30 días
- **Funciones**:
  - Todas las funciones de alumno
  - Préstamos extendidos
  - Prioridad en reservas

#### 👩‍💼 **Empleado**
- **Límite de préstamos**: 10 libros
- **Duración del préstamo**: 60 días
- **Funciones administrativas**:
  - Gestionar catálogo de libros
  - Administrar usuarios
  - Procesar devoluciones
  - Gestionar multas
  - Generar reportes

### Flujo de Trabajo Típico

#### Para Alumnos/Docentes:

1. **Iniciar Sesión**
   ```
   Email: estudiante@universidad.edu
   ```

2. **Consultar Catálogo**
   ```
   === Menú Principal ===
   1. Consultar Catálogo
   ```

3. **Realizar Préstamo**
   ```
   === Menú Principal ===
   2. Realizar Préstamo
   
   Ingrese ID del libro: 1
   ✅ Préstamo realizado exitosamente
   ```

4. **Consultar Mis Préstamos**
   ```
   === Menú Principal ===
   3. Mis Préstamos
   ```

#### Para Empleados:

1. **Gestionar Catálogo**
   ```
   === Menú Empleado ===
   1. Gestionar Libros
   2. Agregar Nuevo Libro
   ```

2. **Administrar Usuarios**
   ```
   === Menú Empleado ===
   3. Gestionar Usuarios
   4. Ver Reportes
   ```

### Operaciones Principales

#### 📚 **Gestión de Préstamos**

```bash
# Proceso de préstamo
1. Usuario selecciona libro del catálogo
2. Sistema verifica disponibilidad
3. Sistema verifica límites del usuario
4. Sistema genera préstamo
5. Sistema actualiza inventario
```

#### 🔄 **Proceso de Devolución**

```bash
# Devolución normal
1. Usuario selecciona "Devolver Libro"
2. Sistema calcula fecha de devolución
3. Sistema actualiza inventario

# Devolución con retraso
1. Sistema calcula días de retraso
2. Sistema genera multa automática
3. Sistema notifica al usuario
```

#### 📅 **Sistema de Reservas**

```bash
# Cuando un libro no está disponible
1. Usuario solicita reserva
2. Sistema crea reserva en cola
3. Al devolver el libro, sistema notifica al siguiente en cola
4. Reserva se convierte automáticamente en préstamo
```

## Scripts Disponibles

### 1. Inicialización de Empleados

```bash
# Crear usuarios empleados de ejemplo
python scripts/init_empleados.py
```

### 2. Creación de Catálogo

```bash
# Poblar base de datos con libros de ejemplo
python scripts/create_catalog.py
```

### 3. Datos de Prueba

```bash
# Generar datos completos para testing
python scripts/test_data.py
```

### 4. Ejecutar Tests

```bash
# Tests unitarios
python -m pytest tests/unit/ -v

# Tests de integración  
python -m pytest tests/integration/ -v

# Todos los tests
python -m pytest tests/ -v

# Tests con coverage
python -m pytest tests/ --cov=src --cov-report=html
```

## Configuración Avanzada

### 1. Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:

```bash
# .env
DATABASE_PATH=data/biblioteca.db
LOG_LEVEL=INFO
LOG_DIR=logs
MAX_PRESTAMOS_ALUMNO=3
MAX_PRESTAMOS_DOCENTE=5
MAX_PRESTAMOS_EMPLEADO=10
DIAS_PRESTAMO_ALUMNO=14
DIAS_PRESTAMO_DOCENTE=30
DIAS_PRESTAMO_EMPLEADO=60
```

### 2. Configuración de Base de Datos

Para usar PostgreSQL en lugar de SQLite:

```python
# src/shared/config.py
DATABASE_TYPE = 'postgresql'
DATABASE_URL = 'postgresql://user:password@localhost/biblioteca'
```

### 3. Personalización de Reglas de Negocio

```python
# src/shared/config.py
BUSINESS_RULES = {
    'multa_por_dia': 10.0,  # $10 por día de retraso
    'max_multas_antes_suspension': 3,
    'dias_expiracion_reserva': 7,
    'max_renovaciones': 2
}
```

## Troubleshooting

### Errores Comunes

#### 1. Error: "Module 'src' not found"

```bash
# Solución: Agregar src al PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# O ejecutar desde la raíz del proyecto
python -m src.main
```

#### 2. Error: "Database locked"

```bash
# Solución: Cerrar todas las conexiones y reiniciar
rm data/biblioteca.db.lock
python main.py
```

#### 3. Error: "Permission denied" en logs

```bash
# Solución: Crear directorio de logs
mkdir logs
chmod 755 logs
```

#### 4. Tests fallan

```bash
# Verificar que el entorno virtual esté activo
which python

# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall

# Limpiar caché de Python
find . -type d -name __pycache__ -delete
find . -name "*.pyc" -delete
```

### Logs de Debugging

```bash
# Ver logs en tiempo real
tail -f logs/biblioteca_$(date +%Y%m%d).log

# Ver solo errores
grep ERROR logs/biblioteca_*.log

# Ver operaciones de negocio
grep BUSINESS_OP logs/biblioteca_*.log
```

### Performance

#### Optimización de Base de Datos

```sql
-- Crear índices para consultas frecuentes
CREATE INDEX idx_usuario_email ON usuarios(email);
CREATE INDEX idx_prestamo_usuario ON prestamos(usuario_id);
CREATE INDEX idx_prestamo_fecha ON prestamos(fecha_prestamo);
```

#### Monitoring

```python
# Activar profiling de performance
import cProfile
cProfile.run('main.py', 'profile_stats.prof')
```

## Desarrollo

### Estructura de Desarrollo

```bash
# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# Ejecutar linter
flake8 src/ tests/

# Ejecutar type checker
mypy src/

# Formatear código
black src/ tests/
```

### Testing

```bash
# Test con coverage detallado
python -m pytest tests/ \
    --cov=src \
    --cov-report=html \
    --cov-report=term-missing \
    --cov-fail-under=80
```

### Contribuir

1. Fork del proyecto
2. Crear rama para feature
3. Ejecutar tests antes de commit
4. Seguir convenciones de código
5. Documentar cambios

## Soporte

### Recursos Adicionales

- **[Documentación de Arquitectura](ARCHITECTURE.md)**
- **[Patrones de Diseño](DESIGN_PATTERNS.md)**
- **[Guía de Testing](TESTING.md)**

### Reportar Problemas

1. Verificar que el problema no esté ya reportado
2. Incluir logs relevantes
3. Describir pasos para reproducir
4. Especificar versión de Python y OS

---

**[⬅️ Volver al README principal](../README.md)**