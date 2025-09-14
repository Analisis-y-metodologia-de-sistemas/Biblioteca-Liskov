"""
Repository interfaces defining contracts for data access
Following the Dependency Inversion Principle - high-level modules depend on abstractions
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from ..domain.entities import (
    CategoriaItem,
    Empleado,
    EstadoItem,
    ItemBiblioteca,
    Multa,
    Prestamo,
    Reserva,
    TipoUsuario,
    Usuario,
)


class IUsuarioRepository(ABC):
    """Interface for Usuario data access operations"""

    @abstractmethod
    def crear(self, usuario: Usuario) -> Usuario:
        """Create a new user"""
        pass

    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Usuario]:
        """Get user by ID"""
        pass

    @abstractmethod
    def obtener_por_email(self, email: str) -> Optional[Usuario]:
        """Get user by email address"""
        pass

    @abstractmethod
    def listar_todos(self) -> List[Usuario]:
        """Get all users"""
        pass

    @abstractmethod
    def listar_por_tipo(self, tipo: TipoUsuario) -> List[Usuario]:
        """Get users by type (ALUMNO, DOCENTE, etc.)"""
        pass

    @abstractmethod
    def actualizar(self, usuario: Usuario) -> Usuario:
        """Update existing user"""
        pass

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        """Delete user by ID"""
        pass

    @abstractmethod
    def buscar_por_nombre(self, nombre: str) -> List[Usuario]:
        """Search users by name (partial match)"""
        pass


class IItemBibliotecaRepository(ABC):
    """Interface for ItemBiblioteca data access operations"""

    @abstractmethod
    def crear(self, item: ItemBiblioteca) -> ItemBiblioteca:
        """Create a new library item"""
        pass

    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[ItemBiblioteca]:
        """Get item by ID"""
        pass

    @abstractmethod
    def listar_todos(self) -> List[ItemBiblioteca]:
        """Get all library items"""
        pass

    @abstractmethod
    def buscar_por_titulo(self, titulo: str) -> List[ItemBiblioteca]:
        """Search items by title (partial match)"""
        pass

    @abstractmethod
    def buscar_por_autor(self, autor: str) -> List[ItemBiblioteca]:
        """Search items by author (partial match)"""
        pass

    @abstractmethod
    def buscar_por_isbn(self, isbn: str) -> Optional[ItemBiblioteca]:
        """Get item by ISBN"""
        pass

    @abstractmethod
    def listar_por_categoria(self, categoria: CategoriaItem) -> List[ItemBiblioteca]:
        """Get items by category"""
        pass

    @abstractmethod
    def listar_por_estado(self, estado: EstadoItem) -> List[ItemBiblioteca]:
        """Get items by status"""
        pass

    @abstractmethod
    def actualizar(self, item: ItemBiblioteca) -> ItemBiblioteca:
        """Update existing item"""
        pass

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        """Delete item by ID"""
        pass


class IPrestamoRepository(ABC):
    """Interface for Prestamo data access operations"""

    @abstractmethod
    def crear(self, prestamo: Prestamo) -> Prestamo:
        """Create a new loan"""
        pass

    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Prestamo]:
        """Get loan by ID"""
        pass

    @abstractmethod
    def listar_todos(self) -> List[Prestamo]:
        """Get all loans"""
        pass

    @abstractmethod
    def listar_activos(self) -> List[Prestamo]:
        """Get all active (not returned) loans"""
        pass

    @abstractmethod
    def listar_por_usuario(self, usuario_id: int) -> List[Prestamo]:
        """Get all loans for a specific user"""
        pass

    @abstractmethod
    def listar_por_item(self, item_id: int) -> List[Prestamo]:
        """Get loan history for a specific item"""
        pass

    @abstractmethod
    def listar_vencidos(self) -> List[Prestamo]:
        """Get all overdue loans"""
        pass

    @abstractmethod
    def actualizar(self, prestamo: Prestamo) -> Prestamo:
        """Update existing loan"""
        pass

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        """Delete loan by ID"""
        pass


class IReservaRepository(ABC):
    """Interface for Reserva data access operations"""

    @abstractmethod
    def crear(self, reserva: Reserva) -> Reserva:
        """Create a new reservation"""
        pass

    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Reserva]:
        """Get reservation by ID"""
        pass

    @abstractmethod
    def listar_todas(self) -> List[Reserva]:
        """Get all reservations"""
        pass

    @abstractmethod
    def listar_activas(self) -> List[Reserva]:
        """Get all active reservations"""
        pass

    @abstractmethod
    def listar_por_usuario(self, usuario_id: int) -> List[Reserva]:
        """Get reservations for a specific user"""
        pass

    @abstractmethod
    def listar_por_item(self, item_id: int) -> List[Reserva]:
        """Get reservations for a specific item"""
        pass

    @abstractmethod
    def listar_expiradas(self) -> List[Reserva]:
        """Get all expired reservations"""
        pass

    @abstractmethod
    def actualizar(self, reserva: Reserva) -> Reserva:
        """Update existing reservation"""
        pass

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        """Delete reservation by ID"""
        pass


class IMultaRepository(ABC):
    """Interface for Multa data access operations"""

    @abstractmethod
    def crear(self, multa: Multa) -> Multa:
        """Create a new fine"""
        pass

    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Multa]:
        """Get fine by ID"""
        pass

    @abstractmethod
    def listar_todas(self) -> List[Multa]:
        """Get all fines"""
        pass

    @abstractmethod
    def listar_por_usuario(self, usuario_id: int) -> List[Multa]:
        """Get fines for a specific user"""
        pass

    @abstractmethod
    def listar_no_pagadas(self) -> List[Multa]:
        """Get all unpaid fines"""
        pass

    @abstractmethod
    def listar_pagadas(self) -> List[Multa]:
        """Get all paid fines"""
        pass

    @abstractmethod
    def actualizar(self, multa: Multa) -> Multa:
        """Update existing fine"""
        pass

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        """Delete fine by ID"""
        pass


class IEmpleadoRepository(ABC):
    """Interface for Empleado data access operations"""

    @abstractmethod
    def crear(self, empleado: Empleado) -> Empleado:
        """Create a new employee"""
        pass

    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Empleado]:
        """Get employee by ID"""
        pass

    @abstractmethod
    def obtener_por_usuario(self, usuario_sistema: str) -> Optional[Empleado]:
        """Get employee by system username"""
        pass

    @abstractmethod
    def listar_todos(self) -> List[Empleado]:
        """Get all employees"""
        pass

    @abstractmethod
    def listar_activos(self) -> List[Empleado]:
        """Get all active employees"""
        pass

    @abstractmethod
    def actualizar(self, empleado: Empleado) -> Empleado:
        """Update existing employee"""
        pass

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        """Delete employee by ID"""
        pass
