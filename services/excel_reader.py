"""
Servicio para lectura y parseo de archivos Excel con pedidos
"""
import pandas as pd
from typing import List, Dict, Tuple, Optional
from pathlib import Path
import re
from models import Player, Order

class ExcelReader:
    """Lee y procesa archivos Excel con pedidos de equipaciones"""
    
    def __init__(self, filepath: str):
        """
        Inicializa el lector
        
        Args:
            filepath: Ruta al archivo Excel
        """
        self.filepath = Path(filepath)
        self.df: Optional[pd.DataFrame] = None
        self.order: Optional[Order] = None
        
    def read_excel(self) -> pd.DataFrame:
        """
        Lee el archivo Excel
        
        Returns:
            DataFrame con los datos
        """
        try:
            # Intentar leer el Excel con openpyxl
            self.df = pd.read_excel(self.filepath, engine='openpyxl')
            return self.df
        except Exception as e:
            raise ValueError(f"Error al leer el archivo Excel: {e}")
    
    def parse_order(self) -> Order:
        """
        Parsea el Excel y crea un objeto Order
        
        Returns:
            Order con todos los jugadores
        """
        if self.df is None:
            self.read_excel()
        
        order = Order(name=self.filepath.stem)
        current_sponsor = ""
        
        # Recorrer todas las filas
        for idx, row in self.df.iterrows():
            # Detectar patrocinador (línea que empieza con "Patrocinador:")
            first_col = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else ""
            
            if first_col.startswith("Patrocinador:"):
                current_sponsor = first_col.replace("Patrocinador:", "").strip()
                continue
            
            # Detectar líneas de resumen (TOTAL, etc.) y saltarlas
            if first_col.upper() in ["TOTAL", "RESUMEN", "OTROS"]:
                break
            
            # Parsear jugador
            player = self._parse_player_row(row, current_sponsor)
            if player:
                order.add_player(player)
        
        self.order = order
        return order
    
    def _parse_player_row(self, row: pd.Series, sponsor: str) -> Optional[Player]:
        """
        Parsea una fila y extrae los datos del jugador
        
        Args:
            row: Fila del DataFrame
            sponsor: Patrocinador actual
            
        Returns:
            Player o None si no es una fila válida
        """
        # Estructura esperada: [Número] [Nombre] [Talla] o [Nombre] [Talla]
        values = [str(v).strip() for v in row if pd.notna(v) and str(v).strip()]
        
        if len(values) < 2:
            return None
        
        # Intentar extraer número y nombre de la primera columna
        first_col = values[0]
        
        # Patrón: "23 ENRÍQUEZ" o "7 GIL" o solo "PALOMA"
        match = re.match(r'^(\d+)\s+(.+)$', first_col)
        
        if match:
            number = match.group(1)
            name = match.group(2)
            size = values[1] if len(values) > 1 else ""
        else:
            # No hay número, solo nombre
            number = None
            name = first_col
            size = values[1] if len(values) > 1 else ""
        
        # Validar que la talla sea válida
        if not size or not self._is_valid_size(size):
            return None
        
        return Player(
            name=name,
            number=number,
            size=size,
            sponsor=sponsor
        )
    
    def _is_valid_size(self, size: str) -> bool:
        """
        Verifica si una talla es válida
        
        Args:
            size: Talla a validar
            
        Returns:
            bool
        """
        valid_sizes = ["2", "4", "6", "8", "10", "12", "14", "16", 
                      "XS", "S", "M", "L", "XL", "XXL", "XXXL"]
        return size.upper() in valid_sizes
    
    def get_size_summary(self) -> Dict[str, int]:
        """
        Obtiene resumen de tallas del pedido
        
        Returns:
            dict: {talla: cantidad}
        """
        if not self.order:
            self.parse_order()
        return self.order.get_size_summary()
    
    def get_sponsor_summary(self) -> Dict[str, int]:
        """
        Obtiene resumen por patrocinador
        
        Returns:
            dict: {patrocinador: cantidad}
        """
        if not self.order:
            self.parse_order()
        return self.order.get_sponsor_summary()
    
    def validate_order(self) -> Tuple[bool, List[str]]:
        """
        Valida el pedido completo
        
        Returns:
            tuple: (es_válido, lista_de_errores)
        """
        if not self.order:
            self.parse_order()
        
        errors = []
        
        # Verificar que hay jugadores
        if self.order.get_total_players() == 0:
            errors.append("No se encontraron jugadores en el Excel")
        
        # Verificar números duplicados
        has_duplicates, duplicate_list = self.order.validate_duplicate_numbers()
        if has_duplicates:
            errors.extend(duplicate_list)
        
        # Validar cada jugador
        from config import VALID_SIZES
        for player in self.order.players:
            is_valid, error_msg = player.validate(VALID_SIZES)
            if not is_valid:
                errors.append(f"Jugador {player.name}: {error_msg}")
        
        return len(errors) == 0, errors
    
    def export_summary(self) -> str:
        """
        Exporta un resumen del pedido en texto
        
        Returns:
            str con el resumen
        """
        if not self.order:
            self.parse_order()
        
        lines = [
            f"=== RESUMEN DEL PEDIDO: {self.order.name} ===\n",
            f"Total de equipaciones: {self.order.get_total_players()}\n",
            "\nRESUMEN POR TALLAS:",
        ]
        
        size_summary = self.get_size_summary()
        for size, count in sorted(size_summary.items()):
            lines.append(f"  {size}: {count} unidades")
        
        lines.append("\nRESUMEN POR PATROCINADORES:")
        sponsor_summary = self.get_sponsor_summary()
        for sponsor, count in sorted(sponsor_summary.items()):
            lines.append(f"  {sponsor}: {count} unidades")
        
        return "\n".join(lines)


# Función auxiliar para uso rápido
def read_order_from_excel(filepath: str) -> Order:
    """
    Función auxiliar para leer un pedido desde Excel
    
    Args:
        filepath: Ruta al archivo Excel
        
    Returns:
        Order con los datos parseados
    """
    reader = ExcelReader(filepath)
    return reader.parse_order()