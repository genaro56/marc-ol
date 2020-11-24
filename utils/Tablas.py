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
        """ Crear una nueva Funcion
            name - nombre de la funcion
            typeValue - tipo de la funcion    
        """
        func = Funcion()
        func.setName(name)
        func.setType(typeValue)
        self.dirFunciones[name] = func

    def getFuncion(self, name):
        """ Regresa la funcion
            name - nombre de la funcion
        """
        return self.dirFunciones[name]

    def setTempArrVar(self, var):
        """ Define la propiedad tempArrVar con una variable temporal
            var - variable
        """
        self.tempArrVar = var

    def getTempArrVar(self):
        """ Regresa el valor de getTempArrVar """
        return self.tempArrVar

    def isNameInDir(self, name):
        """ regresa un booleano indicando si name esta en el directorio
            name - nombre de la funcion
        """
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
        """ Define el tipo de la funcion
            typeValue - tipo
        """
        self.type = typeValue

    def getType(self):
        """ Regresa el tipo de la funcion """
        return self.type
    
    def setName(self, name):
        """ Define el nombre de la funcion 
            name - nombre de la funcion
        """
        self.name = name

    def addParamToSig(self, param):
        """ Agrega el tipo del param a lista signature
            param - tipo del param
        """
        self.signature.append(param)

    def setFuncSize(self, funcSize):
        """ Define el tamaño de la funcion
            funcSize - objeto representativo del tamaño de la funcion
        """
        self.funcSize = funcSize

    def setStartCuadCounter(self, counter):
        """ Define el indice del cuadruplo de inicio
            counter - indice del cuadruplo inicial
        """
        self.startCuadCounter = counter

    def getStartCuadCounter(self):
        """ Regresa el indice del primer cuadruplo """
        return self.startCuadCounter

    def setStartAddress(self, cuadAddr):
        """ Define el indice del cuadruplo de inicio
            cuadAddr - indice del cuadruplo inicial
        """
        self.startAddress = cuadAddr


class FuncSize:
    """
    Mantiene el numero total de variables
    globales, temporles, locales y punteros
    utilizados en una funcion.
    """
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
        """ Agrega el conteo de variables globales 
            counts - conteo de variables
        """
        self.funcVarCounts['global'] = counts

    def getGlobalVarCounts(self):
        """ Regresa el conteo de variables globales """
        return self.funcVarCounts['global']

    def addLocalVarCounts(self, counts):
        """ Agrega el conteo de variables locales 
            counts - conteo de variables
        """
        self.funcVarCounts['local'] = counts

    def getLocalVarCounts(self):
        """ Regresa el conteo de variables locales """
        return self.funcVarCounts['local']

    def addTempVarCounts(self, counts):
        """ Agrega el conteo de variables temporales 
            counts - conteo de variables
        """
        self.funcVarCounts['temporal'] = counts

    def getTempVarCounts(self):
        """ Regresa el conteo de variables temporales """
        return self.funcVarCounts['temporal']
    
    def addPointerVarCounts(self, counts):
        """ Agrega el conteo de apuntadores
            counts - conteo de variables
        """
        self.funcVarCounts['pointer'] = counts
        
    def getPointerVarCounts(self):
        """ Regresa el conteo de punteros"""
        return self.funcVarCounts['pointer'] 

    def getTotalVarCounts(self):
        """ Regresa el total de variables de cada tipo"""
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
        """ Regresa el tipo de la variable """
        return self.type

    def setType(self, typeValue):
        """ Define el tipo de la variable
            typeValue - tipo de la variable
        """
        self.type = typeValue

    def setName(self, name):
        """ Define el nombre de la variable
            name - nombre de la variable
        """
        self.name = name

    def setScope(self, scope):
        """ Define el scope de la variable
            scope - scope de la variable
        """
        self.scope = scope

    def setAddr(self, addr):
        """ Define la direccion de la variable
            addr - direccion
        """
        self.addr = addr

    def setIsArray(self, isArr):
        """ Indica si la variable es un arreglo
            isArr - boolean indicando si es arreglo
        """
        self.isArray = isArr

    def initArray(self):
        """ Crea una instancia de objecto Array """
        self.arrayData = Array()

    def getAddr(self):
        """ Regresa la direccion de la variable """
        return self.addr


