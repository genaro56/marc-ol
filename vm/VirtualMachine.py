class VirtualMachine:
    """
    Maquina virtual realiza proceso de ejecucion
    """
    def __init__(self):
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
        print('in vm', self.addrRange)

    def run(self):
        print('main execution function...')
        
class Memoria:
    def __init__(self):
        super().__init__()
        
    def getValue(self):
        pass
    
    def saveValue(self):
        pass
