"""
Modelo de datos para prenda completa
"""
from dataclasses import dataclass, field
from typing import List, Optional
from models.piece import Piece
from models.player import Player

@dataclass
class Garment:
    """Representa una prenda completa (conjunto de piezas)"""
    
    size: str
    pieces: List[Piece] = field(default_factory=list)
    player: Optional[Player] = None
    
    def add_piece(self, piece: Piece):
        """Añade una pieza a la prenda"""
        if piece.size != self.size:
            raise ValueError(f"La talla de la pieza ({piece.size}) no coincide con la prenda ({self.size})")
        self.pieces.append(piece)
    
    def get_piece_by_name(self, name: str) -> Optional[Piece]:
        """
        Obtiene una pieza por su nombre
        
        Args:
            name: Nombre de la pieza (DELANTERO, POSTERIOR, etc.)
            
        Returns:
            Piece o None si no existe
        """
        for piece in self.pieces:
            if piece.name.upper() == name.upper() or piece.normalized_name == name.lower():
                return piece
        return None
    
    def get_back_piece(self) -> Optional[Piece]:
        """Obtiene la pieza posterior (donde va nombre y número)"""
        for piece in self.pieces:
            if piece.is_back_piece():
                return piece
        return None
    
    def get_total_area(self) -> float:
        """Calcula el área total de todas las piezas"""
        return sum(piece.get_area_mm2() for piece in self.pieces)
    
    def get_bounding_box(self) -> tuple[float, float]:
        """
        Calcula la caja delimitadora que contiene todas las piezas
        
        Returns:
            tuple: (width, height) en mm
        """
        if not self.pieces:
            return (0, 0)
        
        max_width = max(piece.width for piece in self.pieces)
        total_height = sum(piece.height for piece in self.pieces)
        
        return (max_width, total_height)
    
    def is_complete(self) -> bool:
        """Verifica si la prenda tiene todas las piezas necesarias"""
        required_pieces = ["DELANTERO", "POSTERIOR", "@MANGA DER", "@MANGA IZQ"]
        piece_names = [p.name.upper() for p in self.pieces]
        
        return all(req in piece_names for req in required_pieces)
    
    def has_player(self) -> bool:
        """Verifica si la prenda tiene un jugador asignado"""
        return self.player is not None
    
    def get_identifier(self) -> str:
        """Obtiene identificador único de la prenda"""
        if self.player:
            return f"{self.size}_{self.player.get_full_identifier()}"
        return f"{self.size}_sin_asignar"
    
    def validate(self) -> tuple[bool, str]:
        """
        Valida la prenda
        
        Returns:
            tuple: (es_válida, mensaje_error)
        """
        if not self.pieces:
            return False, "La prenda no tiene piezas"
        
        if not all(piece.size == self.size for piece in self.pieces):
            return False, "No todas las piezas tienen la misma talla"
        
        if not self.is_complete():
            return False, f"Faltan piezas. Tiene: {[p.name for p in self.pieces]}"
        
        return True, ""
    
    def __repr__(self):
        player_info = f" - {self.player.name}" if self.player else ""
        return f"Garment(size='{self.size}', pieces={len(self.pieces)}{player_info})"