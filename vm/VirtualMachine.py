class VirtualMachine:
    """
    Maquina virtual realiza proceso de ejecucion
    """
    def __init__(self):
        # instruction pointer
        self.ip = 0
        self.cuadruplos = None
        self.tablaCtes = None
        self.dirFunc = None
        self.addrRange = None

    def setCuadruplos(self, cuadruplos):
        self.cuadruplos = cuadruplos

    def setTablaCtes(self, tablaCtes):
        self.tablaCtes = tablaCtes

    def setDirFunc(self, dirFunc):
        self.dirFunc = dirFunc

    def setAddrRange(self, addrRange):
        self.addrRange = addrRange

    def run(self):

        progName = self.dirFunc.programName
        mainFunc = self.dirFunc.getFuncion(progName)
        mainFuncSize = mainFunc.funcSize
        # se crea instancia con tamaño de funcion global
        memoriaGlobal = Memoria(mainFuncSize, self.addrRange, self.tablaCtes)

        while True:
            operacion, arg1Addr, arg2Addr, resultAddr = self.cuadruplos[
                self.ip]
            if operacion == 'goto':
                self.ip = resultAddr
            elif operacion == '+':
                operand1Val = memoriaGlobal.getValue(arg1Addr)
                operand2Val = memoriaGlobal.getValue(arg2Addr)
                result = operand1Val + operand2Val
                memoriaGlobal.saveValue(resultAddr, result)
                break


class Memoria:
    def __init__(self, funcSize, addrRange, cteTable):

        self.addrRange = addrRange
        self.cteTable = cteTable
        self.baseCteAddr = self.__getBaseCteAddr(addrRange)

        totalVarCounts = funcSize.getTotalVarCounts()
        # define el numero de variables de cada tipo
        intCount = totalVarCounts['int'] if 'int' in totalVarCounts else 0
        floatCount = totalVarCounts['float'] if 'float' in totalVarCounts else 0
        charCount = totalVarCounts['char'] if 'char' in totalVarCounts else 0
        booleanCount = totalVarCounts[
            'boolean'] if 'boolean' in totalVarCounts else 0

        self.bloqueInts = [None] * intCount
        self.bloqueFloats = [None] * floatCount
        self.bloqueChar = [None] * charCount
        self.bloqueBooleans = [None] * booleanCount

        self.typeToBlockMap = {
            'int': self.bloqueInts,
            'float': self.bloqueFloats,
            'char': self.bloqueChar,
            'boolean': self.bloqueBooleans
        }

    def __getBaseCteAddr(self, addrRange):
        return addrRange['constAddr']['int']

    def getValue(self, addr):
        # si la addr es una constante, obten el valor de tabla cte
        if addr >= self.baseCteAddr:
            return self.cteTable.getCteFromAddr(addr).getValor()
        addrType, base = self.__getAddrTypeInfo(addr)
        memoryBlock = self.typeToBlockMap[addrType]
        return memoryBlock[addr - base]

    def saveValue(self, addr, value):
        addrType, base = self.__getAddrTypeInfo(addr)
        memoryBlock = self.typeToBlockMap[addrType]
        memoryBlock[addr - base] = value

    # regresar tipo y addr base
    def __getAddrTypeInfo(self, addr):
        lastType = ''
        lastBase = None
        found = False
        result = ()
        for scope, addrBlock in self.addrRange.items():
            for addrType, base in addrBlock.items():
                if addr < base:
                    result = (lastType, lastBase)
                    found = True
                    break
                else:
                    lastType = addrType
                    lastBase = base
            if found:
                break

        if not found:
            print('Addr not foud')
        return result
