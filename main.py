from sintatico import Sintatico
import os

if __name__ == "__main__":
    print("***********************************************************************")
    print("\tBATERIA DE TESTES: Trabalho 1 de Compiladores 1")
    nome = "./testes/exemplo1.txt"
    parser = Sintatico()
    parser.interprete(nome)

    print("\n\nTabela de Simbolos: \n")
    print(parser.symbolTable)