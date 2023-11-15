def PROG():
    # program
    # id
    # pvirg
    DECLS()
    C_COMP()


def DECLS():
    # Vazio
    if False:
        return
    else:
        # var
        LIST_DECLS()


def LIST_DECLS():
    DECL_TIPO()
    D()


def D():
    # Vazio
    if False:
        return
    else:
        LIST_DECLS()


def DECL_TIPO():
    LIST_ID()
    # dpontos
    TIPO()
    # pvirg


def LIST_ID():
    # id
    E()


def E():
    # Vazio
    if False:
        return
    else:
        # Virg
        LIST_ID()


def TIPO():
    # int / real / bool / char
    pass


def C_COMP():
    # abrech
    LISTA_COMANDOS()
    # fechach


def LISTA_COMANDOS():
    COMANDOS()
    G()


def G():
    # Vazio
    if False:
        return
    else:
        LISTA_COMANDOS()


def COMANDOS():
    if 1:
        SE()
    elif 2:
        ENQUANTO()
    elif 3:
        LEIA()
    elif 4:
        ESCREVA()
    else:
        ATRIBUICAO()


def SE():
    # if
    # abrepar
    EXPR()
    # fechapar
    C_COMP()
    H()


def H():
    # Vazio
    if False:
        return
    else:
        C_COMP()


def ENQUANTO():
    # while
    # abrepar
    EXPR()
    # fechapar
    C_COMP()


def LEIA():
    # read
    # abrepar
    LIST_ID()
    # fechapar
    # pvirg


def ATRIBUICAO():
    # id
    # atrib
    EXPR()
    # fechapar
    # pvig


def ESCREVA():
    # write
    # abrepar
    LIST_W()
    # fechapar
    #pvirg


def LIST_W():
    ELEM_W()
    L()


def L():
    # Vazio
    if False:
        return
    else:
        LIST_W()


def ELEM_W():
    if 1:
        EXPR()
    else:
        # cadeia
        return


def EXPR():
    SIMPLES()
    P()


def P():
    # Vazio
    if False:
        return
    else:
        # oprel
        SIMPLES()


def SIMPLES():
    TERMO()
    R()


def R():
    if False:
        return
    else:
        # opad
        SIMPLES()


def TERMO():
    FAT()
    S()


def S():
    if False:
        return
    else:
        # opmul
        TERMO()


def FAT():
    if 1:
        # id
        return
    elif 2:
        # cte
        return
    elif 3:
        # abrepar
        EXPR()
        # fechapar
    elif 4:
        # true
        return
    elif 5:
        # false
        return
    elif 6:
        # opneg
        FAT()

