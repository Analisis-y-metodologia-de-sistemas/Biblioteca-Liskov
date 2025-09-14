from datetime import datetime
from typing import Any, Dict, List, Optional

from ..application.interfaces import (
    IEmpleadoRepository,
    IItemBibliotecaRepository,
    IMultaRepository,
    IPrestamoRepository,
    IReservaRepository,
    IUsuarioRepository,
)
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
from .database import ORM


class UsuarioRepository(IUsuarioRepository):
    def __init__(self, orm: ORM):
        self.orm = orm
        self.table = "usuarios"

    def _row_to_entity(self, row: Dict[str, Any]) -> Usuario:
        return Usuario(
            id=row["id"],
            nombre=row["nombre"],
            apellido=row["apellido"],
            email=row["email"],
            tipo=TipoUsuario(row["tipo"]),
            numero_identificacion=row["numero_identificacion"],
            telefono=row["telefono"],
            activo=bool(row["activo"]),
            fecha_registro=datetime.fromisoformat(row["fecha_registro"]) if row["fecha_registro"] else None,
        )

    def _entity_to_dict(self, usuario: Usuario) -> Dict[str, Any]:
        data = {
            "nombre": usuario.nombre,
            "apellido": usuario.apellido,
            "email": usuario.email,
            "tipo": usuario.tipo.value,
            "numero_identificacion": usuario.numero_identificacion,
            "activo": usuario.activo,
        }
        if usuario.telefono:
            data["telefono"] = usuario.telefono
        return data

    def crear(self, usuario: Usuario) -> Usuario:
        data = self._entity_to_dict(usuario)
        usuario_id = self.orm.insert(self.table, data)
        usuario.id = usuario_id
        return usuario

    def obtener_por_id(self, id: int) -> Optional[Usuario]:
        rows = self.orm.select(self.table, "id = ?", (id,))
        return self._row_to_entity(rows[0]) if rows else None

    def obtener_por_email(self, email: str) -> Optional[Usuario]:
        rows = self.orm.select(self.table, "email = ?", (email,))
        return self._row_to_entity(rows[0]) if rows else None

    def listar_todos(self) -> List[Usuario]:
        rows = self.orm.select(self.table)
        return [self._row_to_entity(row) for row in rows]

    def actualizar(self, usuario: Usuario) -> Usuario:
        data = self._entity_to_dict(usuario)
        self.orm.update(self.table, data, "id = ?", (usuario.id,))
        return usuario

    def eliminar(self, id: int) -> bool:
        affected_rows = self.orm.delete(self.table, "id = ?", (id,))
        return affected_rows > 0


