# Casos de Uso - Sistema Biblioteca Liskov

## Descripción General

Este documento describe todos los casos de uso del Sistema de Gestión de Biblioteca Liskov, organizados por paquetes funcionales y actores del sistema.

## 👥 Actores del Sistema

### **Bibliotecario**
- **Descripción**: Personal administrativo con acceso completo al sistema
- **Responsabilidades**: Gestión completa de usuarios, items, préstamos, reservas y multas
- **Permisos**: Acceso total a todas las funcionalidades

### **Usuario Docente** 
- **Descripción**: Profesores e instructores de la institución
- **Responsabilidades**: Consultar catálogo, gestionar sus propios préstamos y reservas
- **Permisos**: Consulta de catálogo, gestión de préstamos propios, períodos de préstamo extendidos

### **Usuario Alumno**
- **Descripción**: Estudiantes de la institución
- **Responsabilidades**: Consultar catálogo, gestionar sus propios préstamos y reservas
- **Permisos**: Consulta de catálogo, gestión de préstamos propios, períodos de préstamo estándar

### **Sistema**
- **Descripción**: Procesos automáticos del sistema
- **Responsabilidades**: Verificaciones automáticas, notificaciones, generación de multas
- **Permisos**: Ejecución de procesos programados

## 📦 Paquetes de Casos de Uso

### 🔹 **Gestión de Usuarios**

#### UC01 - Registrar Usuario
**Actor Principal**: Bibliotecario
**Descripción**: Crear un nuevo usuario en el sistema
**Precondiciones**: Bibliotecario autenticado
**Postcondiciones**: Usuario creado y disponible en el sistema

**Flujo Principal**:
1. Bibliotecario selecciona "Registrar nuevo usuario"
2. Sistema muestra formulario de registro
3. Bibliotecario ingresa datos del usuario
4. Sistema presenta menú desplegable para tipo de usuario
5. Bibliotecario selecciona tipo (Alumno/Docente/Bibliotecario)
6. Sistema valida datos y email único
7. Sistema crea usuario y asigna ID
8. Sistema confirma registro exitoso

**Flujos Alternativos**:
- 6a. Email ya existe: Sistema muestra error y solicita email diferente
- 6b. Datos inválidos: Sistema muestra errores de validación

#### UC02 - Buscar Usuario
**Actor Principal**: Bibliotecario, Alumno, Docente
**Descripción**: Localizar usuario por email
**Precondiciones**: Al menos un usuario registrado

**Flujo Principal**:
1. Actor selecciona "Buscar usuario por email"
2. Sistema solicita email
3. Actor ingresa email
4. Sistema busca y muestra información del usuario

#### UC03 - Listar Usuarios
**Actor Principal**: Bibliotecario
**Descripción**: Visualizar todos los usuarios registrados con menú navegable
**Postcondiciones**: Lista de usuarios mostrada con opción de selección

**Flujo Principal**:
1. Bibliotecario selecciona "Listar todos los usuarios"
2. Sistema recupera lista de usuarios
3. Sistema muestra menú desplegable navegable
4. Bibliotecario navega con ↑↓ y selecciona con ENTER
5. Sistema muestra detalles del usuario seleccionado

### 📚 **Gestión de Items**

#### UC05 - Agregar Item
**Actor Principal**: Bibliotecario
**Descripción**: Añadir nuevo material al catálogo de la biblioteca

**Flujo Principal**:
1. Bibliotecario selecciona "Agregar nuevo item"
2. Sistema solicita datos básicos (título, autor, ISBN, etc.)
3. Sistema presenta menú desplegable de categorías
4. Bibliotecario selecciona categoría con navegación interactiva
5. Sistema valida datos y crea item
6. Sistema confirma creación exitosa

#### UC06 - Buscar Item por Título
**Actor Principal**: Bibliotecario, Alumno, Docente
**Descripción**: Localizar items por título con resultados navegables

**Flujo Principal**:
1. Actor ingresa término de búsqueda
2. Sistema busca items que coincidan
3. Sistema muestra menú desplegable con resultados
4. Actor navega y selecciona item de interés
5. Sistema muestra detalles completos del item

#### UC08 - Listar Items Disponibles
**Actor Principal**: Bibliotecario, Alumno, Docente
**Descripción**: Mostrar catálogo de items disponibles para préstamo

