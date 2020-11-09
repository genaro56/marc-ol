import itertools
import json

operadores = [
    # artimeticos
    '+',
    '-',
    '*',
    '/',
    '%',
    '**',
    '//',
    # relacionales
    '==',
    '!=',
    '>',
    '<',
    '>=',
    '<=',
    # logicos
    '&',
    '|',
    '!',
    # asignacion
    '='
]

# tips de datos
types = ['int', 'char', 'float', 'boolean']

pyRelativOpMap = {'&': 'and', '|': 'or', '!': 'not'}

typeExampleVals = {
    'int': '1',
    'char': "'a'",
    'float': '0.5',
    'boolean': 'True'
}

boolOps = set([
    '&',
    '|',
    '==',
    '!=',
])

combinaciones = []

for item in itertools.product(types, repeat=2):
    for operador in operadores:
        op1, op2 = item
        result = ''
        try:
            # define la asignacion de tipos iguales como del mismo tipo
            if operador == '=' and op1 == op2:
                result = op1
            # esto es porque python permite and y or con tipos enteros y chars
            elif operador in set(
                ['&', '|']) and not (op1 == 'boolean' and op2 == 'boolean'):
                result = 'error'
            # cualquier exp entre un bool y otro tipo deberia dar error
            elif (op1 == 'boolean'
                  and op2 != 'boolean') or (op1 != 'boolean'
                                            and op2 == 'boolean'):
                result = 'error'
            # si operandos son bool y el operador no esta en boolOps es error
            elif (op1 == 'boolean' and op2 == 'boolean') and (operador
                                                              not in boolOps):
                result = 'error'
            # mutiplicacion entre char e int es error
            elif (op1 == 'char'
                  and op2 == 'int') or (op1 == 'int'
                                        and op2 == 'char') and operador == '*':
                result = 'error'
            # division entre tipos enteros es int
            elif (op1 == op2 == 'int') and operador == '/':
                result = 'int'
            else:
                exOper1 = typeExampleVals[op1]
                exOper2 = typeExampleVals[op2]

                pyOper = pyRelativOpMap[
                    operador] if operador in pyRelativOpMap else operador

                exp = exOper1 + ' ' + pyOper + ' ' + exOper2
                r = eval(exp)
                typeName = str(type(r).__name__)

                if typeName == 'bool':
                    result = 'boolean'
                elif typeName == 'str':
                    result = 'char'
                else:
                    result = typeName
        except:
            result = 'error'
        comb = {
            "operand1": op1,
            "operand2": op2,
            "operator": operador,
            "result": result
        }
        combinaciones.append(comb)

with open('./auto_generated_combs.json', 'w', newline='') as json_file:
    json.dump(combinaciones, json_file)
