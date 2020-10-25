# *par_plus_plus*

## Autores:

Genaro Martínez | A01566055

Ariel Méndez | A01020690

## Historial de Avances

### - Avance no. 1:

- Se agregaron las expresiones regulares necesarias en lexer.py así como la definición de las reglas gramaticales en parser.py para cumplir con la semántica inicial del lenguaje Par++;

- El archivo de prueba TestProgram.txt contiene un código de prueba para probar la sintaxis.

- Los resultados de esta prueba son 0 shift/reduce conflicts, 0 reduce/reduce conflicts y un parsing apropiado de todos los estatutos.

- Junto con esto también adjuntamos la definición del cubo semántico que se puede examinar en el directorio utils.

### - Avance no. 2:

- Desarrollo de cubo semántico para correlacionar operadores y su validez en la semántica.

- Se creó una tabla de variables tanto Global como para cada función.
  - Esta tabla de variables utiliza el ID de cada variable para indexar la entrada en el diccionario.
  - Utiliza una subclase Var que sería utilizada para declarar atributos principales de una variable (tipo, id)

- Creación del directorio de funciones que alberga el registro de cada función en un diccionario.
  - Utiliza una subclase Funcion pues sería utilizada para declarar atributos principales de una función (tipo, id, tabla de vars)

### - Avance no. 3:

- Desarrollo de la clase Cuadruplos (operaciones aritméticas, expresiones lógicas y expresiones no-lineales)
  - Contiene métodos y atributos útiles para 
    la generación de cuadruplos, cuya función 
    es validar la lógica de operadores y de expresiones.
  - Desarrollo de pilas (Operadores, Operandos, Cuadruplos y Saltos).

- Se crearon las direcciones de memoria para cada variable (temporales, locales, constantes, globales)
  - Cada rango de memoria está distribuido de tal suerte que el compilador pueda albergar rangos de 2mil a 3mil variables
    por scope.
  - Utiliza métodos útiles para manipular la memoria y generar los cuadruplos con sus ids únicos.

