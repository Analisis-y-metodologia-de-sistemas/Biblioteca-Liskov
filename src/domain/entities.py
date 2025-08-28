from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime
from enum import Enum


class TipoUsuario(Enum):
    ALUMNO = "alumno"
    DOCENTE = "docente"
    BIBLIOTECARIO = "bibliotecario"


class EstadoItem(Enum):
    DISPONIBLE = "disponible"
    PRESTADO = "prestado"
    EN_REPARACION = "en_reparacion"
    PERDIDO = "perdido"


class CategoriaItem(Enum):
    LIBRO = "libro"
    REVISTA = "revista"
    DVD = "dvd"
    CD = "cd"
    AUDIOBOOK = "audiobook"
    OTRO = "otro"


@dataclass
class Empleado:
    """Empleados que operan el sistema (bibliotecarios/administradores)"""
    id: Optional[int] = None
    nombre: str = ""
    apellido: str = ""
    email: str = ""
    usuario_sistema: str = ""  # nombre de usuario para login
    password_hash: str = ""    # contraseña hasheada
    cargo: str = "Bibliotecario"
    turno: str = ""           # mañana, tarde, noche
    activo: bool = True
    fecha_registro: Optional[datetime] = None


@dataclass
class Usuario:
    """Usuarios registrados de la biblioteca (alumnos, docentes, etc.)"""
    id: Optional[int] = None
    nombre: str = ""
    apellido: str = ""
    email: str = ""
    tipo: TipoUsuario = TipoUsuario.ALUMNO
    numero_identificacion: str = ""
    telefono: Optional[str] = None
    activo: bool = True
    fecha_registro: Optional[datetime] = None


@dataclass
class ItemBiblioteca:
    id: Optional[int] = None
    titulo: str = ""
    autor: Optional[str] = None
    isbn: Optional[str] = None
    categoria: CategoriaItem = CategoriaItem.LIBRO
    estado: EstadoItem = EstadoItem.DISPONIBLE
    descripcion: Optional[str] = None
    ubicacion: Optional[str] = None
    fecha_adquisicion: Optional[datetime] = None
    valor_reposicion: Optional[float] = None


@dataclass
class Prestamo:
    id: Optional[int] = None
    usuario_id: int = 0
    item_id: int = 0
    empleado_id: int = 0  # Quién procesó el préstamo
    fecha_prestamo: Optional[datetime] = None
    fecha_devolucion_esperada: Optional[datetime] = None
    fecha_devolucion_real: Optional[datetime] = None
    observaciones: Optional[str] = None
    activo: bool = True


@dataclass
class Reserva:
    id: Optional[int] = None
    usuario_id: int = 0
    item_id: int = 0
    empleado_id: int = 0  # Quién procesó la reserva
    fecha_reserva: Optional[datetime] = None
    fecha_expiracion: Optional[datetime] = None
    activa: bool = True


@dataclass
class Multa:
    id: Optional[int] = None
    usuario_id: int = 0
    prestamo_id: int = 0
    empleado_id: int = 0  # Quién registró la multa
    monto: float = 0.0
    descripcion: str = ""
    fecha_multa: Optional[datetime] = None
    pagada: bool = False


@dataclass
class SesionEmpleado:
    """Sesión actual del empleado logueado"""
    empleado: Empleado
    fecha_login: datetime
    activa: bool = True