from abc import ABC, abstractmethod
from typing import List, Optional
from ..domain.entities import Usuario, ItemBiblioteca, Prestamo, Reserva, Multa, Empleado


class IUsuarioRepository(ABC):
    @abstractmethod
    def crear(self, usuario: Usuario) -> Usuario:
        pass

    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Usuario]:
        pass

    @abstractmethod
    def obtener_por_email(self, email: str) -> Optional[Usuario]:
        pass

    @abstractmethod
    def listar_todos(self) -> List[Usuario]:
        pass

    @abstractmethod
    def actualizar(self, usuario: Usuario) -> Usuario:
        pass

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        pass


class IItemBibliotecaRepository(ABC):
    @abstractmethod
    def crear(self, item: ItemBiblioteca) -> ItemBiblioteca:
        pass

    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[ItemBiblioteca]:
        pass

    @abstractmethod
    def buscar_por_titulo(self, titulo: str) -> List[ItemBiblioteca]:
        pass

    @abstractmethod
    def buscar_por_autor(self, autor: str) -> List[ItemBiblioteca]:
        pass

    @abstractmethod
    def listar_por_categoria(self, categoria: str) -> List[ItemBiblioteca]:
        pass

    @abstractmethod
    def listar_todos(self) -> List[ItemBiblioteca]:
        pass

    @abstractmethod
    def actualizar(self, item: ItemBiblioteca) -> ItemBiblioteca:
        pass

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        pass


class IPrestamoRepository(ABC):
    @abstractmethod
    def crear(self, prestamo: Prestamo) -> Prestamo:
        pass

    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Prestamo]:
        pass

    @abstractmethod
    def listar_por_usuario(self, usuario_id: int) -> List[Prestamo]:
        pass

    @abstractmethod
    def listar_activos(self) -> List[Prestamo]:
        pass

    @abstractmethod
    def actualizar(self, prestamo: Prestamo) -> Prestamo:
        pass


class IReservaRepository(ABC):
    @abstractmethod
    def crear(self, reserva: Reserva) -> Reserva:
        pass

    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Reserva]:
        pass

    @abstractmethod
    def listar_por_usuario(self, usuario_id: int) -> List[Reserva]:
        pass

    @abstractmethod
    def listar_activas(self) -> List[Reserva]:
        pass

    @abstractmethod
    def actualizar(self, reserva: Reserva) -> Reserva:
        pass


class IMultaRepository(ABC):
    @abstractmethod
    def crear(self, multa: Multa) -> Multa:
        pass

    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Multa]:
        pass

    @abstractmethod
    def listar_por_usuario(self, usuario_id: int) -> List[Multa]:
        pass

    @abstractmethod
    def listar_no_pagadas(self) -> List[Multa]:
        pass

    @abstractmethod
    def actualizar(self, multa: Multa) -> Multa:
        pass


class IEmpleadoRepository(ABC):
    @abstractmethod
    def crear(self, empleado: Empleado) -> Empleado:
        pass

    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Empleado]:
        pass

    @abstractmethod
    def obtener_por_usuario_sistema(self, usuario: str) -> Optional[Empleado]:
        pass

    @abstractmethod
    def listar_todos(self) -> List[Empleado]:
        pass
    
    @abstractmethod
    def listar_activos(self) -> List[Empleado]:
        pass

    @abstractmethod
    def actualizar(self, empleado: Empleado) -> Empleado:
        pass

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        pass