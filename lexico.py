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

    def getChar(self):
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
        while (True):
            # Estado Inicial
            if estado == 1:
                car = self.getChar()
                if car is None:
                    return Token(TokenType.FIMARQ, '<eof>', self.linha)
                # Se o caracter for qualquer caracter de espaçamento
                elif re.match(r'\s', car):
                    if car == '\n':
                        self.linha = self.linha + 1
                # Se o caracter for parte do alfabeto, sem caracter especial (ç, ã, õ, etc)
                elif car.isalpha():
                    estado = 2
                # Se o caracter for um dígito 0-9
                elif car.isdigit():
                    estado = 3
                # ATRIB
                elif car == '=':
                    # Verifica se o igual é de igual ou de atribuição
                    lexema = lexema + car
                    car = self.getChar()
                    lexema = lexema + car
                    if lexema == '==':
                        return Token(TokenType.OPREL, lexema, self.linha)
                    else:
                        self.ungetChar(car)
                        lexema = '='
                        estado = 4
                # CADEIA
                elif car == '"':
                    estado = 5
                # OPREL
                elif car in {'>', '<'}:
                    estado = 6
                # OPAD
                elif re.match(r'[+-]', car):
                    estado = 7
                # OPMUL
                elif car == '*':
                    estado = 8
                # OPNEG
                elif car == '!':
                    estado = 9
                # PVIRG
                elif car == ';':
                    estado = 10
                # DPONTOS
                elif car == ':':
                    estado = 11
                # VIRG
                elif car == ',':
                    estado = 12
                # ABREPAR
                elif car == '(':
                    estado = 13
                # FECHAPAR
                elif car == ')':
                    estado = 14
                # ABRECH
                elif car == '{':
                    estado = 15
                # FECHACH
                elif car == '}':
                    estado = 16
                # Verificar comentário
                elif car == '/':
                    estado = 17

            elif estado == 2:
                # Estado que trata nomes
                lexema = lexema + car
                car = self.getChar()
                if car is None or (not car.isalnum()):
                    self.ungetChar(car)
                    # Se não for palavra reservada, então é ID
                    if lexema in Lexico.reservadas:
                        return Token(Lexico.reservadas[lexema], lexema, self.linha)
                    else:
                        return Token(TokenType.ID, lexema, self.linha)

            elif estado == 3:
                # Estado que trata números
                lexema = lexema + car
                car = self.getChar()
                if car == '.' and lexema.__contains__('.'):
                    self.ungetChar(car)
                    return Token(TokenType.ERROR, lexema, self.linha)
                if car is None or not car.isdigit() and car != '.':
                    self.ungetChar(car)
                    return Token(TokenType.CTE, lexema, self.linha)

            elif estado == 4:
                return Token(TokenType.ATRIB, lexema, self.linha)

            elif estado == 5:
                # Estado que trata cadeias
                lexema = lexema + car
                car = self.getChar()

                if car is None:
                    return Token(TokenType.ERROR, lexema, self.linha)
                if car == '"':
                    lexema = lexema + car
                    return Token(TokenType.CADEIA, lexema, self.linha)

            elif estado == 6:
                lexema = lexema + car
                car = self.getChar()
                if car not in {'>', '<', '='}:
                    self.ungetChar(car)
                    return Token(TokenType.OPREL, lexema, self.linha)
                else:
                    lexema = lexema + car
                    if lexema in {'==', '<=', '>=', '<>'}:
                        return Token(TokenType.OPREL, lexema, self.linha)
                    else:
                        return Token(TokenType.ERROR, lexema, self.linha)

            elif estado == 7:
                lexema = lexema + car
                return Token(TokenType.OPAD, lexema, self.linha)

            elif estado == 8:
                lexema = lexema + car
                return Token(TokenType.OPMUL, lexema, self.linha)

            elif estado == 9:
                lexema = lexema + car
                return Token(TokenType.OPNEG, lexema, self.linha)

            elif estado == 10:
                lexema = lexema + car
                return Token(TokenType.PVIRG, lexema, self.linha)

            elif estado == 11:
                lexema = lexema + car
                return Token(TokenType.DPONTOS, lexema, self.linha)

            elif estado == 12:
                lexema = lexema + car
                return Token(TokenType.VIRG, lexema, self.linha)

            elif estado == 13:
                lexema = lexema + car
                return Token(TokenType.ABREPAR, lexema, self.linha)

            elif estado == 14:
                lexema = lexema + car
                return Token(TokenType.FECHAPAR, lexema, self.linha)

            elif estado == 15:
                lexema = lexema + car
                return Token(TokenType.ABRECH, lexema, self.linha)

            elif estado == 16:
                lexema = lexema + car
                return Token(TokenType.FECHACH, lexema, self.linha)
            # Tratando '/'. Se o próximo token for diferente de / ou *, então o / é uma divisão, não um comentário.
            elif estado == 17:
                lexema = lexema + car
                car = self.getChar()
                if car is None or not re.match(r'[/*]', car):
                    self.ungetChar(car)
                    estado = 8
                elif car == '/':
                    estado = 18
                else:
                    estado = 19
            # Se for um comentário inline
            elif estado == 18:
                car = self.getChar()
                if car is None:
                    return Token(TokenType.FIMARQ, '<eof>', self.linha)
                # Se o caracter for qualquer caracter de espaçamento
                elif re.match(r'\s', car):
                    if car == '\n':
                        self.linha = self.linha + 1
                        lexema = ''
                        estado = 1
            # Se for um comentário em bloco
            elif estado == 19:
                lexema = lexema + car
                car = self.getChar()
                if car is None:
                    return Token(TokenType.FIMARQ, '<eof>', self.linha)
                # Se o caracter for qualquer caracter de espaçamento
                elif re.match(r'\s', car):
                    if car == '\n':
                        self.linha = self.linha + 1
                # Se achou o fim do comentário, retorna pro estado 1
                elif re.search(r'([*]/)$', lexema):
                    lexema = ''
                    estado = 1

if __name__== "__main__":

   #nome = input("Entre com o nome do arquivo: ")
   nome = './testes/exemplo2.txt'
   lex = Lexico(nome)
   lex.abreArquivo()

   while(True):
       token = lex.getToken()
       print("token= %s , lexema= (%s), linha= %d" % (token.msg, token.lexema, token.linha))
       if token.const == TokenType.FIMARQ[0]:
           break
   lex.fechaArquivo()
