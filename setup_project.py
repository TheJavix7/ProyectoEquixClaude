"""
Script para crear la estructura de directorios del proyecto
"""
import os
from pathlib import Path

def create_directory_structure():
    """Crea toda la estructura de directorios del proyecto"""
    
    # Directorio base
    base_dir = Path.cwd()
    
    # Estructura de directorios
    directories = [
        "controllers",
        "models",
        "services",
        "views",
        "views/components",
        "utils",
        "tests",
        "data",
        "data/templates",
        "data/output",
        "data/logs"
    ]
    
    print("🏗️  Creando estructura de directorios...")
    
    for directory in directories:
        dir_path = base_dir / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"   ✓ {directory}/")
        
        # Crear __init__.py en directorios de código Python
        if directory in ["controllers", "models", "services", "views", "views/components", "utils", "tests"]:
            init_file = dir_path / "__init__.py"
            if not init_file.exists():
                init_file.write_text('"""\n' + directory.replace("/", ".") + '\n"""\n')
    
    print("\n✅ Estructura de directorios creada exitosamente!")


def create_readme():
    """Crea un archivo README.md básico"""
    
    readme_content = """# Generador de Equipaciones Deportivas

Sistema automatizado para la generación de archivos de impresión de equipaciones deportivas personalizadas.

## 📋 Requisitos

- Python 3.10+
- PyQt6
- pandas
- PyMuPDF
- Ver `requirements.txt` para lista completa

## 🚀 Instalación

1. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\\Scripts\\activate
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## 📂 Estructura del Proyecto

```
garment_generator/
├── main.py                 # Punto de entrada
├── config.py              # Configuración global
├── controllers/           # Controladores
├── models/               # Modelos de datos
├── services/             # Servicios (Excel, PDF, etc.)
├── views/                # Interfaz PyQt6
├── utils/                # Utilidades
├── tests/                # Pruebas
└── data/                 # Datos
    ├── templates/        # PDFs de patrones
    ├── output/           # Archivos generados
    └── logs/             # Logs
```

## 🧪 Pruebas de la Fase 1

Para probar la lectura de Excel y PDFs:

```bash
python test_phase1.py
```

## 📝 Uso

1. Colocar el archivo Excel con el pedido en el directorio raíz
2. Colocar los archivos PDF de patrones (S.pdf, M.pdf, L.pdf, etc.) en `data/templates/`
3. Ejecutar la aplicación:

```bash
python main.py
```

## 🔄 Fases del Desarrollo

- [x] **Fase 1**: Lectura de Excel y PDFs
- [ ] **Fase 2**: Optimización de agrupación
- [ ] **Fase 3**: Personalización (nombres y números)
- [ ] **Fase 4**: Motor de nesting
- [ ] **Fase 5**: Generación de archivos .ai
- [ ] **Fase 6**: Interfaz PyQt6

## 📄 Licencia

Proyecto privado - Todos los derechos reservados
"""
    
    readme_path = Path("README.md")
    readme_path.write_text(readme_content)
    print("\n📝 README.md creado")


def create_gitignore():
    """Crea archivo .gitignore"""
    
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# IDEs
.vscode/
.idea/
*.swp
*.swo

# Datos
data/output/*
!data/output/.gitkeep
data/logs/*
!data/logs/.gitkeep
*.xlsx
*.xls

# PDFs temporales
*.pdf
!data/templates/*.pdf

# Sistema
.DS_Store
Thumbs.db

# Archivos generados
*.ai
*.svg
"""
    
    gitignore_path = Path(".gitignore")
    gitignore_path.write_text(gitignore_content)
    print("📝 .gitignore creado")


def create_gitkeep_files():
    """Crea archivos .gitkeep en directorios vacíos"""
    
    dirs = ["data/output", "data/logs"]
    
    for dir_path in dirs:
        gitkeep = Path(dir_path) / ".gitkeep"
        gitkeep.touch()
    
    print("📝 Archivos .gitkeep creados")


def main():
    """Función principal"""
    print("\n" + "=" * 60)
    print("🎨 CONFIGURACIÓN INICIAL DEL PROYECTO")
    print("=" * 60 + "\n")
    
    create_directory_structure()
    #create_readme()
    create_gitignore()
    create_gitkeep_files()
    
    print("\n" + "=" * 60)
    print("✅ PROYECTO CONFIGURADO EXITOSAMENTE")
    print("=" * 60)
    
    print("\n📋 PRÓXIMOS PASOS:\n")
    print("1. Crear entorno virtual:")
    print("   python -m venv venv")
    print("\n2. Activar entorno virtual:")
    print("   source venv/bin/activate  (Linux/Mac)")
    print("   venv\\Scripts\\activate     (Windows)")
    print("\n3. Instalar dependencias:")
    print("   pip install -r requirements.txt")
    print("\n4. Colocar archivos de prueba:")
    print("   - Excel: 1. Pedido 1 Equipaciones - Temp. 25-26.xlsx")
    print("   - PDFs: S.pdf, M.pdf, L.pdf en data/templates/")
    print("\n5. Ejecutar pruebas de Fase 1:")
    print("   python test_phase1.py")
    print("\n")


if __name__ == "__main__":
    main()