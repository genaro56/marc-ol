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
        self.tablaVariables = TablaDeVars()

    def setType(self, typeValue):
        self.type = typeValue

    def setName(self, name):
        self.name = name


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
        
    def getType(self):
        return self.type

    def setType(self, typeValue):
        self.type = typeValue

    def setName(self, name):
        self.name = name

    def setScope(self, scope):
        self.scope = scope


class TablaDeVars:
    def __init__(self):
        self.varsTable = dict()
        self.tempTypeValue = ''
        self.globalVarTable = None

    def addVar(self, name, typeValue, addr = None):
        var = Var()
        var.setName(name)
        var.setType(typeValue)
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

