import sys
from lexer import lexer
from parser_calc import Parser

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def procesar_archivo(ruta_archivo):
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            lineas = archivo.readlines()

        print(f"Analizando: {ruta_archivo}")

        analizador = Parser()
        resultado = None

        for num_linea, linea in enumerate(lineas, 1):
            linea = linea.strip()
            if not linea or linea.startswith('#'):
                continue
            linea = linea.rstrip(';').strip()
            tokens = lexer(linea)
            analizador.reiniciar(tokens)
            resultado = analizador.parse_sentencia()

        print(f"Resultado final: {resultado}")
        if analizador.variables:
            print("Variables guardadas:")
            for var, val in analizador.variables.items():
                print(f"  {var} = {val}")
        return resultado

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{ruta_archivo}'")
    except Exception as e:
        print(f"Detenido por error: {e}")

def modo_interactivo():
    print("Calculadora LL(1) interactiva")
    print("Escribe una operacion (ej: x = 10 o sin(0) + 5)")
    print("Comandos: 'vars' para ver variables, 'limpiar' para reiniciar, 'salir' para terminar\n")

    analizador = Parser()

    while True:
        try:
            linea = input(">> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nSaliendo...")
            break

        if not linea:
            continue

        cmd = linea.lower()
        if cmd in ('salir', 'exit', 'quit'):
            break
        elif cmd in ('vars', 'variables'):
            if analizador.variables:
                for k, v in analizador.variables.items():
                    print(f"{k} = {v}")
            else:
                print("No hay variables guardadas")
            continue
        elif cmd in ('limpiar', 'clear'):
            analizador.variables.clear()
            print("Memoria reiniciada")
            continue

        linea = linea.rstrip(';').strip()

        try:
            tokens = lexer(linea)
            analizador.reiniciar(tokens)
            resultado = analizador.parse_sentencia()
            if resultado is not None:
                print(resultado)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    if len(sys.argv) == 2:
        archivo_txt = sys.argv[1]
        procesar_archivo(archivo_txt)
    else:
        modo_interactivo()
