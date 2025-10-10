"""
Validadores para diferentes tipos de datos
"""
from pathlib import Path
from typing import Tuple, List
from config import VALID_SIZES

def validate_size(size: str) -> Tuple[bool, str]:
    """
    Valida que una talla sea válida
    
    Args:
        size: Talla a validar
        
    Returns:
        tuple: (es_válida, mensaje_error)
    """
    if not size:
        return False, "La talla no puede estar vacía"
    
    normalized_size = size.strip().upper()
    
    if normalized_size not in VALID_SIZES:
        return False, f"Talla '{size}' no válida. Tallas válidas: {', '.join(VALID_SIZES)}"
    
    return True, ""


def validate_player_number(number: str, allow_empty: bool = True) -> Tuple[bool, str]:
    """
    Valida el número de un jugador
    
    Args:
        number: Número a validar
        allow_empty: Si se permite número vacío
        
    Returns:
        tuple: (es_válido, mensaje_error)
    """
    if not number or number.strip() == "":
        if allow_empty:
            return True, ""
        return False, "El número no puede estar vacío"
    
    # Permitir números y texto (ej: "23", "00", "A")
    if len(number.strip()) > 3:
        return False, "El número no puede tener más de 3 caracteres"
    
    return True, ""


def validate_player_name(name: str) -> Tuple[bool, str]:
    """
    Valida el nombre de un jugador
    
    Args:
        name: Nombre a validar
        
    Returns:
        tuple: (es_válido, mensaje_error)
    """
    if not name or name.strip() == "":
        return False, "El nombre no puede estar vacío"
    
    if len(name.strip()) < 2:
        return False, "El nombre debe tener al menos 2 caracteres"
    
    if len(name) > 50:
        return False, "El nombre no puede tener más de 50 caracteres"
    
    return True, ""


def validate_file_path(filepath: str, extension: str = None) -> Tuple[bool, str]:
    """
    Valida que un archivo exista y tenga la extensión correcta
    
    Args:
        filepath: Ruta al archivo
        extension: Extensión requerida (ej: '.pdf', '.xlsx')
        
    Returns:
        tuple: (es_válido, mensaje_error)
    """
    path = Path(filepath)
    
    if not path.exists():
        return False, f"El archivo '{filepath}' no existe"
    
    if not path.is_file():
        return False, f"'{filepath}' no es un archivo"
    
    if extension and path.suffix.lower() != extension.lower():
        return False, f"El archivo debe tener extensión {extension}"
    
    return True, ""


def validate_directory_path(dirpath: str, create_if_missing: bool = False) -> Tuple[bool, str]:
    """
    Valida que un directorio exista
    
    Args:
        dirpath: Ruta al directorio
        create_if_missing: Crear el directorio si no existe
        
    Returns:
        tuple: (es_válido, mensaje_error)
    """
    path = Path(dirpath)
    
    if not path.exists():
        if create_if_missing:
            try:
                path.mkdir(parents=True, exist_ok=True)
                return True, ""
            except Exception as e:
                return False, f"No se pudo crear el directorio: {e}"
        return False, f"El directorio '{dirpath}' no existe"
    
    if not path.is_dir():
        return False, f"'{dirpath}' no es un directorio"
    
    return True, ""


def validate_dimensions(width: float, height: float, min_val: float = 0) -> Tuple[bool, str]:
    """
    Valida dimensiones
    
    Args:
        width: Ancho
        height: Alto
        min_val: Valor mínimo permitido
        
    Returns:
        tuple: (es_válido, mensaje_error)
    """
    if width <= min_val:
        return False, f"El ancho debe ser mayor que {min_val}"
    
    if height <= min_val:
        return False, f"El alto debe ser mayor que {min_val}"
    
    return True, ""


def validate_positive_number(value: float, name: str = "valor") -> Tuple[bool, str]:
    """
    Valida que un número sea positivo
    
    Args:
        value: Valor a validar
        name: Nombre del valor (para mensajes de error)
        
    Returns:
        tuple: (es_válido, mensaje_error)
    """
    if value <= 0:
        return False, f"El {name} debe ser positivo"
    
    return True, ""


def validate_percentage(value: float, name: str = "porcentaje") -> Tuple[bool, str]:
    """
    Valida que un valor esté entre 0 y 1 (porcentaje)
    
    Args:
        value: Valor a validar (0.0 - 1.0)
        name: Nombre del valor
        
    Returns:
        tuple: (es_válido, mensaje_error)
    """
    if value < 0 or value > 1:
        return False, f"El {name} debe estar entre 0 y 1"
    
    return True, ""