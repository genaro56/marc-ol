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
        self.tablaVariables = TablaDeVars()

    def setType(self, typeValue):
        self.type = typeValue

    def setName(self, name):
        self.name = name
        
    def addParamToSig(self, param):
        self.signature.append(param)


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
        self.tablaCte = dict()

    def isCteInTable(self, constant):
        return constant in self.tablaCte

    def addCte(self, valor, addr):
        newCte = Cte()
        newCte.setValor(valor)
        newCte.setAddr(addr)
        self.tablaCte[valor] = newCte

    def getCte(self, constant):
        return self.tablaCte[constant]


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