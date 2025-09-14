from datetime import datetime, timedelta
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
from .interfaces import (
    IEmpleadoRepository,
    IItemBibliotecaRepository,
    IMultaRepository,
    IPrestamoRepository,
    IReservaRepository,
    IUsuarioRepository,
)


class UsuarioService:
    def __init__(self, usuario_repo: IUsuarioRepository):
        self.usuario_repo = usuario_repo

    def registrar_usuario(
        self,
        nombre: str,
        apellido: str,
        email: str,
        tipo: TipoUsuario,
        numero_identificacion: str,
        telefono: Optional[str] = None,
    ) -> Usuario:
        if self.usuario_repo.obtener_por_email(email):
            raise ValueError(f"Ya existe un usuario con el email: {email}")

        usuario = Usuario(
            nombre=nombre,
            apellido=apellido,
            email=email,
            tipo=tipo,
            numero_identificacion=numero_identificacion,
            telefono=telefono,
            fecha_registro=datetime.now(),
        )

        return self.usuario_repo.crear(usuario)

    def buscar_usuario_por_email(self, email: str) -> Optional[Usuario]:
        return self.usuario_repo.obtener_por_email(email)

    def listar_usuarios(self) -> List[Usuario]:
        return self.usuario_repo.listar_todos()

    def actualizar_usuario(self, usuario: Usuario) -> Usuario:
        return self.usuario_repo.actualizar(usuario)


class ItemBibliotecaService:
    def __init__(self, item_repo: IItemBibliotecaRepository):
        self.item_repo = item_repo

    def agregar_item(
        self,
        titulo: str,
        categoria: str,
        autor: Optional[str] = None,
        isbn: Optional[str] = None,
        descripcion: Optional[str] = None,
        ubicacion: Optional[str] = None,
        valor_reposicion: Optional[float] = None,
    ) -> ItemBiblioteca:
        from ..domain.entities import CategoriaItem

        categoria_enum = CategoriaItem(categoria)

        item = ItemBiblioteca(
            titulo=titulo,
            autor=autor,
            isbn=isbn,
            categoria=categoria_enum,
            estado=EstadoItem.DISPONIBLE,
            descripcion=descripcion,
            ubicacion=ubicacion,
            fecha_adquisicion=datetime.now(),
            valor_reposicion=valor_reposicion,
        )

        return self.item_repo.crear(item)

    def buscar_por_titulo(self, titulo: str) -> List[ItemBiblioteca]:
        return self.item_repo.buscar_por_titulo(titulo)

    def buscar_por_autor(self, autor: str) -> List[ItemBiblioteca]:
        return self.item_repo.buscar_por_autor(autor)

    def listar_por_categoria(self, categoria: str) -> List[ItemBiblioteca]:
        categoria_enum = CategoriaItem(categoria) if isinstance(categoria, str) else categoria
        return self.item_repo.listar_por_categoria(categoria_enum)

    def listar_disponibles(self) -> List[ItemBiblioteca]:
        items = self.item_repo.listar_todos()
        return [item for item in items if item.estado == EstadoItem.DISPONIBLE]

    def cambiar_estado_item(self, item_id: int, nuevo_estado: EstadoItem) -> ItemBiblioteca:
        item = self.item_repo.obtener_por_id(item_id)
        if not item:
            raise ValueError(f"No se encontró el item con ID: {item_id}")

        item.estado = nuevo_estado
        return self.item_repo.actualizar(item)


