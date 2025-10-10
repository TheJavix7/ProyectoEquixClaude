"""
Sistema de logging personalizado para la aplicación
"""
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional
from config import LOGS_DIR

class GarmentLogger:
    """Logger personalizado para el sistema"""
    
    def __init__(self, name: str, log_file: Optional[str] = None):
        """
        Inicializa el logger
        
        Args:
            name: Nombre del logger
            log_file: Archivo de log personalizado (opcional)
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Evitar duplicación de handlers
        if not self.logger.handlers:
            # Handler de archivo
            if log_file:
                file_path = LOGS_DIR / log_file
            else:
                timestamp = datetime.now().strftime("%Y%m%d")
                file_path = LOGS_DIR / f"garment_{timestamp}.log"
            
            file_handler = logging.FileHandler(file_path, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            
            # Handler de consola
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            # Formato
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
    
    def debug(self, message: str):
        """Log debug"""
        self.logger.debug(message)
    
    def info(self, message: str):
        """Log info"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Log warning"""
        self.logger.warning(message)
    
    def error(self, message: str, exc_info=False):
        """Log error"""
        self.logger.error(message, exc_info=exc_info)
    
    def critical(self, message: str, exc_info=False):
        """Log critical"""
        self.logger.critical(message, exc_info=exc_info)
    
    def log_operation(self, operation: str, status: str, details: str = ""):
        """
        Log de operación con formato estándar
        
        Args:
            operation: Nombre de la operación
            status: Estado (SUCCESS, ERROR, WARNING)
            details: Detalles adicionales
        """
        message = f"[{operation}] {status}"
        if details:
            message += f" - {details}"
        
        if status == "ERROR":
            self.error(message)
        elif status == "WARNING":
            self.warning(message)
        else:
            self.info(message)


# Logger global de la aplicación
app_logger = GarmentLogger("garment_app")