"""
Script para leer el Excel de equipaciones y convertirlo a objetos Player y Order
"""
import pandas as pd
from pathlib import Path
from models.player import Player
from models.order import Order


def dividir_por_equipos(df):
    """
    Divide el DataFrame en equipos según los encabezados 'Equipo:'
    
    Args:
        df: DataFrame con todos los datos
        
    Returns:
        Lista de diccionarios con información de cada equipo
    """
    equipos = []
    indice_inicio = None
    nombre_equipo = None
    patrocinador = None

    for idx, row in df.iterrows():
        # Detectar si es una fila de encabezado de equipo
        primera_celda = str(row.iloc[0])

        if primera_celda.startswith('Equipo:'):
            # Si ya teníamos un equipo anterior, guardarlo
            if indice_inicio is not None:
                equipo_df = df.iloc[indice_inicio:idx].copy()
                equipos.append({
                    'nombre': nombre_equipo,
                    'patrocinador': patrocinador,
                    'datos': limpiar_equipo(equipo_df)
                })

            # Extraer información del nuevo equipo
            nombre_equipo = primera_celda.replace('Equipo:', '').strip()
            patrocinador = str(row.iloc[1]).replace('Patrocinador:', '').strip()
            indice_inicio = idx + 1  # Siguiente fila será el encabezado

    # Agregar el último equipo
    if indice_inicio is not None:
        equipo_df = df.iloc[indice_inicio:].copy()
        equipos.append({
            'nombre': nombre_equipo,
            'patrocinador': patrocinador,
            'datos': limpiar_equipo(equipo_df)
        })

    return equipos


def limpiar_equipo(equipo_df):
    """
    Limpia los datos de un equipo y establece los encabezados correctos
    
    Args:
        equipo_df: DataFrame con datos del equipo
        
    Returns:
        DataFrame limpio con encabezados
    """
    # Eliminar filas vacías
    equipo_df = equipo_df.dropna(how='all')

    # La primera fila son los encabezados
    if len(equipo_df) > 0:
        encabezados = equipo_df.iloc[0].values
        datos = equipo_df.iloc[1:].copy()
        datos.columns = encabezados
        datos = datos.reset_index(drop=True)
        return datos

    return pd.DataFrame()


def convertir_equipos_a_order(equipos_data, nombre_pedido="Pedido Equipaciones"):
    """
    Convierte los datos de equipos a un objeto Order con Players
    
    Args:
        equipos_data: Lista de diccionarios con datos de equipos
        nombre_pedido: Nombre del pedido
        
    Returns:
        Order con todos los jugadores
    """
    order = Order(name=nombre_pedido)
    
    for equipo in equipos_data:
        nombre_equipo = equipo['nombre']
        patrocinador = equipo['patrocinador']
        datos_jugadores = equipo['datos']
        
        # Iterar sobre cada jugador del equipo
        for idx, row in datos_jugadores.iterrows():
            try:
                # Extraer datos según los nombres de columnas
                # Ajustar según los nombres reales de las columnas en tu Excel
                
                # Opción 1: Si la columna se llama 'Nombre jugador' y 'Talla'
                if 'Nombre jugador' in datos_jugadores.columns:
                    nombre = row['Nombre jugador']
                    numero = row['Numero']
                    talla = str(row['Talla']).strip().upper() if pd.notna(row['Talla']) else ""
                
                # Opción 2: Si las columnas son diferentes (ajustar según tu Excel)
                elif 'Jugador' in datos_jugadores.columns:
                    nombre = row['Nombre jugador']
                    numero = row['Numero']
                    talla = str(row['Talla']).strip().upper() if 'Talla' in datos_jugadores.columns and pd.notna(row['Talla']) else ""
                
                # Opción 3: Usar índices de columnas si no tienen nombre
                else:
                    # Primera columna: Jugador, Segunda columna: Talla
                    nombre = row['Nombre jugador']
                    numero = row['Numero']
                    talla = str(row.iloc[1]).strip().upper() if len(row) > 1 and pd.notna(row.iloc[1]) else ""
                
                # Validar que tengamos al menos nombre y talla
                if nombre and talla:
                    player = Player(
                        name=nombre,
                        number=numero,
                        size=talla,
                        sponsor=patrocinador,
                        team=nombre_equipo
                    )
                    order.add_player(player)
                    
            except Exception as e:
                print(f"⚠️  Error al procesar jugador en {nombre_equipo}: {e}")
                continue
    
    return order


def mostrar_resumen_pedido(order: Order):
    """
    Muestra por pantalla un resumen completo del pedido
    
    Args:
        order: Objeto Order con los datos del pedido
    """
    print("\n" + "=" * 80)
    print(f"📋 PEDIDO: {order.name}")
    print("=" * 80)
    
    print(f"\n✅ Total de jugadores: {order.get_total_players()}")
    
    # Resumen por tallas
    print("\n📊 RESUMEN POR TALLAS:")
    print("-" * 40)
    size_summary = order.get_size_summary()
    for size in size_summary.keys():
        count = size_summary[size]
        print(f"   {size:5s}: {count:3d} unidades")
    
    # Resumen por equipos/patrocinadores
    print("\n🏢 RESUMEN POR EQUIPOS:")
    print("-" * 40)
    sponsor_summary = order.get_sponsor_summary()
    for sponsor in sorted(sponsor_summary.keys()):
        count = sponsor_summary[sponsor]
        print(f"   {sponsor:40s}: {count:3d} jugadores")
    
    # Validar números duplicados
    print("\n🔍 VALIDACIÓN DE NÚMEROS:")
    print("-" * 40)
    has_duplicates, duplicate_list = order.validate_duplicate_numbers()
    if has_duplicates:
        print("   ⚠️  Se encontraron números duplicados:")
        for dup in duplicate_list:
            print(f"      - {dup}")
    else:
        print("   ✅ No hay números duplicados")
    
    print("\n" + "=" * 80)


