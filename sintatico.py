from lexico import TokenType as tt
from lexico import Token
from lexico import Lexico


class Sintatico:
    def __init__(self):
        self.lex = None
        self.tokenAtual = None

    def interprete(self, path):
        if self.lex is not None:
            print('ERRO: Já existe um arquivo sendo processado.')
        else:
            self.lex = Lexico(path)
            self.lex.abreArquivo()
            self.tokenAtual = self.lex.getToken()

            self.PROG()
            self.consome(tt.FIMARQ)
            self.lex.fechaArquivo()

    def atualIgual(self, token):
        (const, msg) = token
        return self.tokenAtual.const == const

    def consome(self, token):
        if self.atualIgual(token):
            self.tokenAtual = self.lex.getToken()
        else:
            (const, msg) = token
            print('ERRO DE SINTAXE [linha {}]: era esperado {} mas veio {}'.format(self.tokenAtual.linha, msg,
                                                                                   self.tokenAtual.lexema))
            quit()

    def PROG(self):
        self.consome(tt.PROGRAM)
        self.consome(tt.ID)
        self.consome(tt.PVIRG)
        self.DECLS()
        self.C_COMP()

    def DECLS(self):
        if self.atualIgual(tt.VAR):
            self.consome(tt.VAR)
            self.LIST_DECLS()
        else:
            pass

    def LIST_DECLS(self):
        self.DECL_TIPO()
        self.D()

    def D(self):
        # Para implementar vazio, verifica o token no first da função, se for aquilo, vai para função específica, se não, passa
        # First(LIST_DECLS) = id
        if self.atualIgual(tt.ID):
            self.LIST_DECLS()
        else:
            pass

    def DECL_TIPO(self):
        self.LIST_ID()
        self.consome(tt.DPONTOS)
        self.TIPO()
        self.consome(tt.PVIRG)

    def LIST_ID(self):
        self.consome(tt.ID)
        self.E()

    def E(self):
        if self.atualIgual(tt.VIRG):
            self.consome(tt.VIRG)
            self.LIST_ID()
        else:
            pass

    def TIPO(self):
        if self.atualIgual(tt.INT):
            self.consome(tt.INT)
        if self.atualIgual(tt.REAL):
            self.consome(tt.REAL)
        if self.atualIgual(tt.BOOL):
            self.consome(tt.BOOL)
        if self.atualIgual(tt.CHAR):
            self.consome(tt.CHAR)

    def C_COMP(self):
        self.consome(tt.ABRECH)
        self.LISTA_COMANDOS()
        self.consome(tt.FECHACH)

    def LISTA_COMANDOS(self):
        self.COMANDOS()
        self.G()

    def G(self):
        # First(LISTA_COMANDOS) = {First(Comandos) = {First(SE), First(ENQUANTO), First(LEIA), First(ESCREVA), First(ATRIBUICAO)}
        # = {if, while, read, write, id}.
        if self.atualIgual(tt.IF):
            self.LISTA_COMANDOS()
        elif self.atualIgual(tt.WHILE):
            self.LISTA_COMANDOS()
        elif self.atualIgual(tt.READ):
            self.LISTA_COMANDOS()
        elif self.atualIgual(tt.WRITE):
            self.LISTA_COMANDOS()
        elif self.atualIgual(tt.ID):
            self.LISTA_COMANDOS()
        else:
            pass

    def COMANDOS(self):
        if self.atualIgual(tt.IF):
            self.SE()
        elif self.atualIgual(tt.WHILE):
            self.ENQUANTO()
        elif self.atualIgual(tt.READ):
            self.LEIA()
        elif self.atualIgual(tt.WRITE):
            self.ESCREVA()
        elif self.atualIgual(tt.ATRIB):
            self.ATRIBUICAO()

    def SE(self):
        self.consome(tt.IF)
        self.consome(tt.ABREPAR)
        self.EXPR()
        self.consome(tt.FECHAPAR)
        self.C_COMP()
        self.H()

    def H(self):
        # First(C_COMP) = abrech
        if self.atualIgual(tt.ABRECH):
            self.C_COMP()
        else:
            pass

    def ENQUANTO(self):
        self.consome(tt.WHILE)
        self.consome(tt.ABREPAR)
        self.EXPR()
        self.consome(tt.FECHAPAR)
        self.C_COMP()

    def LEIA(self):
        self.consome(tt.READ)
        self.consome(tt.ABREPAR)
        self.LIST_ID()
        self.consome(tt.FECHAPAR)
        self.consome(tt.PVIRG)

    def ATRIBUICAO(self):
        self.consome(tt.ID)
        self.consome(tt.ATRIB)
        self.EXPR()
        self.consome(tt.PVIRG)

    def ESCREVA(self):
        self.consome(tt.WRITE)
        self.consome(tt.ABREPAR)
        self.LIST_W()
        self.consome(tt.FECHAPAR)
        self.consome(tt.PVIRG)

    def LIST_W(self):
        self.ELEM_W()
        self.L()

    def L(self):
        if self.atualIgual(tt.VIRG):
            self.consome(tt.VIRG)
            self.LIST_W()
        else:
            pass

    def ELEM_W(self):
        if self.atualIgual(tt.CADEIA):
            self.consome(tt.CADEIA)
        else:
            self.EXPR()

    def EXPR(self):
        self.SIMPLES()
        self.P()

    def P(self):
        if self.atualIgual(tt.OPREL):
            self.consome(tt.OPREL)
            self.SIMPLES()
        else:
            pass

    def SIMPLES(self):
        self.TERMO()
        self.R()

    def R(self):
        if self.atualIgual(tt.OPAD):
            self.consome(tt.OPAD)
            self.SIMPLES()
        else:
            pass

    def TERMO(self):
        self.FAT()
        self.S()

    def S(self):
        if self.atualIgual(tt.OPMUL):
            self.consome(tt.OPMUL)
            self.TERMO()
        else:
            pass

    def FAT(self):
        if self.atualIgual(tt.ID):
            self.consome(tt.ID)
        elif self.atualIgual(tt.CTE):
            self.consome(tt.CTE)
        elif self.atualIgual(tt.ABREPAR):
            self.consome(tt.ABREPAR)
            self.EXPR()
            self.consome(tt.FECHAPAR)
        elif self.atualIgual(tt.TRUE):
            self.consome(tt.TRUE)
        elif self.atualIgual(tt.FALSE):
            self.consome(tt.FALSE)
        elif self.atualIgual(tt.OPNEG):
            self.consome(tt.OPNEG)
            self.FAT()
