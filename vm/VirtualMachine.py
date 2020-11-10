from types import SimpleNamespace


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

    def __getValueFromMemory(self, addr, memoriaGlobal, memoriaStack,
                             cteTable):
        # checa si addr esta en rango de constantes
        if addr >= self.addrRange['constAddr']['int']:
            return self.tablaCtes.getCteFromAddr(addr).getValor()
        # checa si addr esta en rango de globales
        elif addr < self.addrRange['localAddr']['int']:
            return memoriaGlobal.getValue(addr)
        # addr tiene que estar en rango de locales o temporales
        else:
            return memoriaStack.getValue(addr)

    def __getMemoryToSaveVal(self, addr, memoriaGlobal, memoriaStack):
        # checa si addr esta en rango de globales
        if addr < self.addrRange['localAddr']['int']:
            return memoriaGlobal
        # addr tiene que estar en rango de locales o temporales
        else:
            return memoriaStack

    def __generateArithmeticOp(
        self,
        arg1Addr,
        arg2Addr,
        memoriaStack,
        memoriaGlobal,
        resultAddr,
        operator,
    ):
        # obtiene el valor de las addrs
        operand1Val = self.__getValueFromMemory(arg1Addr, memoriaGlobal,
                                                memoriaStack, self.tablaCtes)
        operand2Val = self.__getValueFromMemory(arg2Addr, memoriaGlobal,
                                                memoriaStack, self.tablaCtes)

        # ejecuta la operacion
        result = eval(f"{operand1Val} {operator} {operand2Val}")

        # guarda el valor en memoria
        memoria = self.__getMemoryToSaveVal(resultAddr, memoriaGlobal,
                                            memoriaStack)
        memoria.saveValue(resultAddr, result)

    def run(self):

        progName = self.dirFunc.programName
        mainFunc = self.dirFunc.getFuncion(progName)
        mainFuncSize = mainFunc.funcSize

        stackEjecucion = []

        # se crea instancia con tamaño de funcion global
        memoriaGlobal = Memoria('global', mainFuncSize, self.addrRange)

        # la variable memoriaStack mantendra la referencia de la memoria activa en SS
        memoriaStack = memoriaGlobal

        while True:

            operacion, arg1Addr, arg2Addr, resultAddr = self.cuadruplos[
                self.ip]
            if operacion == 'goto':
                self.ip = resultAddr
            elif operacion == 'era':
                # nombre de la funcion
                funcId = resultAddr

                # obtiene la funcion del dirFunc
                func = self.dirFunc.getFuncion(funcId)

                # obtiene el tamaño de la funcion
                funcSize = func.funcSize

                # crea instancia de memoria local
                memoriaLocal = Memoria('local', funcSize, self.addrRange)

                # se guarda el apuntador de memoria en el stack de ejecucion
                memInfo = SimpleNamespace(lastMemory=memoriaStack,
                                          funcId=funcId,
                                          newMemory=memoriaLocal)
                stackEjecucion.append(memInfo)
                self.ip += 1
            elif operacion == 'param':
                # obtiene el valor de arg1Addr
                operand1Val = self.__getValueFromMemory(
                    arg1Addr, memoriaGlobal, memoriaStack, self.tablaCtes)

                # define memoria con instancia de memoria de la funcion
                memoria = stackEjecucion[-1].newMemory

                memoria.saveValue(resultAddr, operand1Val)
                self.ip += 1
            elif operacion == 'gosub':
                # cambia el apuntador de memoria a la nueva memoria local
                memoriaStack = stackEjecucion[-1].newMemory

                # guardar ip junto con el ultimo activation record (memoria)
                stackEjecucion[-1].ip = self.ip + 1

                # cambiar ip a dir inicial de funcion
                self.ip = resultAddr
            elif operacion == 'return':
                # obtiene el valor de retorno
                resultVal = self.__getValueFromMemory(resultAddr,
                                                      memoriaGlobal,
                                                      memoriaStack,
                                                      self.tablaCtes)

                # construye nombre de global var de la funcion
                funcId = stackEjecucion[-1].funcId
                funcVarName = f"return_var_of:{funcId}"

                # obtiene la addr de global var de la funcion
                globalFuncVarAddr = self.dirFunc.getFuncion(
                    progName).tablaVariables.getVar(funcVarName).getAddr()

                # guarda el resultado en global var de la funcion
                memoriaGlobal.saveValue(globalFuncVarAddr, resultVal)
                self.ip += 1
            elif operacion == 'endfunc':
                # cambiar el apuntador de memoria (prior to call)
                memInfo = stackEjecucion.pop()
                memoriaStack = memInfo.lastMemory

                # cambiar ip (prior to the call)
                self.ip = memInfo.ip
            elif operacion == "gotof":
                # obtiene el valor de las addrs
                operand1Val = self.__getValueFromMemory(
                    arg1Addr, memoriaGlobal, memoriaStack, self.tablaCtes)

                # si la condicion es falsa saltar bloque
                if not operand1Val:
                    self.ip = resultAddr
                else:
                    # incrementa el ip
                    self.ip += 1
            elif operacion == "<":
                self.__generateArithmeticOp(arg1Addr, arg2Addr, memoriaStack,
                                            memoriaGlobal, resultAddr, '<')
                
                # incrementa el ip
                self.ip += 1
            elif operacion == '=':
                operand1Val = self.__getValueFromMemory(
                    arg1Addr, memoriaGlobal, memoriaStack, self.tablaCtes)
                memoria = self.__getMemoryToSaveVal(resultAddr, memoriaGlobal,
                                                    memoriaStack)
                memoria.saveValue(resultAddr, operand1Val)
                self.ip += 1
            elif operacion == '+':
                self.__generateArithmeticOp(arg1Addr, arg2Addr, memoriaStack,
                                            memoriaGlobal, resultAddr, '+')
                # incrementa el ip
                self.ip += 1
            elif operacion == '-':
                # obtiene el valor de las addrs
                self.__generateArithmeticOp(arg1Addr, arg2Addr, memoriaStack,
                                            memoriaGlobal, resultAddr, '-')
                # incrementa el ip
                self.ip += 1
            elif operacion == '*':
                self.__generateArithmeticOp(arg1Addr, arg2Addr, memoriaStack,
                                            memoriaGlobal, resultAddr, '*')
                # incrementa el ip
                self.ip += 1
            elif operacion == '/':
                self.__generateArithmeticOp(arg1Addr, arg2Addr, memoriaStack,
                                            memoriaGlobal, resultAddr, '/')
                # incrementa el ip
                self.ip += 1
            elif operacion == 'print':
                resultVal = self.__getValueFromMemory(resultAddr,
                                                      memoriaGlobal,
                                                      memoriaStack,
                                                      self.tablaCtes)
                print('PRINTING... ', resultVal)

                self.ip += 1
            elif operacion == 'read':
                # resultVal = self.__getValueFromMemory(
                #     resultAddr, memoriaGlobal, memoriaStack, self.tablaCtes
                # )
                print('READING... ')
                readValue = input()
                memoria.saveValue(resultAddr, readValue)
                self.ip += 1
            elif operacion == 'end':
                print('Fin Ejecucion')
                break


