class DirFunciones:
    '''
    Directorio de funciones - matiene
    * dict con key (funcName), value(Funcion)
    * referencia a tabla de variables global
    '''

    def __init__(self):
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

    def addVar(self, name, typeValue, addr = None):
        var = Var()
        var.setName(name)
        var.setType(typeValue)
        self.varsTable[name] = var
    
    def setTempTypeValue(self, valueType):
        self.tempTypeValue = valueType
    
    def getTempTypeValue(self):
        return self.tempTypeValue
    
    def getVar(self, name, scope):
        return self.varsTable[name]

    def isVarInTable(self, name):
        return name in self.varsTable
        