class PrestamoService:
    def __init__(
        self,
        prestamo_repo: IPrestamoRepository,
        item_repo: IItemBibliotecaRepository,
        usuario_repo: IUsuarioRepository,
        multa_repo: IMultaRepository,
    ):
        self.prestamo_repo = prestamo_repo
        self.item_repo = item_repo
        self.usuario_repo = usuario_repo
        self.multa_repo = multa_repo

    def realizar_prestamo(self, usuario_id: int, item_id: int, empleado_id: int, dias_prestamo: int = 15) -> Prestamo:
        usuario = self.usuario_repo.obtener_por_id(usuario_id)
        if not usuario:
            raise ValueError(f"No se encontró el usuario con ID: {usuario_id}")

        item = self.item_repo.obtener_por_id(item_id)
        if not item:
            raise ValueError(f"No se encontró el item con ID: {item_id}")

        if item.estado != EstadoItem.DISPONIBLE:
            raise ValueError(f"El item '{item.titulo}' no está disponible")

        fecha_devolucion = datetime.now() + timedelta(days=dias_prestamo)

        prestamo = Prestamo(
            usuario_id=usuario_id,
            item_id=item_id,
            empleado_id=empleado_id,
            fecha_prestamo=datetime.now(),
            fecha_devolucion_esperada=fecha_devolucion,
        )

        prestamo = self.prestamo_repo.crear(prestamo)

        item.estado = EstadoItem.PRESTADO
        self.item_repo.actualizar(item)

        return prestamo

    def devolver_item(self, prestamo_id: int, observaciones: Optional[str] = None) -> Prestamo:
        prestamo = self.prestamo_repo.obtener_por_id(prestamo_id)
        if not prestamo:
            raise ValueError(f"No se encontró el préstamo con ID: {prestamo_id}")

        if not prestamo.activo:
            raise ValueError("Este préstamo ya fue devuelto")

        prestamo.fecha_devolucion_real = datetime.now()
        prestamo.observaciones = observaciones
        prestamo.activo = False

        item = self.item_repo.obtener_por_id(prestamo.item_id)
        if item:
            item.estado = EstadoItem.DISPONIBLE
            self.item_repo.actualizar(item)

        if prestamo.fecha_devolucion_real > prestamo.fecha_devolucion_esperada:
            dias_atraso = (prestamo.fecha_devolucion_real - prestamo.fecha_devolucion_esperada).days
            monto_multa = dias_atraso * 50.0  # $50 por día de atraso

            multa = Multa(
                usuario_id=prestamo.usuario_id,
                prestamo_id=prestamo.id,
                empleado_id=prestamo.empleado_id,  # El mismo empleado que procesó el préstamo
                monto=monto_multa,
                descripcion=f"Devolución tardía: {dias_atraso} días de atraso",
                fecha_multa=datetime.now(),
            )
            self.multa_repo.crear(multa)

        return self.prestamo_repo.actualizar(prestamo)

    def listar_prestamos_activos(self) -> List[Prestamo]:
        return self.prestamo_repo.listar_activos()

    def listar_prestamos_usuario(self, usuario_id: int) -> List[Prestamo]:
        return self.prestamo_repo.listar_por_usuario(usuario_id)


class ReservaService:
    def __init__(
        self, reserva_repo: IReservaRepository, item_repo: IItemBibliotecaRepository, usuario_repo: IUsuarioRepository
    ):
        self.reserva_repo = reserva_repo
        self.item_repo = item_repo
        self.usuario_repo = usuario_repo

    def realizar_reserva(self, usuario_id: int, item_id: int, empleado_id: int, dias_expiracion: int = 3) -> Reserva:
        usuario = self.usuario_repo.obtener_por_id(usuario_id)
        if not usuario:
            raise ValueError(f"No se encontró el usuario con ID: {usuario_id}")

        item = self.item_repo.obtener_por_id(item_id)
        if not item:
            raise ValueError(f"No se encontró el item con ID: {item_id}")

        if item.estado == EstadoItem.DISPONIBLE:
            raise ValueError(f"El item '{item.titulo}' está disponible, no necesita reserva")

        fecha_expiracion = datetime.now() + timedelta(days=dias_expiracion)

        reserva = Reserva(
            usuario_id=usuario_id,
            item_id=item_id,
            empleado_id=empleado_id,
            fecha_reserva=datetime.now(),
            fecha_expiracion=fecha_expiracion,
        )

        return self.reserva_repo.crear(reserva)

    def cancelar_reserva(self, reserva_id: int) -> Reserva:
        reserva = self.reserva_repo.obtener_por_id(reserva_id)
        if not reserva:
            raise ValueError(f"No se encontró la reserva con ID: {reserva_id}")

        reserva.activa = False
        return self.reserva_repo.actualizar(reserva)

    def listar_reservas_activas(self) -> List[Reserva]:
        return self.reserva_repo.listar_activas()


class MultaService:
    def __init__(self, multa_repo: IMultaRepository, usuario_repo: IUsuarioRepository):
        self.multa_repo = multa_repo
        self.usuario_repo = usuario_repo

    def pagar_multa(self, multa_id: int) -> Multa:
        multa = self.multa_repo.obtener_por_id(multa_id)
        if not multa:
            raise ValueError(f"No se encontró la multa con ID: {multa_id}")

        if multa.pagada:
            raise ValueError("Esta multa ya fue pagada")

        multa.pagada = True
        return self.multa_repo.actualizar(multa)

    def listar_multas_pendientes(self) -> List[Multa]:
        return self.multa_repo.listar_no_pagadas()

    def listar_multas_usuario(self, usuario_id: int) -> List[Multa]:
        return self.multa_repo.listar_por_usuario(usuario_id)
