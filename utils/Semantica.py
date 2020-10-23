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
            'constAddr': {
                'int': 11000,
                'float': 12000,
                'char': 13000
            }
        }

        self.counter = copy.deepcopy(self.baseAddr)

    def nextGlobalAddr(self, typeVar):
        nextAddr = self.__getNextAddr('globalAddr', typeVar)
        return nextAddr

    def nextLocalAddr(self, typeVar):
        nextAddr = self.__getNextAddr('localAddr', typeVar)
        return nextAddr

    def nextTemporalAddr(self, typeVar):
        nextAddr = self.__getNextAddr('temporalAddr', typeVar)
        return nextAddr

    def nextConstAddr(self, typeVar):
        nextAddr = self.__getNextAddr('constAddr', typeVar)
        return nextAddr

    def __getNextAddr(self, scope, typeVar):
        nextAddr = self.counter[scope][typeVar]
        self.counter[scope][typeVar] = nextAddr + 1
        return nextAddr

    def resetLocalCounter(self):
        self.counter['localAddr']['int'] = self.baseAddr['localAddr']['int']
        self.counter['localAddr']['float'] = self.baseAddr['localAddr'][
            'float']
        self.counter['localAddr']['char'] = self.baseAddr['localAddr']['char']
        return
