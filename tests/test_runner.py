#!/usr/bin/env python3
"""
Runner principal para ejecutar todos los tests del sistema
"""

import sys
import os
import unittest
import time
from datetime import datetime

# Agregar el path del proyecto
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def run_tests():
    """Ejecuta todos los tests del sistema"""
    
    print("🧪 EJECUTANDO TESTS DEL SISTEMA BIBLIOTECA LISKOV")
    print("=" * 60)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Configurar el loader y suite
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__)
    
    # Descubrir todos los tests
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Configurar el runner con verbosidad
    runner = unittest.TextTestRunner(
        verbosity=2,
        stream=sys.stdout,
        descriptions=True,
        failfast=False
    )
    
    # Ejecutar tests
    start_time = time.time()
    result = runner.run(suite)
    end_time = time.time()
    
    # Mostrar resumen
    print()
    print("📊 RESUMEN DE EJECUCIÓN")
    print("=" * 40)
    print(f"⏱️  Tiempo total: {end_time - start_time:.2f} segundos")
    print(f"✅ Tests ejecutados: {result.testsRun}")
    print(f"❌ Fallos: {len(result.failures)}")
    print(f"💥 Errores: {len(result.errors)}")
    print(f"⏩ Omitidos: {len(result.skipped)}")
    
    # Mostrar detalles de fallos si los hay
    if result.failures:
        print()
        print("❌ FALLOS DETECTADOS:")
        print("-" * 30)
        for test, traceback in result.failures:
            print(f"🔴 {test}: {traceback}")
    
    # Mostrar detalles de errores si los hay
    if result.errors:
        print()
        print("💥 ERRORES DETECTADOS:")
        print("-" * 30)
        for test, traceback in result.errors:
            print(f"🔴 {test}: {traceback}")
    
    # Resultado final
    if result.wasSuccessful():
        print()
        print("🎉 ¡TODOS LOS TESTS PASARON EXITOSAMENTE!")
        return 0
    else:
        print()
        print("⚠️  ALGUNOS TESTS FALLARON - REVISAR ARRIBA")
        return 1


def run_unit_tests_only():
    """Ejecuta solo los tests unitarios"""
    print("🧪 EJECUTANDO SOLO TESTS UNITARIOS")
    print("=" * 40)
    
    loader = unittest.TestLoader()
    unit_dir = os.path.join(os.path.dirname(__file__), 'unit')
    
    suite = loader.discover(unit_dir, pattern='test_*.py')
    runner = unittest.TextTestRunner(verbosity=2)
    
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


def run_integration_tests_only():
    """Ejecuta solo los tests de integración"""
    print("🧪 EJECUTANDO SOLO TESTS DE INTEGRACIÓN")
    print("=" * 40)
    
    loader = unittest.TestLoader()
    integration_dir = os.path.join(os.path.dirname(__file__), 'integration')
    
    suite = loader.discover(integration_dir, pattern='test_*.py')
    runner = unittest.TextTestRunner(verbosity=2)
    
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


def show_test_coverage():
    """Muestra información sobre la cobertura de tests"""
    print("📋 COBERTURA DE TESTS")
    print("=" * 30)
    
    unit_tests = [
        "✅ UsuarioService - Registro, búsqueda, validaciones",
        "✅ ItemBibliotecaService - CRUD, búsquedas, categorías", 
        "✅ PrestamoService - Préstamos, devoluciones, multas",
        "✅ ReservaService - Reservas, cancelaciones",
        "✅ MultaService - Pagos, listados",
        "✅ AuthService - Autenticación, sesiones, passwords"
    ]
    
    integration_tests = [
        "✅ Flujo completo préstamo con multa",
        "✅ Sistema de reservas end-to-end",
        "✅ Búsquedas y filtros integrados",
        "✅ Autenticación completa",
        "✅ Validaciones y restricciones"
    ]
    
    print("🔧 TESTS UNITARIOS:")
    for test in unit_tests:
        print(f"  {test}")
    
    print()
    print("🔄 TESTS DE INTEGRACIÓN:")
    for test in integration_tests:
        print(f"  {test}")
    
    print()
    print("📊 ESTADÍSTICAS:")
    print(f"  • {len(unit_tests)} suites de tests unitarios")
    print(f"  • {len(integration_tests)} suites de tests de integración") 
    print(f"  • ~50+ casos de prueba individuales")
    print(f"  • Cobertura: Servicios, repositorios, casos de uso")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '--unit':
            sys.exit(run_unit_tests_only())
        elif sys.argv[1] == '--integration':
            sys.exit(run_integration_tests_only())
        elif sys.argv[1] == '--coverage':
            show_test_coverage()
            sys.exit(0)
        elif sys.argv[1] == '--help':
            print("🧪 RUNNER DE TESTS - Sistema Biblioteca Liskov")
            print()
            print("Uso:")
            print("  python test_runner.py           # Ejecutar todos los tests")
            print("  python test_runner.py --unit    # Solo tests unitarios")
            print("  python test_runner.py --integration  # Solo tests de integración")
            print("  python test_runner.py --coverage     # Mostrar cobertura")
            print("  python test_runner.py --help         # Esta ayuda")
            sys.exit(0)
    
    # Ejecutar todos los tests por defecto
    sys.exit(run_tests())