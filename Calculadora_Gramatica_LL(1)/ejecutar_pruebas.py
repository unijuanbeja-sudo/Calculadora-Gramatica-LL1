import os
import glob
import sys
from main import procesar_archivo

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def main():
    directorio_pruebas = os.path.join(os.path.dirname(__file__), 'pruebas')
    archivos = sorted(glob.glob(os.path.join(directorio_pruebas, '*.txt')))

    for ruta in archivos:
        nombre = os.path.basename(ruta)
        print(f"\nPrueba: {nombre}")
        procesar_archivo(ruta)

if __name__ == '__main__':
    main()