class Memoria:
    def __init__(self, memType, funcSize, addrRange):

        self.memType = memType
        self.addrRange = addrRange
        self.typeToBlockMap = self.__buildMemoryBlocks(funcSize)
        # print('Memory block generated', self.typeToBlockMap)

    def __buildMemoryBlocks(self, funcSize):
        memoryBlock = dict()
        if self.memType == 'global':
            memoryBlock['globalAddr'] = self.__getScopeBlock(
                funcSize, 'global')
        elif self.memType == 'local':
            memoryBlock['localAddr'] = self.__getScopeBlock(funcSize, 'local')

        memoryBlock['temporalAddr'] = self.__getScopeBlock(
            funcSize, 'temporal')
        return memoryBlock

    def __getScopeBlock(self, funcSize, scope):

        varCounts = None
        if scope == 'global':
            varCounts = funcSize.getGlobalVarCounts()
        elif scope == 'local':
            varCounts = funcSize.getLocalVarCounts()
        elif scope == 'temporal':
            varCounts = funcSize.getTempVarCounts()

        # define el numero de variables de cada tipo
        intCount = varCounts['int'] if 'int' in varCounts else 0
        floatCount = varCounts['float'] if 'float' in varCounts else 0
        charCount = varCounts['char'] if 'char' in varCounts else 0
        booleanCount = varCounts['boolean'] if 'boolean' in varCounts else 0

        # se crean bloques de memoria del tamaño definido por el era de la funcion
        bloqueInts = [None] * intCount
        bloqueFloats = [None] * floatCount
        bloqueChar = [None] * charCount
        bloqueBooleans = [None] * booleanCount

        typeToBlockMap = {
            'int': bloqueInts,
            'float': bloqueFloats,
            'char': bloqueChar,
            'boolean': bloqueBooleans
        }

        return typeToBlockMap

    def getValue(self, addr):
        scope, addrType, base = self.__getAddrTypeInfo(addr)
        memoryBlock = self.typeToBlockMap[scope][addrType]
        return memoryBlock[addr - base]

    def saveValue(self, addr, value):
        scope, addrType, base = self.__getAddrTypeInfo(addr)
        # print(scope, addrType, addr, base, value)
        memoryBlock = self.typeToBlockMap[scope][addrType]
        memoryBlock[addr - base] = value

    # regresar tipo y addr base
    def __getAddrTypeInfo(self, addr):
        lastScope = 'globalAddr'
        lastType = ''
        lastBase = None
        found = False
        result = ()
        for scope, addrBlock in self.addrRange.items():
            for addrType, base in addrBlock.items():
                if addr < base:
                    result = (lastScope, lastType, lastBase)
                    found = True
                    break
                else:
                    lastType = addrType
                    lastBase = base
            if found:
                break
            lastScope = scope

        if not found:
            raise Exception(f"Address {addr} not found")
        return result
