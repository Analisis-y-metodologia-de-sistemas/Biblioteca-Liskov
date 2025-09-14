from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional

from .value_objects import ISBN, Email, Money


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
    password_hash: str = ""  # contraseña hasheada
    cargo: str = "Bibliotecario"
    turno: str = ""  # mañana, tarde, noche
    activo: bool = True
    fecha_registro: Optional[datetime] = None


@dataclass
class Usuario:
    """Usuarios registrados de la biblioteca (alumnos, docentes, etc.)"""

    id: Optional[int] = None
    nombre: str = ""
    apellido: str = ""
    email: Email = field(default_factory=lambda: Email(""))
    tipo: TipoUsuario = TipoUsuario.ALUMNO
    numero_identificacion: str = ""
    telefono: Optional[str] = None
    activo: bool = True
    fecha_registro: Optional[datetime] = None
    _multas_pendientes: List["Multa"] = field(default_factory=list, init=False)

    def nombre_completo(self) -> str:
        """Retorna el nombre completo del usuario"""
        return f"{self.nombre} {self.apellido}"

    def puede_hacer_prestamo(self) -> bool:
        """Verifica si el usuario puede hacer préstamos"""
        return self.activo and not self.tiene_multas_pendientes()

    def tiene_multas_pendientes(self) -> bool:
        """Verifica si el usuario tiene multas sin pagar"""
        return any(not multa.pagada for multa in self._multas_pendientes)


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