class ItemBibliotecaRepository(IItemBibliotecaRepository):
    def __init__(self, orm: ORM):
        self.orm = orm
        self.table = "items_biblioteca"

    def _row_to_entity(self, row: Dict[str, Any]) -> ItemBiblioteca:
        return ItemBiblioteca(
            id=row["id"],
            titulo=row["titulo"],
            autor=row["autor"],
            isbn=row["isbn"],
            categoria=CategoriaItem(row["categoria"]),
            estado=EstadoItem(row["estado"]),
            descripcion=row["descripcion"],
            ubicacion=row["ubicacion"],
            fecha_adquisicion=datetime.fromisoformat(row["fecha_adquisicion"]) if row["fecha_adquisicion"] else None,
            valor_reposicion=row["valor_reposicion"],
        )

    def _entity_to_dict(self, item: ItemBiblioteca) -> Dict[str, Any]:
        data = {"titulo": item.titulo, "categoria": item.categoria.value, "estado": item.estado.value}
        if item.autor:
            data["autor"] = item.autor
        if item.isbn:
            data["isbn"] = item.isbn
        if item.descripcion:
            data["descripcion"] = item.descripcion
        if item.ubicacion:
            data["ubicacion"] = item.ubicacion
        if item.valor_reposicion:
            data["valor_reposicion"] = item.valor_reposicion
        return data

    def crear(self, item: ItemBiblioteca) -> ItemBiblioteca:
        data = self._entity_to_dict(item)
        item_id = self.orm.insert(self.table, data)
        item.id = item_id
        return item

    def obtener_por_id(self, id: int) -> Optional[ItemBiblioteca]:
        rows = self.orm.select(self.table, "id = ?", (id,))
        return self._row_to_entity(rows[0]) if rows else None

    def buscar_por_titulo(self, titulo: str) -> List[ItemBiblioteca]:
        rows = self.orm.select(self.table, "titulo LIKE ?", (f"%{titulo}%",))
        return [self._row_to_entity(row) for row in rows]

    def buscar_por_autor(self, autor: str) -> List[ItemBiblioteca]:
        rows = self.orm.select(self.table, "autor LIKE ?", (f"%{autor}%",))
        return [self._row_to_entity(row) for row in rows]

    def listar_por_categoria(self, categoria: str) -> List[ItemBiblioteca]:
        rows = self.orm.select(self.table, "categoria = ?", (categoria,))
        return [self._row_to_entity(row) for row in rows]

    def buscar_por_categoria(self, categoria: CategoriaItem) -> List[ItemBiblioteca]:
        return self.listar_por_categoria(categoria.value)

    def listar_todos(self) -> List[ItemBiblioteca]:
        rows = self.orm.select(self.table)
        return [self._row_to_entity(row) for row in rows]

    def listar_disponibles(self) -> List[ItemBiblioteca]:
        rows = self.orm.select(self.table, "estado = ?", ("disponible",))
        return [self._row_to_entity(row) for row in rows]

    def actualizar(self, item: ItemBiblioteca) -> ItemBiblioteca:
        data = self._entity_to_dict(item)
        self.orm.update(self.table, data, "id = ?", (item.id,))
        return item

    def eliminar(self, id: int) -> bool:
        affected_rows = self.orm.delete(self.table, "id = ?", (id,))
        return affected_rows > 0


class PrestamoRepository(IPrestamoRepository):
    def __init__(self, orm: ORM):
        self.orm = orm
        self.table = "prestamos"

    def _row_to_entity(self, row: Dict[str, Any]) -> Prestamo:
        return Prestamo(
            id=row["id"],
            usuario_id=row["usuario_id"],
            item_id=row["item_id"],
            empleado_id=row["empleado_id"],
            fecha_prestamo=datetime.fromisoformat(row["fecha_prestamo"]) if row["fecha_prestamo"] else None,
            fecha_devolucion_esperada=(
                datetime.fromisoformat(row["fecha_devolucion_esperada"]) if row["fecha_devolucion_esperada"] else None
            ),
            fecha_devolucion_real=(
                datetime.fromisoformat(row["fecha_devolucion_real"]) if row["fecha_devolucion_real"] else None
            ),
            observaciones=row["observaciones"],
            activo=bool(row["activo"]),
        )

    def _entity_to_dict(self, prestamo: Prestamo) -> Dict[str, Any]:
        data = {
            "usuario_id": prestamo.usuario_id,
            "item_id": prestamo.item_id,
            "empleado_id": prestamo.empleado_id,
            "fecha_prestamo": prestamo.fecha_prestamo.isoformat() if prestamo.fecha_prestamo else None,
            "fecha_devolucion_esperada": (
                prestamo.fecha_devolucion_esperada.isoformat() if prestamo.fecha_devolucion_esperada else None
            ),
            "activo": prestamo.activo,
        }
        if prestamo.observaciones:
            data["observaciones"] = prestamo.observaciones
        if prestamo.fecha_devolucion_real:
            data["fecha_devolucion_real"] = prestamo.fecha_devolucion_real.isoformat()
        return data

    def crear(self, prestamo: Prestamo) -> Prestamo:
        data = self._entity_to_dict(prestamo)
        prestamo_id = self.orm.insert(self.table, data)
        prestamo.id = prestamo_id
        return prestamo

    def obtener_por_id(self, id: int) -> Optional[Prestamo]:
        rows = self.orm.select(self.table, "id = ?", (id,))
        return self._row_to_entity(rows[0]) if rows else None

    def listar_por_usuario(self, usuario_id: int) -> List[Prestamo]:
        rows = self.orm.select(self.table, "usuario_id = ?", (usuario_id,))
        return [self._row_to_entity(row) for row in rows]

    def listar_activos(self) -> List[Prestamo]:
        rows = self.orm.select(self.table, "activo = ?", (True,))
        return [self._row_to_entity(row) for row in rows]

    def listar_prestamos_activos(self) -> List[Prestamo]:
        return self.listar_activos()

    def actualizar(self, prestamo: Prestamo) -> Prestamo:
        data = self._entity_to_dict(prestamo)
        self.orm.update(self.table, data, "id = ?", (prestamo.id,))
        return prestamo


