class DirFunciones:
    '''
    Directorio de funciones - matiene 
    * dict con key (funcName), value(Funcion)
    * referencia a tabla de variables global
    '''
    def __init__(self):
        self.tablaGlobal = None
        self.dirFunciones = dict()

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
    mantiene las propiedades de cada funcion y una referncia
    a su tabla de variables
    '''
    def __init__(self):
        self.name = ''
        self.type = ''
        self.tablaVariables = None

    def setType(self, typeValue):
        self.type = typeValue

    def setName(self, name):
        self.name = name