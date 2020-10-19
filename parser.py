import os
from utils.Semantica import CuboSemantico, AddrGenerator
from utils.Tablas import DirFunciones, TablaDeVars
from utils.Cuadruplos import Cuadruplos
from sly import Parser
from lexer import MyLexer

dirFunc = None
addrCounter = AddrGenerator()
cuadruplos = Cuadruplos()

filePath = os.path.abspath('./utils/combinaciones.json')
cuboSemantico = CuboSemantico(filePath).getCuboSemantico()

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
        dirFunc.programName = funcName
        pass

    @_('vars functions main',
       'vars main',
       'functions main',
       'main')
    def begin(self, p): pass

    # VARS
    @_('VAR vars1')
    def vars(self, p): pass
    
    # @_('')
    # def seen_endof_vars(self, p):
    #     if len(dirFunc.funcStack) > 0:
    #         dirFunc.funcStack.pop()
    #     pass

    @_('var_def ";" vars1', 'var_def ";"')
    def vars1(self, p): pass

    @_('tipo var_list')
    def var_def(self, p): pass

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
                nextAdrr = None
                scope = dirFunc.dirFunciones[funcId].type
                # checa si la variable pertenece al scope global o local
                if scope == "PROGRAM":
                    nextAdrr = addrCounter.nextGlobalAddr(varType)
                else:
                    nextAdrr = addrCounter.nextLocalAddr(varType)

                dirFunc.dirFunciones[funcId].tablaVariables.addVar(
                    varName, varType, nextAdrr)
            else:
                raise Exception('Variable arleady declared in Table')
        pass

    # TIPO
    @_('INT', 'FLOAT', 'CHAR')
    def tipo(self, p):
        # p[-1] es el tipo de la listas de variables
        typeValue = p[0]
        # busca el tope del stack para ver la siguiente entrada
        if len(dirFunc.funcStack) > 0:
            funcId = dirFunc.funcStack[-1]
            dirFunc.dirFunciones[funcId].tablaVariables.setTempTypeValue(typeValue)
        return p[0]

    # FUNCTION
    @_('FUNC func_list')
    def functions(self, p):
        pass

    @_('func_def func_list', 'func_def')
    def func_list(self, p):
        pass

    @_('tipo_fun MODULE ID seen_funcId "(" params ")" ";" func_body seen_func_end')
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
            # agrega referencia a la tabla de variables global
            globalVarTable = dirFunc.getFuncion(dirFunc.programName).tablaVariables
            dirFunc.getFuncion(funcName).tablaVariables.setGlobalVarTable(globalVarTable)
            # saca el nombre de fucion anterior y agrega el nuevo a funcStack
            dirFunc.funcStack.pop()
            dirFunc.funcStack.append(funcName)
        else:
            raise Exception(f'MultipleDeclaration: module {funcName} already defined')
        pass

    @_('')
    def seen_func_end(self, p):
        addrCounter.resetLocalCounter()
        return
    
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
        'termino "+" seen_oper_suma exp',
        'termino "-" seen_oper_resta exp',
        'termino seen_termino',
    )
    def exp(self, p): pass
    
    @_('')
    def seen_termino(self, p):
        pilaOperadores = cuadruplos.pilaOperadores
        pilaOperandos = cuadruplos.pilaOperandos
        if len(pilaOperadores) > 0 and (pilaOperadores[-1] == "+" or pilaOperadores[-1] == "-"):
            rightOperand, rightType = pilaOperandos.pop()
            leftOperand, leftType = pilaOperandos.pop()
            operator = pilaOperadores.pop()
            resultType = cuboSemantico[(leftType, rightType, operator)]
            # print(leftType, rightType, operator, resultType)
            if (resultType != 'error'):
                result = addrCounter.nextTemporalAddr(resultType)
                quad = (operator, leftOperand, rightOperand, result)
                cuadruplos.pilaCuadruplos.append(quad)
                pilaOperandos.append((result, resultType))
            else:
                raise Exception('Type mismatch')
        pass
    
    @_('')
    def seen_oper_suma(self, p):
        cuadruplos.pilaOperadores.append("+")
        
    @_('')
    def seen_oper_resta(self, p):
        cuadruplos.pilaOperadores.append("-")

    @_('factor seen_factor', 
       'factor "*" seen_oper_mult termino', 
       'factor "/" seen_oper_div termino',
    )
    def termino(self, p): pass
    
    @_('')
    def seen_factor(self, p):
        pilaOperadores = cuadruplos.pilaOperadores
        pilaOperandos = cuadruplos.pilaOperandos
        if len(pilaOperadores) > 0 and (pilaOperadores[-1] == "*" or pilaOperadores[-1] == "/"):
            rightOperand, rightType = pilaOperandos.pop()
            leftOperand, leftType = pilaOperandos.pop()
            operator = pilaOperadores.pop()
            resultType = cuboSemantico[(leftType, rightType, operator)]
            # print(leftType, rightType, operator, resultType)
            if (resultType != 'error'):
                result = addrCounter.nextTemporalAddr(resultType)
                quad = (operator, leftOperand, rightOperand, result)
                cuadruplos.pilaCuadruplos.append(quad)
                pilaOperandos.append((result, resultType))
            else:
                raise Exception('Type mismatch')
        pass
    
    @_('')
    def seen_oper_mult(self, p):
        cuadruplos.pilaOperadores.append("*")
        
    @_('')
    def seen_oper_div(self, p):
        cuadruplos.pilaOperadores.append("/")

    @_('"(" expresion ")"', 
       'var_cte', 
       '"+" var_cte', 
       '"-" var_cte',
    )
    def factor(self, p): pass

    @_('id_dim', 
       'CTE_INT seen_int_cte', 
       'CTE_FLOAT seen_float_cte', 
       'call_fun'
    )
    def var_cte(self, p): pass
    
    @_('ID', 'ID "[" expresion "]"', 'ID "[" expresion "," expresion "]"')
    def id_dim(self, p):
        ID = p[0]
        funcId = dirFunc.funcStack[-1]
        varTable = dirFunc.getFuncion(funcId).tablaVariables
        varType = idAddr = None
        if varTable.isVarInTable(ID):
            varObj = varTable.getVar(ID)
            varType = varObj.getType()
            idAddr = varObj.getAddr()
        elif varTable.isVarInGlobalTable(ID):
            varObj = varTable.getGlobalVarTable().getVar(ID)
            varType = varObj.getType()
            idAddr = varObj.getAddr()
        else:
            raise Exception(f'Undefined variable {ID}')
        cuadruplos.pilaOperandos.append((idAddr, varType))
        return p[0]

    @_('')
    def seen_int_cte(self, p):
        cte = p[-1]
        cuadruplos.pilaOperandos.append((cte, 'int'))
        pass
        
    @_('')
    def seen_float_cte(self, p):
        cte = p[-1]
        cuadruplos.pilaOperandos.append((cte, 'float'))
        pass
    
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
    @_('MAIN seen_main "(" ")" bloque')
    def main(self, p): pass
    
    @_('')
    def seen_main(self, p):
        dirFunc.funcStack.pop()
        programName = dirFunc.programName
        dirFunc.funcStack.append(programName)
        pass

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
    parser = MyParser()
    lexer = MyLexer()

    inputFile = open("./TestProgram3.txt", "r")
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
    
    print(cuadruplos.pilaCuadruplos)
    print(cuadruplos.pilaOperandos)
    print(cuadruplos.pilaOperadores)