class ReservaRepository(IReservaRepository):
    def __init__(self, orm: ORM):
        self.orm = orm
        self.table = "reservas"

    def _row_to_entity(self, row: Dict[str, Any]) -> Reserva:
        return Reserva(
            id=row["id"],
            usuario_id=row["usuario_id"],
            item_id=row["item_id"],
            empleado_id=row["empleado_id"],
            fecha_reserva=datetime.fromisoformat(row["fecha_reserva"]) if row["fecha_reserva"] else None,
            fecha_expiracion=datetime.fromisoformat(row["fecha_expiracion"]) if row["fecha_expiracion"] else None,
            activa=bool(row["activa"]),
        )

    def _entity_to_dict(self, reserva: Reserva) -> Dict[str, Any]:
        return {
            "usuario_id": reserva.usuario_id,
            "item_id": reserva.item_id,
            "empleado_id": reserva.empleado_id,
            "fecha_reserva": reserva.fecha_reserva.isoformat() if reserva.fecha_reserva else None,
            "fecha_expiracion": reserva.fecha_expiracion.isoformat() if reserva.fecha_expiracion else None,
            "activa": reserva.activa,
        }

    def crear(self, reserva: Reserva) -> Reserva:
        data = self._entity_to_dict(reserva)
        reserva_id = self.orm.insert(self.table, data)
        reserva.id = reserva_id
        return reserva

    def obtener_por_id(self, id: int) -> Optional[Reserva]:
        rows = self.orm.select(self.table, "id = ?", (id,))
        return self._row_to_entity(rows[0]) if rows else None

    def listar_por_usuario(self, usuario_id: int) -> List[Reserva]:
        rows = self.orm.select(self.table, "usuario_id = ?", (usuario_id,))
        return [self._row_to_entity(row) for row in rows]

    def listar_activas(self) -> List[Reserva]:
        rows = self.orm.select(self.table, "activa = ?", (True,))
        return [self._row_to_entity(row) for row in rows]

    def listar_reservas_activas(self) -> List[Reserva]:
        return self.listar_activas()

    def listar_por_item(self, item_id: int) -> List[Reserva]:
        rows = self.orm.select(self.table, "item_id = ?", (item_id,))
        return [self._row_to_entity(row) for row in rows]

    def cancelar_reserva(self, id: int):
        self.orm.update(self.table, {"activa": False}, "id = ?", (id,))

    def actualizar(self, reserva: Reserva) -> Reserva:
        data = self._entity_to_dict(reserva)
        self.orm.update(self.table, data, "id = ?", (reserva.id,))
        return reserva


