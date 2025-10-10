"""
Modelo de datos para pieza de prenda
"""
from dataclasses import dataclass, field
from typing import Optional, List, Tuple
import numpy as np

@dataclass
class Piece:
    """Representa una pieza vectorial de una prenda (delantero, manga, etc.)"""
    
    name: str  # DELANTERO, POSTERIOR, @MANGA DER, etc.
    size: str  # S, M, L, XL, etc.
    svg_path: str = ""  # Path SVG de la pieza
    width: float = 0.0  # Ancho en mm
    height: float = 0.0  # Alto en mm
    area: float = 0.0  # Área en mm²
    vertices: List[Tuple[float, float]] = field(default_factory=list)  # Vértices del polígono
    
    # Transformaciones
    rotation: float = 0.0  # Rotación en grados
    position: Tuple[float, float] = (0.0, 0.0)  # Posición (x, y) en mm
    
    # Metadata
    pdf_page: Optional[int] = None  # Página del PDF de origen
    normalized_name: Optional[str] = None  # Nombre normalizado
    
    def __post_init__(self):
        """Inicialización adicional"""
        if self.normalized_name is None:
            self.normalized_name = self._normalize_name()
    
    def _normalize_name(self) -> str:
        """Normaliza el nombre de la pieza"""
        name_map = {
            "DELANTERO": "front",
            "POSTERIOR": "back",
            "@MANGA DER": "sleeve_right",
            "@MANGA IZQ": "sleeve_left",
            "SESGO CUELLO": "collar_bias"
        }
        return name_map.get(self.name.upper(), self.name.lower().replace(" ", "_"))
    
    def calculate_area(self) -> float:
        """
        Calcula el área de la pieza usando la fórmula del área de polígono
        (Shoelace formula)
        """
        if not self.vertices or len(self.vertices) < 3:
            return self.width * self.height
        
        vertices = np.array(self.vertices)
        x = vertices[:, 0]
        y = vertices[:, 1]
        
        # Fórmula de Shoelace
        area = 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))
        self.area = area
        return area
    
    def calculate_bounding_box(self) -> Tuple[float, float, float, float]:
        """
        Calcula la caja delimitadora de la pieza
        
        Returns:
            tuple: (min_x, min_y, max_x, max_y)
        """
        if not self.vertices:
            return (0, 0, self.width, self.height)
        
        vertices = np.array(self.vertices)
        min_x, min_y = vertices.min(axis=0)
        max_x, max_y = vertices.max(axis=0)
        
        self.width = max_x - min_x
        self.height = max_y - min_y
        
        return (min_x, min_y, max_x, max_y)
    
    def rotate(self, angle: float):
        """
        Rota la pieza un ángulo dado
        
        Args:
            angle: Ángulo en grados
        """
        self.rotation = (self.rotation + angle) % 360
        
        # Si hay vértices, rotarlos
        if self.vertices:
            angle_rad = np.radians(angle)
            cos_a = np.cos(angle_rad)
            sin_a = np.sin(angle_rad)
            
            rotated = []
            for x, y in self.vertices:
                new_x = x * cos_a - y * sin_a
                new_y = x * sin_a + y * cos_a
                rotated.append((new_x, new_y))
            
            self.vertices = rotated
            self.calculate_bounding_box()
    
    def translate(self, dx: float, dy: float):
        """
        Traslada la pieza
        
        Args:
            dx: Desplazamiento en x
            dy: Desplazamiento en y
        """
        self.position = (self.position[0] + dx, self.position[1] + dy)
        
        if self.vertices:
            self.vertices = [(x + dx, y + dy) for x, y in self.vertices]
    
    def get_area_mm2(self) -> float:
        """Retorna el área en mm²"""
        if self.area == 0:
            self.calculate_area()
        return self.area
    
    def is_back_piece(self) -> bool:
        """Verifica si es la pieza posterior (donde va el nombre y número)"""
        return "POSTERIOR" in self.name.upper() or "BACK" in self.normalized_name.lower()
    
    def __repr__(self):
        return f"Piece(name='{self.name}', size='{self.size}', area={self.area:.2f}mm²)"