"""
Script de prueba para la Fase 1: Lectura de Excel y PDFs
"""
import sys
from pathlib import Path

# Añadir el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from services import ExcelReader, PDFPatternLoader
from config import TEMPLATES_DIR

def test_excel_reader():
    """Prueba el lector de Excel"""
    print("=" * 60)
    print("PRUEBA 1: LECTURA DE EXCEL")
    print("=" * 60)
    
    # Ruta al archivo Excel de prueba
    excel_path = "1. Pedido 1 Equipaciones - Temp. 25-26.xlsx"
    
    if not Path(excel_path).exists():
        print(f"❌ Error: No se encuentra el archivo {excel_path}")
        print("   Por favor, coloca el archivo Excel en el directorio raíz del proyecto")
        return None
    
    try:
        # Crear lector
        reader = ExcelReader(excel_path)
        
        # Parsear pedido
        print("\n📄 Leyendo archivo Excel...")
        order = reader.parse_order()
        
        # Mostrar resumen
        print(f"\n✅ Pedido cargado exitosamente!")
        print(f"   Total de jugadores: {order.get_total_players()}")
        
        # Resumen por tallas
        print("\n📊 RESUMEN POR TALLAS:")
        size_summary = reader.get_size_summary()
        for size, count in sorted(size_summary.items()):
            print(f"   {size:5s}: {count:3d} unidades")
        
        # Resumen por patrocinadores
        print("\n🏢 RESUMEN POR PATROCINADORES:")
        sponsor_summary = reader.get_sponsor_summary()
        for sponsor, count in sorted(sponsor_summary.items()):
            print(f"   {sponsor:40s}: {count:3d} unidades")
        
        # Validar
        print("\n🔍 VALIDANDO PEDIDO...")
        is_valid, errors = reader.validate_order()
        
        if is_valid:
            print("   ✅ Pedido válido, sin errores")
        else:
            print(f"   ⚠️  Se encontraron {len(errors)} errores:")
            for error in errors[:10]:  # Mostrar solo los primeros 10
                print(f"      - {error}")
        
        # Exportar resumen
        print("\n📋 RESUMEN COMPLETO:")
        print(reader.export_summary())
        
        return order
        
    except Exception as e:
        print(f"❌ Error al procesar Excel: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_pdf_processor():
    """Prueba el procesador de PDFs"""
    print("\n" + "=" * 60)
    print("PRUEBA 2: PROCESAMIENTO DE PDFs")
    print("=" * 60)
    
    # Archivos PDF de prueba
    pdf_files = ["S.pdf", "M.pdf", "L.pdf"]
    
    print("\n📂 Buscando archivos PDF de patrones...")
    
    for pdf_file in pdf_files:
        if not Path(pdf_file).exists():
            print(f"   ⚠️  No se encuentra {pdf_file}")
        else:
            print(f"   ✓ {pdf_file} encontrado")
    
    # Intentar cargar patrones
    try:
        print("\n📄 Cargando patrones desde PDFs...")
        
        # Opción 1: Cargar un PDF individual
        if Path("S.pdf").exists():
            from services import PDFProcessor
            
            with PDFProcessor("S.pdf") as processor:
                pieces = processor.extract_pieces()
                
                print(f"\n✅ PDF 'S.pdf' procesado:")
                print(f"   Talla: {processor.size}")
                print(f"   Piezas encontradas: {len(pieces)}")
                
                print("\n   📏 DETALLE DE PIEZAS:")
                for piece in pieces:
                    print(f"      - {piece.name:20s}: {piece.width:.1f}mm x {piece.height:.1f}mm (área: {piece.get_area_mm2():.0f} mm²)")
                
                # Validar completitud
                is_complete, missing = processor.validate_completeness()
                if is_complete:
                    print("\n   ✅ Patrón completo")
                else:
                    print(f"\n   ⚠️  Faltan piezas: {missing}")
        
        # Opción 2: Cargar todos los patrones del directorio
        print("\n\n📁 Cargando todos los patrones del directorio actual...")
        loader = PDFPatternLoader(".")
        garments = loader.load_all_patterns()
        
        if garments:
            print(f"\n✅ Se cargaron {len(garments)} patrones:")
            for size, garment in sorted(garments.items()):
                print(f"   Talla {size:5s}: {len(garment.pieces)} piezas (área total: {garment.get_total_area():.0f} mm²)")
            
            # Validar todos
            print("\n🔍 VALIDANDO TODOS LOS PATRONES...")
            is_valid, errors = loader.validate_all()
            
            if is_valid:
                print("   ✅ Todos los patrones son válidos")
            else:
                print(f"   ⚠️  Se encontraron errores:")
                for error in errors:
                    print(f"      - {error}")
        else:
            print("   ⚠️  No se cargaron patrones. Verifica que los archivos PDF estén en el directorio")
        
        return garments
        
    except Exception as e:
        print(f"❌ Error al procesar PDFs: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_integration():
    """Prueba la integración entre Excel y PDFs"""
    print("\n" + "=" * 60)
    print("PRUEBA 3: INTEGRACIÓN EXCEL + PDFs")
    print("=" * 60)
    
    # Cargar pedido
    reader = ExcelReader("1. Pedido 1 Equipaciones - Temp. 25-26.xlsx")
    
    try:
        order = reader.parse_order()
        size_summary = order.get_size_summary()
        
        # Cargar patrones
        loader = PDFPatternLoader(".")
        garments = loader.load_all_patterns()
        available_sizes = loader.get_available_sizes()
        
        print(f"\n📊 Tallas en el pedido: {list(size_summary.keys())}")
        print(f"📁 Tallas con patrones disponibles: {available_sizes}")
        
        # Verificar coincidencia
        print("\n🔍 VERIFICANDO COINCIDENCIAS:")
        missing_patterns = []
        
        for size, count in size_summary.items():
            if size in available_sizes:
                print(f"   ✅ Talla {size:5s}: {count:3d} unidades → Patrón disponible")
            else:
                print(f"   ❌ Talla {size:5s}: {count:3d} unidades → ⚠️  FALTA PATRÓN")
                missing_patterns.append(size)
        
        if missing_patterns:
            print(f"\n⚠️  ATENCIÓN: Faltan patrones para las tallas: {missing_patterns}")
            print("   Debes proporcionar los archivos PDF para estas tallas")
        else:
            print("\n✅ ¡Perfecto! Todos los patrones necesarios están disponibles")
        
        # Estadísticas finales
        print("\n📈 ESTADÍSTICAS FINALES:")
        print(f"   Total de equipaciones: {order.get_total_players()}")
        print(f"   Tallas diferentes: {len(size_summary)}")
        print(f"   Patrones cargados: {len(garments)}")
        coverage = (len(garments) / len(size_summary) * 100) if size_summary else 0
        print(f"   Cobertura: {coverage:.1f}%")
        
        return order, garments
        
    except Exception as e:
        print(f"❌ Error en la integración: {e}")
        import traceback
        traceback.print_exc()
        return None, None


def main():
    """Función principal de pruebas"""
    print("\n" + "🚀" * 30)
    print("PRUEBAS DE LA FASE 1: LECTURA Y PARSEO")
    print("🚀" * 30)

    # Ejecutar pruebas
    order = test_excel_reader()
    garments = test_pdf_processor()

    if order and garments:
        test_integration()

    print("\n" + "=" * 60)
    print("✅ PRUEBAS COMPLETADAS")
    print("=" * 60)
    print("\nSi todas las pruebas fueron exitosas, puedes continuar con la Fase 2.")
    print("Si hay errores, revisa los archivos y vuelve a intentar.")

if __name__ == "__main__":
    main()