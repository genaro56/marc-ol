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

- Se creó una tabla de variables tanto Global como para cada función.
  - Esta tabla de variables utiliza el ID de cada variable para indexar la entrada en el diccionario.

- Desarrollo de cubo semántico para correlacionar operadores y su validez en la semántica.
