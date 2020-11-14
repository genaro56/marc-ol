from collections import Counter


class DirFunciones:
    '''
    Directorio de funciones - matiene
    * dict con key (funcName), value(Funcion)
    * referencia a tabla de variables global
    '''

    def __init__(self):
        self.programName = None
        self.tablaGlobal = TablaDeVars()
        self.dirFunciones = dict()
        self.funcStack = []
        self.tempArrVar = None

    def addFuncion(self, name, typeValue):

        func = Funcion()
        func.setName(name)
        func.setType(typeValue)
        self.dirFunciones[name] = func

    def getFuncion(self, name):
        return self.dirFunciones[name]

    def setTempArrVar(self, var):
        self.tempArrVar = var

    def getTempArrVar(self):
        return self.tempArrVar

    def isNameInDir(self, name):
        return name in self.dirFunciones


class Funcion:
    '''
    Funcion - representa una entrada del directorio de funciones
    mantiene las propiedades de cada funcion y una referencia
    a su tabla de variables
    '''

    def __init__(self):
        self.name = ''
        self.type = ''
        self.signature = []
        self.funcSize = None
        self.tablaVariables = TablaDeVars()
        self.startAddress = None

    def setType(self, typeValue):
        self.type = typeValue

    def setName(self, name):
        self.name = name

    def addParamToSig(self, param):
        self.signature.append(param)

    def setFuncSize(self, funcSize):
        self.funcSize = funcSize

    def setStartCuadCounter(self, counter):
        self.startCuadCounter = counter

    def getStartCuadCounter(self):
        return self.startCuadCounter

    def setStartAddress(self, cuadAddr):
        self.startAddress = cuadAddr


class FuncSize:
    def __init__(self):
        self.funcVarCounts = {
            'global': {
                'int': 0,
                'float': 0,
                'char': 0
            },
            'local': {
                'int': 0,
                'float': 0,
                'char': 0
            },
            'temporal': {
                'int': 0,
                'float': 0,
                'char': 0,
                'boolean': 0
            },
            'pointer': {
                'int': 0,
                'float': 0,
                'char': 0,
                'boolean': 0
            }
        }

    def addGlobalVarCounts(self, counts):
        self.funcVarCounts['global'] = counts

    def getGlobalVarCounts(self):
        return self.funcVarCounts['global']

    def addLocalVarCounts(self, counts):
        self.funcVarCounts['local'] = counts

    def getLocalVarCounts(self):
        return self.funcVarCounts['local']

    def addTempVarCounts(self, counts):
        self.funcVarCounts['temporal'] = counts

    def getTempVarCounts(self):
        return self.funcVarCounts['temporal']
    
    def addPointerVarCounts(self, counts):
        self.funcVarCounts['pointer'] = counts
        
    def getPointerVarCounts(self):
        return self.funcVarCounts['pointer'] 

    def getTotalVarCounts(self):
        globalCounts = self.funcVarCounts['global']
        localCounts = self.funcVarCounts['local']
        temporalCounts = self.funcVarCounts['temporal']
        return dict(
            Counter(globalCounts) + Counter(localCounts) +
            Counter(temporalCounts))


class Var():
    '''
    Var - representa una entrada del directorio de funciones
    mantiene las propiedades de cada funcion y una referncia
    a su tabla de variables
    '''

    def __init__(self):
        self.name = ''
        self.type = ''
        self.scope = ''
        self.addr = None
        self.arrayData = None
        self.isArray = False

    def getType(self):
        return self.type

    def setType(self, typeValue):
        self.type = typeValue

    def setName(self, name):
        self.name = name

    def setScope(self, scope):
        self.scope = scope

    def setAddr(self, addr):
        self.addr = addr

    def setIsArray(self, isArr):
        self.isArray = isArr

    def initArray(self):
        self.arrayData = Array()

    def getAddr(self):
        return self.addr


