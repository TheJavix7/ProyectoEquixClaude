# 🎯 Guía de Uso - Fase 1 Completada

## 📦 Estructura Creada

Has completado la estructura base del proyecto y la **Fase 1: Lectura y Parseo**. Aquí está todo lo que tienes:

### Archivos Principales

1. **config.py** - Configuración global del proyecto
2. **requirements.txt** - Dependencias de Python
3. **main.py** - Punto de entrada (interfaz vendrá en Fase 6)
4. **setup_project.py** - Script para crear la estructura
5. **test_phase1.py** - Script de pruebas para Fase 1

### Modelos de Datos (`models/`)

- **Player** - Representa un jugador con nombre, número y talla
- **Piece** - Representa una pieza vectorial (delantero, manga, etc.)
- **Garment** - Representa una prenda completa (conjunto de piezas)
- **Order** - Representa un pedido completo con múltiples jugadores

### Servicios (`services/`)

- **ExcelReader** - Lee archivos Excel con pedidos
- **PDFProcessor** - Procesa PDFs con patrones vectoriales
- **PDFPatternLoader** - Carga múltiples patrones de diferentes tallas

### Utilidades (`utils/`)

- **GarmentLogger** - Sistema de logging personalizado
- **validators** - Funciones de validación

---

## 🚀 Instalación Paso a Paso

### 1. Crear la estructura del proyecto

```bash
# Ejecutar el script de setup
python setup_project.py
```

Esto creará todos los directorios necesarios.

### 2. Crear entorno virtual

```bash
# Linux/Mac
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Preparar archivos de prueba

Necesitas colocar:

1. **Excel del pedido**: `1. Pedido 1 Equipaciones - Temp. 25-26.xlsx`
   - En el directorio raíz del proyecto

2. **PDFs de patrones**: `S.pdf`, `M.pdf`, `L.pdf`, etc.
   - En el directorio `data/templates/`
   - O en el directorio raíz para pruebas

---

## 🧪 Ejecutar Pruebas de la Fase 1

```bash
python test_phase1.py
```

Este script probará:

1. ✅ **Lectura de Excel**
   - Carga del archivo
   - Extracción de jugadores
   - Resumen por tallas
   - Resumen por patrocinadores
   - Validación de datos

2. ✅ **Procesamiento de PDFs**
   - Carga de patrones
   - Extracción de piezas vectoriales
   - Cálculo de áreas
   - Validación de completitud

3. ✅ **Integración**
   - Verificación de coincidencias entre tallas pedidas y patrones disponibles
   - Estadísticas completas

---

## 💻 Ejemplos de Uso Programático

### Ejemplo 1: Leer un pedido de Excel

```python
from services import ExcelReader

# Crear lector
reader = ExcelReader("1. Pedido 1 Equipaciones - Temp. 25-26.xlsx")

# Parsear pedido
order = reader.parse_order()

# Ver resumen
print(f"Total jugadores: {order.get_total_players()}")
print(f"Tallas: {order.get_size_summary()}")

# Validar
is_valid, errors = reader.validate_order()
if not is_valid:
    for error in errors:
        print(f"Error: {error}")
```

### Ejemplo 2: Procesar un PDF de patrón

```python
from services import PDFProcessor

# Cargar PDF
processor = PDFProcessor("S.pdf")
garment = processor.create_garment()

# Ver piezas
print(f"Talla: {garment.size}")
print(f"Piezas: {len(garment.pieces)}")

for piece in garment.pieces:
    print(f"- {piece.name}: {piece.get_area_mm2():.0f} mm²")

# Validar completitud
is_valid, msg = garment.validate()
print(f"Válido: {is_valid}")

processor.close()
```

### Ejemplo 3: Cargar múltiples patrones

```python
from services import PDFPatternLoader

# Cargar todos los patrones de un directorio
loader = PDFPatternLoader("data/templates/")
garments = loader.load_all_patterns()

# Ver tallas disponibles
print(f"Tallas disponibles: {loader.get_available_sizes()}")

# Obtener patrón de una talla específica
garment_m = loader.get_garment_by_size("M")
if garment_m:
    print(f"Patrón M tiene {len(garment_m.pieces)} piezas")
