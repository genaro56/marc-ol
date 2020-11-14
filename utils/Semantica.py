import copy
import json
import os
from collections import namedtuple


class CuboSemantico:
    def __init__(self, filePath):

        with open(filePath, 'r') as file:
            combinaciones = json.load(file)
            self.cuboSemantico = self.__buildCuboSematico(combinaciones)

    def __buildCuboSematico(self, combinaciones):
        TypeMatch = namedtuple('TypeMatch',
                               ['operand1', 'operand2', 'operator'])

        combDict = dict()
        for comb in combinaciones:
            typeMatch = TypeMatch(operand1=comb['operand1'],
                                  operand2=comb['operand2'],
                                  operator=comb['operator'])
            combDict[typeMatch] = comb['result']
        return combDict

    def getCuboSemantico(self):
        return self.cuboSemantico


class AddrGenerator:
    '''
    Asigna las direcciones de variables
    globales, locales, temporales y constantes
    '''
    def __init__(self):

        self.baseAddr = {
            'globalAddr': {
                'int': 1000,
                'float': 2000,
                'char': 3000
            },
            'localAddr': {
                'int': 4000,
                'float': 5000,
                'char': 6000
            },
            'temporalAddr': {
                'int': 7000,
                'float': 8000,
                'char': 9000,
                'boolean': 10000
            },
            'pointerAddr': {
                'int': 11000,
                'float': 12000,
                'char': 13000,
                'boolean': 14000
            },
            'constAddr': {
                'int': 15000,
                'float': 16000,
                'char': 17000
            }
        }

        self.globalCounts = {'int': 0, 'float': 0, 'char': 0}
        self.localCounts = {'int': 0, 'float': 0, 'char': 0}
        self.temporalCounts = {'int': 0, 'float': 0, 'char': 0, 'boolean': 0}
        self.pointerCounts = {'int': 0, 'float': 0, 'char': 0, 'boolean': 0}
        self.arrAddrCounter = 0
        self.counter = copy.deepcopy(self.baseAddr)
        
    def exportBaseAddrs(self):
        return copy.deepcopy(self.baseAddr)

    def nextGlobalAddr(self, typeVar):
        self.globalCounts[typeVar] += 1
        nextAddr = self.__getNextAddr('globalAddr', typeVar)
        return nextAddr

    def nextLocalAddr(self, typeVar):
        self.localCounts[typeVar] += 1
        nextAddr = self.__getNextAddr('localAddr', typeVar)
        return nextAddr

    def nextTemporalAddr(self, typeVar):
        self.temporalCounts[typeVar] += 1
        nextAddr = self.__getNextAddr('temporalAddr', typeVar)
        return nextAddr
        
    def nextPointerAddr(self, typeVar):
        self.pointerCounts[typeVar] += 1
        nextAddr = self.__getNextAddr('pointerAddr', typeVar)
        return nextAddr

    def nextConstAddr(self, typeVar):
        nextAddr = self.__getNextAddr('constAddr', typeVar)
        return nextAddr

    def __getNextAddr(self, scope, typeVar):
        nextAddr = self.counter[scope][typeVar]
        self.counter[scope][typeVar] = nextAddr + 1
        return nextAddr
    
    def __incrementCounter(self, scope, typeVar, count):
        self.counter[scope][typeVar] += count
    
    def incrementGlobalAddr(self, count, typeVar):
        self.globalCounts[typeVar] += count
        self.__incrementCounter('globalAddr', typeVar, count)
    
    def incrementLocalAddr(self, count, typeVar):
        self.localCounts[typeVar] += count
        self.__incrementCounter('localAddr', typeVar, count)
    
    def incrementTemporalAddr(self, count, typeVar):
        self.temporalCounts[typeVar] += count
        self.__incrementCounter('temporalAddr', typeVar, count)

    def getGlobalCounts(self):
        return self.globalCounts

    def getLocalAddrsCount(self):
        return self.localCounts

    def getTmpAddrsCount(self):
        return self.temporalCounts
    
    def getPointerAddrCount(self):
        return self.pointerCounts
    
    def resetGlobalCounts(self):
        self.__resetCounter('globalAddr')
        # reset counts de global vars a 0
        self.globalCounts = self.__getBaseCounts(self.globalCounts)
        return

    def resetLocalCounter(self):
        self.__resetCounter('localAddr')
        # reset counts de local vars a 0
        self.localCounts = self.__getBaseCounts(self.localCounts)
        return

    def resetTemporalCounter(self):
        self.__resetCounter('temporalAddr', hasBool=True)
        # reset counts de tmp vars a 0
        self.temporalCounts = self.__getBaseCounts(self.temporalCounts)
        return

    def resetPointerCounter(self):
        self.__resetCounter('pointerAddr', hasBool=True)
        # reset counts de tmp vars a 0
        self.pointerCounts = self.__getBaseCounts(self.pointerCounts)
        return

    def __resetCounter(self, addrType, hasBool=False):
        self.counter[addrType]['int'] = self.baseAddr[addrType]['int']
        self.counter[addrType]['float'] = self.baseAddr[addrType]['float']
        self.counter[addrType]['char'] = self.baseAddr[addrType]['char']
        if hasBool:
            # reset las dir de var temporales booleanas
            self.counter[addrType]['boolean'] = self.baseAddr[addrType][
                'boolean']
        return

    def __getBaseCounts(self, countsDict):
        return dict.fromkeys(countsDict, 0)