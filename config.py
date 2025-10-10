"""
Configuración global de la aplicación
"""
import os
from pathlib import Path

# Rutas del proyecto
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
TEMPLATES_DIR = DATA_DIR / "templates"
OUTPUT_DIR = DATA_DIR / "output"
LOGS_DIR = DATA_DIR / "logs"

# Crear directorios si no existen
for directory in [DATA_DIR, TEMPLATES_DIR, OUTPUT_DIR, LOGS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Tallas válidas
VALID_SIZES = ["2", "4", "6", "8", "10", "12", "14", "16", 
               "XS", "S", "M", "L", "XL", "XXL", "XXXL"]

# Nombres de piezas estándar
PIECE_NAMES = {
    "DELANTERO": "front",
    "POSTERIOR": "back",
    "@MANGA DER": "sleeve_right",
    "@MANGA IZQ": "sleeve_left",
    "SESGO CUELLO": "collar_bias"
}

# Configuración del rollo de tejido (en mm)
ROLL_CONFIG = {
    "width": 1800,  # ancho del rollo en mm
    "height": 3000,  # alto del rollo en mm
    "margin": 10,    # margen entre piezas en mm
    "edge_margin": 20  # margen del borde del rollo en mm
}

# Configuración de nesting
NESTING_CONFIG = {
    "allowed_rotations": [0, 90, 180, 270],  # rotaciones permitidas en grados
    "spacing": 10,  # espacio mínimo entre piezas en mm
    "max_pieces_per_file": 50,  # máximo de prendas por archivo
    "optimization_level": "medium"  # low, medium, high
}

# Configuración de texto (nombres y números)
TEXT_CONFIG = {
    "font_name": "Arial",
    "font_size_number": 200,  # tamaño del número en puntos
    "font_size_name": 80,     # tamaño del nombre en puntos
    "number_position": (0.5, 0.35),  # posición relativa (x, y) en la pieza posterior
    "name_position": (0.5, 0.65),    # posición relativa (x, y) en la pieza posterior
    "color": "#000000"
}

# Configuración de exportación
EXPORT_CONFIG = {
    "format": "ai",  # formato de salida: ai, pdf, svg
    "dpi": 300,
    "color_mode": "RGB"
}

# Configuración de logs
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": LOGS_DIR / "app.log"
}

# Límites de optimización
OPTIMIZATION_LIMITS = {
    "min_group_size": 2,  # mínimo de tallas en un grupo
    "max_group_size": 4,  # máximo de tallas en un grupo
    "max_file_size_mb": 50,  # tamaño máximo del archivo en MB
    "target_efficiency": 0.75  # eficiencia objetivo del nesting (75%)
}