**Flujo Principal**:
1. Actor selecciona "Listar items disponibles"
2. Sistema filtra items con estado "disponible"
3. Sistema presenta menú desplegable navegable
4. Actor puede explorar catálogo completo

### 🔄 **Gestión de Préstamos**

#### UC11 - Realizar Préstamo
**Actor Principal**: Bibliotecario
**Descripción**: Procesar préstamo de item a usuario
**Precondiciones**: Usuario registrado, item disponible

**Flujo Principal**:
1. Bibliotecario selecciona "Realizar préstamo"
2. Sistema muestra menú desplegable de usuarios
3. Bibliotecario selecciona usuario con navegación
4. Bibliotecario busca item por título
5. Sistema muestra items encontrados en menú navegable
6. Bibliotecario selecciona item específico
7. Sistema solicita días de préstamo (15 por defecto)
8. Sistema presenta confirmación interactiva
9. Bibliotecario confirma con diálogo Sí/No
10. Sistema procesa préstamo y actualiza estados
11. Sistema muestra confirmación con detalles

**Flujos Alternativos**:
- 6a. Item no disponible: Sistema muestra error y sugiere reserva
- 9a. Confirmación negativa: Sistema cancela operación

#### UC12 - Devolver Item
**Actor Principal**: Bibliotecario
**Descripción**: Procesar devolución de item prestado

**Flujo Principal**:
1. Bibliotecario identifica préstamo activo
2. Sistema procesa devolución
3. Sistema actualiza estado del item a "disponible"
4. Sistema verifica fechas para multas automáticas
5. Sistema confirma devolución

**Extensiones**:
- 4a. Devolución tardía: Sistema ejecuta UC20 (Generar Multa Automática)

### 📋 **Gestión de Reservas**

#### UC16 - Realizar Reserva
**Actor Principal**: Bibliotecario, Alumno, Docente
**Descripción**: Reservar item no disponible para uso futuro

**Flujo Principal**:
1. Actor busca item deseado
2. Sistema verifica que item no está disponible
3. Actor solicita reserva
4. Sistema crea reserva con fecha de expiración
5. Sistema confirma reserva exitosa

#### UC19 - Notificar Disponibilidad
**Actor Principal**: Sistema
**Descripción**: Proceso automático de notificación cuando item reservado queda disponible

### 💰 **Gestión de Multas**

#### UC20 - Generar Multa Automática
**Actor Principal**: Sistema
**Descripción**: Proceso automático que genera multas por devoluciones tardías

**Flujo Principal**:
1. Sistema detecta devolución tardía en UC12
2. Sistema calcula días de atraso
3. Sistema calcula monto ($50 por día)
4. Sistema crea registro de multa
5. Sistema asocia multa con préstamo y usuario

#### UC21 - Pagar Multa
**Actor Principal**: Bibliotecario
**Descripción**: Registrar pago de multa pendiente

### 🎮 **Sistema de Menús Interactivos**

#### UC28 - Navegar Menús Desplegables
**Actor Principal**: Todos los usuarios
**Descripción**: Interactuar con menús desplegables navegables

**Flujo Principal**:
1. Sistema presenta menú desplegable
2. Usuario navega con teclas ↑ y ↓
3. Sistema resalta opción actual
4. Usuario presiona ENTER para seleccionar
5. Sistema ejecuta acción seleccionada

**Flujos Alternativos**:
- 3a. Usuario presiona número (1-9): Sistema selecciona directamente
- 4a. Usuario presiona ESC/Q: Sistema cancela y retorna

#### UC29 - Seleccionar con Teclas
**Actor Principal**: Todos los usuarios
**Descripción**: Navegación mediante teclado en interfaces

#### UC30 - Confirmar Acciones
**Actor Principal**: Todos los usuarios
**Descripción**: Sistema de confirmación interactivo para acciones importantes

**Flujo Principal**:
1. Sistema presenta diálogo de confirmación
2. Sistema muestra opciones "Sí/No" con default
3. Usuario ingresa respuesta (s/n/enter)
4. Sistema procesa respuesta y continúa flujo

## 🔗 Relaciones Entre Casos de Uso