class TablaDeVars:
    '''
    TablaDeVars - representa la tabla de variables perteneciente
    a una Funcion. Mantiene un diccionario que mapea el nombre de la 
    variable al objeto Var
    '''
    
    def __init__(self):
        self.varsTable = dict()
        self.tempTypeValue = ''
        self.globalVarTable = None

    def addVar(self, name, typeValue, addr=None):
        """ Agregar una nueva variable a la tabla
            name - nombre de la variable
            typeValue - tipo de la variable
            addr - direccion de la variable
        """
        var = Var()
        var.setName(name)
        var.setType(typeValue)
        if addr:
            var.setAddr(addr)
        self.varsTable[name] = var

    def setTempTypeValue(self, valueType):
        """ Define la propiedad tempTypeValue
            valueType - tipo de la ultima variable indentificada
        """
        self.tempTypeValue = valueType

    def getTempTypeValue(self):
        """ Regresa tempTypeValue """
        return self.tempTypeValue

    def getVar(self, name):
        """ Regresa la variable 
            name - nombre de la variable
        """
        return self.varsTable[name]

    def isVarInTable(self, name):
        """ Checa si la variable esta en la tabla
            name - nombre de la variable
        """
        return name in self.varsTable

    def isVarInGlobalTable(self, name):
        """ Checa si la variable esta en la tabla global
            name - nombre de la variable
        """
        return name in self.globalVarTable.varsTable

    def setGlobalVarTable(self, globalVarTable):
        """ Guarda la referencia a la tabla de variables global
            globalVarTable - referencia a tabla de variables global
        """
        self.globalVarTable = globalVarTable

    def getGlobalVarTable(self):
        """ Regresa la referencia de la tabla de variables global """
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
        """ Checa si la constante esta en la tabla
            constant - valor de la constante
        """
        return constant in self.cteToAddrMap

    def addCte(self, valor, addr):
        """ Agrega una constante a la tabla
            valor - valor de la constante
            addr - direccion de la constante
        """
        newCte = Cte()
        newCte.setValor(valor)
        newCte.setAddr(addr)

        self.cteToAddrMap[valor] = newCte
        self.addrToCteMap[addr] = newCte

    def getCte(self, constant):
        """ Regresa un objecto tipo Cte
            constant - valor de la constante
        """
        return self.cteToAddrMap[constant]

    def getCteFromAddr(self, addr):
        """ Regresa un objecto tipo Cte
            addr - direccion de la constante
        """
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
        """ Define el valor de la constante
            valor - valor de la constante
        """
        self.valor = valor

    def getValor(self):
        """ Regresa el valor de la constante """
        return self.valor

    def setAddr(self, addr):
        """ Define la direccion de la constante
            addr - direccion de la constante
        """
        self.addr = addr

    def getAddr(self):
        """ Regresa la direccion de la constante """
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
        """ Mantiene el contadore del numero de parametros 
            valor - valor del contador
        """
        self.counterParams = valor

    def generateEraSize(self, size):
        """ Guarda el tamaño de la funcion 
            size - tamanio funcion
        """
        self.eraSize = size

    def setTempFuncId(self, tempId):
        """ el nombre de la funcion a la que pertenecen los params 
            tempId - nombre de la funcion
        """
        self.tempFuncId = tempId

    def setAddr(self, addr):
        """ Guarda la direccion del parametro 
            addr - direccion
        """
        self.addr = addr

    def getAddr(self):
        """ Regresa la direccion del parametro """
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
        """ Define el valor de la M 
            m - valor de m
        """
        self.m = m

    def getM(self):
        """ Regresa el valor de la M """
        return self.m

    def setLimiteInf(self, inf):
        """ Define el limite inferior 
            inf - limite inferior
        """
        self.limInf = inf
        
    def getLimiteInf(self):
        """ Regresa el limite inferior """
        return self.limInf

    def setLimiteSup(self, sup):
        """ Define el limite superior 
            sup - limite superior
        """
        self.limSup = sup
        
    def getLimiteSup(self):
        """ Regresa el limite superior """
        return self.limSup

    def setDimension(self, dim):
        """ Define la dimension actual 
            dim - valor dimension
        """
        self.dimension = dim

    def setRange(self, r):
        """ Define el rango
            r - rango
        """
        self.range = r

    def calculateRange(self, currentRange):
        """ Cualcula y regresa el nuevo rango
            currentRange - valor del rango actual
        """
        _range = (self.limSup * currentRange)
        self.setRange(_range)
        return _range


class Array:
    def __init__(self):
        self.nodesList = []
        self.currentRange = 1
        self.currentDim = 1

    def setCurrentDim(self, dim):
        """ Define la dimension actual
            dim - valor del rango actual
        """
        self.currentDim = dim
        
    def getCurrentDim(self):
        """ Regresa la dimension actual """
        return self.currentDim

    def setCurrentRange(self, _range):
        """ Define el valor de rango 
            _range - rango
        """
        self.currentRange = _range

    def createNode(self, intDimension):
        """ Crea un nuevo Node y lo agrega a la lista 
            intDimension - limite superior
        """
        node = Node()
        node.setLimiteInf(0)
        node.setLimiteSup(intDimension)
        self.nodesList.append(node)
        return node

    def addNode(self, node):
        """ Agrega un nuevo nodo a la lista 
            node - nodo
        """
        self.nodeListHead.append(node)

class Pointer:
    """
    Representa un puntero y almacena la direccion
    del puntero y direccion inicial de arreglo a la que
    pertenece
    """
    
    def __init__(self):
        self.baseAddr = None
        self.pointerAddr = None
    
    def getPointerAddr(self):
        """ Regrea la direccion del puntero """
        return self.pointerAddr
    
    def setPointerAddr(self, addr):
        """ Define la direccion del puntero 
            addr - direccion
        """
        self.pointerAddr = addr
        
    def setBaseAddr(self, addr):
        """ Define la direccion base del arreglo
            a la que pertenece el puntero 
            addr - direccion
        """
        self.baseAddr = addr
        
    def getBaseAddr(self):
        """ Regresa la direccion base del
            arreglo a la que pertenece el puntero
        """
        return self.baseAddr