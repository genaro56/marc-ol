class DirFunciones:
    def __init__(self):
        self.tablaGlobal = None
        self.dirFunciones = dict()

    def addFuncion(self, name, typeValue):

        func = Funcion()
        func.setType(typeValue)

        self.dirFunciones[name] = func
        
    def getFuncion(self, name):
        return self.dirFunciones[name]


class Funcion:
    def __init__(self):
        self.name = ''
        self.type = ''
        self.tablaVariables = None

    def setType(self, typeValue):
        self.type = typeValue