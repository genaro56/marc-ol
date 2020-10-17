import os
from utils.Semantica import CuboSemantico
from utils.Tablas import DirFunciones, TablaDeVars
from sly import Parser
from lexer import MyLexer

dirFunc = None


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
    @_('PROGRAM seen_program ID seen_programId ";" begin')
    def program(self, p):
        return 'apropiado'

    @_('')
    def seen_program(self, p):
        '''
        crea instancia global de dir. de funciones
        despues del token PROGRAM
        '''
        global dirFunc
        dirFunc = DirFunciones()
        pass

    @_('')
    def seen_programId(self, p):
        '''
        agrega funcion tipo PROGRAM
        al dir. de funciones
        '''
        # p[-1] es ID
        funcName = p[-1]
        # agrega el siguiente ID de función para la lista de variables
        dirFunc.funcStack.append(funcName)
        dirFunc.addFuncion(funcName, 'PROGRAM')
        pass

    @_('vars functions main',
       'vars main',
       'functions main',
       'main')
    def begin(self, p): pass

    # VARS
    @_('VAR vars1 seen_endof_vars')
    def vars(self, p): pass
    
    @_('')
    def seen_endof_vars(self, p):
        if len(dirFunc.funcStack) > 0:
            dirFunc.funcStack.pop()
        pass

    @_('var_def ";" vars1', 'var_def ";"')
    def vars1(self, p): pass

    @_('tipo var_list seen_var_list')
    def var_def(self, p): pass

    @_('')
    def seen_var_list(self, p):
        # p[-1] es el tipo de la listas de variables
        listType = p[-2]
        # busca el tope del stack para ver la siguiente entrada
        if len(dirFunc.funcStack) > 0:
            funcId = dirFunc.funcStack[-1]
            dirFunc.dirFunciones[funcId].tablaVariables.setTempTypeValue(listType)

    @_('var "," var_list', 'var')
    def var_list(self, p):
        pass

    @_('ID seen_var_name ', 'ID seen_var_name "[" CTE_INT "]"', 'ID seen_var_name "[" CTE_INT "]" "[" CTE_INT "]"')
    def var(self, p): pass

    @_('')
    def seen_var_name(self, p):
        if len(dirFunc.funcStack) > 0:
            funcId = dirFunc.funcStack[-1]
            varName = p[-1]
            varType = dirFunc.dirFunciones[funcId].tablaVariables.tempTypeValue
            if not dirFunc.dirFunciones[funcId].tablaVariables.isVarInTable(varName):
                dirFunc.dirFunciones[funcId].tablaVariables.addVar(
                    varName, varType)
            else:
                raise Exception('Variable arleady declared in Table')
        pass

    # TIPO
    @_('INT', 'FLOAT', 'CHAR')
    def tipo(self, p):
        return p[0]

    # FUNCTION
    @_('FUNC func_list')
    def functions(self, p):
        pass

    @_('func_def func_list', 'func_def')
    def func_list(self, p):
        pass

    @_('tipo_fun MODULE ID seen_funcId "(" params ")" ";" func_body')
    def func_def(self, p): pass

    @_('')
    def seen_funcId(self, p):
        '''
        Agrega funcion al dir. de funciones 
        con nomre funcName y tipo funcType
        '''

        funcName = p[-1]
        funcType = p[-3]

        if not dirFunc.isNameInDir(funcName):
            dirFunc.addFuncion(funcName, funcType)
            dirFunc.funcStack.append(funcName)
        else:
            raise Exception('MultipleDeclaration')
        pass

    @_('vars bloque', 'bloque')
    def func_body(self, p): pass

    @_('tipo', 'VOID')
    def tipo_fun(self, p):
        return p[0]

    # PARAMETERS
    @_('tipo var "," params', 'tipo var')
    def params(self, p): pass

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

    # VOID FUNC
    @_('call_fun ";"')
    def void_fun(self, p): pass

    # RETURN
    @_('RETURN "(" expresion ")" ";"')
    def _return(self, p): pass

    # LECTURA
    @_('READ "(" lectura1 ")" ";"')
    def lectura(self, p): pass

    @_('id_dim "," lectura1', 'id_dim')
    def lectura1(self, p): pass

    # CONDICION
    @_(
        'IF "(" expresion ")" THEN bloque',
        'IF "(" expresion ")" THEN bloque ELSE bloque'
    )
    def condicion(self, p): pass

    # REPETICION
    @_('_while', '_for')
    def repeticion(self, p): pass

    @_('WHILE "(" expresion ")" DO bloque')
    def _while(self, p): pass

    @_('FOR id_dim "=" expresion TO expresion DO bloque')
    def _for(self, p): pass

    # MAIN
    @_('MAIN "(" ")" bloque')
    def main(self, p): pass

    # ERROR
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

    inputFile = open("./TestProgram.txt", "r")
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
