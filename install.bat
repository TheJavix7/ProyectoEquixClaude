@echo off
chcp 65001 >nul
color 0A

echo ╔════════════════════════════════════════════════════════════╗
echo ║   INSTALACIÓN: GENERADOR DE EQUIPACIONES DEPORTIVAS       ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Verificar Python
echo Verificando instalación de Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no está instalado
    echo Por favor, instala Python 3.10 o superior desde python.org
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Python %PYTHON_VERSION% encontrado
echo.

REM Verificar pip
echo Verificando pip...
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] pip no está instalado
    echo Instalando pip...
    python -m ensurepip --upgrade
)
echo [OK] pip encontrado
echo.

REM Crear estructura del proyecto
echo Creando estructura del proyecto...
python setup_project.py
if %errorlevel% neq 0 (
    echo [ERROR] Error al crear la estructura
    pause
    exit /b 1
)
echo [OK] Estructura creada
echo.

REM Crear entorno virtual
echo Creando entorno virtual...
python -m venv venv
if %errorlevel% neq 0 (
    echo [ERROR] Error al crear entorno virtual
    pause
    exit /b 1
)
echo [OK] Entorno virtual creado
echo.

REM Activar entorno virtual
echo Activando entorno virtual...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [ERROR] Error al activar entorno virtual
    pause
    exit /b 1
)
echo [OK] Entorno virtual activado
echo.

REM Actualizar pip
echo Actualizando pip...
python -m pip install --upgrade pip >nul 2>&1
echo [OK] pip actualizado
echo.

REM Instalar dependencias
echo Instalando dependencias...
echo Esto puede tardar unos minutos...
echo.

python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [WARNING] Algunos paquetes no se instalaron correctamente
    echo Intenta ejecutar manualmente: pip install -r requirements.txt
) else (
    echo [OK] Dependencias instaladas
)
echo.

REM Verificar instalación
echo Verificando instalación...
python -c "import PyQt6" 2>nul && echo [OK] PyQt6 instalado || echo [ERROR] PyQt6 NO instalado
python -c "import pandas" 2>nul && echo [OK] pandas instalado || echo [ERROR] pandas NO instalado
python -c "import openpyxl" 2>nul && echo [OK] openpyxl instalado || echo [ERROR] openpyxl NO instalado
python -c "import fitz" 2>nul && echo [OK] PyMuPDF instalado || echo [ERROR] PyMuPDF NO instalado
python -c "import svgwrite" 2>nul && echo [OK] svgwrite instalado || echo [ERROR] svgwrite NO instalado
python -c "import shapely" 2>nul && echo [OK] shapely instalado || echo [ERROR] shapely NO instalado
python -c "import numpy" 2>nul && echo [OK] numpy instalado || echo [ERROR] numpy NO instalado
python -c "import reportlab" 2>nul && echo [OK] reportlab instalado || echo [ERROR] reportlab NO instalado
echo.

REM Crear archivo de ejemplo
echo Creando archivo de ejemplo...
(
echo """
echo Ejemplo de uso básico del sistema
echo """
echo from services import ExcelReader, PDFPatternLoader
echo.
echo def ejemplo_basico^(^):
echo     # 1. Leer pedido de Excel
echo     print^("1. Leyendo pedido..."^)
echo     reader = ExcelReader^("1. Pedido 1 Equipaciones - Temp. 25-26.xlsx"^)
echo     order = reader.parse_order^(^)
echo.    
echo     print^(f"   Total jugadores: {order.get_total_players^(^)}"^)
echo     print^(f"   Tallas: {order.get_size_summary^(^)}"^)
echo.    
echo     # 2. Cargar patrones
echo     print^("\n2. Cargando patrones..."^)
echo     loader = PDFPatternLoader^("data/templates/"^)
echo     garments = loader.load_all_patterns^(^)
echo.    
echo     print^(f"   Patrones cargados: {loader.get_available_sizes^(^)}"^)
echo.    
echo     # 3. Verificar coincidencias
echo     print^("\n3. Verificando coincidencias..."^)
echo     size_summary = order.get_size_summary^(^)
echo     available_sizes = loader.get_available_sizes^(^)
echo.    
echo     for size, count in size_summary.items^(^):
echo         if size in available_sizes:
echo             print^(f"   ✓ {size}: {count} unidades - Patrón OK"^)
echo         else:
echo             print^(f"   ✗ {size}: {count} unidades - FALTA PATRÓN"^)
echo.
echo if __name__ == "__main__":
echo     ejemplo_basico^(^)
) > ejemplo_uso.py

echo [OK] Archivo ejemplo_uso.py creado
echo.

REM Resumen
echo ╔════════════════════════════════════════════════════════════╗
echo ║                   INSTALACIÓN COMPLETA                     ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo [INFO] PRÓXIMOS PASOS:
echo.
echo   1. Coloca los archivos de prueba:
echo      - 1. Pedido 1 Equipaciones - Temp. 25-26.xlsx ^(raíz del proyecto^)
echo      - S.pdf, M.pdf, L.pdf, etc. ^(en data/templates/^)
echo.
echo   2. Activa el entorno virtual:
echo      venv\Scripts\activate
echo.
echo   3. Ejecuta las pruebas de Fase 1:
echo      python test_phase1.py
echo.
echo   4. O prueba el ejemplo:
echo      python ejemplo_uso.py
echo.
echo [INFO] Para más información, consulta README.md
echo.
pause