def mostrar_jugadores_detallado(order: Order, max_jugadores=None):
    """
    Muestra todos los jugadores del pedido con sus datos completos
    
    Args:
        order: Objeto Order con los datos del pedido
        max_jugadores: Número máximo de jugadores a mostrar (None = todos)
    """
    print("\n" + "=" * 80)
    print("👥 LISTADO DETALLADO DE JUGADORES")
    print("=" * 80)
    
    jugadores_a_mostrar = order.players[:max_jugadores] if max_jugadores else order.players
    
    for idx, player in enumerate(jugadores_a_mostrar, 1):
        numero_str = f"#{player.number:3s}" if player.number else "  ---"
        print(f"\n[{idx:3d}] {numero_str} | {player.name:25s} | Talla: {player.size:4s}")
        print(f"       Equipo: {player.team:30s} | Patrocinador: {player.sponsor}")
    
    if max_jugadores and len(order.players) > max_jugadores:
        restantes = len(order.players) - max_jugadores
        print(f"\n... y {restantes} jugadores más")
    
    print("\n" + "=" * 80)


def mostrar_jugadores_por_equipo(order: Order):
    """
    Muestra los jugadores agrupados por equipo
    
    Args:
        order: Objeto Order con los datos del pedido
    """
    print("\n" + "=" * 80)
    print("🏀 JUGADORES AGRUPADOS POR EQUIPO")
    print("=" * 80)
    
    sponsor_summary = order.get_sponsor_summary()
    
    for sponsor in sorted(sponsor_summary.keys()):
        jugadores_equipo = order.get_players_by_sponsor(sponsor)
        
        print(f"\n📌 {sponsor} ({len(jugadores_equipo)} jugadores)")
        print("-" * 60)
        
        for player in jugadores_equipo:
            numero_str = f"#{player.number}" if player.number else "---"
            print(f"   {numero_str:5s} {player.name:25s} Talla: {player.size}")
    
    print("\n" + "=" * 80)


def main():
    """Función principal"""
    # Ruta al archivo Excel
    excel_path = Path("equipaciones_interactivo_final_v2.xlsm")
    
    if not excel_path.exists():
        print(f"❌ Error: No se encuentra el archivo {excel_path}")
        print("   Coloca el archivo en el directorio actual o ajusta la ruta")
        return
    
    print("📂 Leyendo archivo Excel...")
    
    # Leer Excel (ajustar parámetros según tu archivo)
    df = pd.read_excel(
        excel_path,
        sheet_name='Equipaciones',
        usecols=[0, 1, 2],  # Ajustar columnas según tu Excel
        skiprows=4,          # Ajustar filas a saltar según tu Excel
        header=None
    )
    
    print("✅ Archivo leído correctamente")
    
    # Dividir por equipos
    print("\n🔄 Procesando equipos...")
    equipos_data = dividir_por_equipos(df)
    print(f"✅ Se encontraron {len(equipos_data)} equipos")
    
    # Convertir a Order
    print("\n🔄 Convirtiendo a objetos Player y Order...")
    order = convertir_equipos_a_order(equipos_data, nombre_pedido="Temporada 2024-25")
    print(f"✅ Se crearon {order.get_total_players()} jugadores")
    
    # Mostrar resultados
    mostrar_resumen_pedido(order)
    
    # Mostrar jugadores detallado (primeros 10)
    mostrar_jugadores_detallado(order, max_jugadores=10)
    
    # Mostrar jugadores por equipo
    mostrar_jugadores_por_equipo(order)
    
    # Acceder a un jugador específico (ejemplo)
    print("\n" + "=" * 80)
    print("🎯 EJEMPLO: ACCEDER A DATOS ESPECÍFICOS")
    print("=" * 80)
    
    if order.players:
        primer_jugador = order.players[0]
        print(f"\nPrimer jugador del pedido:")
        print(f"   Nombre: {primer_jugador.name}")
        print(f"   Número: {primer_jugador.number}")
        print(f"   Talla: {primer_jugador.size}")
        print(f"   Equipo: {primer_jugador.team}")
        print(f"   Patrocinador: {primer_jugador.sponsor}")
        print(f"   Identificador completo: {primer_jugador.get_full_identifier()}")
    
    # Buscar jugadores de una talla específica
    talla_buscar = "M"
    jugadores_m = order.get_players_by_size(talla_buscar)
    print(f"\n\nJugadores con talla {talla_buscar}: {len(jugadores_m)}")
    for player in jugadores_m[:5]:  # Mostrar solo los primeros 5
        print(f"   - {player.get_full_identifier()} ({player.team})")
    
    print("\n" + "=" * 80)
    print("✅ PROCESO COMPLETADO")
    print("=" * 80)
    
    return order


if __name__ == "__main__":
    order = main()