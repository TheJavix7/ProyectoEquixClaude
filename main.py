"""
Punto de entrada principal de la aplicación
Generador de Equipaciones Deportivas
"""
import sys
from pathlib import Path

# Añadir directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from PyQt6.QtWidgets import QApplication
from config import LOGGING_CONFIG
import logging

# Configurar logging
logging.basicConfig(
    level=LOGGING_CONFIG["level"],
    format=LOGGING_CONFIG["format"],
    handlers=[
        logging.FileHandler(LOGGING_CONFIG["file"]),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def main():
    """Función principal de la aplicación"""
    logger.info("Iniciando aplicación Generador de Equipaciones")
    
    try:
        # Crear aplicación PyQt6
        app = QApplication(sys.argv)
        app.setApplicationName("Generador de Equipaciones")
        app.setOrganizationName("SportWear")
        
        # Importar ventana principal (se implementará en Fase 6)
        # from views.main_window import MainWindow
        # window = MainWindow()
        # window.show()
        
        # Por ahora, mostrar mensaje de fase de desarrollo
        from PyQt6.QtWidgets import QMessageBox, QWidget
        
        widget = QWidget()
        QMessageBox.information(
            widget,
            "Generador de Equipaciones",
            "🚧 Aplicación en desarrollo\n\n"
            "Fase 1 completada: Lectura de Excel y PDFs\n\n"
            "Para probar la Fase 1, ejecuta:\n"
            "python test_phase1.py\n\n"
            "La interfaz gráfica estará disponible en la Fase 6."
        )
        
        logger.info("Aplicación cerrada por el usuario")
        return 0
        
        # Cuando la interfaz esté lista, usar esto:
        # sys.exit(app.exec())
        
    except Exception as e:
        logger.error(f"Error crítico en la aplicación: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())