class MultaRepository(IMultaRepository):
    def __init__(self, orm: ORM):
        self.orm = orm
        self.table = "multas"

    def _row_to_entity(self, row: Dict[str, Any]) -> Multa:
        return Multa(
            id=row["id"],
            usuario_id=row["usuario_id"],
            prestamo_id=row["prestamo_id"],
            empleado_id=row["empleado_id"],
            monto=row["monto"],
            descripcion=row["descripcion"],
            fecha_multa=datetime.fromisoformat(row["fecha_multa"]) if row["fecha_multa"] else None,
            pagada=bool(row["pagada"]),
        )

    def _entity_to_dict(self, multa: Multa) -> Dict[str, Any]:
        return {
            "usuario_id": multa.usuario_id,
            "prestamo_id": multa.prestamo_id,
            "empleado_id": multa.empleado_id,
            "monto": multa.monto,
            "descripcion": multa.descripcion,
            "fecha_multa": multa.fecha_multa.isoformat() if multa.fecha_multa else None,
            "pagada": multa.pagada,
        }

    def crear(self, multa: Multa) -> Multa:
        data = self._entity_to_dict(multa)
        multa_id = self.orm.insert(self.table, data)
        multa.id = multa_id
        return multa

    def obtener_por_id(self, id: int) -> Optional[Multa]:
        rows = self.orm.select(self.table, "id = ?", (id,))
        return self._row_to_entity(rows[0]) if rows else None

    def listar_por_usuario(self, usuario_id: int) -> List[Multa]:
        rows = self.orm.select(self.table, "usuario_id = ?", (usuario_id,))
        return [self._row_to_entity(row) for row in rows]

    def listar_no_pagadas(self) -> List[Multa]:
        rows = self.orm.select(self.table, "pagada = ?", (False,))
        return [self._row_to_entity(row) for row in rows]

    def listar_multas_pendientes(self) -> List[Multa]:
        return self.listar_no_pagadas()

    def marcar_como_pagada(self, id: int, fecha_pago):
        from datetime import date

        self.orm.update(self.table, {"pagada": True, "fecha_pago": fecha_pago.isoformat()}, "id = ?", (id,))

    def actualizar(self, multa: Multa) -> Multa:
        data = self._entity_to_dict(multa)
        self.orm.update(self.table, data, "id = ?", (multa.id,))
        return multa


class EmpleadoRepository(IEmpleadoRepository):
    def __init__(self, orm: ORM):
        self.orm = orm
        self.table = "empleados"

    def _row_to_entity(self, row: Dict[str, Any]) -> Empleado:
        return Empleado(
            id=row["id"],
            nombre=row["nombre"],
            apellido=row["apellido"],
            email=row["email"],
            usuario_sistema=row["usuario_sistema"],
            password_hash=row["password_hash"],
            cargo=row["cargo"],
            turno=row["turno"],
            activo=bool(row["activo"]),
            fecha_registro=datetime.fromisoformat(row["fecha_registro"]) if row["fecha_registro"] else None,
        )

    def _entity_to_dict(self, empleado: Empleado) -> Dict[str, Any]:
        data = {
            "nombre": empleado.nombre,
            "apellido": empleado.apellido,
            "email": empleado.email,
            "usuario_sistema": empleado.usuario_sistema,
            "password_hash": empleado.password_hash,
            "cargo": empleado.cargo,
            "activo": empleado.activo,
        }
        if empleado.turno:
            data["turno"] = empleado.turno
        return data

    def crear(self, empleado: Empleado) -> Empleado:
        data = self._entity_to_dict(empleado)
        empleado_id = self.orm.insert(self.table, data)
        empleado.id = empleado_id
        return empleado

    def obtener_por_id(self, id: int) -> Optional[Empleado]:
        rows = self.orm.select(self.table, "id = ?", (id,))
        return self._row_to_entity(rows[0]) if rows else None

    def obtener_por_usuario_sistema(self, usuario: str) -> Optional[Empleado]:
        rows = self.orm.select(self.table, "usuario_sistema = ?", (usuario,))
        return self._row_to_entity(rows[0]) if rows else None

    def listar_todos(self) -> List[Empleado]:
        rows = self.orm.select(self.table)
        return [self._row_to_entity(row) for row in rows]

    def listar_activos(self) -> List[Empleado]:
        rows = self.orm.select(self.table, "activo = 1")
        return [self._row_to_entity(row) for row in rows]

    def actualizar(self, empleado: Empleado) -> Empleado:
        data = self._entity_to_dict(empleado)
        self.orm.update(self.table, data, "id = ?", (empleado.id,))
        return empleado

    def eliminar(self, id: int) -> bool:
        affected_rows = self.orm.delete(self.table, "id = ?", (id,))
        return affected_rows > 0
