from sly import Lexer


class MyLexer(Lexer):
    literals = {
        # bloques
        '(', ')',
        '{', '}',
        # separadores
        ',', ':',
        # delimitantes
        ';',
        # asignacion
        '=',
        # expresiones aritmeticas
        '*', '/', '-', '+',
        # condicionales
        '&', '|',
        '>', '<'
    }

    tokens = {
        ID,
        CTE_STRING, CTE_FLOAT, CTE_INT,
        IF, ELSE,
        INT, FLOAT,
        PROGRAM,
        VAR, EQUALS, FROM, DO, THEN, MODULE,
        FOR, WHILE, 
        READ, WRITE,
        MAIN, RETURN
    }

    ignore = ' \t'
    EQUALS = r'=='

    @_(r'\d+\.\d+')
    def CTE_FLOAT(self, t):
        t.value = float(t.value)
        return t

    @_(r'\d+')
    def CTE_INT(self, t):
        t.value = int(t.value)
        return t

    @_(r'\".*?\"')
    def CTE_STRING(self, t):
        return t

    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['if'] = IF
    ID['else'] = ELSE

    ID['int'] = INT
    ID['float'] = FLOAT

    ID['program'] = PROGRAM
    ID['var'] = VAR

    ID['main'] = MAIN
    ID['read'] = READ
    ID['write'] = WRITE
    ID['return'] = RETURN

    ID['while'] = WHILE
    ID['for'] = FOR

    ID['from'] = FROM
    ID['do'] = DO
    ID['then'] = THEN
    ID['module'] = MODULE

    # Line number tracking
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1
    ignore_comment = r'\#.*'


if __name__ == '__main__':
    lexer = MyLexer()
    env = {}
    while True:
        try:
            text = input('basic > ')
        except EOFError:
            break
        if text:
            lex = lexer.tokenize(text)
            for token in lex:
                print(token)
