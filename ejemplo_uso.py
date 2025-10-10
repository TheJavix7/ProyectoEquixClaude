"""
Ejemplo de uso básico del sistema
"""
from services import ExcelReader, PDFPatternLoader

def ejemplo_basico():
    # 1. Leer pedido de Excel
    print("1. Leyendo pedido...")
    reader = ExcelReader("1. Pedido 1 Equipaciones - Temp. 25-26.xlsx")
    order = reader.parse_order()
    
    print(f"   Total jugadores: {order.get_total_players()}")
    print(f"   Tallas: {order.get_size_summary()}")
    
    # 2. Cargar patrones
    print("\n2. Cargando patrones...")
    loader = PDFPatternLoader("data/templates/")
    garments = loader.load_all_patterns()
    
    print(f"   Patrones cargados: {loader.get_available_sizes()}")
    
    # 3. Verificar coincidencias
    print("\n3. Verificando coincidencias...")
    size_summary = order.get_size_summary()
    available_sizes = loader.get_available_sizes()
    
    for size, count in size_summary.items():
        if size in available_sizes:
            print(f"   ✓ {size}: {count} unidades - Patrón OK")
        else:
            print(f"   ✗ {size}: {count} unidades - FALTA PATRÓN")

if __name__ == "__main__":
    ejemplo_basico()
