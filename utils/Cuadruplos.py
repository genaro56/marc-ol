class Cuadruplos:
    def __init__(self):
        self.pilaOperandos = []
        self.pilaOperadores = []
        self.pilaSaltos = []
        self.pilaCuadruplos = []
        self.pilaAsignacionFor = []
        self.counter = 0

    # actualiza el contador
    def setCounter(self, newCounter):
        self.counter = newCounter

    # crea un nuevo cuadruplo y actualiza el contador
    def createQuad(self, op1, op2, op3, res):
        self.pilaCuadruplos.append((op1, op2, op3, res))
        self.setCounter(self.counter+1)

    # agrega el salto pendiente al cuadruplo
    def fillQuadIndex(self, previousJumpIndex, currentCounter):
        op1, op2, _, _ = self.pilaCuadruplos[previousJumpIndex]
        self.pilaCuadruplos[previousJumpIndex] = (
            op1, op2, None, currentCounter
        )