### **Relaciones de Inclusión** (<<include>>)
- **UC11 (Realizar Préstamo) include UC15 (Verificar Disponibilidad)**: Todo préstamo debe verificar disponibilidad
- **UC16 (Realizar Reserva) include UC15 (Verificar Disponibilidad)**: Las reservas verifican que el item no esté disponible
- **UC04 (Actualizar Perfil) include UC02 (Buscar Usuario)**: Actualizar requiere primero localizar al usuario

### **Relaciones de Extensión** (<<extend>>)
- **UC12 (Devolver Item) extend UC20 (Generar Multa Automática)**: Solo si hay retraso en devolución
- **UC19 (Notificar Disponibilidad) extend UC12 (Devolver Item)**: Solo si hay reservas pendientes

## 🎯 Casos de Uso por Actor

### **Bibliotecario** (Acceso Completo)
- ✅ Todos los casos de uso de gestión (UC01-UC27)
- ✅ Generación de reportes y estadísticas
- ✅ Administración completa del sistema
- ✅ Navegación con menús interactivos (UC28-UC31)

### **Docente** (Acceso Limitado - Consulta y Gestión Personal)
- ✅ Consultar catálogo (UC06, UC07, UC08, UC10)
- ✅ Ver historial personal (UC14, UC23)  
- ✅ Gestionar reservas propias (UC16, UC17)
- ✅ Navegación con menús interactivos (UC28-UC31)
- ⏱️ Períodos de préstamo extendidos (30 días vs 15 días)

### **Alumno** (Acceso Limitado - Consulta y Gestión Personal)
- ✅ Consultar catálogo (UC06, UC07, UC08, UC10)
- ✅ Ver historial personal (UC14, UC23)
- ✅ Gestionar reservas propias (UC16, UC17)  
- ✅ Navegación con menús interactivos (UC28-UC31)
- ⏱️ Períodos de préstamo estándar (15 días)

### **Sistema** (Procesos Automáticos)
- 🤖 Verificación automática de disponibilidad (UC15)
- 🤖 Notificaciones de disponibilidad (UC19)
- 🤖 Generación automática de multas (UC20)

## 📋 Matriz de Trazabilidad

| Funcionalidad | Bibliotecario | Docente | Alumno | Sistema |
|---------------|---------------|---------|---------|---------|
| Gestión Usuarios | ✅ | ❌ | ❌ | ❌ |
| Gestión Items | ✅ | 👁️ | 👁️ | ❌ |  
| Gestión Préstamos | ✅ | 👤 | 👤 | ✅ |
| Gestión Reservas | ✅ | 👤 | 👤 | ✅ |
| Gestión Multas | ✅ | 👁️ | 👁️ | ✅ |
| Reportes | ✅ | ❌ | ❌ | ❌ |
| Menús Interactivos | ✅ | ✅ | ✅ | ❌ |

**Leyenda**:
- ✅ Acceso completo
- 👁️ Solo consulta/lectura  
- 👤 Solo datos propios
- ❌ Sin acceso

## 🚀 Innovaciones en UX

### **Menús Desplegables Navegables**
- Navegación con teclas de flecha
- Selección directa por número
- Cancelación intuitiva (ESC/Q)
- Información contextual en tiempo real

### **Confirmaciones Inteligentes**
- Diálogos interactivos para acciones críticas
- Valores por defecto sensatos
- Respuestas flexibles (s/sí/y/yes)

### **Mensajes Contextuales**
- Feedback visual inmediato
- Colores diferenciados por tipo (éxito/error/advertencia)
- Información de estado en tiempo real

## 📊 Métricas y KPIs

### **Indicadores de Uso**
- Número de préstamos por usuario/mes
- Items más solicitados
- Tiempo promedio de préstamo
- Tasa de devoluciones tardías

### **Indicadores de Eficiencia**
- Tiempo promedio de procesamiento de préstamos
- Uso de menús interactivos vs entrada manual
- Tasa de errores de usuario
- Satisfacción con la interfaz

## 🔮 Casos de Uso Futuros

### **Extensiones Planeadas**
- **Notificaciones por Email**: Ampliar UC19 con notificaciones electrónicas
- **Renovación de Préstamos**: Extender períodos antes de vencimiento
- **Multas con Cálculo Dinámico**: Diferentes tarifas según tipo de usuario/item
- **Reservas con Prioridad**: Sistema de colas por tipo de usuario
- **Reportes Avanzados**: Dashboard con métricas en tiempo real
- **Integración Web**: API REST para interfaz web manteniendo misma lógica