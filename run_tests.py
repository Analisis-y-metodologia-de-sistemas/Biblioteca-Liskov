#!/usr/bin/env python3
"""
Script simple para ejecutar todos los tests del sistema
Compatible con Windows y Unix/Linux/macOS
"""

import os
import subprocess
import sys


def main():
    """Ejecutar los tests usando el test runner"""

    # Cambiar al directorio del proyecto
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    # Determinar el comando python apropiado
    python_cmd = "python3" if os.name != "nt" else "python"

    # Ejecutar el test runner
    test_runner_path = os.path.join("tests", "test_runner.py")

    print("🚀 Iniciando ejecución de tests...")
    print("=" * 50)

    try:
        # Pasar cualquier argumento adicional al test runner
        cmd = [python_cmd, test_runner_path] + sys.argv[1:]
        result = subprocess.run(cmd, cwd=script_dir)
        sys.exit(result.returncode)

    except FileNotFoundError:
        print(f"❌ Error: No se encontró {python_cmd}")
        print("   Asegúrate de tener Python instalado y en el PATH")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏹️  Ejecución cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
