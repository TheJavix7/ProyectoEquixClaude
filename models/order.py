"""
Modelo de datos para pedido completo
"""
from dataclasses import dataclass, field
from typing import List, Dict
from collections import defaultdict
from .player import Player
from .garment import Garment

@dataclass
class Order:
    """Representa un pedido completo de equipaciones"""
    
    name: str = ""
    players: List[Player] = field(default_factory=list)
    garments: List[Garment] = field(default_factory=list)
    
    def add_player(self, player: Player):
        """Añade un jugador al pedido"""
        self.players.append(player)
    
    def add_garment(self, garment: Garment):
        """Añade una prenda al pedido"""
        self.garments.append(garment)
    
    def get_size_summary(self) -> Dict[str, int]:
        """
        Obtiene resumen de cantidades por talla
        
        Returns:
            dict: {talla: cantidad}
        """
        summary = defaultdict(int)
        for player in self.players:
            summary[player.size] += 1
        return dict(summary)
    
    def get_sponsor_summary(self) -> Dict[str, int]:
        """
        Obtiene resumen de cantidades por patrocinador
        
        Returns:
            dict: {patrocinador: cantidad}
        """
        summary = defaultdict(int)
        for player in self.players:
            sponsor = player.sponsor or "SIN PATROCINADOR"
            summary[sponsor] += 1
        return dict(summary)
    
    def get_players_by_size(self, size: str) -> List[Player]:
        """
        Obtiene todos los jugadores de una talla específica
        
        Args:
            size: Talla a buscar
            
        Returns:
            Lista de jugadores
        """
        return [p for p in self.players if p.size == size]
    
    def get_players_by_sponsor(self, sponsor: str) -> List[Player]:
        """
        Obtiene todos los jugadores de un patrocinador
        
        Args:
            sponsor: Nombre del patrocinador
            
        Returns:
            Lista de jugadores
        """
        return [p for p in self.players if p.sponsor == sponsor]
    
    def get_total_players(self) -> int:
        """Obtiene el total de jugadores"""
        return len(self.players)
    
    def get_available_sizes(self) -> List[str]:
        """Obtiene lista de tallas disponibles en el pedido"""
        return sorted(list(set(p.size for p in self.players)))
    
    def validate_duplicate_numbers(self) -> tuple[bool, List[str]]:
        """
        Verifica si hay números duplicados por equipo/patrocinador
        
        Returns:
            tuple: (hay_duplicados, lista_de_duplicados)
        """
        duplicates = []
        by_sponsor = defaultdict(list)
        
        for player in self.players:
            if player.number:
                key = player.sponsor or "SIN PATROCINADOR"
                by_sponsor[key].append((player.number, player.name))
        
        for sponsor, numbers in by_sponsor.items():
            seen = {}
            for num, name in numbers:
                if num in seen:
                    duplicates.append(f"{sponsor}: número {num} duplicado ({seen[num]} y {name})")
                else:
                    seen[num] = name
        
        return len(duplicates) > 0, duplicates
    
    def get_statistics(self) -> Dict[str, any]:
        """
        Obtiene estadísticas del pedido
        
        Returns:
            dict con estadísticas
        """
        return {
            "total_players": self.get_total_players(),
            "size_summary": self.get_size_summary(),
            "sponsor_summary": self.get_sponsor_summary(),
            "available_sizes": self.get_available_sizes(),
            "total_garments": len(self.garments)
        }
    
    def __repr__(self):
        return f"Order(name='{self.name}', players={len(self.players)}, garments={len(self.garments)})"