```

### Ejemplo 4: Integración completa

```python
from services import ExcelReader, PDFPatternLoader

# Leer pedido
reader = ExcelReader("pedido.xlsx")
order = reader.parse_order()

# Cargar patrones
loader = PDFPatternLoader("data/templates/")
garments = loader.load_all_patterns()

# Verificar cobertura
size_summary = order.get_size_summary()
available_sizes = loader.get_available_sizes()

for size, count in size_summary.items():
    if size in available_sizes:
        print(f"✅ Talla {size}: {count} unidades - Patrón disponible")
    else:
        print(f"❌ Talla {size}: {count} unidades - FALTA PATRÓN")
```

---

## 📊 Qué Datos Extraemos

### Del Excel:
- Nombre del jugador
- Número de dorsal
- Talla
- Patrocinador/Equipo
- Totales por talla
- Totales por patrocinador

### De los PDFs:
- Nombre de cada pieza (DELANTERO, POSTERIOR, etc.)
- Dimensiones (ancho × alto en mm)
- Área de cada pieza (mm²)
- Vértices del polígono (para nesting futuro)
- Talla del patrón

---

## ✅ Validaciones Implementadas

### Validación de Pedidos:
- Tallas válidas (S, M, L, XL, etc.)
- Nombres no vacíos
- Números no duplicados por equipo
- Datos completos

### Validación de Patrones:
- Todas las piezas necesarias presentes
- Dimensiones válidas
- Áreas calculables
- Coherencia de tallas

---

## 🔜 Próximos Pasos (Fase 2)

Una vez que las pruebas de Fase 1 funcionen correctamente, el siguiente paso será:

**Fase 2: Optimización de Agrupación**
- Crear algoritmo para agrupar tallas en pares/tríos/cuartetos
- Minimizar número de archivos generados
- Optimizar uso de espacio en cada rollo

Archivos a crear:
- `services/grouping_optimizer.py`
- `tests/test_grouping.py`

---

## 🐛 Solución de Problemas

### Error: "No module named 'PyQt6'"
```bash
pip install PyQt6
```

### Error: "No module named 'fitz'"
```bash
pip install PyMuPDF
```

### Error: "No se encuentra el archivo Excel"
Asegúrate de que el archivo esté en el directorio correcto con el nombre exacto.

### Error: "PDF vacío o sin piezas"
Verifica que el PDF contenga vectores y texto con los nombres de las piezas.

---

## 📝 Notas Importantes

1. Los archivos PDF deben contener:
   - Texto con "Piece Name: NOMBRE_PIEZA"
   - Vectores dibujados (no imágenes rasterizadas)
   - Una pieza por página

2. El archivo Excel debe seguir el formato:
   - Líneas "Patrocinador: NOMBRE"
   - Columnas: Número+Nombre | Talla
   - Línea "TOTAL" para finalizar

3. Los logs se guardan en `data/logs/`

4. Los archivos generados irán a `data/output/`

---

## 🎓 Arquitectura del Código

### Patrón MVC
- **Models**: Datos puros (Player, Piece, Garment, Order)
- **Services**: Lógica de negocio (lectura, procesamiento)
- **Views**: Interfaz (Fase 6)
- **Controllers**: Orquestación (Fases 2-5)
- **Utils**: Herramientas transversales (logging, validación)

### Flujo de Datos
```
Excel → ExcelReader → Order (con Players)
PDFs → PDFProcessor → Garments (con Pieces)
Order + Garments → Grouping → Grupos optimizados (Fase 2)
Grupos → Nesting → Layout en rollos (Fase 4)
Layout → AI Generator → Archivos .ai (Fase 5)
```

---

## 📚 Referencia Rápida de Clases

### Player
```python
player = Player(
    name="FIGUEROA",
    number="6",
    size="L",
    sponsor="Pagancar"
)

# Métodos útiles
player.get_full_identifier()  # "6 FIGUEROA"
player.validate(VALID_SIZES)  # (True, "")
```

### Piece
```python
piece = Piece(
    name="POSTERIOR",
    size="M",
    width=350.0,
    height=450.0
)

