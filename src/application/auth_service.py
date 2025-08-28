import hashlib
from typing import Optional
from datetime import datetime
from ..domain.entities import Empleado, SesionEmpleado
from .interfaces import IEmpleadoRepository
from ..shared.logger import get_logger


class AuthService:
    def __init__(self, empleado_repo: IEmpleadoRepository):
        self.empleado_repo = empleado_repo
        self.logger = get_logger()
        self._sesion_actual: Optional[SesionEmpleado] = None

    def hash_password(self, password: str) -> str:
        """Genera hash de contraseña usando SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def verificar_password(self, password: str, hash_password: str) -> bool:
        """Verifica si la contraseña coincide con el hash"""
        return self.hash_password(password) == hash_password

    def login(self, usuario_sistema: str, password: str) -> bool:
        """
        Autentica un empleado
        
        Args:
            usuario_sistema: Nombre de usuario del sistema
            password: Contraseña en texto plano
            
        Returns:
            True si la autenticación es exitosa
        """
        try:
            empleado = self.empleado_repo.obtener_por_usuario_sistema(usuario_sistema)
            
            if not empleado:
                self.logger.warning(f"Intento de login fallido: usuario '{usuario_sistema}' no encontrado")
                return False
            
            if not empleado.activo:
                self.logger.warning(f"Intento de login con usuario inactivo: '{usuario_sistema}'")
                return False
            
            if not self.verificar_password(password, empleado.password_hash):
                self.logger.warning(f"Intento de login fallido: contraseña incorrecta para '{usuario_sistema}'")
                return False
            
            # Login exitoso
            self._sesion_actual = SesionEmpleado(
                empleado=empleado,
                fecha_login=datetime.now(),
                activa=True
            )
            
            self.logger.info(f"Login exitoso: {empleado.nombre} {empleado.apellido} ({usuario_sistema})")
            return True
            
        except Exception as e:
            self.logger.error(f"Error durante login: {str(e)}")
            return False

    def logout(self):
        """Cierra la sesión actual"""
        if self._sesion_actual:
            self.logger.info(f"Logout: {self._sesion_actual.empleado.nombre} {self._sesion_actual.empleado.apellido}")
            self._sesion_actual.activa = False
            self._sesion_actual = None

    def get_empleado_actual(self) -> Optional[Empleado]:
        """Obtiene el empleado logueado actualmente"""
        if self._sesion_actual and self._sesion_actual.activa:
            return self._sesion_actual.empleado
        return None

    def get_sesion_actual(self) -> Optional[SesionEmpleado]:
        """Obtiene la sesión actual"""
        return self._sesion_actual if self._sesion_actual and self._sesion_actual.activa else None

    def esta_logueado(self) -> bool:
        """Verifica si hay un empleado logueado"""
        return self._sesion_actual is not None and self._sesion_actual.activa

    def crear_empleado(self, nombre: str, apellido: str, email: str, 
                      usuario_sistema: str, password: str, cargo: str = "Bibliotecario",
                      turno: str = "") -> Empleado:
        """
        Crea un nuevo empleado
        
        Args:
            nombre: Nombre del empleado
            apellido: Apellido del empleado
            email: Email del empleado
            usuario_sistema: Nombre de usuario para login
            password: Contraseña en texto plano
            cargo: Cargo del empleado
            turno: Turno de trabajo
            
        Returns:
            Empleado creado
            
        Raises:
            ValueError: Si el usuario del sistema ya existe
        """
        # Verificar que el usuario del sistema no exista
        empleado_existente = self.empleado_repo.obtener_por_usuario_sistema(usuario_sistema)
        if empleado_existente:
            raise ValueError(f"El usuario del sistema '{usuario_sistema}' ya existe")
        
        empleado = Empleado(
            nombre=nombre,
            apellido=apellido,
            email=email,
            usuario_sistema=usuario_sistema,
            password_hash=self.hash_password(password),
            cargo=cargo,
            turno=turno,
            fecha_registro=datetime.now()
        )
        
        empleado_creado = self.empleado_repo.crear(empleado)
        self.logger.info(f"Empleado creado: {nombre} {apellido} ({usuario_sistema})")
        
        return empleado_creado

    def listar_empleados_activos(self) -> list[Empleado]:
        """Lista todos los empleados activos"""
        return self.empleado_repo.listar_activos()

    def cambiar_password(self, empleado_id: int, password_actual: str, password_nuevo: str) -> bool:
        """
        Cambia la contraseña de un empleado
        
        Args:
            empleado_id: ID del empleado
            password_actual: Contraseña actual
            password_nuevo: Nueva contraseña
            
        Returns:
            True si el cambio fue exitoso
        """
        try:
            empleado = self.empleado_repo.obtener_por_id(empleado_id)
            if not empleado:
                return False
            
            # Verificar contraseña actual
            if not self.verificar_password(password_actual, empleado.password_hash):
                return False
            
            # Actualizar contraseña
            empleado.password_hash = self.hash_password(password_nuevo)
            self.empleado_repo.actualizar(empleado)
            
            self.logger.info(f"Contraseña cambiada para empleado: {empleado.nombre} {empleado.apellido}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error al cambiar contraseña: {str(e)}")
            return False