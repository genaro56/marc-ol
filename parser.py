import os
from utils.Semantica import CuboSemantico
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
    @_('PROGRAM ID ";" begin')
    def program(self, p):
        return 'apropiado'

    @_('vars functions main', 
       'vars main', 
       'functions main', 
       'main')
    def begin(self, p): pass

    @_('func functions', 'func')
    def functions(self, p):
        pass

    # VARS
    @_('VAR vars1')
    def vars(self, p): pass

    @_('var_list ";" vars1', 'var_list ";"')
    def vars1(self, p): pass

    @_('tipo var "," var_list', 'tipo var')
    def var_list(self, p): pass

    @_('ID', 'ID "[" CTE_INT "]"', 'ID "[" CTE_INT "]" "[" CTE_INT "]"')
    def var(self, p): pass

    # TIPO
    @_('INT', 'FLOAT', 'CHAR')
    def tipo(self, p): pass

    # FUNCTION
    @_('tipo_fun MODULE ID "(" var_list ")" ";" func_body')
    def func(self, p): pass
    
    @_('vars bloque', 'bloque')
    def func_body(self, p): pass

    @_('tipo', 'VOID')
    def tipo_fun(self, p): pass

    # BLOQUE
    @_('"{" bloque1 "}"', '"{" empty "}"')
    def bloque(self, p):
        pass

    @_('estatuto bloque1', 'estatuto')
    def bloque1(self, p): pass

    # ESTATUTO
    @_(
        'asignacion',
        'void_fun',
        '_return',
        'lectura',
        'escritura',
        'condicion',
        'repeticion'
    )
    def estatuto(self, p): pass

    # ASIGNACION
    @_('id_dim "=" expresion ";"')
    def asignacion(self, p): pass

    @_('ID', 'ID "[" expresion "]"', 'ID "[" expresion "," expresion "]"')
    def id_dim(self, p): pass

    # ESCRITURA
    @_('WRITE "(" escritura1 ")" ";"')
    def escritura(self, p): pass

    @_('out "," escritura1', 'out')
    def escritura1(self, p): pass

    @_('CTE_STRING', 'expresion')
    def out(self, p): pass

    # EXPRESION
    @_('logic_exp',
       'logic_exp "|" expresion',
       )
    def expresion(self, p): pass

    @_('relation_exp',
       'relation_exp "&" logic_exp',
       'relation_exp "!" logic_exp'
       )
    def logic_exp(self, p): pass

    @_('exp',
       'exp "<" exp',
       'exp ">" exp',
       'exp EQUALS exp',
       )
    def relation_exp(self, p): pass

    @_(
        'termino "+" exp',
        'termino "-" exp',
        'termino',
    )
    def exp(self, p): pass

    @_('factor', 'termino "*" factor', 'termino "/" factor')
    def termino(self, p): pass

    @_('"(" expresion ")"', 'var_cte', '"+" var_cte', '"-" var_cte')
    def factor(self, p): pass

    @_('id_dim', 'CTE_INT', 'CTE_FLOAT', 'call_fun')
    def var_cte(self, p): pass

    # Seria otra expresion regular NOMBRE_MODULO?
    @_('ID "(" call_fun1 ")"')
    def call_fun(self, p): pass

    @_('expresion "," call_fun1', 'expresion')
    def call_fun1(self, p): pass

    @_('call_fun ";"')
    def void_fun(self, p): pass

    @_('RETURN "(" expresion ")" ";"')
    def _return(self, p): pass

    @_('READ "(" lectura1 ")" ";"')
    def lectura(self, p): pass

    @_('id_dim "," lectura1', 'id_dim')
    def lectura1(self, p): pass

    @_(
        'IF "(" expresion ")" THEN bloque',
        'IF "(" expresion ")" THEN ELSE bloque'
    )
    def condicion(self, p): pass

    @_('_while', '_for')
    def repeticion(self, p): pass

    @_('WHILE "(" expresion ")" DO bloque')
    def _while(self, p): pass

    @_('FOR id_dim "=" expresion TO expresion DO bloque')
    def _for(self, p): pass

    @_('MAIN "(" ")" bloque')
    def main(self, p): pass

    def error(self, p):
        if p:
            print("Syntax error at token", p.type)
            print("no apropiado")
            # Just discard the token and tell the parser it's okay.
            # self.errok()
        else:
            print("Syntax error at EOF")


if __name__ == '__main__':
    
    filePath = os.path.abspath('./utils/combinaciones.json')
    semantica = CuboSemantico(filePath)
    cubo = semantica.getCuboSemantico()
    
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
