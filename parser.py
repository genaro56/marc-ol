import os
from utils.Semantica import CuboSemantico, AddrGenerator
from utils.Tablas import DirFunciones, TablaDeVars, TablaCtes, FuncSize, TablaParams, Pointer
from utils.Cuadruplos import Cuadruplos
from vm.VirtualMachine import VirtualMachine
from sly import Parser
from lexer import MyLexer
from flask import Flask, request
app = Flask(__name__)

dirFunc = None
addrCounter = AddrGenerator()
cuadruplos = Cuadruplos()
tablaCtes = TablaCtes()
tablaParams = TablaParams()

filePath = os.path.abspath('./utils/combinaciones.json')
cuboSemantico = CuboSemantico(filePath).getCuboSemantico()


class MyParser(Parser):
    start = 'program'
    # debugfile = 'parser.out'
    tokens = MyLexer.tokens
    precedence = (
        ('nonassoc', '<', '>'),  # Nonassociative operators
        ('left', '+', '-'),
        ('left', '*', '/'),
    )
    # Helper functions

    def getCteAddr(self, constant):
        """
        docstring
        """
        if tablaCtes.isCteInTable(constant):
            cteAddr = tablaCtes.getCte(constant).getAddr()
        else:
            cteAddr = addrCounter.nextConstAddr('int')
            tablaCtes.addCte(constant, cteAddr)

        return cteAddr
    
    def getVarInfo(self, funcId, ID):
        """
        Regresa una tupla de tres valores: varible, tipo, addr
        o un error en caso de que no este definida
        """
        varTable = dirFunc.getFuncion(funcId).tablaVariables
        varType = idAddr = None
        globalVarTable = dirFunc.getFuncion(dirFunc.programName).tablaVariables
        
        # checa si la variable esta en la tabla local o global
        if varTable.isVarInTable(ID):
            varObj = varTable.getVar(ID)
            varType = varObj.getType()
            idAddr = varObj.getAddr()
        elif globalVarTable.isVarInTable(ID):
            varObj = varTable.getGlobalVarTable().getVar(ID)
            varType = varObj.getType()
            idAddr = varObj.getAddr()
        else:
            raise Exception(f'Error: undefined variable {ID}.')
        
        return (varObj, varType, idAddr)
        

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
        # agrega cuadruplo goto para iniciar ejecucion en main
        cuadruplos.createQuad('goto', None, None, None)
        cuadruplos.pilaSaltos.append(cuadruplos.counter - 1)
        pass

    @_('vars functions main',
       'vars main',
       'functions main',
       'main')
    def begin(self, p): pass

    # VARS
    @_('VAR vars1')
    def vars(self, p): pass

    @_('var_def ";" vars1', 'var_def ";"')
    def vars1(self, p): pass

    @_('tipo var_list')
    def var_def(self, p): pass

    @_('var "," var_list', 'var')
    def var_list(self, p):
        pass

    @_('ID seen_var_name', 'ID seen_var_name seen_array_start "[" CTE_INT seen_arr_dim "]" array_dims seen_arr_dim_end')
    def var(self, p):
        # returns tuple from seen_var_name
        return p[1]

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
                raise Exception('ER-1: Variable arleady declared in Table')
        return (varType, varName, nextAdrr)

    @_('empty', '"[" CTE_INT seen_arr_dim2 "]" array_dims')
    def array_dims(self, p):
        pass

    @_('')
    def seen_array_start(self, p):
        _, varName, addr = p[-1]

        # obtiene la variable y asigna al temporal
        funcId = dirFunc.funcStack[-1]
        var = dirFunc.getFuncion(funcId).tablaVariables.getVar(varName)
        dirFunc.setTempArrVar(var)

        var = dirFunc.getTempArrVar()
        var.setIsArray(True)
        var.initArray()
        return var

    @_('')
    def seen_arr_dim(self, p):
        _, varName, _ = p[-4]
        intDimension = p[-1]
        var = dirFunc.getTempArrVar()
        # crea un nuevo nodo con los limites
        nodeHead = var.arrayData.createNode(intDimension)
        # calcula el rango del nodo actual
        calculatedRange = nodeHead.calculateRange(var.arrayData.currentRange)
        # actualiza el rango para el sig.
        var.arrayData.setCurrentRange(calculatedRange)

    @_('')
    def seen_arr_dim2(self, p):
        var = dirFunc.getTempArrVar()
        intDimension = p[-1]
        # crea un nuevo nodo con los limites
        nodeHead = var.arrayData.createNode(intDimension)
        # calcula el rango del nodo actual
        calculatedRange = nodeHead.calculateRange(var.arrayData.currentRange)
        # actualiza el rango para el sig.
        var.arrayData.setCurrentRange(calculatedRange)
        return var

    @_('')
    def seen_arr_dim_end(self, p):
        var = dirFunc.getTempArrVar()
        nodesList = var.arrayData.nodesList

        Range = var.arrayData.currentRange
        # print('range', Range)
        Size = Range
        offSet = 0

        for node in nodesList:
            mDim = Range / node.limSup
            # print('M', mDim)
            node.setM(mDim)
            Range = mDim

        funcId = dirFunc.funcStack[-1]
        scope = dirFunc.dirFunciones[funcId].type
        # checa si la variable pertenece al scope global o local
        if scope == "PROGRAM":
            addrCounter.incrementGlobalAddr(Size, var.type)
        else:
            addrCounter.incrementLocalAddr(Size, var.type)

    # TIPO
    @_('INT', 'FLOAT', 'CHAR')
    def tipo(self, p):
        # p[-1] es el tipo de la listas de variables
        typeValue = p[0]
        # busca el tope del stack para ver la siguiente entrada
        if len(dirFunc.funcStack) > 0:
            funcId = dirFunc.funcStack[-1]
            dirFunc.dirFunciones[funcId].tablaVariables.setTempTypeValue(
                typeValue)
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
        con nombre funcName y tipo funcType
        '''

        funcName = p[-1]
        funcType = p[-3]

        if not dirFunc.isNameInDir(funcName):
            dirFunc.addFuncion(funcName, funcType)
            # agrega referencia a la tabla de variables global
            globalVarTable = dirFunc.getFuncion(
                dirFunc.programName).tablaVariables
            dirFunc.getFuncion(
                funcName).tablaVariables.setGlobalVarTable(globalVarTable)
            # revisa el tipo de función y verifica si debe agregar variable de retorno.
            if funcType != 'void':
                returnVarAddr = addrCounter.nextGlobalAddr(funcType)
                globalVarTable.addVar(
                    f"return_var_of:{funcName}", funcType, returnVarAddr)
            # saca el nombre de fucion anterior y agrega el nuevo a funcStack
            dirFunc.funcStack.pop()
            dirFunc.funcStack.append(funcName)
        else:
            raise Exception(
                f'ER-2: MultipleDeclaration: module {funcName} already defined.')
        pass

    @_('')
    def seen_func_end(self, p):
        # obtiene el num de vars locales y temps de esta funcion
        localVarCounts = addrCounter.getLocalAddrsCount()
        tmpVarCounts = addrCounter.getTmpAddrsCount()
        pointerVarCounts = addrCounter.getPointerAddrCount()

        # crea una instacia representativa del tamaño de la funcion
        funcSize = FuncSize()
        funcSize.addLocalVarCounts(localVarCounts)
        funcSize.addTempVarCounts(tmpVarCounts)
        funcSize.addPointerVarCounts(pointerVarCounts)

        # guarda el tamaña de la func en el dir de funciones
        funcId = dirFunc.funcStack[-1]
        dirFunc.getFuncion(funcId).setFuncSize(funcSize)

        # resetea las direciones locales y temporales
        addrCounter.resetLocalCounter()
        addrCounter.resetTemporalCounter()
        addrCounter.resetPointerCounter()

        # genera cuadruplo endfunc si funcion es tipo void
        if dirFunc.getFuncion(funcId).getType() == 'void':
            cuadruplos.createQuad('endfunc', None, None, None)
        return

    @_('vars seen_start_func bloque', 'seen_start_func bloque')
    def func_body(self, p): pass

    @_('')
    def seen_start_func(self, p):
        funcId = dirFunc.funcStack[-1]
        # agrega al dir de func el num de cuadruplo donde empieza la funcion
        dirFunc.getFuncion(funcId).setStartAddress(cuadruplos.counter)

    @_('tipo', 'VOID')
    def tipo_fun(self, p):
        return p[0]

    # PARAMETERS
    @_('tipo var seen_tipo_param "," params', 'tipo var seen_tipo_param', 'empty')
    def params(self, p): pass

    @_('')
    def seen_tipo_param(self, p):
        tipoParam, _, addr = p[-1]
        funcId = dirFunc.funcStack[-1]
        # agrega el tipo del parametro al signature de la funcion
        dirFunc.getFuncion(funcId).addParamToSig((tipoParam, addr))
        return

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
    @_('id_dim "=" expresion seen_asignacion ";"')
    def asignacion(self, p): pass

    @_('')
    def seen_asignacion(self, p):
        ID, _, _ = p[-3]
        # print(cuadruplos.pilaOperandos)
        exp, exp_tipo = cuadruplos.pilaOperandos.pop()
        var, var_tipo = cuadruplos.pilaOperandos.pop()
        asignacionType = cuboSemantico[(var_tipo, exp_tipo, '=')]
        if asignacionType != 'error':
            cuadruplos.createQuad('=', exp, None, var)
        else:
            raise Exception(
                f"ER-3: Type mismatch: {ID} of type {var_tipo} cannot match with {exp_tipo}")
        pass

    # ESCRITURA
    @_('WRITE "(" escritura1 ")" ";"')
    def escritura(self, p): pass

    @_('out seen_write "," escritura1', 'out seen_write')
    def escritura1(self, p): pass

    @_('')
    def seen_write(self, p):
        outVal = p[-1]
        cteAddr = None

        # checa si outVal es CTE_STRING
        if outVal and isinstance(outVal, str):
            if tablaCtes.isCteInTable(outVal):
                cteAddr = tablaCtes.getCte(outVal).getAddr()
            else:
                cteAddr = addrCounter.nextConstAddr('char')
                tablaCtes.addCte(outVal, cteAddr)
        else:
            exp, expTipo = cuadruplos.pilaOperandos.pop()
            cteAddr = exp

        cuadruplos.createQuad('print', None, None, cteAddr)

    @_('CTE_STRING', 'expresion')
    def out(self, p):
        # regresa o la cte string o None
        return p[0]

    # EXPRESION
    @_('logic_exp seen_rel_exp1',
       'logic_exp seen_rel_exp1 "|" seen_or_op expresion',
       )
    def expresion(self, p): pass

    @_('')
    def seen_rel_exp1(self, p):
        pilaOperadores = cuadruplos.pilaOperadores
        pilaOperandos = cuadruplos.pilaOperandos
        if len(pilaOperadores) > 0 and (pilaOperadores[-1] in set(['|'])):
            rightOperand, rightType = pilaOperandos.pop()
            leftOperand, leftType = pilaOperandos.pop()
            operator = pilaOperadores.pop()
            resultType = cuboSemantico[(leftType, rightType, operator)]
            if (resultType != 'error'):
                result = addrCounter.nextTemporalAddr(resultType)
                cuadruplos.createQuad(
                    operator, leftOperand, rightOperand, result)
                pilaOperandos.append((result, resultType))
            else:
                raise Exception('ER-3: Type mismatch')
        pass

    @_('')
    def seen_or_op(self, p):
        cuadruplos.pilaOperadores.append("|")

    @_('relation_exp seen_rel_exp2',
       'relation_exp seen_rel_exp2 "&" seen_and_op logic_exp',
       )
    def logic_exp(self, p): pass

    @_('')
    def seen_rel_exp2(self, p):
        pilaOperadores = cuadruplos.pilaOperadores
        pilaOperandos = cuadruplos.pilaOperandos
        if len(pilaOperadores) > 0 and (pilaOperadores[-1] in set(['&'])):
            rightOperand, rightType = pilaOperandos.pop()
            leftOperand, leftType = pilaOperandos.pop()
            operator = pilaOperadores.pop()
            resultType = cuboSemantico[(leftType, rightType, operator)]
            if (resultType != 'error'):
                result = addrCounter.nextTemporalAddr(resultType)
                cuadruplos.createQuad(
                    operator, leftOperand, rightOperand, result)
                pilaOperandos.append((result, resultType))
            else:
                raise Exception('ER-3: Type mismatch')
        pass

    @_('')
    def seen_and_op(self, p):
        cuadruplos.pilaOperadores.append("&")

    @_('exp seen_exp',
       'exp "<" seen_oper_menor exp seen_exp',
       'exp ">" seen_oper_mayor exp seen_exp',
       'exp LESSEQUAL seen_oper_menor_igual exp seen_exp',
       'exp GREATEREQUAL seen_oper_mayor_igual exp seen_exp',
       'exp EQUALS seen_oper_equals exp seen_exp',
       'exp NOTEQUAL seen_oper_notequal exp seen_exp',
       )
    def relation_exp(self, p): pass

    @_('')
    def seen_exp(self, p):
        pilaOperadores = cuadruplos.pilaOperadores
        pilaOperandos = cuadruplos.pilaOperandos
        # TODO: extract this to a function.
        if len(pilaOperadores) > 0 and (pilaOperadores[-1] in set(['<', '>', '==', '>=', '<=', '!='])):
            rightOperand, rightType = pilaOperandos.pop()
            leftOperand, leftType = pilaOperandos.pop()
            operator = pilaOperadores.pop()
            resultType = cuboSemantico[(leftType, rightType, operator)]
            if (resultType != 'error'):
                result = addrCounter.nextTemporalAddr(resultType)
                cuadruplos.createQuad(
                    operator, leftOperand, rightOperand, result)
                pilaOperandos.append((result, resultType))
            else:
                raise Exception('ER-3: Type mismatch')
        pass

    @_('')
    def seen_oper_menor(self, p):
        cuadruplos.pilaOperadores.append("<")

    @_('')
    def seen_oper_mayor(self, p):
        cuadruplos.pilaOperadores.append(">")
    
    @_('')
    def seen_oper_menor_igual(self, p):
        cuadruplos.pilaOperadores.append("<=")
    
    @_('')
    def seen_oper_mayor_igual(self, p):
        cuadruplos.pilaOperadores.append(">=")

    @_('')
    def seen_oper_equals(self, p):
        cuadruplos.pilaOperadores.append("==")
        
    @_('')
    def seen_oper_notequal(self, p):
        cuadruplos.pilaOperadores.append("!=")

    @_(
        'termino seen_termino "+" seen_oper_suma exp',
        'termino seen_termino "-" seen_oper_resta exp',
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
            if (resultType != 'error'):
                result = addrCounter.nextTemporalAddr(resultType)
                cuadruplos.createQuad(
                    operator, leftOperand, rightOperand, result)
                pilaOperandos.append((result, resultType))
            else:
                raise Exception('ER-3: Type mismatch')
        pass

    @_('')
    def seen_oper_suma(self, p):
        cuadruplos.pilaOperadores.append("+")

    @_('')
    def seen_oper_resta(self, p):
        cuadruplos.pilaOperadores.append("-")

    @_('factor seen_factor',
       'factor seen_factor "*" seen_oper_mult termino',
       'factor seen_factor "/" seen_oper_div termino',
       'factor seen_factor "%" seen_oper_mod termino',
       'factor seen_factor INTDIVISION seen_oper_intdiv termino'
       )
    def termino(self, p): pass

    @_('')
    def seen_factor(self, p):
        pilaOperadores = cuadruplos.pilaOperadores
        pilaOperandos = cuadruplos.pilaOperandos
        if len(pilaOperadores) > 0 and (pilaOperadores[-1] in set(['*', '/', '%', '//'])):
            rightOperand, rightType = pilaOperandos.pop()
            leftOperand, leftType = pilaOperandos.pop()
            operator = pilaOperadores.pop()
            resultType = cuboSemantico[(leftType, rightType, operator)]
            if (resultType != 'error'):
                result = addrCounter.nextTemporalAddr(resultType)
                cuadruplos.createQuad(
                    operator, leftOperand, rightOperand, result)
                pilaOperandos.append((result, resultType))
            else:
                raise Exception('ER-3: Type mismatch')
        pass

    @_('')
    def seen_oper_mult(self, p):
        cuadruplos.pilaOperadores.append("*")

    @_('')
    def seen_oper_div(self, p):
        cuadruplos.pilaOperadores.append("/")
        
    @_('')
    def seen_oper_mod(self, p):
        cuadruplos.pilaOperadores.append("%")
    
    @_('')
    def seen_oper_intdiv(self, p):
        cuadruplos.pilaOperadores.append("//")

    @_('"(" seen_left_paren expresion ")" seen_right_paren',
       'var_cte',
       '"+" var_cte',
       '"-" var_cte',
       )
    def factor(self, p): pass

    @_('')
    def seen_left_paren(self, p):
        cuadruplos.pilaOperadores.append("(")
        pass

    @_('')
    def seen_right_paren(self, p):
        cuadruplos.pilaOperadores.pop()
        pass

    @_('id_dim',
       'CTE_INT seen_int_cte',
       'CTE_FLOAT seen_float_cte',
       'call_fun'
       )
    def var_cte(self, p): pass

    @_(
        'ID',
        'ID "[" seen_array_access seen_left_paren expresion seen_access_exp "]" seen_right_bracket',
        'ID "[" seen_array_access seen_left_paren expresion seen_access_exp "]" "[" seen_access_next_dim expresion seen_access_exp "]" seen_right_bracket'
    )
    def id_dim(self, p):
        ID = p[0]
        funcId = dirFunc.funcStack[-1]
        varTable = dirFunc.getFuncion(funcId).tablaVariables
        varType = idAddr = None
        globalVarTable = dirFunc.getFuncion(dirFunc.programName).tablaVariables
        # checa si la variable esta en la tabla local o global
        if varTable.isVarInTable(ID):
            varObj = varTable.getVar(ID)
            varType = varObj.getType()
            idAddr = varObj.getAddr()
        elif globalVarTable.isVarInTable(ID):
            varObj = varTable.getGlobalVarTable().getVar(ID)
            varType = varObj.getType()
            idAddr = varObj.getAddr()
        else:
            raise Exception(f'Error: undefined variable {ID}.')
        
        # print('ID', ID, cuadruplos.pilaOperandos, p[0], len(p), len(p) == 1)
        
        # checa que la variable no sea un arreglo
        if len(p) == 1:
            cuadruplos.pilaOperandos.append((idAddr, varType))
        
        return (p[0], idAddr, varType)

    # 2
    @_('')
    def seen_array_access(self, p):
        # obtiene la variable del arreglo actual y la guarda en tempArrVar
        varName = p[-2]
        funcId = dirFunc.funcStack[-1]
        
        # obtiene la variable del arreglo actual
        var, _, _ = self.getVarInfo(funcId, varName)
        dirFunc.setTempArrVar(var)

        # define la primera dimesion
        var.arrayData.setCurrentDim(1)
    # 3
    @_('')
    def seen_access_exp(self, p):

        var = dirFunc.getTempArrVar()
        topOperand, _ = cuadruplos.pilaOperandos[-1]

        # obtener el nodo de la dimension actual
        currDim = var.arrayData.getCurrentDim()
        # print('NODES', var.arrayData.nodesList)
        # print('currDim', currDim)
        # print()
        node = var.arrayData.nodesList[currDim - 1]
        # obtener el limiteinf
        lowerLim = node.getLimiteInf()
        # otener el limite sup
        upperLim = node.getLimiteSup()

        # obtiene la addr de la tabla de ctes
        lowerLimAddr = self.getCteAddr(lowerLim)
        upperLimAddr = self.getCteAddr(upperLim)

        cuadruplos.createQuad("verify", topOperand, lowerLimAddr, upperLimAddr)
        if currDim < len(var.arrayData.nodesList):
            # obtiene la direccion del auxiliar
            aux, _ = cuadruplos.pilaOperandos.pop()
            # # obtiene la direccion del apuntador
            tJ = addrCounter.nextTemporalAddr(var.type)
            m = int(node.getM())
            # print('M', m)
            constantAddrM = self.getCteAddr(m)
            # genera cuadruplo de indexacion de dimensiones
            cuadruplos.createQuad('*', aux, constantAddrM, tJ)
            cuadruplos.pilaOperandos.append((tJ, var.type))
        if currDim > 1:
            # obtiene la direccion del auxiliar
            aux1, _ = cuadruplos.pilaOperandos.pop()
            aux2, _ = cuadruplos.pilaOperandos.pop()
            # # obtiene la direccion del apuntador
            tK = addrCounter.nextTemporalAddr(var.type)
            # genera cuadruplo de indexacion de dimensiones
            cuadruplos.createQuad('+', aux1, aux2, tK)
            cuadruplos.pilaOperandos.append((tK, var.type))
            
        pass
    # 4
    @_('')
    def seen_access_next_dim(self, p):
        var = dirFunc.getTempArrVar()
        currentDim = var.arrayData.getCurrentDim()
        var.arrayData.setCurrentDim(currentDim + 1)

    # 5
    @_('')
    def seen_right_bracket(self, p):
        # obtiene la variable temporal asignada al arreglo
        var = dirFunc.getTempArrVar()
        aux1, _ = cuadruplos.pilaOperandos.pop()
        
        # obtiene addr base del arreglo
        arrayBaseAddr = var.getAddr()
        # obtiene siguiete addr de tipo puntero
        pointerAddr = addrCounter.nextPointerAddr(var.type)
        
        # crear una instancia de Puntero para guardar addrs del arreglo
        newPointer = Pointer()
        newPointer.setBaseAddr(arrayBaseAddr)
        newPointer.setPointerAddr(pointerAddr)

        # calcula el valor constante de la dirección para usarse directamente (addr -> cte).
        cteAddr = self.getCteAddr(arrayBaseAddr)
        # print('cteAddr', cteAddr)
        cuadruplos.createQuad('+', aux1, cteAddr, pointerAddr)
        
        # introduce a la pila de operandos el objeto puntero
        cuadruplos.pilaOperandos.append((newPointer, var.type))
        # elimina el fake bottom.
        cuadruplos.pilaOperadores.pop()

    @_('')
    def seen_int_cte(self, p):
        cte = p[-1]
        cteAddr = None
        if tablaCtes.isCteInTable(cte):
            cteAddr = tablaCtes.getCte(cte).getAddr()
        else:
            cteAddr = addrCounter.nextConstAddr('int')
            tablaCtes.addCte(cte, cteAddr)
        cuadruplos.pilaOperandos.append((cteAddr, 'int'))
        pass

    @_('')
    def seen_float_cte(self, p):
        cte = p[-1]
        cteAddr = None
        if tablaCtes.isCteInTable(cte):
            cteAddr = tablaCtes.getCte(cte).getAddr()
        else:
            cteAddr = addrCounter.nextConstAddr('float')
            tablaCtes.addCte(cte, cteAddr)
        cuadruplos.pilaOperandos.append((cteAddr, 'float'))
        pass

    @_('ID seen_funcall_id "(" seen_left_paren seen_funcall_era call_fun1 ")" seen_right_paren seen_params_end seen_funcall_end')
    def call_fun(self, p): pass

    @_('')
    def seen_funcall_id(self, p):
        funcID = p[-1]
        if not dirFunc.isNameInDir(funcID):
            raise Exception(f'Error: function {funcID} is not declared.')
        else:
            tablaParams.setTempFuncId(funcID)
        pass

    @_('')
    def seen_funcall_era(self, p):
        funcId = tablaParams.tempFuncId
        cuadruplos.createQuad('era', None, None, funcId)
        return funcId

    @_('expresion seen_param_exp "," seen_next_param call_fun1', 'expresion seen_param_exp', 'empty')
    def call_fun1(self, p): pass

    @_('')
    def seen_param_exp(self, p):
        # get func id from seen_funcall_era
        funcId = tablaParams.tempFuncId
        exp, expType = cuadruplos.pilaOperandos.pop()
        counter = tablaParams.counterParams
        paramType, paramAddr = dirFunc.getFuncion(funcId).signature[counter]
        if paramType == expType:
            cuadruplos.createQuad('param', exp, None, paramAddr)
        else:
            raise Exception(
                f"Parameter mismatch: {expType} should match with {paramType} in {funcId} call."
            )
        pass

    @_('')
    def seen_next_param(self, p):
        tablaParams.setCounterParams(tablaParams.counterParams + 1)

    @_('')
    def seen_params_end(self, p):
        # obtiene el objeto de función a partir de call_fun1.
        funcId = tablaParams.tempFuncId
        func = dirFunc.getFuncion(funcId)
        signatureLength = len(func.signature)
        if not (signatureLength == tablaParams.counterParams == 0) and tablaParams.counterParams != signatureLength - 1:
            raise Exception(
                f'Function signature: {func.name} has incorrect no. of parameters')
        return func

    @_('')
    def seen_funcall_end(self, p):
        # obtiene el objeto de función a partir de call_fun1
        func = p[-1]
        # reinicia el contador de parámetros.
        tablaParams.setCounterParams(0)
        cuadruplos.createQuad('gosub', func.name, None, func.startAddress)
        if func.type != 'void':
            result = addrCounter.nextTemporalAddr(func.type)
            returnValueAddr = dirFunc.getFuncion(
                dirFunc.programName).tablaVariables.getVar(f"return_var_of:{func.name}").getAddr()
            cuadruplos.createQuad('=', returnValueAddr, None, result)
            cuadruplos.pilaOperandos.append((result, func.type))
        tablaParams.setTempFuncId(None)
        pass

    # RETURN
    @_('RETURN "(" expresion seen_return_exp ")" ";"')
    def _return(self, p): pass

    @_('')
    def seen_return_exp(self, p):
        funcId = dirFunc.funcStack[-1]
        func = dirFunc.getFuncion(funcId)
        if func.type == 'void':
            raise Exception(f'Function TypeMismatch: {funcId} cannot have a return statement.')
        
        exp, expType = cuadruplos.pilaOperandos.pop()
        
        # genera operacion de retorno
        cuadruplos.createQuad('return', None, None, exp)
        
        # genera operacion endfunc para funciones de tipo distinto a void
        cuadruplos.createQuad('endfunc', None, None, None)
        pass

    # VOID FUNC
    @_('call_fun ";"')
    def void_fun(self, p): pass

    # LECTURA
    @_('READ "(" lectura1 ")" ";"')
    def lectura(self, p): pass

    @_('id_dim seen_read "," lectura1', 'id_dim seen_read')
    def lectura1(self, p): pass

    @_('')
    def seen_read(self, p):
        idAddr, _ = cuadruplos.pilaOperandos.pop()
        cuadruplos.createQuad('read', None, None, idAddr)

    # CONDICION
    @_(
        'IF "(" expresion ")" seen_gotof THEN bloque seen_if_end',
        'IF "(" expresion ")" seen_gotof THEN bloque ELSE seen_goto bloque seen_if_end'
    )
    def condicion(self, p): pass

    @_('')
    def seen_gotof(self, p):
        print(cuadruplos.pilaOperandos)
        result, resultType = cuadruplos.pilaOperandos.pop()
        if resultType != 'boolean':
            raise Exception('Type mismatch.')
        else:
            cuadruplos.createQuad('gotof', result, None, None)
            cuadruplos.pilaSaltos.append(cuadruplos.counter - 1)
            pass

    @_('')
    def seen_goto(self, p):
        cuadruplos.createQuad('goto', None, None, None)
        falseJumpIndex = cuadruplos.pilaSaltos.pop()
        cuadruplos.pilaSaltos.append(cuadruplos.counter - 1)
        cuadruplos.fillQuadIndex(falseJumpIndex, cuadruplos.counter)

    @_('')
    def seen_if_end(self, p):
        endJumpIndex = cuadruplos.pilaSaltos.pop()
        cuadruplos.fillQuadIndex(endJumpIndex, cuadruplos.counter)

    # REPETICION
    @_('_while', '_for')
    def repeticion(self, p): pass

    @_('WHILE seen_while_start "(" expresion ")" seen_gotof DO bloque seen_while_end')
    def _while(self, p): pass

    @_('')
    def seen_while_start(self, p):
        cuadruplos.pilaSaltos.append(cuadruplos.counter)

    @_('')
    def seen_while_end(self, p):
        endIndex = cuadruplos.pilaSaltos.pop()
        returnIndex = cuadruplos.pilaSaltos.pop()
        cuadruplos.createQuad('goto', None, None, returnIndex)
        cuadruplos.fillQuadIndex(endIndex, cuadruplos.counter)

    @_('FOR id_dim seen_for_start "=" expresion seen_for_assign TO expresion seen_for_exp DO bloque seen_for_end')
    def _for(self, p): pass

    @_('')
    def seen_for_start(self, p):
        _, idAddr, expType = p[-1]
        if expType != 'int':
            raise Exception('Type mismatch')

    @_('')
    def seen_for_assign(self, p):
        exp, expType = cuadruplos.pilaOperandos.pop()
        id, idType = cuadruplos.pilaOperandos.pop()
        tipoRes = cuboSemantico[(idType, expType, '=')]
        if tipoRes != 'error':
            cuadruplos.createQuad('=', exp, None, id)
            return id
        else:
            raise Exception(
                f'Type mismatch: cannot initialize FOR with type {idType}')

    @_('')
    def seen_for_exp(self, p):
        exp, expType = cuadruplos.pilaOperandos[-1]
        if expType == 'int':
            exp2, exp2Type = cuadruplos.pilaOperandos.pop()
            # genera la dirección temporal para asignar el nuevo valor
            temporalFor = addrCounter.nextTemporalAddr('boolean')
            # asigna el cuadruplo de la expresion
            cuadruplos.createQuad(
                '<', p[-3], exp2, temporalFor)
            cuadruplos.pilaSaltos.append(cuadruplos.counter - 1)
            # asigna el cuadruplo de el salto
            cuadruplos.createQuad('gotof', temporalFor, None, None)
            cuadruplos.pilaSaltos.append(cuadruplos.counter - 1)

    @_('')
    def seen_for_end(self, p):
        vControl = p[-6]
        cteAddr = None
        if tablaCtes.isCteInTable(1):
            cteAddr = tablaCtes.getCte(1).getAddr()
        else:
            cteAddr = addrCounter.nextConstAddr('int')
            tablaCtes.addCte(1, cteAddr)
        cuadruplos.createQuad('+', vControl, cteAddr, vControl)
        finAddr = cuadruplos.pilaSaltos.pop()
        returnAddr = cuadruplos.pilaSaltos.pop()
        cuadruplos.createQuad('goto', None, None, returnAddr)
        cuadruplos.fillQuadIndex(finAddr, cuadruplos.counter)

    # MAIN
    @_('MAIN seen_main "(" ")" bloque seen_end_main')
    def main(self, p): pass

    @_('')
    def seen_main(self, p):
        # saca el nombre de funcion anterior
        # y define programName como la funcion actual en funcStack
        dirFunc.funcStack.pop()
        programName = dirFunc.programName
        dirFunc.funcStack.append(programName)

        # define goto a primera instruccion del main
        firstQuadIndex = cuadruplos.pilaSaltos.pop()
        cuadruplos.fillQuadIndex(firstQuadIndex, cuadruplos.counter)
        pass

    @_('')
    def seen_end_main(self, p):
        programName = dirFunc.funcStack.pop()

        # obtiene el numero de variables globales
        globalVarCounts = addrCounter.getGlobalCounts()
        # obtiene numero de variables temporales en main
        globalTmpVarCounts = addrCounter.getTmpAddrsCount()
        # obtiene el contador global de pointers
        globalPointerVarCounts = addrCounter.getPointerAddrCount()

        # crea una instancia FuncSize y definie contadores de vars
        funcSize = FuncSize()
        funcSize.addGlobalVarCounts(globalVarCounts)
        funcSize.addTempVarCounts(globalTmpVarCounts)
        # actualiza el contador global de pointers
        funcSize.addPointerVarCounts(globalPointerVarCounts)

        # guarda workspace de funcion global
        dirFunc.getFuncion(programName).setFuncSize(funcSize)

        # resetea las direciones locales y temporales
        addrCounter.resetTemporalCounter()
        addrCounter.resetGlobalCounts()
        addrCounter.resetPointerCounter()

        # genera cuadruplo end
        cuadruplos.createQuad('end', None, None, None)
        pass

    # ERROR
    def error(self, p):
        if p:
            print("Syntax error at token", p.type)
            print("no apropiado")
            print(p)
            # Just discard the token and tell the parser it's okay.
            # self.errok()
        else:
            print("Syntax error at EOF")

# @app.route('/compile/', methods=['POST'])
# def compile():
#     data = request.get_json()
#     inputText = data['program'].encode().decode()
    
#     parser = MyParser()
#     lexer = MyLexer()
#     # LEXER: Lexical Analysis
#     print('\n\nLEXER Analysis:')
#     tokens = lexer.tokenize(inputText)
#     for tok in tokens:
#         print('type=%r, value=%r' % (tok.type, tok.value))

#     # PARSER: Synctactic Analysis
#     print('\n\nPARSER Analysis:')
#     result = parser.parse(lexer.tokenize(inputText))
#     print(result)

#     # Print de pilas de cuadruplos
#     for i in range(len(cuadruplos.pilaCuadruplos)):
#         quad = cuadruplos.pilaCuadruplos[i]
#         print(f"{i+1}.- {quad}")
#     print('Pila operandos', cuadruplos.pilaOperandos)
#     print('Pila operadores', cuadruplos.pilaOperadores)
#     print('Pila de saltos', cuadruplos.pilaSaltos)
#     print()
#     print('---------TEST END---------')
#     print()

#     # EJECUCION
#     vm = VirtualMachine()
#     # vm recibe inputes necesarios para ejecucion
#     vm.setCuadruplos(cuadruplos.pilaCuadruplos)
#     vm.setTablaCtes(tablaCtes)
#     vm.setDirFunc(dirFunc)
#     # vm recibe rango de direcciones
#     baseAddrs = addrCounter.exportBaseAddrs()
#     vm.setAddrRange(baseAddrs)

#     print('---------START EXECUTION---------')
#     vm.run()

#     output = vm.getOutputStr()
#     return output

# if __name__ == '__main__':
#    app.run()


if __name__ == '__main__':
    parser = MyParser()
    lexer = MyLexer()
    # './test_sort/TestInsertionSort.txt'
    tests = ['./test_sort/TestInsertionSort.txt']
    for file in tests:
        testFilePath = os.path.abspath(f'test_files/{file}')
        inputFile = open(testFilePath, "r")
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

        # Print de pilas de cuadruplos
        for i in range(len(cuadruplos.pilaCuadruplos)):
            quad = cuadruplos.pilaCuadruplos[i]
            print(f"{i+1}.- {quad}")
        print('Pila operandos', cuadruplos.pilaOperandos)
        print('Pila operadores', cuadruplos.pilaOperadores)
        print('Pila de saltos', cuadruplos.pilaSaltos)
        print()
        print('---------TEST END---------')
        print()

        # EJECUCION
        vm = VirtualMachine()
        # vm recibe inputes necesarios para ejecucion
        vm.setCuadruplos(cuadruplos.pilaCuadruplos)
        vm.setTablaCtes(tablaCtes)
        vm.setDirFunc(dirFunc)
        # vm recibe rango de direcciones
        baseAddrs = addrCounter.exportBaseAddrs()
        vm.setAddrRange(baseAddrs)

        print('---------START EXECUTION---------')
        vm.run()