class TablaDeVars:
    def __init__(self):
        self.varsTable = dict()
        self.tempTypeValue = ''
        self.globalVarTable = None

    def addVar(self, name, typeValue, addr=None):
        var = Var()
        var.setName(name)
        var.setType(typeValue)
        if addr:
            var.setAddr(addr)
        self.varsTable[name] = var

    def setTempTypeValue(self, valueType):
        self.tempTypeValue = valueType

    def getTempTypeValue(self):
        return self.tempTypeValue

    def getVar(self, name):
        return self.varsTable[name]

    def isVarInTable(self, name):
        return name in self.varsTable

    def isVarInGlobalTable(self, name):
        return name in self.globalVarTable.varsTable

    def setGlobalVarTable(self, globalVarTable):
        self.globalVarTable = globalVarTable

    def getGlobalVarTable(self):
        return self.globalVarTable


class TablaCtes:
    '''
    Tabla de constantes, crea un mapa de
    valor de constante a objeto Cte
    '''

    def __init__(self):
        self.cteToAddrMap = dict()
        self.addrToCteMap = dict()

    def isCteInTable(self, constant):
        return constant in self.cteToAddrMap

    def addCte(self, valor, addr):
        newCte = Cte()
        newCte.setValor(valor)
        newCte.setAddr(addr)

        self.cteToAddrMap[valor] = newCte
        self.addrToCteMap[addr] = newCte

    def getCte(self, constant):
        return self.cteToAddrMap[constant]

    def getCteFromAddr(self, addr):
        return self.addrToCteMap[addr]


class Cte:
    '''
    Representa una constante, mantiene el 
    valor y la direccion de la constante
    '''

    def __init__(self):
        self.valor = None
        self.addr = None

    def setValor(self, valor):
        self.valor = valor

    def getValor(self):
        return self.valor

    def setAddr(self, addr):
        self.addr = addr

    def getAddr(self):
        return self.addr


class TablaParams:
    '''
    Tabla de parámetros - crea un mapa de parámetros para
    cada llamada de función, instanciando las direcciones
    de memoria de cada param para ejecutarlo en cuadruplos.
    '''

    def __init__(self):
        self.tablaParams = dict()
        self.counterParams = 0
        self.eraSize = None
        self.tempFuncId = None

    def setCounterParams(self, valor):
        self.counterParams = valor

    def generateEraSize(self, size):
        self.eraSize = size

    def setTempFuncId(self, tempId):
        self.tempFuncId = tempId

    def setAddr(self, addr):
        self.addr = addr

    def getAddr(self):
        return self.addr


class Node():
    '''
    Clase principal para generar el nodo de un arreglo
    y guardar información sobre sus dimensiones.
    '''

    def __init__(self):
        # límites del arreglo
        self.limInf = None
        self.limSup = None
        self.addr = None
        self.range = 1
        self.dimension = 1
        self.m = None

    def setM(self, m):
        self.m = m

    def getM(self):
        return self.m

    def setLimiteInf(self, inf):
        self.limInf = inf
        
    def getLimiteInf(self):
        return self.limInf

    def setLimiteSup(self, sup):
        self.limSup = sup
        
    def getLimiteSup(self):
        return self.limSup

    def setDimension(self, dim):
        self.dimension = dim

    def setRange(self, r):
        self.range = r

    def calculateRange(self, currentRange):
        _range = (self.limSup * currentRange)
        self.setRange(_range)
        return _range


class Array:
    def __init__(self):
        self.nodesList = []
        self.currentRange = 1
        self.currentDim = 1

    def setCurrentDim(self, dim):
        self.currentDim = dim
        
    def getCurrentDim(self):
        return self.currentDim

    def setCurrentRange(self, _range):
        self.currentRange = _range

    def createNode(self, intDimension):
        node = Node()
        node.setLimiteInf(0)
        node.setLimiteSup(intDimension)
        self.nodesList.append(node)
        return node

    def addNode(self, node):
        self.nodeListHead.append(node)

class Pointer:
    def __init__(self):
        self.pointerAddr = None
    
    def getPointerAddr(self):
        return self.pointerAddr
    
    def setPointerAddr(self, addr):
        self.pointerAddr = addr