# Métodos útiles
piece.calculate_area()        # Calcula área en mm²
piece.is_back_piece()         # True si es posterior
piece.rotate(90)              # Rota la pieza
piece.translate(100, 50)      # Mueve la pieza
```

### Garment
```python
garment = Garment(size="M")
garment.add_piece(piece)

# Métodos útiles
garment.get_back_piece()      # Obtiene pieza posterior
garment.get_total_area()      # Área total de todas las piezas
garment.is_complete()         # Verifica si tiene todas las piezas
garment.validate()            # (True, "")
```

### Order
```python
order = Order(name="Temporada 25-26")
order.add_player(player)

# Métodos útiles
order.get_size_summary()              # {'M': 10, 'L': 5}
order.get_players_by_size("M")        # [player1, player2, ...]
order.validate_duplicate_numbers()    # (False, [])
order.get_statistics()                # Dict completo
```

---

## 🔧 Configuración Personalizada

El archivo `config.py` contiene todas las configuraciones modificables:

### Dimensiones del Rollo
```python
ROLL_CONFIG = {
    "width": 1800,      # ancho en mm
    "height": 3000,     # alto en mm
    "margin": 10,       # margen entre piezas
    "edge_margin": 20   # margen del borde
}
```

### Configuración de Nesting (Fase 4)
```python
NESTING_CONFIG = {
    "allowed_rotations": [0, 90, 180, 270],
    "spacing": 10,
    "max_pieces_per_file": 50,
    "optimization_level": "medium"
}
```

### Configuración de Texto
```python
TEXT_CONFIG = {
    "font_name": "Arial",
    "font_size_number": 200,
    "font_size_name": 80,
    "number_position": (0.5, 0.35),
    "name_position": (0.5, 0.65),
    "color": "#000000"
}
```

---

## 🎨 Personalización

### Añadir nuevas tallas válidas
Editar `config.py`:
```python
VALID_SIZES = ["2", "4", "6", "8", "10", "12", "14", "16", 
               "XS", "S", "M", "L", "XL", "XXL", "XXXL",
               "CUSTOM1", "CUSTOM2"]  # Añadir aquí
```

### Añadir nuevos nombres de piezas
Editar `config.py`:
```python
PIECE_NAMES = {
    "DELANTERO": "front",
    "POSTERIOR": "back",
    "@MANGA DER": "sleeve_right",
    "@MANGA IZQ": "sleeve_left",
    "SESGO CUELLO": "collar_bias",
    "CAPUCHA": "hood"  # Añadir aquí
}
```

---

## 📈 Métricas y Estadísticas

### Información disponible del pedido:
- Total de equipaciones
- Distribución por tallas
- Distribución por patrocinadores/equipos
- Números duplicados
- Jugadores por categoría

### Información disponible de patrones:
- Área de cada pieza
- Área total por prenda
- Dimensiones (ancho × alto)
- Número de vértices
- Completitud del patrón

---

## 🧩 Extensibilidad

El código está diseñado para ser fácilmente extensible:

### Añadir nuevo formato de entrada (CSV, JSON, etc.)
Crear nuevo servicio en `services/`:
```python
class CSVReader:
    def parse_order(self) -> Order:
        # Implementar lógica
        pass
```

### Añadir nuevo formato de salida (DXF, SVG, etc.)
Crear generador en `services/`:
```python
class DXFGenerator:
    def generate(self, garments):
        # Implementar lógica
        pass
```

### Añadir nuevas validaciones
Añadir en `utils/validators.py`:
```python
def validate_custom_field(value) -> Tuple[bool, str]:
    # Implementar validación
    return True, ""
```

---

## 🔍 Debugging

### Activar logs detallados
En tu código:
```python
from utils.logger import GarmentLogger

