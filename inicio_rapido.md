# 🚀 Inicio Rápido - Generador de Equipaciones

## ⚡ Instalación Rápida (5 minutos)

### Opción 1: Instalación Automática

**Linux/Mac:**
```bash
chmod +x install.sh
./install.sh
```

**Windows:**
```batch
install.bat
```

### Opción 2: Instalación Manual

```bash
# 1. Crear estructura
python setup_project.py

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 4. Instalar dependencias
pip install -r requirements.txt
```

---

## 📁 Archivos que Debes Crear/Copiar

Crea estos archivos en tu proyecto siguiendo los artefactos proporcionados:

### 1. **Configuración Base**
- `config.py` ✅
- `requirements.txt` ✅
- `setup_project.py` ✅

### 2. **Modelos** (carpeta `models/`)
- `__init__.py` ✅
- `player.py` ✅
- `piece.py` ✅
- `garment.py` ✅
- `order.py` ✅

### 3. **Servicios** (carpeta `services/`)
- `__init__.py` ✅
- `excel_reader.py` ✅
- `pdf_processor.py` ✅

### 4. **Utilidades** (carpeta `utils/`)
- `__init__.py` ✅
- `logger.py` ✅
- `validators.py` ✅

### 5. **Scripts de Prueba**
- `main.py` ✅
- `test_phase1.py` ✅

### 6. **Scripts de Instalación**
- `install.sh` (Linux/Mac) ✅
- `install.bat` (Windows) ✅

---

## 📦 Archivos de Datos Necesarios

Coloca estos archivos en tu proyecto:

1. **Excel de Pedido:**
   - Nombre: `1. Pedido 1 Equipaciones - Temp. 25-26.xlsx`
   - Ubicación: Raíz del proyecto
   - Contenido: Tabla con jugadores, números y tallas

2. **PDFs de Patrones:**
   - Nombres: `S.pdf`, `M.pdf`, `L.pdf`, `XL.pdf`, etc.
   - Ubicación: `data/templates/` (o raíz para pruebas)
   - Contenido: Vectores de piezas de prendas

---

## ✅ Checklist Pre-Ejecución

Antes de ejecutar las pruebas, verifica:

- [ ] Python 3.10+ instalado
- [ ] Todos los archivos de código creados
- [ ] Estructura de carpetas creada (`python setup_project.py`)
- [ ] Entorno virtual creado y activado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Excel de pedido en su lugar
- [ ] PDFs de patrones en `data/templates/`

---

## 🧪 Primera Prueba

```bash
# Activar entorno virtual
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Ejecutar pruebas
python test_phase1.py
```

### Salida Esperada:

```
🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀
PRUEBAS DE LA FASE 1: LECTURA Y PARSEO
🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀

============================================================
PRUEBA 1: LECTURA DE EXCEL
============================================================

📄 Leyendo archivo Excel...

✅ Pedido cargado exitosamente!
   Total de jugadores: 101

📊 RESUMEN POR TALLAS:
   M    :  45 unidades
   L    :  25 unidades
   XL   :  15 unidades
   S    :  10 unidades
   XXL  :   6 unidades

🏢 RESUMEN POR PATROCINADORES:
   Pagancar                                :  10 unidades
   ACG                                     :  10 unidades
   Cl. Fisioterapia Ignacio Martínez      :   8 unidades
   ...

🔍 VALIDANDO PEDIDO...
   ✅ Pedido válido, sin errores

============================================================
PRUEBA 2: PROCESAMIENTO DE PDFs
============================================================

📂 Buscando archivos PDF de patrones...
   ✓ S.pdf encontrado
   ✓ M.pdf encontrado
   ✓ L.pdf encontrado

📄 Cargando patrones desde PDFs...

✅ PDF 'S.pdf' procesado:
   Talla: S
   Piezas encontradas: 5

   📏 DETALLE DE PIEZAS:
      - DELANTERO         : 350.0mm x 450.0mm (área: 157500 mm²)
      - POSTERIOR         : 350.0mm x 450.0mm (área: 157500 mm²)
      - @MANGA DER        : 200.0mm x 300.0mm (área: 60000 mm²)
      - @MANGA IZQ        : 200.0mm x 300.0mm (área: 60000 mm²)
      - SESGO CUELLO      : 100.0mm x 50.0mm (área: 5000 mm²)

   ✅ Patrón completo

============================================================
PRUEBA 3: INTEGRACIÓN EXCEL + PDFs
============================================================

📊 Tallas en el pedido: ['M', 'L', 'XL', 'S', 'XXL']
📁 Tallas con patrones disponibles: ['L', 'M', 'S']

🔍 VERIFICANDO COINCIDENCIAS:
   ✅ Talla M    :  45 unidades → Patrón disponible
   ✅ Talla L    :  25 unidades → Patrón disponible
   ❌ Talla XL   :  15 unidades → ⚠️  FALTA PATRÓN
   ✅ Talla S    :  10 unidades → Patrón disponible
   ❌ Talla XXL  :   6 unidades → ⚠️  FALTA PATRÓN

⚠️  ATENCIÓN: Faltan patrones para las tallas: ['XL', 'XXL']
   Debes proporcionar los archivos PDF para estas tallas

📈 ESTADÍSTICAS FINALES:
   Total de equipaciones: 101
   Tallas diferentes: 5
   Patrones cargados: 3
   Cobertura: 60.0%

============================================================
✅ PRUEBAS COMPLETADAS
============================================================
```

