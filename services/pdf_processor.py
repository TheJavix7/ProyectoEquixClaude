"""
Servicio para procesamiento de archivos PDF con patrones de prendas
"""
import fitz  # PyMuPDF
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import re
from models import Piece, Garment

class PDFProcessor:
    """Procesa archivos PDF con patrones vectoriales de prendas"""
    
    def __init__(self, pdf_path: str):
        """
        Inicializa el procesador
        
        Args:
            pdf_path: Ruta al archivo PDF
        """
        self.pdf_path = Path(pdf_path)
        self.doc: Optional[fitz.Document] = None
        self.size: Optional[str] = None
        self.pieces: List[Piece] = []
        
        # Extraer talla del nombre del archivo (ej: "S.pdf" -> "S")
        self._extract_size_from_filename()
    
    def _extract_size_from_filename(self):
        """Extrae la talla del nombre del archivo"""
        # Buscar patrón de talla en el nombre del archivo
        filename = self.pdf_path.stem  # nombre sin extensión
        
        # Tallas posibles
        size_patterns = [
            r'\b(XXXL|XXL|XL|L|M|S|XS)\b',  # Tallas de letras
            r'\b(2|4|6|8|10|12|14|16)\b'     # Tallas numéricas
        ]
        
        for pattern in size_patterns:
            match = re.search(pattern, filename, re.IGNORECASE)
            if match:
                self.size = match.group(1).upper()
                return
        
        # Si no se encuentra, usar el nombre completo
        self.size = filename.upper()
    
    def load_pdf(self) -> fitz.Document:
        """
        Carga el archivo PDF
        
        Returns:
            Documento PDF
        """
        try:
            self.doc = fitz.open(self.pdf_path)
            return self.doc
        except Exception as e:
            raise ValueError(f"Error al cargar PDF {self.pdf_path}: {e}")
    
    def extract_pieces(self) -> List[Piece]:
        """
        Extrae todas las piezas del PDF
        
        Returns:
            Lista de piezas extraídas
        """
        if self.doc is None:
            self.load_pdf()
        
        pieces = []
        
        # Recorrer todas las páginas
        for page_num in range(len(self.doc)):
            page = self.doc[page_num]
            
            # Extraer texto para identificar el nombre de la pieza
            text = page.get_text()
            piece_name = self._extract_piece_name(text)
            
            # Extraer información vectorial
            piece = self._extract_piece_from_page(page, page_num, piece_name)
            
            if piece:
                pieces.append(piece)
        
        self.pieces = pieces
        return pieces
    
    def _extract_piece_name(self, text: str) -> str:
        """
        Extrae el nombre de la pieza del texto
        
        Args:
            text: Texto de la página
            
        Returns:
            Nombre de la pieza
        """
        # Buscar patrones como "Piece Name: DELANTERO"
        patterns = [
            r'Piece Name:\s*(.+)',
            r'PIEZA:\s*(.+)',
            r'(DELANTERO|POSTERIOR|@MANGA DER|@MANGA IZQ|SESGO CUELLO)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                name = match.group(1).strip()
                return name
        
        return "UNKNOWN"
    
    def _extract_piece_from_page(self, page: fitz.Page, page_num: int, piece_name: str) -> Optional[Piece]:
        """
        Extrae información de una pieza desde una página
        
        Args:
            page: Página del PDF
            page_num: Número de página
            piece_name: Nombre de la pieza
            
        Returns:
            Piece o None
        """
        # Obtener dimensiones de la página (en puntos)
        rect = page.rect
        width_pt = rect.width
        height_pt = rect.height
        
        # Convertir de puntos a milímetros (1 pt = 0.352778 mm)
        PT_TO_MM = 0.352778
        width_mm = width_pt * PT_TO_MM
        height_mm = height_pt * PT_TO_MM
        
        # Extraer paths vectoriales
        paths = page.get_drawings()
        vertices = self._extract_vertices_from_paths(paths)
        
        # Crear pieza
        piece = Piece(
            name=piece_name,
            size=self.size,
            width=width_mm,
            height=height_mm,
            pdf_page=page_num,
            vertices=vertices
        )
        
        # Calcular área
        piece.calculate_area()
        
        return piece
    
    def _extract_vertices_from_paths(self, paths: List) -> List[Tuple[float, float]]:
        """
        Extrae vértices de los paths vectoriales
        
        Args:
            paths: Lista de paths del PDF
            
        Returns:
            Lista de vértices (x, y)
        """
        vertices = []
        PT_TO_MM = 0.352778
        
        for path in paths:
            # Extraer puntos del path
            for item in path.get("items", []):
                if item[0] == "l":  # línea
                    p1 = item[1]
                    vertices.append((p1.x * PT_TO_MM, p1.y * PT_TO_MM))
                elif item[0] == "c":  # curva
                    # Para curvas, tomar el punto final
                    p3 = item[3]
                    vertices.append((p3.x * PT_TO_MM, p3.y * PT_TO_MM))
        
        return vertices
    
    def create_garment(self) -> Garment:
        """
        Crea una prenda con todas las piezas extraídas
        
        Returns:
            Garment
        """
        if not self.pieces:
            self.extract_pieces()
        
        garment = Garment(size=self.size)
        
        for piece in self.pieces:
            garment.add_piece(piece)
        
        return garment
    
    def get_piece_summary(self) -> Dict[str, float]:
        """
        Obtiene resumen de piezas con sus áreas
        
        Returns:
            dict: {nombre_pieza: área_mm2}
        """
        if not self.pieces:
            self.extract_pieces()
        
        return {piece.name: piece.get_area_mm2() for piece in self.pieces}
    
    def validate_completeness(self) -> Tuple[bool, List[str]]:
        """
        Valida que el PDF tenga todas las piezas necesarias
        
        Returns:
            tuple: (es_completo, lista_de_piezas_faltantes)
        """
        if not self.pieces:
            self.extract_pieces()
        
        required_pieces = [
            "DELANTERO",
            "POSTERIOR",
            "@MANGA DER",
            "@MANGA IZQ"
        ]
        
        piece_names = [p.name.upper() for p in self.pieces]
        missing = [req for req in required_pieces if req not in piece_names]
        
        return len(missing) == 0, missing
    
    def close(self):
        """Cierra el documento PDF"""
        if self.doc:
            self.doc.close()
    
    def __enter__(self):
        """Context manager entry"""
        self.load_pdf()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


class PDFPatternLoader:
    """Cargador de múltiples patrones PDF (diferentes tallas)"""
    
    def __init__(self, patterns_dir: str):
        """
        Inicializa el cargador
        
        Args:
            patterns_dir: Directorio con los PDFs de patrones
        """
        self.patterns_dir = Path(patterns_dir)
        self.garments: Dict[str, Garment] = {}
    
    def load_all_patterns(self) -> Dict[str, Garment]:
        """
        Carga todos los patrones PDF del directorio
        
        Returns:
            dict: {talla: Garment}
        """
        # Buscar todos los PDFs en el directorio
        pdf_files = list(self.patterns_dir.glob("*.pdf"))
        
        for pdf_file in pdf_files:
            try:
                processor = PDFProcessor(str(pdf_file))
                garment = processor.create_garment()
                
                # Validar completitud
                is_complete, missing = processor.validate_completeness()
                if not is_complete:
                    print(f"Advertencia: {pdf_file.name} no está completo. Faltan: {missing}")
                
                self.garments[garment.size] = garment
                processor.close()
                
            except Exception as e:
                print(f"Error al procesar {pdf_file.name}: {e}")
        
        return self.garments
    
    def get_garment_by_size(self, size: str) -> Optional[Garment]:
        """
        Obtiene la prenda de una talla específica
        
        Args:
            size: Talla buscada
            
        Returns:
            Garment o None
        """
        return self.garments.get(size.upper())
    
    def get_available_sizes(self) -> List[str]:
        """Obtiene lista de tallas disponibles"""
        return sorted(list(self.garments.keys()))
    
    def validate_all(self) -> Tuple[bool, List[str]]:
        """
        Valida todos los patrones cargados
        
        Returns:
            tuple: (todos_válidos, lista_de_errores)
        """
        errors = []
        
        for size, garment in self.garments.items():
            is_valid, error_msg = garment.validate()
            if not is_valid:
                errors.append(f"Talla {size}: {error_msg}")
        
        return len(errors) == 0, errors