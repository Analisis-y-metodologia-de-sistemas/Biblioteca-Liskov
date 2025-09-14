import os
import sys
from typing import Any, Callable, List, Optional


# Cross-platform colors (simple approach without external dependencies)
class Colors:
    # Simple color codes that work on most terminals
    # If terminal doesn't support colors, they'll be ignored
    HEADER = "\033[95m" if sys.stdout.isatty() else ""
    BLUE = "\033[94m" if sys.stdout.isatty() else ""
    CYAN = "\033[96m" if sys.stdout.isatty() else ""
    GREEN = "\033[92m" if sys.stdout.isatty() else ""
    YELLOW = "\033[93m" if sys.stdout.isatty() else ""
    RED = "\033[91m" if sys.stdout.isatty() else ""
    BOLD = "\033[1m" if sys.stdout.isatty() else ""
    UNDERLINE = "\033[4m" if sys.stdout.isatty() else ""
    END = "\033[0m" if sys.stdout.isatty() else ""


# Aliases for backward compatibility
class Fore:
    CYAN = Colors.CYAN
    YELLOW = Colors.YELLOW
    GREEN = Colors.GREEN
    RED = Colors.RED
    BLUE = Colors.BLUE


class Style:
    BRIGHT = Colors.BOLD
    RESET_ALL = Colors.END


class Back:
    GREEN = "\033[42m" if sys.stdout.isatty() else ""


# Sistema simplificado basado en input() estándar


class MenuItem:
    def __init__(self, text: str, value: Any = None, description: str = ""):
        self.text = text
        self.value = value if value is not None else text
        self.description = description


def get_user_choice():
    """Obtiene la elección del usuario usando entrada simple"""
    try:
        response = input(f"\n{Fore.CYAN}Seleccione una opción (número o 'q' para salir): {Style.RESET_ALL}").strip().lower()

        if response == "q":
            return "q"
        elif response == "":
            return "enter"
        elif response.isdigit():
            return f"digit_{response}"
        else:
            return "invalid"
    except (EOFError, KeyboardInterrupt):
        return "q"


def show_dropdown_menu(
    title: str,
    items: List[MenuItem],
    selected_index: int = 0,
    show_numbers: bool = True,
    show_descriptions: bool = True,
    allow_cancel: bool = True,
) -> Optional[MenuItem]:
    """
    Muestra un menú numerado simple

    Args:
        title: Título del menú
        items: Lista de elementos MenuItem
        selected_index: Índice inicial seleccionado (no usado en modo numérico)
        show_numbers: Mostrar números de opción
        show_descriptions: Mostrar descripciones de items
        allow_cancel: Permitir cancelar con Q

    Returns:
        MenuItem seleccionado o None si se canceló
    """
    if not items:
        return None

    while True:
        # Mostrar título
        print(f"\n{Fore.CYAN}{Style.BRIGHT}{title}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * len(title)}{Style.RESET_ALL}")

        # Mostrar instrucciones
        instructions = f"{Fore.YELLOW}Ingrese el número de la opción"
        if allow_cancel:
            instructions += f" | 'q' para cancelar"
        print(instructions + Style.RESET_ALL)

        print()  # Línea en blanco

        # Mostrar items
        for i, item in enumerate(items):
            prefix = f"{i + 1}. "
            line = f"  {prefix}{item.text}"
            print(line)

            # Mostrar descripción si está disponible
            if show_descriptions and item.description:
                desc_line = f"     {Fore.YELLOW}💡 {item.description}{Style.RESET_ALL}"
                print(desc_line)

        # Obtener input del usuario
        choice = get_user_choice()

        if choice == "q" and allow_cancel:
            return None
        elif choice.startswith("digit_"):
            digit = choice.split("_")[1]
            try:
                num = int(digit)
                if 1 <= num <= len(items):
                    return items[num - 1]
                else:
                    print(f"{Fore.RED}❌ Opción inválida. Seleccione un número entre 1 y {len(items)}{Style.RESET_ALL}")
                    continue
            except ValueError:
                print(f"{Fore.RED}❌ Entrada inválida{Style.RESET_ALL}")
                continue
        else:
            print(f"{Fore.RED}❌ Entrada inválida. Use números del 1 al {len(items)}{Style.RESET_ALL}")
            continue


def select_from_list(
    title: str,
    items: List[Any],
    display_func: Callable[[Any], str] = str,
    value_func: Callable[[Any], Any] = lambda x: x,
    description_func: Optional[Callable[[Any], str]] = None,
    allow_cancel: bool = True,
    show_numbers: bool = False,
) -> Optional[Any]:
    """
    Selecciona un item de una lista usando menú desplegable

    Args:
        title: Título del menú
        items: Lista de items a mostrar
        display_func: Función para mostrar el texto del item
        value_func: Función para obtener el valor del item
        description_func: Función opcional para describir el item
        allow_cancel: Permitir cancelar
        show_numbers: Mostrar números

    Returns:
        Item seleccionado o None si se canceló
    """
    if not items:
        print(f"{Fore.YELLOW}⚠️  No hay elementos disponibles{Style.RESET_ALL}")
        return None

    menu_items = []
    for item in items:
        text = display_func(item)
        value = value_func(item)
        description = description_func(item) if description_func else ""
        menu_items.append(MenuItem(text, value, description))

    selected_item = show_dropdown_menu(
        title=title,
        items=menu_items,
        show_numbers=show_numbers,
        show_descriptions=bool(description_func),
        allow_cancel=allow_cancel,
    )

    return selected_item.value if selected_item else None


def confirm_action(message: str, default: bool = False) -> bool:
    """
    Muestra un diálogo de confirmación simple

    Args:
        message: Mensaje a mostrar
        default: Valor por defecto

    Returns:
        True si confirma, False si cancela
    """
    options = [MenuItem("Sí", True, "Confirmar la acción"), MenuItem("No", False, "Cancelar la acción")]

    result = show_dropdown_menu(title=message, items=options, show_descriptions=True, allow_cancel=True)

    return result.value if result else False


def show_info(message: str, title: str = "Información"):
    """Muestra un mensaje informativo"""
    print(f"\n{Fore.BLUE}{Style.BRIGHT}ℹ️  {title}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}{'─' * (len(title) + 3)}{Style.RESET_ALL}")
    print(f"{message}")


def show_success(message: str):
    """Muestra un mensaje de éxito"""
    print(f"\n{Fore.GREEN}✅ {message}{Style.RESET_ALL}")


def show_error(message: str):
    """Muestra un mensaje de error"""
    print(f"\n{Fore.RED}❌ {message}{Style.RESET_ALL}")


def show_warning(message: str):
    """Muestra un mensaje de advertencia"""
    print(f"\n{Fore.YELLOW}⚠️  {message}{Style.RESET_ALL}")