---

## 🎯 Casos de Uso Rápidos

### Uso 1: Leer un Pedido

```python
from services import ExcelReader

reader = ExcelReader("pedido.xlsx")
order = reader.parse_order()

print(f"Total: {order.get_total_players()}")
print(f"Tallas: {order.get_size_summary()}")
```

### Uso 2: Procesar un Patrón

```python
from services import PDFProcessor

with PDFProcessor("M.pdf") as processor:
    garment = processor.create_garment()
    print(f"Talla: {garment.size}")
    print(f"Piezas: {len(garment.pieces)}")
```

### Uso 3: Verificar Cobertura

```python
from services import ExcelReader, PDFPatternLoader

# Leer pedido
reader = ExcelReader("pedido.xlsx")
order = reader.parse_order()

# Cargar patrones
loader = PDFPatternLoader("data/templates/")
garments = loader.load_all_patterns()

# Verificar
for size, count in order.get_size_summary().items():
    has_pattern = size in loader.get_available_sizes()
    status = "✓" if has_pattern else "✗"
    print(f"{status} Talla {size}: {count} unidades")
```

---

## 🔧 Solución de Problemas Comunes

### Error: "No module named 'PyQt6'"
```bash
pip install PyQt6
```

### Error: "No module named 'fitz'"
```bash
pip install PyMuPDF
```

### Error: Excel no se encuentra
- Verifica que el archivo esté en el directorio correcto
- Verifica el nombre exacto (incluyendo espacios)
- Usa ruta absoluta si es necesario

### Error: PDF vacío
- Verifica que el PDF contenga vectores (no imágenes)
- Asegúrate de que tenga texto "Piece Name: ..."
- Abre el PDF en Illustrator para verificar contenido

### Error: Tallas no válidas
- Revisa `config.py` → `VALID_SIZES`
- Añade las tallas personalizadas que necesites

### Error: ImportError
```bash
# Reinstalar todas las dependencias
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

---

## 📊 Estructura de Datos

### Excel Esperado:
```
| Patrocinador: Pagancar |     |
|------------------------|-----|
| 6 FIGUEROA            | L   |
| 1 VELÁZQUEZ           | XL  |
| 23 ENRÍQUEZ           | XL  |
| ...                   | ... |
| Patrocinador: ACG     |     |
| 7 GIL                 | M   |
| ...                   | ... |
```

### PDF Esperado:
```
Página 1:
- Texto: "Piece Name: @MANGA DER"
- Texto: "Size: M"
- Vectores: Contorno de la manga

Página 2:
- Texto: "Piece Name: @MANGA IZQ"
- Texto: "Size: M"
- Vectores: Contorno de la manga

