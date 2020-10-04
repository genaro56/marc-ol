import json
import os
from collections import namedtuple


class CuboSemantico:
    cuboSemantico = dict()

    def __init__(self):

        path = os.getcwd()
        filePath = path + '/utils/combinaciones.json'

        with open(filePath, 'r') as file:
            combinaciones = json.load(file)
            self.cuboSemantico = self.__buildCuboSematico(combinaciones)

    def __buildCuboSematico(self, combinaciones):
        TypeMatch = namedtuple(
            'TypeMatch', ['operand1', 'operand2', 'operator'])

        combDict = dict()
        for comb in combinaciones:
            typeMatch = TypeMatch(
                operand1=comb['operand1'], operand2=comb['operand2'], operator=comb['operator'])
            combDict[typeMatch] = comb['result']
        return combDict