import pandas as pd
from pathlib import Path

def dividir_por_equipos(df):
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


def main():
    excel_path = Path("equipaciones_interactivo_final_v2.xlsm")
    df = pd.read_excel(excel_path, sheet_name='Equipaciones',
                       usecols=[0, 1, 2], skiprows=4, header=None)

    equipos = dividir_por_equipos(df)

    # Mostrar resultados
    for equipo in equipos:
        print(f"\n{'=' * 50}")
        print(f"Equipo: {equipo['nombre']}")
        print(f"Patrocinador: {equipo['patrocinador']}")
        print(f"\nJugadores:")
        print(equipo['datos'])
        print(f"Total jugadores: {len(equipo['datos'])}")

    print(f"\n{'=' * 50}")
    print(f"\n{'=' * 50}")
    archivel = equipos[1]
    print(archivel)

    print(f"\n{'=' * 50}")
    print(archivel['datos'])
    print(f"\n{'=' * 50}")

    datosArchivel = archivel['datos']
    print(datosArchivel.iloc[0]['Talla'])

    print("\n--------ANGEEEL--------\n")
    for i, jugadores in archivel['datos'].iloc[:].iterrows():
        print(archivel['datos'].iloc[i])

    print("\n--------\n")

    jugadorFelipe = archivel['datos'].iloc[0]
    print(jugadorFelipe['Nombre jugador'])


if __name__ == "__main__":
    main()