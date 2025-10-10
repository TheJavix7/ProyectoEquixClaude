"""
Modelo de datos para jugador/cliente
"""
from dataclasses import dataclass
from typing import Optional

@dataclass
class Player:
    """Representa un jugador o persona que recibe una equipación"""
    
    name: str
    number: Optional[str]  # Puede ser número o texto
    size: str
    sponsor: str = ""
    team: str = ""
    
    def __post_init__(self):
        """Validación después de inicialización"""
        # Normalizar talla
        self.size = self.size.strip().upper()
        
        # Normalizar nombre
        self.name = self.name.strip()
        
        # Convertir número a string si es necesario
        if self.number is not None:
            self.number = str(self.number).strip()
    
    def get_full_identifier(self) -> str:
        """Retorna identificador completo del jugador"""
        if self.number:
            return f"{self.number} {self.name}"
        return self.name
    
    def validate(self, valid_sizes: list[str]) -> tuple[bool, str]:
        """
        Valida los datos del jugador
        
        Args:
            valid_sizes: Lista de tallas válidas
            
        Returns:
            tuple: (es_válido, mensaje_error)
        """
        if not self.name:
            return False, "El nombre no puede estar vacío"
        
        if self.size not in valid_sizes:
            return False, f"Talla '{self.size}' no es válida. Tallas válidas: {', '.join(valid_sizes)}"
        
        return True, ""
    
    def __repr__(self):
        return f"Player(name='{self.name}', number='{self.number}', size='{self.size}')"
    
    def __hash__(self):
        """Permite usar Player en sets"""
        return hash((self.name, self.number, self.size))