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

    def addFuncion(self, name, typeValue):

        func = Funcion()
        func.setName(name)
        func.setType(typeValue)
        self.dirFunciones[name] = func

    def getFuncion(self, name):
        return self.dirFunciones[name]

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
        self.startCuadCounter = None
        self.tablaVariables = TablaDeVars()

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
            }
        }

    def addGlobalVarCounts(self, counts):
        self.funcVarCounts['global'] = counts

    def addLocalVarCounts(self, counts):
        self.funcVarCounts['local'] = counts

    def addTempVarCounts(self, counts):
        self.funcVarCounts['temporal'] = counts

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