logger = GarmentLogger("mi_modulo")
logger.debug("Mensaje de debug detallado")
logger.info("Operación completada")
logger.error("Error encontrado", exc_info=True)
```

### Ver logs en archivo
Los logs se guardan en `data/logs/garment_YYYYMMDD.log`

### Modo verbose en pruebas
Modificar `test_phase1.py` para más detalles:
```python
# Añadir prints adicionales donde sea necesario
print(f"Debug: {variable}")
```

---

## 📦 Estructura de Archivos Generados (Futuro)

```
data/output/
├── pedido_temporada_25-26/
│   ├── 01_M-L_VICTOR-FIGUEROA.ai
│   ├── 02_M-L_ITALO-LOPEZ.ai
│   ├── 03_S_IVAN-RUBEN.ai
│   ├── index.csv                    # Índice de archivos
│   └── resumen.txt                  # Resumen del pedido
```

Cada archivo `.ai` contendrá:
- Múltiples prendas (según agrupación)
- Nombres y números personalizados
- Layout optimizado (nesting)
- Metadata del pedido

---

## 🚦 Checklist de Fase 1

Antes de continuar a la Fase 2, verifica:

- [ ] ✅ `setup_project.py` ejecutado correctamente
- [ ] ✅ Entorno virtual creado y activado
- [ ] ✅ Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] ✅ Archivos de prueba ubicados correctamente
- [ ] ✅ `test_phase1.py` ejecutado sin errores
- [ ] ✅ Excel parseado correctamente
- [ ] ✅ PDFs procesados correctamente
- [ ] ✅ Validaciones funcionando
- [ ] ✅ Logs generados en `data/logs/`
- [ ] ✅ Todas las tallas del pedido tienen patrones disponibles

---

## 💡 Tips y Buenas Prácticas

1. **Siempre validar antes de procesar**
   ```python
   is_valid, errors = reader.validate_order()
   if not is_valid:
       # Manejar errores antes de continuar
   ```

2. **Usar context managers para PDFs**
   ```python
   with PDFProcessor("pattern.pdf") as processor:
       garment = processor.create_garment()
   # PDF se cierra automáticamente
   ```

3. **Cachear resultados pesados**
   ```python
   # Guardar garments cargados para reutilizar
   self.cached_garments = loader.load_all_patterns()
   ```

4. **Logging en operaciones importantes**
   ```python
   logger.info(f"Procesando pedido con {order.get_total_players()} jugadores")
   ```

5. **Manejar excepciones específicas**
   ```python
   try:
       order = reader.parse_order()
   except ValueError as e:
       logger.error(f"Error de validación: {e}")
   except Exception as e:
       logger.error(f"Error inesperado: {e}", exc_info=True)
   ```

---

## 🎯 Objetivos de la Fase 2

Una vez completada la Fase 1, los objetivos de la Fase 2 serán:

1. **Algoritmo de Agrupación Inteligente**
   - Agrupar tallas con la misma cantidad
   - Minimizar el número de archivos finales
   - Maximizar la eficiencia del espacio

2. **Calculador de Multiplicación**
   - Determinar repeticiones necesarias
   - Distribuir prendas entre archivos

3. **Optimizador de Combinaciones**
   - Encontrar mejores pares/tríos/cuartetos
   - Balance entre cantidad de archivos y tamaño

**Ejemplo de agrupación óptima:**
```
Pedido: 15×M, 15×L, 10×S, 5×XL

Agrupación óptima:
- Grupo 1: (M+L) × 15 repeticiones = 15M + 15L ✓
- Grupo 2: (S+S) × 5 repeticiones = 10S ✓
- Grupo 3: XL × 5 repeticiones = 5XL ✓

Total: 3 archivos en lugar de 45
```

---

## 📞 Soporte y Ayuda

Si encuentras problemas:

1. Revisa los logs en `data/logs/`
2. Ejecuta `test_phase1.py` para diagnóstico
3. Verifica la estructura de archivos
4. Comprueba las versiones de dependencias
5. Revisa esta guía completa

---

## 🎉 ¡Felicidades!

Has completado exitosamente la **Fase 1** del proyecto. Tienes:

✅ Estructura completa del proyecto
✅ Modelos de datos robustos
✅ Lector de Excel funcional
✅ Procesador de PDFs funcional
✅ Sistema de validación
✅ Sistema de logging
✅ Tests automatizados

**¡Estás listo para la Fase 2!** 🚀