Página 3:
- Texto: "Piece Name: DELANTERO"
...
```

---

## 📈 Métricas de Éxito

Después de ejecutar `test_phase1.py`, deberías ver:

✅ **Excel:**
- Total de jugadores leído correctamente
- Resumen por tallas correcto
- Sin errores de validación

✅ **PDFs:**
- Todas las piezas extraídas (mínimo 4-5 por talla)
- Áreas calculadas correctamente
- Patrones completos

✅ **Integración:**
- Cobertura 100% (todas las tallas tienen patrón)
- Estadísticas coherentes

---

## 🔄 Flujo de Trabajo Típico

```
1. Recibir pedido del cliente (Excel)
   ↓
2. Cargar Excel en la aplicación
   ↓
3. Validar pedido (números, tallas, datos)
   ↓
4. Cargar patrones PDF correspondientes
   ↓
5. Verificar cobertura de tallas
   ↓
6. [FASE 2] Optimizar agrupación
   ↓
7. [FASE 3] Añadir nombres/números
   ↓
8. [FASE 4] Aplicar nesting
   ↓
9. [FASE 5] Generar archivos .ai
   ↓
10. Enviar a impresión
```

---

## 📚 Documentación por Módulo

### config.py
Configuración global: dimensiones, tallas válidas, límites, etc.

### models/
Clases de datos: Player, Piece, Garment, Order

### services/
Lógica de negocio: ExcelReader, PDFProcessor, PDFPatternLoader

### utils/
Herramientas: GarmentLogger, validators

---

## 🎓 Conceptos Clave

### Player
Representa una persona que recibirá equipación:
- name: Nombre del jugador
- number: Dorsal
- size: Talla (S, M, L, etc.)
- sponsor: Patrocinador/equipo

### Piece
Pieza vectorial de una prenda:
- name: DELANTERO, POSTERIOR, @MANGA DER, etc.
- size: Talla de la pieza
- width/height: Dimensiones en mm
- area: Área en mm²
- vertices: Puntos del polígono

### Garment
Prenda completa (conjunto de piezas):
- size: Talla
- pieces: Lista de Piece
- player: Player asignado (opcional)

### Order
Pedido completo:
- name: Nombre del pedido
- players: Lista de Player
- garments: Lista de Garment

---

## 🚀 Comandos Rápidos

```bash
# Activar entorno
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows

# Ejecutar pruebas
python test_phase1.py

# Ejecutar aplicación (GUI en Fase 6)
python main.py

# Ejemplo de uso
python ejemplo_uso.py

# Ver logs
cat data/logs/garment_*.log    # Linux/Mac
type data\logs\garment_*.log   # Windows

# Desactivar entorno
deactivate
```

---

## 📞 Siguientes Pasos

Una vez que `test_phase1.py` funcione correctamente:

1. ✅ **Fase 1 Completada** - Lectura y Parseo
2. 🔜 **Fase 2** - Algoritmo de Agrupación
3. 🔜 **Fase 3** - Personalización (nombres/números)
4. 🔜 **Fase 4** - Motor de Nesting
5. 🔜 **Fase 5** - Generación de .ai
6. 🔜 **Fase 6** - Interfaz PyQt6

---

## 💡 Tips Finales

1. **Siempre valida antes de procesar**
2. **Revisa los logs en caso de error**
3. **Usa context managers para PDFs**
4. **Cachea resultados pesados**
5. **Mantén los archivos de datos organizados**

---

## 🎉 ¡Listo para Empezar!

Si has llegado hasta aquí, tienes todo lo necesario para comenzar.

**Orden de creación de archivos:**
1. Crea todos los archivos de código
2. Ejecuta `python setup_project.py`
3. Ejecuta el script de instalación (`install.sh` o `install.bat`)
4. Coloca los archivos de datos
5. Ejecuta `python test_phase1.py`

**¿Todo funciona?** ¡Excelente! Estás listo para la Fase 2.

**¿Tienes errores?** Revisa:
- Logs en `data/logs/`
- Esta guía de solución de problemas
- Versiones de dependencias en `requirements.txt`

---

## 📖 Referencias

- **Documentación PyQt6**: https://doc.qt.io/qtforpython/
- **Documentación pandas**: https://pandas.pydata.org/docs/
- **Documentación PyMuPDF**: https://pymupdf.readthedocs.io/
- **Documentación shapely**: https://shapely.readthedocs.io/

---

**¡Mucha suerte con tu proyecto! 🚀**