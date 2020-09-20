from sly import Parser
from lexer import MyLexer


class MyParser(Parser):
    start = 'program'
    tokens = MyLexer.tokens
    precedence = (
        ('nonassoc', '<', '>'),  # Nonassociative operators
        ('left', '+', '-'),
        ('left', '*', '/'),
    )
    # Grammar rules and action

    def __init__(self):
        self.env = {}

    @_('')
    def empty(self, p): pass

    # PROGRAM
    @_('PROGRAM ID ";" program1 bloque')
    def program(self, p):
        return 'apropiado'

    @_('vars', 'empty')
    def program1(self, p):
        pass

    # VARS
    @_('VAR var1')
    def vars(self, p):
        pass

    @_('ID var2 ":" tipo ";"', 'ID var2 ":" tipo ";" var1')
    def var1(self, p): pass

    @_('"," ID var2', 'empty')
    def var2(self, p): pass

    # TIPO
    @_('INT', 'FLOAT')
    def tipo(self, p): pass

    # BLOQUE
    @_('"{" bloque1 "}"')
    def bloque(self, p):
        pass

    @_('estatuto bloque1', 'empty')
    def bloque1(self, p): pass

    # ESTATUTO
    @_('asignacion', 'condicion', 'escritura')
    def estatuto(self, p): pass

    # ASIGNACION
    @_('ID "=" expresion ";"')
    def asignacion(self, p): pass

    # ESCRITURA
    @_('PRINT "(" escritura1 ")" ";"')
    def escritura(self, p): pass

    @_('expresion escritura2', 'CTE_STRING escritura2')
    def escritura1(self, p): pass

    @_('"," escritura1', 'empty')
    def escritura2(self, p): pass

    # EXPRESION
    @_('exp expresion1')
    def expresion(self, p): pass

    @_('expresion2 exp', 'empty')
    def expresion1(self, p): pass

    @_('EQUALS', '"<"', '">"')
    def expresion2(self, p): pass

    # CONDICION
    @_('IF "(" expresion ")" bloque condicion1 ";"')
    def condicion(self, p): pass

    @_('ELSE bloque', 'empty')
    def condicion1(self, p): pass

    # TERMINO
    @_('factor termino1')
    def termino(self, p): pass

    @_('termino2', 'empty')
    def termino1(self, p): pass

    @_('"*"', '"/"')
    def termino2(self, p): pass

    # EXP
    @_('termino exp1')
    def exp(self, p): pass

    @_('exp2 termino exp1', 'empty')
    def exp1(self, p): pass

    @_('"+"', '"-"')
    def exp2(self, p): pass

    # FACTOR
    @_('"(" expresion ")"', 'factor1 var_cte')
    def factor(self, p): pass

    @_('"+"', '"-"', 'empty')
    def factor1(self, p): pass

    # VAR_CTE
    @_('ID', 'CTE_INT', 'CTE_FLOAT')
    def var_cte(self, p): pass

    def error(self, p):
        if p:
            print("Syntax error at token", p.type)
            print("no apropiado")
            # Just discard the token and tell the parser it's okay.
            # self.errok()
        else:
            print("Syntax error at EOF")


if __name__ == '__main__':
    parser = MyParser()
    lexer = MyLexer()

    inputFile = open("./fail.txt", "r")
    inputText = inputFile.read()
    print(inputText)

    # LEXER: Lexical Analysis
    print('\n\nLEXER Analysis:')
    tokens = lexer.tokenize(inputText)
    for tok in tokens:
        print('type=%r, value=%r' % (tok.type, tok.value))

    # PARSER: Synctactic Analysis
    print('\n\nPARSER Analysis:')
    result = parser.parse(lexer.tokenize(inputText))
    print(result)

    inputFile.close()
