from lexico import TokenType as tt
from lexico import Token
from lexico import Lexico




class Sintatico:
    def __init__(self):
        self.lex = None
        self.tokenAtual = None
        self.symbolTable = dict()
        self.modoDeclarativo = False
        self.modoPanico = False
        self.deuErro = False
        self.tokensDeSincronismo = [tt.PVIRG, tt.FIMARQ]

    def interprete(self, path):
        if self.lex is not None:
            print('ERRO: Já existe um arquivo sendo processado.')
        else:
            self.lex = Lexico(path)
            self.lex.abreArquivo()
            self.tokenAtual = self.lex.getToken()

            self.EMPTY()
            self.consome(tt.FIMARQ)
            if not self.deuErro:
                print("Análise Executada com Sucesso !")
            else:
                print("PROGRAMA COM ERROS")
            self.lex.fechaArquivo()

    def atualIgual(self, token):
        (const, msg) = token
        return self.tokenAtual.const == const

    def atribuiTipo(self, tipo):
        for i in self.symbolTable:
            if self.symbolTable[i] is None:
                self.symbolTable[i] = tipo

    def consome(self, token, psync=None):
        if psync is not None:
            for i in psync:
                if i not in self.tokensDeSincronismo:
                    self.tokensDeSincronismo.append(i)
        if self.atualIgual(token) and not self.modoPanico:
            self.tokenAtual = self.lex.getToken()
        elif not self.modoPanico:
            self.modoPanico = True
            self.deuErro = True
            (const, msg) = token
            print('ERRO [linha {}]: era esperado "{}" mas veio "{}"'.format(self.tokenAtual.linha, msg, self.tokenAtual.lexema))
            procuraTokenDeSincronismo = True
            while procuraTokenDeSincronismo:
                self.tokenAtual = self.lex.getToken()
                for tk in self.tokensDeSincronismo:
                    (const, msg) = tk
                    if self.tokenAtual.const == const:
                        # tokenAtual é um token de sincronismo
                        procuraTokenDeSincronismo = False
                        break
        elif self.atualIgual(token):
            self.tokenAtual = self.lex.getToken()
            self.modoPanico = False
            self.tokensDeSincronismo = [tt.PVIRG, tt.FIMARQ]
        else:
            pass

    # Não retorna erro quando o arquivo for vazio.
    def EMPTY(self):
        if self.atualIgual(tt.PROGRAM):
            self.PROG()
        else:
            pass

    def PROG(self):
        psync = [tt.FIMARQ, tt.PROGRAM]
        self.consome(tt.PROGRAM, psync)
        self.consome(tt.ID, psync)
        self.consome(tt.PVIRG, psync)
        self.DECLS()
        self.C_COMP()

    def DECLS(self):
        psync = [tt.ABRECH]
        if self.atualIgual(tt.VAR):
            self.consome(tt.VAR, psync)
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
        psync = [tt.ID, tt.ABRECH]
        self.modoDeclarativo = True
        self.LIST_ID()
        self.consome(tt.DPONTOS, psync)
        self.TIPO()
        self.consome(tt.PVIRG, psync)
        self.modoDeclarativo = False

    def LIST_ID(self):
        psync = [tt.ID, tt.DPONTOS, tt.FECHAPAR]
        if self.modoDeclarativo:
            self.symbolTable[self.tokenAtual.lexema] = None
        self.consome(tt.ID, psync)
        self.E()

    def E(self):
        psync = [tt.VIRG, tt.DPONTOS, tt.FECHAPAR]
        if self.atualIgual(tt.VIRG):
            self.consome(tt.VIRG, psync)
            self.LIST_ID()
        else:
            pass

    def TIPO(self):
        psync = [tt.INT, tt.REAL, tt.BOOL, tt.CHAR, tt.ABRECH, tt.ID, tt.PVIRG]
        if self.modoDeclarativo:
            self.atribuiTipo(self.tokenAtual.lexema)
        if self.atualIgual(tt.INT):
            self.consome(tt.INT, psync)
        elif self.atualIgual(tt.REAL):
            self.consome(tt.REAL, psync)
        elif self.atualIgual(tt.BOOL):
            self.consome(tt.BOOL, psync)
        elif self.atualIgual(tt.CHAR):
            self.consome(tt.CHAR, psync)
        else:
            print("ERRO DE SINTAXE [linha{}]: Tipo de identificador não informado".format(self.tokenAtual.linha))
            quit()

    def C_COMP(self):
        psync = [tt.FIMARQ, tt.ABRECH, tt.FECHACH, tt.IF, tt.WHILE, tt.READ, tt.WRITE, tt.ATRIB]
        self.consome(tt.ABRECH, psync)
        self.LISTA_COMANDOS()
        self.consome(tt.FECHACH, psync)

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
        elif self.atualIgual(tt.ID):
            self.ATRIBUICAO()

    def SE(self):
        psync = [tt.IF, tt.FECHACH, tt.WHILE, tt.READ, tt.WRITE, tt.ATRIB]
        self.consome(tt.IF, psync)
        self.consome(tt.ABREPAR, psync)
        self.EXPR()
        self.consome(tt.FECHAPAR, psync)
        self.C_COMP()
        self.H()

    def H(self):
        psync = [tt.ELSE, tt.FECHACH, tt.IF, tt.WHILE, tt.READ, tt.WRITE, tt.ATRIB]
        # First(C_COMP) = abrech
        if self.atualIgual(tt.ELSE):
            self.consome(tt.ELSE, psync)
            self.C_COMP()
        else:
            pass

    def ENQUANTO(self):
        psync = [tt.WHILE, tt.FECHACH, tt.IF, tt.READ, tt.WRITE, tt.ATRIB]
        self.consome(tt.WHILE, psync)
        self.consome(tt.ABREPAR, psync)
        self.EXPR()
        self.consome(tt.FECHAPAR, psync)
        self.C_COMP()

    def LEIA(self):
        psync = [tt.WHILE, tt.FECHACH, tt.IF, tt.READ, tt.WRITE, tt.ATRIB]
        self.consome(tt.READ, psync)
        self.consome(tt.ABREPAR, psync)
        self.LIST_ID()
        self.consome(tt.FECHAPAR, psync)
        self.consome(tt.PVIRG, psync)

    def ATRIBUICAO(self):
        psync = [tt.WHILE, tt.FECHACH, tt.IF, tt.READ, tt.WRITE, tt.ATRIB, tt.ID]
        self.consome(tt.ID, psync)
        self.consome(tt.ATRIB, psync)
        self.EXPR()
        self.consome(tt.PVIRG, psync)

    def ESCREVA(self):
        psync = [tt.WHILE, tt.FECHACH, tt.IF, tt.READ, tt.WRITE, tt.ATRIB]
        self.consome(tt.WRITE, psync)
        self.consome(tt.ABREPAR, psync)
        self.LIST_W()
        self.consome(tt.FECHAPAR, psync)
        self.consome(tt.PVIRG, psync)

    def LIST_W(self):
        self.ELEM_W()
        self.L()

    def L(self):
        psync = [tt.VIRG, tt.FECHAPAR]
        if self.atualIgual(tt.VIRG):
            self.consome(tt.VIRG, psync)
            self.LIST_W()
        else:
            pass

    def ELEM_W(self):
        psync = [tt.ID, tt.CTE, tt.ABREPAR, tt.TRUE, tt.FALSE, tt.CADEIA, tt.VIRG, tt.FECHAPAR]
        if self.atualIgual(tt.CADEIA):
            self.consome(tt.CADEIA, psync)
        else:
            self.EXPR()

    def EXPR(self):
        self.SIMPLES()
        self.P()

    def P(self):
        psync = [tt.OPREL, tt.PVIRG, tt.FECHAPAR]
        if self.atualIgual(tt.OPREL):
            self.consome(tt.OPREL, psync)
            self.SIMPLES()
        else:
            pass

    def SIMPLES(self):
        self.TERMO()
        self.R()

    def R(self):
        psync = [tt.OPAD, tt.OPREL, tt.PVIRG, tt.FECHAPAR]
        if self.atualIgual(tt.OPAD):
            self.consome(tt.OPAD, psync)
            self.SIMPLES()
        else:
            pass

    def TERMO(self):
        self.FAT()
        self.S()

    def S(self):
        psync = [tt.OPMUL, tt.OPAD, tt.OPREL, tt.PVIRG, tt.FECHAPAR]
        if self.atualIgual(tt.OPMUL):
            self.consome(tt.OPMUL, psync)
            self.TERMO()
        else:
            pass

    def FAT(self):
        psync = [tt.ID, tt.CTE, tt.ABREPAR, tt.TRUE, tt.FALSE, tt.OPNEG, tt.OPMUL, tt.OPAD, tt.OPREL, tt.PVIRG, tt.FECHAPAR]
        if self.atualIgual(tt.ID):
            self.consome(tt.ID, psync)
        elif self.atualIgual(tt.CTE):
            self.consome(tt.CTE, psync)
        elif self.atualIgual(tt.ABREPAR):
            self.consome(tt.ABREPAR, psync)
            self.EXPR()
            self.consome(tt.FECHAPAR, psync)
        elif self.atualIgual(tt.TRUE):
            self.consome(tt.TRUE, psync)
        elif self.atualIgual(tt.FALSE):
            self.consome(tt.FALSE, psync)
        elif self.atualIgual(tt.OPNEG):
            self.consome(tt.OPNEG, psync)
            self.FAT()
