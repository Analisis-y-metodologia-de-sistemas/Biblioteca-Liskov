from .infrastructure.database import DatabaseConnection, ORM
from .infrastructure.repositories import (
    UsuarioRepository, ItemBibliotecaRepository, PrestamoRepository,
    ReservaRepository, MultaRepository, EmpleadoRepository
)
from .application.services import (
    UsuarioService, ItemBibliotecaService, PrestamoService,
    ReservaService, MultaService
)
from .application.auth_service import AuthService
from .presentation.console_ui import ConsoleUI
from .shared.config import get_config


class Container:
    def __init__(self):
        self._config = get_config()
        self._db_connection = None
        self._orm = None
        self._repositories = {}
        self._services = {}
        self._console_ui = None
    
    def get_db_connection(self) -> DatabaseConnection:
        if not self._db_connection:
            self._db_connection = DatabaseConnection(self._config.database.path)
        return self._db_connection
    
    def get_orm(self) -> ORM:
        if not self._orm:
            self._orm = ORM(self.get_db_connection())
            self._orm.create_tables()
        return self._orm
    
    def get_usuario_repository(self) -> UsuarioRepository:
        if 'usuario' not in self._repositories:
            self._repositories['usuario'] = UsuarioRepository(self.get_orm())
        return self._repositories['usuario']
    
    def get_item_repository(self) -> ItemBibliotecaRepository:
        if 'item' not in self._repositories:
            self._repositories['item'] = ItemBibliotecaRepository(self.get_orm())
        return self._repositories['item']
    
    def get_prestamo_repository(self) -> PrestamoRepository:
        if 'prestamo' not in self._repositories:
            self._repositories['prestamo'] = PrestamoRepository(self.get_orm())
        return self._repositories['prestamo']
    
    def get_reserva_repository(self) -> ReservaRepository:
        if 'reserva' not in self._repositories:
            self._repositories['reserva'] = ReservaRepository(self.get_orm())
        return self._repositories['reserva']
    
    def get_multa_repository(self) -> MultaRepository:
        if 'multa' not in self._repositories:
            self._repositories['multa'] = MultaRepository(self.get_orm())
        return self._repositories['multa']
    
    def get_empleado_repository(self) -> EmpleadoRepository:
        if 'empleado' not in self._repositories:
            self._repositories['empleado'] = EmpleadoRepository(self.get_orm())
        return self._repositories['empleado']
    
    def get_usuario_service(self) -> UsuarioService:
        if 'usuario' not in self._services:
            self._services['usuario'] = UsuarioService(self.get_usuario_repository())
        return self._services['usuario']
    
    def get_item_service(self) -> ItemBibliotecaService:
        if 'item' not in self._services:
            self._services['item'] = ItemBibliotecaService(self.get_item_repository())
        return self._services['item']
    
    def get_prestamo_service(self) -> PrestamoService:
        if 'prestamo' not in self._services:
            self._services['prestamo'] = PrestamoService(
                self.get_prestamo_repository(),
                self.get_item_repository(),
                self.get_usuario_repository(),
                self.get_multa_repository()
            )
        return self._services['prestamo']
    
    def get_reserva_service(self) -> ReservaService:
        if 'reserva' not in self._services:
            self._services['reserva'] = ReservaService(
                self.get_reserva_repository(),
                self.get_item_repository(),
                self.get_usuario_repository()
            )
        return self._services['reserva']
    
    def get_multa_service(self) -> MultaService:
        if 'multa' not in self._services:
            self._services['multa'] = MultaService(
                self.get_multa_repository(),
                self.get_usuario_repository()
            )
        return self._services['multa']
    
    def get_auth_service(self) -> AuthService:
        if 'auth' not in self._services:
            self._services['auth'] = AuthService(self.get_empleado_repository())
        return self._services['auth']
    
    def get_console_ui(self) -> ConsoleUI:
        if not self._console_ui:
            self._console_ui = ConsoleUI(
                self.get_usuario_service(),
                self.get_item_service(),
                self.get_prestamo_service(),
                self.get_reserva_service(),
                self.get_multa_service(),
                self.get_auth_service()
            )
        return self._console_ui