import sys
import os
from typing import List, Any, Optional, Callable
from colorama import Fore, Back, Style, init

init(autoreset=True)

try:
    from getch import getch
    GETCH_AVAILABLE = True
except ImportError:
    GETCH_AVAILABLE = False


class MenuItem:
    def __init__(self, text: str, value: Any = None, description: str = ""):
        self.text = text
        self.value = value if value is not None else text
        self.description = description


def wait_for_key():
    """Espera a que se presione una tecla y devuelve el código de la tecla"""
    if not GETCH_AVAILABLE:
        # Fallback si getch no está disponible
        response = input(f"\n{Fore.CYAN}Usa números o ENTER: {Style.RESET_ALL}").strip()
        if response.isdigit():
            return f"digit_{response}"
        return 'enter'
    
    try:
        key = getch()
        
        # Detectar secuencias de escape para teclas de flecha
        if key == '\x1b':  # ESC
            try:
                key2 = getch()
                if key2 == '[':
                    key3 = getch()
                    if key3 == 'A':
                        return 'up'
                    elif key3 == 'B':
                        return 'down'
                    elif key3 == 'C':
                        return 'right'
                    elif key3 == 'D':
                        return 'left'
                return 'esc'
            except:
                return 'esc'
        elif key == '\r' or key == '\n':
            return 'enter'
        elif key == 'q' or key == 'Q':
            return 'q'
        elif key.isdigit():
            return f"digit_{key}"
        else:
            return 'other'
            
    except Exception:
        # Fallback final
        return 'enter'


def clear_lines(num_lines: int):
    """Limpia un número específico de líneas hacia arriba"""
    for _ in range(num_lines):
        print('\033[1A\033[2K', end='')  # Mover hacia arriba y limpiar línea


def show_dropdown_menu(
    title: str,
    items: List[MenuItem],
    selected_index: int = 0,
    show_numbers: bool = False,
    show_descriptions: bool = True,
    allow_cancel: bool = True
) -> Optional[MenuItem]:
    """
    Muestra un menú desplegable interactivo
    
    Args:
        title: Título del menú
        items: Lista de elementos MenuItem
        selected_index: Índice inicial seleccionado
        show_numbers: Mostrar números de opción
        show_descriptions: Mostrar descripciones de items
        allow_cancel: Permitir cancelar con ESC/Q
        
    Returns:
        MenuItem seleccionado o None si se canceló
    """
    if not items:
        return None
    
    current_index = max(0, min(selected_index, len(items) - 1))
    
    while True:
        # Limpiar pantalla parcialmente si es necesario
        if 'lines_printed' in locals():
            clear_lines(lines_printed)
        
        lines_printed = 0
        
        # Mostrar título
        print(f"\n{Fore.CYAN}{Style.BRIGHT}{title}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * len(title)}{Style.RESET_ALL}")
        lines_printed += 2
        
        # Mostrar instrucciones
        if GETCH_AVAILABLE:
            instructions = f"{Fore.YELLOW}↑↓ Navegar | ENTER Seleccionar | 1-9 Directo"
        else:
            instructions = f"{Fore.YELLOW}Números para seleccionar | ENTER para confirmar"
        
        if allow_cancel:
            instructions += f" | Q Cancelar"
        print(instructions + Style.RESET_ALL)
        lines_printed += 1
        
        print()  # Línea en blanco
        lines_printed += 1
        
        # Mostrar items
        for i, item in enumerate(items):
            prefix = f"{i + 1}. " if len(items) <= 9 else f"{i + 1:2d}. "
            
            if i == current_index:
                # Item activo/seleccionado (resaltado)
                line = f"{Back.BLUE}{Fore.WHITE}▶ {prefix}{item.text[:45]:<47}{Style.RESET_ALL}"
            else:
                # Item normal
                line = f"  {prefix}{item.text[:45]}"
            
            print(line)
            lines_printed += 1
            
            # Mostrar descripción del item activo
            if show_descriptions and i == current_index and item.description:
                desc_line = f"   {Fore.YELLOW}💡 {item.description}{Style.RESET_ALL}"
                print(desc_line)
                lines_printed += 1
        
        # Obtener input del usuario
        key = wait_for_key()
        
        if not key:  # Si no se capturó tecla válida, continuar
            continue
            
        if key == 'up':
            current_index = (current_index - 1) % len(items)
        elif key == 'down':
            current_index = (current_index + 1) % len(items)
        elif key == 'enter':
            # Solo ENTER selecciona el item
            return items[current_index]
        elif key.startswith('digit_'):
            # Selección por número como alternativa
            digit = key.split('_')[1]
            try:
                num = int(digit)
                if 1 <= num <= len(items):
                    return items[num - 1]
            except ValueError:
                pass
        elif key in ['q', 'esc'] and allow_cancel:
            return None
        # Ignorar cualquier otra tecla y continuar navegando


def select_from_list(
    title: str,
    items: List[Any],
    display_func: Callable[[Any], str] = str,
    value_func: Callable[[Any], Any] = lambda x: x,
    description_func: Optional[Callable[[Any], str]] = None,
    allow_cancel: bool = True,
    show_numbers: bool = False
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
        allow_cancel=allow_cancel
    )
    
    return selected_item.value if selected_item else None


def confirm_action(message: str, default: bool = False) -> bool:
    """
    Muestra un diálogo de confirmación con navegación por flechas
    
    Args:
        message: Mensaje a mostrar
        default: Valor por defecto
        
    Returns:
        True si confirma, False si cancela
    """
    options = [
        MenuItem("Sí", True, "Confirmar la acción"),
        MenuItem("No", False, "Cancelar la acción")
    ]
    
    initial_index = 0 if default else 1
    
    result = show_dropdown_menu(
        title=message,
        items=options,
        selected_index=initial_index,
        show_descriptions=True,
        allow_cancel=True
    )
    
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