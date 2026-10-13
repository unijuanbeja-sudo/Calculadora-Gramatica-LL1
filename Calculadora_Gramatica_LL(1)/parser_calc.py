import math
from lexer import Token

class Parser:
    def __init__(self, tokens=None, variables=None):
        self.tokens = tokens if tokens is not None else []
        self.pos = 0
        self.variables = variables if variables is not None else {}

    def reiniciar(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def token_actual(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return Token('EOF', '$')

    def match(self, tipo_esperado):
        actual = self.token_actual()
        if actual.tipo == tipo_esperado:
            self.pos += 1
            return actual
        raise Exception(f"Error sintáctico: Se esperaba '{tipo_esperado}', pero se encontró '{actual.tipo}' ({actual.valor}) en línea {actual.linea}")

    def parse(self):
        return self.parse_programa()

    def parse_programa(self):
        resultado = None
        while self.token_actual().tipo != 'EOF':
            resultado = self.parse_sentencia()
        return resultado

    def parse_sentencia(self):
        token = self.token_actual()
        if token.tipo == 'ID':
            var_nombre = token.valor
            self.match('ID')
            return self.parse_resto_id(var_nombre)
        elif token.tipo in ('NUMERO', 'PAREN_I', 'SIN', 'COS', 'TAN', 'ABS', 'RESTA', 'SUMA'):
            return self.parse_E()
        else:
            raise Exception(f"Error sintáctico: Sentencia inválida iniciada con '{token.tipo}' en línea {token.linea}")

    def parse_resto_id(self, var_nombre):
        token = self.token_actual()
        if token.tipo == 'ASIGNAR':
            self.match('ASIGNAR')
            val = self.parse_E()
            self.variables[var_nombre] = val
            return val
        elif token.tipo in ('MULT', 'DIV', 'MOD', 'SUMA', 'RESTA', 'EOF'):
            if var_nombre not in self.variables:
                raise Exception(f"Error semántico: Variable '{var_nombre}' no definida")
            val = self.variables[var_nombre]
            val = self.parse_T_prima(val)
            val = self.parse_E_prima(val)
            return val
        else:
            raise Exception(f"Error sintáctico: Se esperaba '=' u operador tras '{var_nombre}', se encontró '{token.tipo}'")

    def parse_E(self):
        val = self.parse_T()
        return self.parse_E_prima(val)

    def parse_E_prima(self, acumulado):
        token = self.token_actual()
        if token.tipo == 'SUMA':
            self.match('SUMA')
            der = self.parse_T()
            return self.parse_E_prima(acumulado + der)
        elif token.tipo == 'RESTA':
            self.match('RESTA')
            der = self.parse_T()
            return self.parse_E_prima(acumulado - der)
        elif token.tipo in ('PAREN_D', 'EOF'):
            return acumulado
        raise Exception(f"Error sintáctico: Operador inesperado '{token.tipo}' en línea {token.linea}")

    def parse_T(self):
        val = self.parse_F()
        return self.parse_T_prima(val)

    def parse_T_prima(self, acumulado):
        token = self.token_actual()
        if token.tipo == 'MULT':
            self.match('MULT')
            der = self.parse_F()
            return self.parse_T_prima(acumulado * der)
        elif token.tipo == 'DIV':
            self.match('DIV')
            der = self.parse_F()
            if der == 0:
                raise Exception("Error semántico: División por cero")
            return self.parse_T_prima(acumulado / der)
        elif token.tipo == 'MOD':
            self.match('MOD')
            der = self.parse_F()
            if der == 0:
                raise Exception("Error semántico: Módulo por cero")
            return self.parse_T_prima(acumulado % der)
        elif token.tipo in ('SUMA', 'RESTA', 'PAREN_D', 'EOF'):
            return acumulado
        raise Exception(f"Error sintáctico: Token inesperado '{token.tipo}' en término en línea {token.linea}")

    def parse_F(self):
        token = self.token_actual()
        if token.tipo == 'ID':
            self.match('ID')
            if token.valor not in self.variables:
                raise Exception(f"Error semántico: Variable '{token.valor}' no definida")
            return self.variables[token.valor]
        return self.parse_factor_no_id()

    def parse_factor_no_id(self):
        token = self.token_actual()
        if token.tipo == 'NUMERO':
            self.match('NUMERO')
            return float(token.valor)
        elif token.tipo == 'PAREN_I':
            self.match('PAREN_I')
            val = self.parse_E()
            self.match('PAREN_D')
            return val
        elif token.tipo in ('SIN', 'COS', 'TAN', 'ABS'):
            fn = token.tipo
            self.match(fn)
            self.match('PAREN_I')
            val = self.parse_E()
            self.match('PAREN_D')
            return self.evaluar_funcion(fn, val)
        elif token.tipo == 'RESTA':
            self.match('RESTA')
            return -self.parse_F()
        elif token.tipo == 'SUMA':
            self.match('SUMA')
            return self.parse_F()
        else:
            raise Exception(f"Error sintáctico: Se esperaba número, variable o función, se encontró '{token.tipo}' en línea {token.linea}")

    def evaluar_funcion(self, fn, val):
        if fn == 'SIN':
            return math.sin(val)
        elif fn == 'COS':
            return math.cos(val)
        elif fn == 'TAN':
            if abs(math.cos(val)) < 1e-12:
                raise Exception(f"Error semántico: Tangente indefinida para el ángulo {val} rad")
            return math.tan(val)
        elif fn == 'ABS':
            return abs(val)
        raise Exception(f"Error semántico: Función desconocida '{fn}'")
