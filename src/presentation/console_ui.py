import sys
from datetime import datetime

from ..application.auth_service import AuthService
from ..application.services import ItemBibliotecaService, MultaService, PrestamoService, ReservaService, UsuarioService
from ..domain.entities import CategoriaItem, TipoUsuario
from ..shared.logger import get_logger
from ..shared.menu_utils import (
    MenuItem,
    confirm_action,
    select_from_list,
    show_dropdown_menu,
    show_error,
    show_info,
    show_success,
    show_warning,
)


class ConsoleUI:
    def __init__(
        self,
        usuario_service: UsuarioService,
        item_service: ItemBibliotecaService,
        prestamo_service: PrestamoService,
        reserva_service: ReservaService,
        multa_service: MultaService,
        auth_service: AuthService,
    ):
        self.usuario_service = usuario_service
        self.item_service = item_service
        self.prestamo_service = prestamo_service
        self.reserva_service = reserva_service
        self.multa_service = multa_service
        self.auth_service = auth_service
        self.logger = get_logger()

    def mostrar_menu_principal(self):
        opciones = [
            ("👤 Gestión de Usuarios", "1", "Registrar, buscar y gestionar usuarios del sistema"),
            ("📚 Gestión de Items", "2", "Agregar, buscar y gestionar items de la biblioteca"),
            ("🔄 Préstamos", "3", "Realizar y gestionar préstamos de items"),
            ("📋 Reservas", "4", "Sistema de reservas para items no disponibles"),
            ("💰 Multas", "5", "Gestión de multas y pagos"),
            ("📊 Reportes", "6", "Generar reportes y estadísticas"),
            ("❌ Salir", "0", "Salir del sistema"),
        ]

        menu_items = []
        for texto, valor, descripcion in opciones:
            menu_items.append(MenuItem(texto, valor, descripcion))

        return show_dropdown_menu(title="SISTEMA DE GESTIÓN BIBLIOTECA LISKOV", items=menu_items, allow_cancel=False)

    def mostrar_menu_usuarios(self):
        opciones = [
            ("Registrar nuevo usuario", "1", "Crear un nuevo usuario en el sistema"),
            ("Buscar usuario por email", "2", "Localizar usuario específico por email"),
            ("Listar todos los usuarios", "3", "Ver lista completa de usuarios registrados"),
            ("Volver al menú principal", "0", "Regresar al menú principal"),
        ]

        menu_items = []
        for texto, valor, descripcion in opciones:
            menu_items.append(MenuItem(texto, valor, descripcion))

        return show_dropdown_menu(title="GESTIÓN DE USUARIOS", items=menu_items, allow_cancel=True)

    def mostrar_menu_items(self):
        opciones = [
            ("Agregar nuevo item", "1", "Añadir nuevo material al catálogo"),
            ("Buscar por título", "2", "Localizar items por título"),
            ("Buscar por autor", "3", "Localizar items por autor"),
            ("Listar por categoría", "4", "Ver items agrupados por categoría"),
            ("Listar items disponibles", "5", "Ver catálogo de items disponibles para préstamo"),
            ("Volver al menú principal", "0", "Regresar al menú principal"),
        ]

        menu_items = []
        for texto, valor, descripcion in opciones:
            menu_items.append(MenuItem(texto, valor, descripcion))

        return show_dropdown_menu(title="GESTIÓN DE ITEMS", items=menu_items, allow_cancel=True)

    def mostrar_menu_prestamos(self):
        opciones = [
            ("Realizar préstamo", "1", "Procesar préstamo de item a usuario"),
            ("Devolver item", "2", "Registrar devolución de item prestado"),
            ("Listar préstamos activos", "3", "Ver todos los préstamos vigentes"),
            ("Historial de préstamos de usuario", "4", "Consultar historial de préstamos"),
            ("Volver al menú principal", "0", "Regresar al menú principal"),
        ]

        menu_items = []
        for texto, valor, descripcion in opciones:
            menu_items.append(MenuItem(texto, valor, descripcion))

        return show_dropdown_menu(title="GESTIÓN DE PRÉSTAMOS", items=menu_items, allow_cancel=True)

    def registrar_usuario(self):
        try:
            show_info("Ingrese los datos del nuevo usuario", "REGISTRO DE USUARIO")
            nombre = input("Nombre: ").strip()
            apellido = input("Apellido: ").strip()
            email = input("Email: ").strip()
            numero_identificacion = input("Número de identificación: ").strip()
            telefono = input("Teléfono (opcional): ").strip() or None

            tipos_usuario = [
                (TipoUsuario.ALUMNO, "Alumno", "Estudiante de la institución"),
                (TipoUsuario.DOCENTE, "Docente", "Profesor o instructor"),
                (TipoUsuario.BIBLIOTECARIO, "Bibliotecario", "Personal administrativo de biblioteca"),
            ]

            tipo_seleccionado = select_from_list(
                title="Seleccione el tipo de usuario",
                items=tipos_usuario,
                display_func=lambda x: x[1],
                value_func=lambda x: x[0],
                description_func=lambda x: x[2],
                allow_cancel=True,
            )

            if not tipo_seleccionado:
                show_warning("Registro cancelado")
                return

            usuario = self.usuario_service.registrar_usuario(
                nombre=nombre,
                apellido=apellido,
                email=email,
                tipo=tipo_seleccionado,
                numero_identificacion=numero_identificacion,
                telefono=telefono,
            )

            show_success(f"Usuario registrado exitosamente con ID: {usuario.id}")
            self.logger.info(f"Usuario registrado: {usuario.email}")

        except Exception as e:
            show_error(f"Error: {str(e)}")
            self.logger.error(f"Error al registrar usuario: {str(e)}")

    def agregar_item(self):
        try:
            show_info("Ingrese los datos del nuevo item", "AGREGAR ITEM")
            titulo = input("Título: ").strip()
            autor = input("Autor (opcional): ").strip() or None
            isbn = input("ISBN (opcional): ").strip() or None
            descripcion = input("Descripción (opcional): ").strip() or None
            ubicacion = input("Ubicación (opcional): ").strip() or None

            categorias_info = [
                (CategoriaItem.LIBRO, "Libro", "Libros físicos y digitales"),
                (CategoriaItem.REVISTA, "Revista", "Publicaciones periódicas"),
                (CategoriaItem.DVD, "DVD", "Contenido audiovisual en formato DVD"),
                (CategoriaItem.CD, "CD", "Discos compactos de audio o datos"),
                (CategoriaItem.AUDIOBOOK, "AudioBook", "Libros en formato de audio"),
                (CategoriaItem.OTRO, "Otro", "Otros materiales de biblioteca"),
            ]

            categoria_seleccionada = select_from_list(
                title="Seleccione la categoría del item",
                items=categorias_info,
                display_func=lambda x: x[1],
                value_func=lambda x: x[0],
                description_func=lambda x: x[2],
                allow_cancel=True,
            )

            if not categoria_seleccionada:
                show_warning("Agregado de item cancelado")
                return

            valor_str = input("Valor de reposición (opcional): ").strip()
            valor_reposicion = float(valor_str) if valor_str else None

            item = self.item_service.agregar_item(
                titulo=titulo,
                categoria=categoria_seleccionada,
                autor=autor,
                isbn=isbn,
                descripcion=descripcion,
                ubicacion=ubicacion,
                valor_reposicion=valor_reposicion,
            )

            show_success(f"Item agregado exitosamente con ID: {item.id}")
            self.logger.info(f"Item agregado: {item.titulo}")

        except Exception as e:
            show_error(f"Error: {str(e)}")
            self.logger.error(f"Error al agregar item: {str(e)}")

    def realizar_prestamo(self):
        try:
            show_info("Proceso de préstamo de items", "REALIZAR PRÉSTAMO")

            # Seleccionar usuario
            usuarios = self.usuario_service.listar_usuarios()
            if not usuarios:
                show_error("No hay usuarios registrados")
                return

            usuario_seleccionado = select_from_list(
                title="Seleccione el usuario para el préstamo",
                items=usuarios,
                display_func=lambda u: f"{u.nombre} {u.apellido} ({u.email})",
                value_func=lambda u: u,
                description_func=lambda u: f"Tipo: {u.tipo.value} - ID: {u.numero_identificacion}",
                allow_cancel=True,
            )

            if not usuario_seleccionado:
                show_warning("Préstamo cancelado")
                return

            show_info(f"Usuario seleccionado: {usuario_seleccionado.nombre} {usuario_seleccionado.apellido}")

            # Buscar y seleccionar item
            titulo_buscar = input("Buscar item por título: ").strip()
            items = self.item_service.buscar_por_titulo(titulo_buscar)

            if not items:
                show_error("No se encontraron items")
                return

            item_seleccionado = select_from_list(
                title="Seleccione el item para préstamo",
                items=items,
                display_func=lambda i: f"[{i.id}] {i.titulo}",
                value_func=lambda i: i,
                description_func=lambda i: (
                    f"Estado: {i.estado.value} - Autor: {i.autor or 'N/A'} - Categoría: {i.categoria.value}"
                ),
                allow_cancel=True,
            )

            if not item_seleccionado:
                show_warning("Préstamo cancelado")
                return

            dias = input("Días de préstamo (15 por defecto): ").strip()
            dias_prestamo = int(dias) if dias else 15

            # Confirmar préstamo
            if not confirm_action(
                (f"¿Confirmar préstamo de '{item_seleccionado.titulo}' "
                 f"a {usuario_seleccionado.nombre} por {dias_prestamo} días?"),
                default=True,
            ):
                show_warning("Préstamo cancelado")
                return

            # Obtener el empleado actual logueado
            empleado_actual = self.auth_service.get_empleado_actual()
            if not empleado_actual:
                show_error("Error: No hay empleado logueado")
                return

            prestamo = self.prestamo_service.realizar_prestamo(
                usuario_id=usuario_seleccionado.id,
                item_id=item_seleccionado.id,
                empleado_id=empleado_actual.id,
                dias_prestamo=dias_prestamo,
            )

            show_success("Préstamo realizado exitosamente")
            show_info(f"ID Préstamo: {prestamo.id}")
            show_info(f"Fecha devolución: {prestamo.fecha_devolucion_esperada.strftime('%d/%m/%Y')}")

            self.logger.info(f"Préstamo realizado: Usuario {usuario_seleccionado.email}, Item {item_seleccionado.titulo}")

        except Exception as e:
            show_error(f"Error: {str(e)}")
            self.logger.error(f"Error al realizar préstamo: {str(e)}")

    def listar_usuarios(self):
        try:
            usuarios = self.usuario_service.listar_usuarios()

            if not usuarios:
                show_warning("No hay usuarios registrados")
                return

            usuario_seleccionado = select_from_list(
                title=f"Lista de usuarios ({len(usuarios)} total)",
                items=usuarios,
                display_func=lambda u: f"{u.nombre} {u.apellido} ({u.email})",
                value_func=lambda u: u,
                description_func=lambda u: (
                    f"Tipo: {u.tipo.value} - Estado: {'Activo' if u.activo else 'Inactivo'} - ID: {u.numero_identificacion}"
                ),
                allow_cancel=True,
                show_numbers=False,
            )

            if usuario_seleccionado:
                show_info(f"Usuario seleccionado: {usuario_seleccionado.nombre} {usuario_seleccionado.apellido}")

        except Exception as e:
            show_error(f"Error: {str(e)}")
            self.logger.error(f"Error al listar usuarios: {str(e)}")

    def listar_items_disponibles(self):
        try:
            items = self.item_service.listar_disponibles()

            if not items:
                show_warning("No hay items disponibles")
                return

            item_seleccionado = select_from_list(
                title=f"Items disponibles ({len(items)} total)",
                items=items,
                display_func=lambda i: f"[{i.id}] {i.titulo}",
                value_func=lambda i: i,
                description_func=lambda i: (
                    f"Autor: {i.autor or 'N/A'} - Categoría: {i.categoria.value} - Ubicación: {i.ubicacion or 'N/A'}"
                ),
                allow_cancel=True,
                show_numbers=False,
            )

            if item_seleccionado:
                show_info(f"Item seleccionado: {item_seleccionado.titulo}")

        except Exception as e:
            show_error(f"Error: {str(e)}")
            self.logger.error(f"Error al listar items: {str(e)}")

    def mostrar_login(self):
        """Muestra la pantalla de login para empleados"""
        print("🔐 Autenticación de Empleado - Sistema Biblioteca Liskov")
        print("=" * 60)

        empleados_activos = self.auth_service.listar_empleados_activos()

        if not empleados_activos:
            show_error("No hay empleados registrados en el sistema. Contacte al administrador.")
            return False

        empleado_seleccionado = select_from_list(
            title="Seleccione su usuario:",
            items=empleados_activos,
            display_func=lambda e: f"{e.nombre} {e.apellido} ({e.usuario_sistema})",
            value_func=lambda e: e,
            description_func=lambda e: f"Cargo: {e.cargo} - Turno: {e.turno or 'No definido'}",
            allow_cancel=False,
        )

        if not empleado_seleccionado:
            return False

        # Solicitar contraseña (fallback para entornos sin getpass)
        try:
            import getpass

            password = getpass.getpass(f"\n🔑 Contraseña para {empleado_seleccionado.nombre}: ")
        except (ImportError, OSError):
            # Fallback para entornos que no soportan getpass
            password = input(f"\n🔑 Contraseña para {empleado_seleccionado.nombre}: ")
        except KeyboardInterrupt:
            print("\n")
            return False

        if self.auth_service.login(empleado_seleccionado.usuario_sistema, password):
            show_success(f"¡Bienvenido/a {empleado_seleccionado.nombre} {empleado_seleccionado.apellido}!")
            return True
        else:
            show_error("Credenciales incorrectas. Acceso denegado.")
            return False

    def ejecutar(self):
        print("🚀 Iniciando Sistema de Biblioteca Liskov...")

        # Login obligatorio
        if not self.mostrar_login():
            print("👋 Sistema cerrado - Login requerido")
            return

        while True:
            try:
                opcion_seleccionada = self.mostrar_menu_principal()

                if not opcion_seleccionada:
                    continue

                opcion = opcion_seleccionada.value

                if opcion == "0":
                    print("👋 ¡Gracias por usar el Sistema de Biblioteca Liskov!")
                    sys.exit(0)
                elif opcion == "1":
                    self._menu_usuarios()
                elif opcion == "2":
                    self._menu_items()
                elif opcion == "3":
                    self._menu_prestamos()
                elif opcion == "4":
                    self._menu_reservas()
                elif opcion == "5":
                    self._menu_multas()
                elif opcion == "6":
                    self._menu_reportes()
                else:
                    show_error("Opción inválida. Por favor seleccione una opción válida.")

            except KeyboardInterrupt:
                print("\n\n👋 ¡Hasta luego!")
                sys.exit(0)
            except Exception as e:
                show_error(f"Error inesperado: {str(e)}")
                self.logger.error(f"Error inesperado: {str(e)}")

    def _menu_usuarios(self):
        while True:
            opcion_seleccionada = self.mostrar_menu_usuarios()

            if not opcion_seleccionada:
                break

            opcion = opcion_seleccionada.value

            if opcion == "0":
                break
            elif opcion == "1":
                self.registrar_usuario()
            elif opcion == "2":
                email = input("Email del usuario: ").strip()
                usuario = self.usuario_service.buscar_usuario_por_email(email)
                if usuario:
                    show_success(f"Usuario encontrado: {usuario.nombre} {usuario.apellido} ({usuario.tipo.value})")
                else:
                    show_error("Usuario no encontrado")
            elif opcion == "3":
                self.listar_usuarios()
            else:
                show_error("Opción inválida")

    def _menu_items(self):
        while True:
            opcion_seleccionada = self.mostrar_menu_items()

            if not opcion_seleccionada:
                break

            opcion = opcion_seleccionada.value

            if opcion == "0":
                break
            elif opcion == "1":
                self.agregar_item()
            elif opcion == "2":
                titulo = input("Título a buscar: ").strip()
                items = self.item_service.buscar_por_titulo(titulo)
                if items:
                    item_seleccionado = select_from_list(
                        title=f"Items encontrados para '{titulo}' ({len(items)} resultados)",
                        items=items,
                        display_func=lambda i: f"[{i.id}] {i.titulo}",
                        value_func=lambda i: i,
                        description_func=lambda i: (
                            f"Estado: {i.estado.value} - Autor: {i.autor or 'N/A'} - Categoría: {i.categoria.value}"
                        ),
                        allow_cancel=True,
                    )
                    if item_seleccionado:
                        show_info(f"Item seleccionado: {item_seleccionado.titulo}")
                else:
                    show_error("No se encontraron items")
            elif opcion == "3":
                autor = input("Autor a buscar: ").strip()
                items = self.item_service.buscar_por_autor(autor)
                if items:
                    item_seleccionado = select_from_list(
                        title=f"Items del autor '{autor}' ({len(items)} resultados)",
                        items=items,
                        display_func=lambda i: f"[{i.id}] {i.titulo}",
                        value_func=lambda i: i,
                        description_func=lambda i: f"Estado: {i.estado.value} - Categoría: {i.categoria.value}",
                        allow_cancel=True,
                    )
                    if item_seleccionado:
                        show_info(f"Item seleccionado: {item_seleccionado.titulo}")
                else:
                    show_error("No se encontraron items de ese autor")
            elif opcion == "4":
                self.listar_por_categoria()
            elif opcion == "5":
                self.listar_items_disponibles()
            else:
                show_error("Opción inválida")

    def _menu_prestamos(self):
        while True:
            opcion_seleccionada = self.mostrar_menu_prestamos()

            if not opcion_seleccionada:
                break

            opcion = opcion_seleccionada.value

            if opcion == "0":
                break
            elif opcion == "1":
                self.realizar_prestamo()
            elif opcion == "2":
                self.devolver_item()
            elif opcion == "3":
                prestamos = self.prestamo_service.listar_prestamos_activos()
                if prestamos:
                    prestamo_seleccionado = select_from_list(
                        title=f"Préstamos activos ({len(prestamos)} total)",
                        items=prestamos,
                        display_func=lambda p: f"Préstamo #{p.id} - Usuario: {p.usuario_id}",
                        value_func=lambda p: p,
                        description_func=lambda p: (
                            f"Item: {p.item_id} - Vence: {p.fecha_devolucion_esperada.strftime('%d/%m/%Y')}"
                        ),
                        allow_cancel=True,
                    )
                    if prestamo_seleccionado:
                        show_info(f"Préstamo seleccionado: ID {prestamo_seleccionado.id}")
                else:
                    show_warning("No hay préstamos activos")
            elif opcion == "4":
                self.historial_prestamos_usuario()
            else:
                show_error("Opción inválida")

    def mostrar_menu_reservas(self):
        opciones = [
            ("Realizar reserva", "1", "Crear nueva reserva para item no disponible"),
            ("Listar reservas activas", "2", "Ver todas las reservas vigentes"),
            ("Cancelar reserva", "3", "Cancelar una reserva existente"),
            ("Convertir reserva a préstamo", "4", "Procesar reserva cuando item esté disponible"),
            ("Volver al menú principal", "0", "Regresar al menú principal"),
        ]

        menu_items = []
        for texto, valor, descripcion in opciones:
            menu_items.append(MenuItem(texto, valor, descripcion))

        return show_dropdown_menu(title="GESTIÓN DE RESERVAS", items=menu_items, allow_cancel=True)

    def mostrar_menu_multas(self):
        opciones = [
            ("Listar multas pendientes", "1", "Ver multas no pagadas del sistema"),
            ("Buscar multas de usuario", "2", "Consultar multas de un usuario específico"),
            ("Registrar pago de multa", "3", "Marcar multa como pagada"),
            ("Generar reporte de multas", "4", "Crear reporte de multas del período"),
            ("Volver al menú principal", "0", "Regresar al menú principal"),
        ]

        menu_items = []
        for texto, valor, descripcion in opciones:
            menu_items.append(MenuItem(texto, valor, descripcion))

        return show_dropdown_menu(title="GESTIÓN DE MULTAS", items=menu_items, allow_cancel=True)

    def mostrar_menu_reportes(self):
        opciones = [
            ("Reporte de préstamos activos", "1", "Items actualmente prestados"),
            ("Estadísticas de uso", "2", "Items más solicitados y estadísticas"),
            ("Reporte de usuarios activos", "3", "Usuarios con mayor actividad"),
            ("Reporte de multas del mes", "4", "Multas generadas en el período"),
            ("Auditoria de operaciones", "5", "Log de operaciones por empleado"),
            ("Volver al menú principal", "0", "Regresar al menú principal"),
        ]

        menu_items = []
        for texto, valor, descripcion in opciones:
            menu_items.append(MenuItem(texto, valor, descripcion))

        return show_dropdown_menu(title="REPORTES Y ESTADÍSTICAS", items=menu_items, allow_cancel=True)

    def _menu_reservas(self):
        while True:
            opcion_seleccionada = self.mostrar_menu_reservas()

            if not opcion_seleccionada:
                break

            opcion = opcion_seleccionada.value

            if opcion == "0":
                break
            elif opcion == "1":
                self.realizar_reserva()
            elif opcion == "2":
                self.listar_reservas_activas()
            elif opcion == "3":
                self.cancelar_reserva()
            elif opcion == "4":
                self.convertir_reserva_prestamo()
            else:
                show_error("Opción inválida")

    def _menu_multas(self):
        while True:
            opcion_seleccionada = self.mostrar_menu_multas()

            if not opcion_seleccionada:
                break

            opcion = opcion_seleccionada.value

            if opcion == "0":
                break
            elif opcion == "1":
                self.listar_multas_pendientes()
            elif opcion == "2":
                self.buscar_multas_usuario()
            elif opcion == "3":
                self.registrar_pago_multa()
            elif opcion == "4":
                self.generar_reporte_multas()
            else:
                show_error("Opción inválida")

    def _menu_reportes(self):
        while True:
            opcion_seleccionada = self.mostrar_menu_reportes()

            if not opcion_seleccionada:
                break

            opcion = opcion_seleccionada.value

            if opcion == "0":
                break
            elif opcion == "1":
                self.reporte_prestamos_activos()
            elif opcion == "2":
                self.estadisticas_uso()
            elif opcion == "3":
                self.reporte_usuarios_activos()
            elif opcion == "4":
                self.reporte_multas_mes()
            elif opcion == "5":
                self.auditoria_operaciones()
            else:
                show_error("Opción inválida")

    # =============== FUNCIONALIDADES DE PRÉSTAMOS ===============

    def devolver_item(self):
        """Registra la devolución de un item prestado"""
        try:
            prestamos_activos = self.prestamo_service.listar_prestamos_activos()

            if not prestamos_activos:
                show_warning("No hay préstamos activos para devolver")
                return

            prestamo_seleccionado = select_from_list(
                title="Seleccione el préstamo a devolver:",
                items=prestamos_activos,
                display_func=lambda p: f"Préstamo #{p.id} - Usuario: {p.usuario_id}",
                value_func=lambda p: p,
                description_func=lambda p: f"Item: {p.item_id} - Vence: {p.fecha_devolucion_esperada.strftime('%d/%m/%Y')}",
                allow_cancel=True,
            )

            if not prestamo_seleccionado:
                show_warning("Devolución cancelada")
                return

            observaciones = input("Observaciones (opcional): ").strip()

            if confirm_action(f"¿Confirmar devolución del préstamo #{prestamo_seleccionado.id}?", default=True):
                prestamo_actualizado = self.prestamo_service.devolver_item(
                    prestamo_seleccionado.id, observaciones if observaciones else None
                )

                show_success("Devolución registrada exitosamente")
                show_info(f"Fecha de devolución: {prestamo_actualizado.fecha_devolucion_real.strftime('%d/%m/%Y %H:%M')}")

                if prestamo_actualizado.fecha_devolucion_real > prestamo_actualizado.fecha_devolucion_esperada:
                    dias_atraso = (
                        prestamo_actualizado.fecha_devolucion_real - prestamo_actualizado.fecha_devolucion_esperada
                    ).days
                    show_warning(f"Devolución tardía: {dias_atraso} días de atraso - Se generó multa automáticamente")

                self.logger.info(f"Devolución registrada: Préstamo {prestamo_seleccionado.id}")
            else:
                show_warning("Devolución cancelada")

        except Exception as e:
            show_error(f"Error al devolver item: {str(e)}")
            self.logger.error(f"Error al devolver item: {str(e)}")

    def historial_prestamos_usuario(self):
        """Consulta el historial de préstamos de un usuario específico"""
        try:
            usuarios = self.usuario_service.listar_usuarios()

            if not usuarios:
                show_warning("No hay usuarios registrados")
                return

            usuario_seleccionado = select_from_list(
                title="Seleccione el usuario para consultar historial:",
                items=usuarios,
                display_func=lambda u: f"{u.nombre} {u.apellido} ({u.email})",
                value_func=lambda u: u,
                description_func=lambda u: f"Tipo: {u.tipo.value} - ID: {u.numero_identificacion}",
                allow_cancel=True,
            )

            if not usuario_seleccionado:
                return

            prestamos = self.prestamo_service.listar_prestamos_usuario(usuario_seleccionado.id)

            if not prestamos:
                show_warning(
                    f"No hay préstamos registrados para {usuario_seleccionado.nombre} {usuario_seleccionado.apellido}"
                )
                return

            print(f"\n📚 HISTORIAL DE PRÉSTAMOS - {usuario_seleccionado.nombre} {usuario_seleccionado.apellido}")
            print("=" * 80)

            for prestamo in prestamos:
                estado = "✅ Devuelto" if not prestamo.activo else "📖 Activo"
                fecha_dev = (
                    prestamo.fecha_devolucion_real.strftime("%d/%m/%Y") if prestamo.fecha_devolucion_real else "Pendiente"
                )

                print(f"Préstamo #{prestamo.id} - Item ID: {prestamo.item_id}")
                print(f"  📅 Fecha préstamo: {prestamo.fecha_prestamo.strftime('%d/%m/%Y')}")
                print(f"  ⏰ Fecha esperada: {prestamo.fecha_devolucion_esperada.strftime('%d/%m/%Y')}")
                print(f"  🔄 Fecha devolución: {fecha_dev}")
                print(f"  📊 Estado: {estado}")
                if prestamo.observaciones:
                    print(f"  📝 Observaciones: {prestamo.observaciones}")
                print("-" * 50)

            input("\\nPresione Enter para continuar...")

        except Exception as e:
            show_error(f"Error al consultar historial: {str(e)}")
            self.logger.error(f"Error al consultar historial: {str(e)}")

    # =============== FUNCIONALIDADES DE RESERVAS ===============

    def realizar_reserva(self):
        """Crear nueva reserva para item no disponible"""
        try:
            show_info("Proceso de reserva de items", "REALIZAR RESERVA")

            # Seleccionar usuario
            usuarios = self.usuario_service.listar_usuarios()
            if not usuarios:
                show_error("No hay usuarios registrados")
                return

            usuario_seleccionado = select_from_list(
                title="Seleccione el usuario para la reserva:",
                items=usuarios,
                display_func=lambda u: f"{u.nombre} {u.apellido} ({u.email})",
                value_func=lambda u: u,
                description_func=lambda u: f"Tipo: {u.tipo.value} - ID: {u.numero_identificacion}",
                allow_cancel=True,
            )

            if not usuario_seleccionado:
                show_warning("Reserva cancelada")
                return

            # Buscar item
            titulo_buscar = input("Buscar item por título: ").strip()
            items = self.item_service.buscar_por_titulo(titulo_buscar)

            if not items:
                show_error("No se encontraron items")
                return

            item_seleccionado = select_from_list(
                title="Seleccione el item para reservar:",
                items=items,
                display_func=lambda i: f"[{i.id}] {i.titulo}",
                value_func=lambda i: i,
                description_func=lambda i: f"Estado: {i.estado.value} - Autor: {i.autor or 'N/A'}",
                allow_cancel=True,
            )

            if not item_seleccionado:
                show_warning("Reserva cancelada")
                return

            dias_expiracion = input("Días de vigencia de la reserva (3 por defecto): ").strip()
            dias_reserva = int(dias_expiracion) if dias_expiracion else 3

            # Obtener empleado actual
            empleado_actual = self.auth_service.get_empleado_actual()
            if not empleado_actual:
                show_error("Error: No hay empleado logueado")
                return

            if confirm_action(
                f"¿Confirmar reserva de '{item_seleccionado.titulo}' para {usuario_seleccionado.nombre}?", default=True
            ):
                reserva = self.reserva_service.realizar_reserva(
                    usuario_id=usuario_seleccionado.id,
                    item_id=item_seleccionado.id,
                    empleado_id=empleado_actual.id,
                    dias_expiracion=dias_reserva,
                )

                show_success("Reserva creada exitosamente")
                show_info(f"ID Reserva: {reserva.id}")
                show_info(f"Fecha expiración: {reserva.fecha_expiracion.strftime('%d/%m/%Y')}")

                self.logger.info(f"Reserva creada: Usuario {usuario_seleccionado.email}, Item {item_seleccionado.titulo}")
            else:
                show_warning("Reserva cancelada")

        except Exception as e:
            show_error(f"Error al crear reserva: {str(e)}")
            self.logger.error(f"Error al crear reserva: {str(e)}")

    def listar_reservas_activas(self):
        """Ver todas las reservas vigentes"""
        try:
            reservas = self.reserva_service.listar_reservas_activas()

            if not reservas:
                show_warning("No hay reservas activas")
                return

            print(f"\\n📋 RESERVAS ACTIVAS ({len(reservas)} total)")
            print("=" * 80)

            for reserva in reservas:
                print(f"Reserva #{reserva.id}")
                print(f"  👤 Usuario ID: {reserva.usuario_id}")
                print(f"  📚 Item ID: {reserva.item_id}")
                print(f"  📅 Fecha reserva: {reserva.fecha_reserva.strftime('%d/%m/%Y')}")
                print(f"  ⏰ Expira: {reserva.fecha_expiracion.strftime('%d/%m/%Y')}")
                print(f"  👔 Empleado: {reserva.empleado_id}")
                print("-" * 50)

            input("\\nPresione Enter para continuar...")

        except Exception as e:
            show_error(f"Error al listar reservas: {str(e)}")
            self.logger.error(f"Error al listar reservas: {str(e)}")

    def cancelar_reserva(self):
        """Cancelar una reserva existente"""
        try:
            reservas_activas = self.reserva_service.listar_reservas_activas()

            if not reservas_activas:
                show_warning("No hay reservas activas para cancelar")
                return

            reserva_seleccionada = select_from_list(
                title="Seleccione la reserva a cancelar:",
                items=reservas_activas,
                display_func=lambda r: f"Reserva #{r.id} - Usuario: {r.usuario_id}",
                value_func=lambda r: r,
                description_func=lambda r: f"Item: {r.item_id} - Expira: {r.fecha_expiracion.strftime('%d/%m/%Y')}",
                allow_cancel=True,
            )

            if not reserva_seleccionada:
                show_warning("Cancelación cancelada")
                return

            if confirm_action(f"¿Confirmar cancelación de la reserva #{reserva_seleccionada.id}?", default=False):
                self.reserva_service.cancelar_reserva(reserva_seleccionada.id)

                show_success("Reserva cancelada exitosamente")
                self.logger.info(f"Reserva cancelada: {reserva_seleccionada.id}")
            else:
                show_warning("Cancelación cancelada")

        except Exception as e:
            show_error(f"Error al cancelar reserva: {str(e)}")
            self.logger.error(f"Error al cancelar reserva: {str(e)}")

    def convertir_reserva_prestamo(self):
        """Procesar reserva cuando item esté disponible"""
        show_warning("🚧 Funcionalidad en desarrollo - Conversión de reserva a préstamo")
        # Esta funcionalidad requiere lógica adicional en los servicios

    # =============== FUNCIONALIDADES DE MULTAS ===============

    def listar_multas_pendientes(self):
        """Ver multas no pagadas del sistema"""
        try:
            multas = self.multa_service.listar_multas_pendientes()

            if not multas:
                show_success("No hay multas pendientes en el sistema")
                return

            total_monto = sum(multa.monto for multa in multas)

            print(f"\\n💰 MULTAS PENDIENTES ({len(multas)} total - Monto: ${total_monto:.2f})")
            print("=" * 80)

            for multa in multas:
                print(f"Multa #{multa.id}")
                print(f"  👤 Usuario ID: {multa.usuario_id}")
                print(f"  📚 Préstamo ID: {multa.prestamo_id}")
                print(f"  💵 Monto: ${multa.monto:.2f}")
                print(f"  📝 Descripción: {multa.descripcion}")
                print(f"  📅 Fecha multa: {multa.fecha_multa.strftime('%d/%m/%Y')}")
                print(f"  👔 Empleado: {multa.empleado_id}")
                print("-" * 50)

            input("\\nPresione Enter para continuar...")

        except Exception as e:
            show_error(f"Error al listar multas: {str(e)}")
            self.logger.error(f"Error al listar multas: {str(e)}")

    def buscar_multas_usuario(self):
        """Consultar multas de un usuario específico"""
        try:
            usuarios = self.usuario_service.listar_usuarios()

            if not usuarios:
                show_warning("No hay usuarios registrados")
                return

            usuario_seleccionado = select_from_list(
                title="Seleccione el usuario para consultar multas:",
                items=usuarios,
                display_func=lambda u: f"{u.nombre} {u.apellido} ({u.email})",
                value_func=lambda u: u,
                description_func=lambda u: f"Tipo: {u.tipo.value} - ID: {u.numero_identificacion}",
                allow_cancel=True,
            )

            if not usuario_seleccionado:
                return

            multas = self.multa_service.listar_multas_usuario(usuario_seleccionado.id)

            if not multas:
                show_success(f"El usuario {usuario_seleccionado.nombre} {usuario_seleccionado.apellido} no tiene multas")
                return

            multas_pendientes = [m for m in multas if not m.pagada]
            total_pendiente = sum(m.monto for m in multas_pendientes)

            print(f"\\n💰 MULTAS DE {usuario_seleccionado.nombre} {usuario_seleccionado.apellido}")
            print("=" * 80)
            print(f"Total multas: {len(multas)} | Pendientes: {len(multas_pendientes)} (${total_pendiente:.2f})")
            print("-" * 80)

            for multa in multas:
                estado = "✅ Pagada" if multa.pagada else "❌ Pendiente"
                print(f"Multa #{multa.id} - {estado}")
                print(f"  💵 Monto: ${multa.monto:.2f}")
                print(f"  📝 Descripción: {multa.descripcion}")
                print(f"  📅 Fecha: {multa.fecha_multa.strftime('%d/%m/%Y')}")
                print("-" * 40)

            input("\\nPresione Enter para continuar...")

        except Exception as e:
            show_error(f"Error al buscar multas: {str(e)}")
            self.logger.error(f"Error al buscar multas: {str(e)}")

    def registrar_pago_multa(self):
        """Marcar multa como pagada"""
        try:
            multas_pendientes = self.multa_service.listar_multas_pendientes()

            if not multas_pendientes:
                show_success("No hay multas pendientes para pagar")
                return

            multa_seleccionada = select_from_list(
                title="Seleccione la multa a pagar:",
                items=multas_pendientes,
                display_func=lambda m: f"Multa #{m.id} - Usuario: {m.usuario_id} - ${m.monto:.2f}",
                value_func=lambda m: m,
                description_func=lambda m: f"{m.descripcion} - {m.fecha_multa.strftime('%d/%m/%Y')}",
                allow_cancel=True,
            )

            if not multa_seleccionada:
                show_warning("Pago cancelado")
                return

            if confirm_action(
                f"¿Confirmar pago de multa #{multa_seleccionada.id} por ${multa_seleccionada.monto:.2f}?", default=True
            ):
                multa_actualizada = self.multa_service.pagar_multa(multa_seleccionada.id)

                show_success(f"Pago registrado exitosamente - ${multa_actualizada.monto:.2f}")
                self.logger.info(f"Pago de multa registrado: {multa_seleccionada.id}")
            else:
                show_warning("Pago cancelado")

        except Exception as e:
            show_error(f"Error al registrar pago: {str(e)}")
            self.logger.error(f"Error al registrar pago: {str(e)}")

    def generar_reporte_multas(self):
        """Crear reporte de multas del período"""
        show_warning("🚧 Funcionalidad en desarrollo - Reporte de multas")

    # =============== FUNCIONALIDADES DE REPORTES ===============

    def reporte_prestamos_activos(self):
        """Items actualmente prestados"""
        try:
            prestamos = self.prestamo_service.listar_prestamos_activos()

            if not prestamos:
                show_success("No hay préstamos activos")
                return

            print(f"\\n📊 REPORTE DE PRÉSTAMOS ACTIVOS ({len(prestamos)} total)")
            print("=" * 80)

            for prestamo in prestamos:
                dias_restantes = (prestamo.fecha_devolucion_esperada - datetime.now()).days
                estado_tiempo = "⚠️ Vencido" if dias_restantes < 0 else f"📅 {dias_restantes} días restantes"

                print(f"Préstamo #{prestamo.id}")
                print(f"  👤 Usuario ID: {prestamo.usuario_id}")
                print(f"  📚 Item ID: {prestamo.item_id}")
                print(f"  📅 Prestado: {prestamo.fecha_prestamo.strftime('%d/%m/%Y')}")
                print(f"  ⏰ Vence: {prestamo.fecha_devolucion_esperada.strftime('%d/%m/%Y')} - {estado_tiempo}")
                print(f"  👔 Empleado: {prestamo.empleado_id}")
                print("-" * 50)

            input("\\nPresione Enter para continuar...")

        except Exception as e:
            show_error(f"Error al generar reporte: {str(e)}")
            self.logger.error(f"Error al generar reporte: {str(e)}")

    def estadisticas_uso(self):
        """Items más solicitados y estadísticas"""
        show_warning("🚧 Funcionalidad en desarrollo - Estadísticas de uso")

    def reporte_usuarios_activos(self):
        """Usuarios con mayor actividad"""
        show_warning("🚧 Funcionalidad en desarrollo - Reporte de usuarios activos")

    def reporte_multas_mes(self):
        """Multas generadas en el período"""
        show_warning("🚧 Funcionalidad en desarrollo - Reporte de multas del mes")

    def auditoria_operaciones(self):
        """Log de operaciones por empleado"""
        try:
            empleado_actual = self.auth_service.get_empleado_actual()

            print("\\n🔍 AUDITORÍA DE OPERACIONES")
            print("=" * 50)
            print(f"👔 Empleado actual: {empleado_actual.nombre} {empleado_actual.apellido}")
            print(f"🏢 Cargo: {empleado_actual.cargo}")
            print(f"📧 Email: {empleado_actual.email}")
            print(f"🕐 Turno: {empleado_actual.turno}")

            if empleado_actual.cargo == "Bibliotecario Jefe":
                print("\\n🔐 Como Bibliotecario Jefe tiene acceso a:")
                print("  • Gestión de empleados")
                print("  • Reportes completos del sistema")
                print("  • Auditoria total de operaciones")

            print("\\n📝 Funcionalidad completa de auditoría en desarrollo...")
            print("Las operaciones se registran automáticamente en logs del sistema.")

            input("\\nPresione Enter para continuar...")

        except Exception as e:
            show_error(f"Error en auditoría: {str(e)}")
            self.logger.error(f"Error en auditoría: {str(e)}")

    # =============== FUNCIONALIDADES DE ITEMS ADICIONALES ===============

    def listar_por_categoria(self):
        """Navegación por categorías con listado navegable"""
        try:
            from ..domain.entities import CategoriaItem

            # Crear lista de categorías disponibles
            categorias = list(CategoriaItem)
            categorias_con_emoji = {
                CategoriaItem.LIBRO: "📚 Libros",
                CategoriaItem.REVISTA: "📰 Revistas",
                CategoriaItem.DVD: "📀 DVDs",
                CategoriaItem.CD: "💿 CDs",
                CategoriaItem.AUDIOBOOK: "🎧 Audiolibros",
                CategoriaItem.OTRO: "📄 Otros",
            }

            categoria_seleccionada = select_from_list(
                title="Seleccione una categoría para explorar:",
                items=categorias,
                display_func=lambda c: categorias_con_emoji.get(c, c.value.capitalize()),
                value_func=lambda c: c,
                description_func=lambda c: f"Ver todos los items de tipo {c.value}",
                allow_cancel=True,
            )

            if not categoria_seleccionada:
                return

            # Obtener items de la categoría seleccionada
            items = self.item_service.listar_por_categoria(categoria_seleccionada.value)

            if not items:
                categoria_nombre = categorias_con_emoji.get(categoria_seleccionada, categoria_seleccionada.value.capitalize())
                show_warning(f"No hay items en la categoría: {categoria_nombre}")
                return

            # Mostrar items de forma navegable
            while True:
                categoria_nombre = categorias_con_emoji.get(categoria_seleccionada, categoria_seleccionada.value.capitalize())

                opciones_items = []
                for item in items:
                    estado_emoji = {"disponible": "✅", "prestado": "📤", "en_reparacion": "🔧", "perdido": "❌"}
                    emoji = estado_emoji.get(item.estado.value, "❓")
                    opciones_items.append(
                        MenuItem(
                            f"[{item.id}] {item.titulo}",
                            item,
                            (f"{emoji} {item.estado.value.capitalize()} | Autor: {item.autor or 'N/A'} | "
                             f"Ubicación: {item.ubicacion or 'N/A'}"),
                        )
                    )

                # Agregar opción para volver
                opciones_items.append(MenuItem("🔙 Volver a categorías", None, "Regresar a la selección de categorías"))

                item_seleccionado = show_dropdown_menu(
                    title=f"{categoria_nombre} ({len(items)} items)", items=opciones_items, allow_cancel=True
                )

                if not item_seleccionado or item_seleccionado.value is None:
                    break

                # Mostrar detalles del item seleccionado
                item = item_seleccionado.value
                self.mostrar_detalles_item(item)

        except Exception as e:
            show_error(f"Error al listar por categoría: {str(e)}")
            self.logger.error(f"Error al listar por categoría: {str(e)}")

    def mostrar_detalles_item(self, item):
        """Muestra detalles completos de un item"""
        try:
            estado_emoji = {"disponible": "✅", "prestado": "📤", "en_reparacion": "🔧", "perdido": "❌"}
            emoji = estado_emoji.get(item.estado.value, "❓")

            print("\\n📖 DETALLES DEL ITEM")
            print("=" * 60)
            print(f"🆔 ID: {item.id}")
            print(f"📚 Título: {item.titulo}")
            print(f"✍️  Autor: {item.autor or 'No especificado'}")
            print(f"📋 Categoría: {item.categoria.value.capitalize()}")
            print(f"📖 ISBN: {item.isbn or 'No especificado'}")
            print(f"📊 Estado: {emoji} {item.estado.value.capitalize()}")
            print(f"📍 Ubicación: {item.ubicacion or 'No especificada'}")
            print(f"📅 Fecha adquisición: "
                  f"{item.fecha_adquisicion.strftime('%d/%m/%Y') if item.fecha_adquisicion else 'No registrada'}")

            if item.descripcion:
                print(f"📝 Descripción: {item.descripcion}")

            if item.valor_reposicion:
                print(f"💰 Valor reposición: ${item.valor_reposicion:.2f}")

            print("=" * 60)

            # Opciones de acción
            if item.estado.value == "disponible":
                print("💡 Este item está disponible para préstamo")
            elif item.estado.value == "prestado":
                print("⏳ Este item está actualmente prestado")
            elif item.estado.value == "en_reparacion":
                print("🔧 Este item está en reparación")
            elif item.estado.value == "perdido":
                print("❌ Este item está reportado como perdido")

            input("\\nPresione Enter para continuar...")

        except Exception as e:
            show_error(f"Error al mostrar detalles: {str(e)}")
            self.logger.error(f"Error al mostrar detalles: {str(e)}")
