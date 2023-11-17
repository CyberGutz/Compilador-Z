import re
from os import path


class TokenType:
    ID = (1, 'identificador')
    CTE = (2, 'constante numérica')
    PROGRAM = (3, 'program')
    VAR = (4, 'var')
    INT = (5, 'int')
    REAL = (6, 'real')
    BOOL = (7, 'bool')
    CHAR = (8, 'char')
    IF = (9, 'if')
    ELSE = (10, 'else')
    WHILE = (11, 'while')
    READ = (12, 'read')
    WRITE = (13, 'write')
    FALSE = (14, 'false')
    TRUE = (15, 'true')
    CADEIA = (16, 'string')
    ATRIB = (17, '=')
    OPREL = (18, 'operações relacionais: == , < , > , <= , >= , <>')
    OPAD = (19, '+, -')
    OPMUL = (20, '*, /')
    OPNEG = (21, '!')
    PVIRG = (22, ';')
    DPONTOS = (23, ':')
    VIRG = (24, ',')
    ABREPAR = (25, '(')
    FECHAPAR = (26, ')')
    ABRECH = (27, '{')
    FECHACH = (28, '}')
    ERROR = (29, 'erro')
    FIMARQ = (30, 'fim-de-arquivo')


class Token:
    def __init__(self, tipo, lexema, linha):
        self.tipo = tipo
        (const, msg) = tipo
        self.const = const
        self.msg = msg
        self.lexema = lexema
        self.linha = linha


class Lexico:
    reservadas = {
        'program': TokenType.PROGRAM,
        'var': TokenType.VAR,
        'int': TokenType.INT,
        'real': TokenType.REAL,
        'bool': TokenType.BOOL,
        'char': TokenType.CHAR,
        'if': TokenType.IF,
        'else': TokenType.ELSE,
        'while': TokenType.WHILE,
        'read': TokenType.READ,
        'write': TokenType.WRITE,
        'false': TokenType.FALSE,
        'true': TokenType.TRUE
    }

    def __init__(self, nomeArquivo):
        self.linha = None
        self.buffer = None
        self.nomeArquivo = nomeArquivo
        self.arquivo = None

    def abreArquivo(self):
        if self.arquivo is not None:
            print('ERRO: Arquivo já aberto')
            quit()
        elif path.exists(self.nomeArquivo):
            self.arquivo = open(self.nomeArquivo, "r")
            self.buffer = ''
            self.linha = 1
        else:
            print('ERRO: Arquivo {} inexistente'.format(self.nomeArquivo))
            quit()

    def fechaArquivo(self):
        if self.arquivo is None:
            print('ERRO: Não há arquivo aberto')
            quit()
        else:
            self.arquivo.close()

    def getchar(self):
        if self.arquivo is None:
            print('ERRO: Não há arquivo aberto')
            quit()
        elif len(self.buffer) > 0:
            c = self.buffer[0]
            self.buffer = self.buffer[1:]
            return c
        else:
            c = self.arquivo.read(1)
            if len(c) == 0:
                return None
            else:
                return c.lower()

    def ungetChar(self, c):
        if c is not None:
            self.buffer = self.buffer + c

    def getToken(self):
        lexema = ''
        estado = 1
        car = None
        while(True):
            if estado == 1:
                car = self.getChar()
                if car is None:
                    return Token(TokenType.FIMARQ, '<eof>', self.linha)
                elif re.match(r'\s', car):
                    if car == '\n':
                        self.linha = self.linha + 1
                elif car.isalpha():
                    estado = 2
                elif car.isdigit():
                    estado = 3
                elif re.match(r'[=/+*()]', car):
                    estado = 4
                elif car == '#':
                    estado = 5
