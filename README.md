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

- Faltantes: 
  - Expresiones no lineales para ciclo FOR y WHILE.

- Correcciones:
  - Cambiar la forma en que se obtiene la tabla global ya que en main no funciona pues no tiene su tabla global, utilizar una variable que no existe en ese scope es "incachable".

### - Avance no. 4:

- Se agrego el goto al MAIN

- Se agrego tabla de constantes.
  - En la tabla de constantes se almacena el valor y la direccion.
  - El parser primero valida si la constante ya se encuentra en la tabla, en caso contrario agrega la constante a la tabla.

- Se agrego una estructura que almacena el signature de la funcion.
  - unicamente almacena los tipos e.g ['int', 'int', 'float']
  
- Se agregaron los contadores de variables locales y temporales para las funciones. 
  - El proposito de estos contadores es servir como referencia del tamaño del workspace de la funcion.
  - Estos datos se utilizaran para definir la operacion ERA size

- Se agrego clase FuncSize que almacena los contadores y podra contener funciones para calcular el tamaño.

- Se agrego cuadruplo 'endfunc' al terminar una funcion

### - Avance no. 5:

- Se agregó la acción de 'END' para el programa.

- Se agregaron contadores de variables globales y funcionalidad para exportar el los rangos de direcciones.

- Se agregó una clase VirtualMachine para realizar el proceso de ejecución.

- Se implemento clase Memoria para realizar los procesos de gestion de direcciones.

- Se agregaron operaciones aritmeticas en funcion de ejecución (+, -, *, /).

- Se agregaron las operaciones para hacer 'PRINT' y 'READ' en ejecución. 

### - Avance no, 6:

- Ejecución
  - Se agregaron las acciones: (ERA, PARAM, RETURN, ENDFUNC, GOSUB) y su ejecución.
  - Se agregaron las operacion no-lineales (if, else, while y for).
  - Ejecución de operaciones relacionales (>, <, |, &).
  - Se modificó el RETURN para generar las llamadas recursivas.
- BUGS
  - Correción de asignación de memoria en semántica.
- IN PROGRESS
  - Arrays: Nos falta corregir un bug para la ejecución.

### - Avance no. 7:
- Ejecución
  - Se agrego la ejecucion de las siguientes operaciones (>=, <=, //, %)
  - Se actualizó la operacion de 'read' para que se puedera leer del teclado y guardar en dirección de puntero.
  - Se agregaron pruebas que evaluan lo sugiente:
    - factorial recursivo/iterativo
    - fibonacci recursivo/iterativo
    - multiplicación de matrices
    - binary search
    - bubble sort
  - Se corrigieron los bugs relacionados con apuntadores y la gestión de memoria.
- Parsing
  - Se agregaron comentarios de documentación al archivo parser.py
- Integracion
  - Se agrego un endpoint con Flask para poder interactuar con la interfaz gráfica.
- DONE:
  - Interfaz - Se esta trabajando la generación de codigo con la herramienta open source Blockly
  
- Estado del proyecto: TERMINADO
