import sys

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

gramatica = [
    ("1", "P",  ["L", "$"]),
    ("2", "L",  ["S", "L"]),
    ("3", "L",  ["EPSILON"]),
    ("4", "S",  ["ID", "R"]),
    ("5", "S",  ["Fnoid", "T'", "E'"]),
    ("6", "R",  ["=", "E"]),
    ("7", "R",  ["T'", "E'"]),
    ("8", "E",  ["T", "E'"]),
    ("9", "E'", ["+", "T", "E'"]),
    ("10", "E'", ["-", "T", "E'"]),
    ("11", "E'", ["EPSILON"]),
    ("12", "T",  ["F", "T'"]),
    ("13", "T'", ["*", "F", "T'"]),
    ("14", "T'", ["/", "F", "T'"]),
    ("15", "T'", ["%", "F", "T'"]),
    ("16", "T'", ["EPSILON"]),
    ("17", "F",  ["ID"]),
    ("18", "F",  ["Fnoid"]),
    ("19", "Fnoid", ["NUMERO"]),
    ("20", "Fnoid", ["(", "E", ")"]),
    ("21", "Fnoid", ["Fn", "(", "E", ")"]),
    ("22", "Fnoid", ["-", "F"]),
    ("23", "Fnoid", ["+", "F"]),
    ("24", "Fn", ["sin"]),
    ("25", "Fn", ["cos"]),
    ("26", "Fn", ["tan"]),
    ("27", "Fn", ["abs"]),
]

primeros = {
    "P":     {"ID", "NUMERO", "(", "sin", "cos", "tan", "abs", "-", "+", "$"},
    "L":     {"ID", "NUMERO", "(", "sin", "cos", "tan", "abs", "-", "+", "EPSILON"},
    "S":     {"ID", "NUMERO", "(", "sin", "cos", "tan", "abs", "-", "+"},
    "R":     {"=", "*", "/", "%", "+", "-", "$"},
    "E":     {"ID", "NUMERO", "(", "sin", "cos", "tan", "abs", "-", "+"},
    "E'":    {"+", "-", "EPSILON"},
    "T":     {"ID", "NUMERO", "(", "sin", "cos", "tan", "abs", "-", "+"},
    "T'":    {"*", "/", "%", "EPSILON"},
    "F":     {"ID", "NUMERO", "(", "sin", "cos", "tan", "abs", "-", "+"},
    "Fnoid": {"NUMERO", "(", "sin", "cos", "tan", "abs", "-", "+"},
    "Fn":    {"sin", "cos", "tan", "abs"},
}

siguientes = {
    "P":     {"$"},
    "L":     {"$"},
    "S":     {"ID", "NUMERO", "(", "sin", "cos", "tan", "abs", "-", "+", "$"},
    "R":     {"ID", "NUMERO", "(", "sin", "cos", "tan", "abs", "-", "+", "$"},
    "E":     {")", "$"},
    "E'":    {")", "$"},
    "T":     {"+", "-", ")", "$"},
    "T'":    {"+", "-", ")", "$"},
    "F":     {"*", "/", "%", "+", "-", ")", "$"},
    "Fnoid": {"*", "/", "%", "+", "-", ")", "$"},
    "Fn":    {"("},
}

prediccion = {
    "1":  {"ID", "NUMERO", "(", "sin", "cos", "tan", "abs", "-", "+", "$"},
    "2":  {"ID", "NUMERO", "(", "sin", "cos", "tan", "abs", "-", "+"},
    "3":  {"$"},
    "4":  {"ID"},
    "5":  {"NUMERO", "(", "sin", "cos", "tan", "abs", "-", "+"},
    "6":  {"="},
    "7":  {"*", "/", "%", "+", "-", "$"},
    "8":  {"ID", "NUMERO", "(", "sin", "cos", "tan", "abs", "-", "+"},
    "9":  {"+"},
    "10": {"-"},
    "11": {")", "$"},
    "12": {"ID", "NUMERO", "(", "sin", "cos", "tan", "abs", "-", "+"},
    "13": {"*"},
    "14": {"/"},
    "15": {"%"},
    "16": {")", "+", "-", "$"},
    "17": {"ID"},
    "18": {"NUMERO", "(", "sin", "cos", "tan", "abs", "-", "+"},
    "19": {"NUMERO"},
    "20": {"("},
    "21": {"sin", "cos", "tan", "abs"},
    "22": {"-"},
    "23": {"+"},
    "24": {"sin"},
    "25": {"cos"},
    "26": {"tan"},
    "27": {"abs"},
}

def mostrar_conjuntos():
    print("CONJUNTOS PRIMEROS Y SIGUIENTES")
    print(f"{'No Terminal':<12} | {'PRIMEROS':<36} | {'SIGUIENTES'}")
    for nt in ["P", "L", "S", "R", "E", "E'", "T", "T'", "F", "Fnoid", "Fn"]:
        prim = "{" + ", ".join(sorted(primeros[nt])) + "}"
        sigu = "{" + ", ".join(sorted(siguientes[nt])) + "}"
        print(f"{nt:<12} | {prim:<36} | {sigu}")

    print("\nCONJUNTOS DE PREDICCION")
    print(f"{'N°':<3} | {'Producción':<24} | {'Conjunto de Predicción'}")
    for num, cabeza, cuerpo in gramatica:
        prod_str = f"{cabeza} -> {' '.join(cuerpo)}"
        pred_str = "{" + ", ".join(sorted(prediccion[num])) + "}"
        print(f"{num:<3} | {prod_str:<24} | {pred_str}")

    print("\nVERIFICACION DE CRITERIO LL(1)")
    no_terminales = ["L", "S", "R", "E'", "T'", "F", "Fnoid", "Fn"]
    es_ll1 = True
    for nt in no_terminales:
        reglas_nt = [num for num, c, _ in gramatica if c == nt]
        if len(reglas_nt) > 1:
            for i in range(len(reglas_nt)):
                for j in range(i + 1, len(reglas_nt)):
                    r1 = reglas_nt[i]
                    r2 = reglas_nt[j]
                    inter = prediccion[r1].intersection(prediccion[r2])
                    if inter:
                        print(f"Conflicto en {nt} entre regla {r1} y {r2}: {inter}")
                        es_ll1 = False
                    else:
                        print(f"[OK] {nt}: Regla {r1} y Regla {r2} son disjuntas")

    if es_ll1:
        print("\nConclusion: La gramatica es LL(1) sin conflictos.")

if __name__ == '__main__':
    mostrar_conjuntos()
