class BibliotecaException(Exception):
    pass


class UsuarioNoEncontradoException(BibliotecaException):
    def __init__(self, usuario_id: int):
        super().__init__(f"Usuario con ID {usuario_id} no encontrado")


class ItemNoEncontradoException(BibliotecaException):
    def __init__(self, item_id: int):
        super().__init__(f"Item con ID {item_id} no encontrado")


class ItemNoDisponibleException(BibliotecaException):
    def __init__(self, titulo: str):
        super().__init__(f"El item '{titulo}' no está disponible")


class PrestamoNoEncontradoException(BibliotecaException):
    def __init__(self, prestamo_id: int):
        super().__init__(f"Préstamo con ID {prestamo_id} no encontrado")


class ReservaNoEncontradaException(BibliotecaException):
    def __init__(self, reserva_id: int):
        super().__init__(f"Reserva con ID {reserva_id} no encontrada")


class MultaNoEncontradaException(BibliotecaException):
    def __init__(self, multa_id: int):
        super().__init__(f"Multa con ID {multa_id} no encontrada")


class UsuarioYaExisteException(BibliotecaException):
    def __init__(self, email: str):
        super().__init__(f"Ya existe un usuario con el email: {email}")


class LimitePrestamosExcedidoException(BibliotecaException):
    def __init__(self, limite: int):
        super().__init__(f"El usuario ha excedido el límite de préstamos simultáneos ({limite})")


class LimiteReservasExcedidoException(BibliotecaException):
    def __init__(self, limite: int):
        super().__init__(f"El usuario ha excedido el límite de reservas simultáneas ({limite})")


class MultaYaPagadaException(BibliotecaException):
    def __init__(self):
        super().__init__("Esta multa ya fue pagada")


class PrestamoYaDevueltoException(BibliotecaException):
    def __init__(self):
        super().__init__("Este préstamo ya fue devuelto")
