import re

class Token:
    def __init__(self, tipo, valor, linea=1, columna=1):
        self.tipo = tipo
        self.valor = valor
        self.linea = linea
        self.columna = columna

    def __repr__(self):
        return f"{self.tipo}({self.valor})"

def lexer(codigo):
    patrones = [
        ('NUMERO',  r'\d+(\.\d*)?'),
        ('ASIGNAR', r'='),
        ('SIN',     r'(?i)sin\b'),
        ('COS',     r'(?i)cos\b'),
        ('TAN',     r'(?i)tan\b'),
        ('ABS',     r'(?i)abs\b'),
        ('ID',      r'[a-zA-Z_][a-zA-Z0-9_]*'),
        ('SUMA',    r'\+'),
        ('RESTA',   r'-'),
        ('MULT',    r'\*'),
        ('DIV',     r'/'),
        ('MOD',     r'%'),
        ('PAREN_I', r'\('),
        ('PAREN_D', r'\)'),
        ('ESPACIO', r'[ \t\r\n]+'),
    ]

    tokens = []
    pos = 0
    linea = 1
    columna = 1

    while pos < len(codigo):
        match = None
        for tipo, patron in patrones:
            regex = re.compile(patron)
            match = regex.match(codigo, pos)
            if match:
                texto = match.group(0)
                if tipo != 'ESPACIO':
                    tokens.append(Token(tipo, texto, linea, columna))

                saltos = texto.count('\n')
                if saltos > 0:
                    linea += saltos
                    columna = len(texto) - texto.rfind('\n')
                else:
                    columna += len(texto)

                pos = match.end(0)
                break

        if not match:
            raise Exception(f"Error léxico: Carácter no reconocido '{codigo[pos]}' en línea {linea}, columna {columna}")

    return tokens
