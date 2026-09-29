from motor.cadastrar import cadastrar
from motor.listar import listar
from motor.buscar import buscaProduto
from motor.alterar import alterar
from Globais import tratarErroPergunta, limparTela
import sys

def menu():
    limparTela()
    while True:
        resposta = tratarErroPergunta("====================\n" \
            "1 - Cadastrar produto\n" \
            "2 - Listar produtos\n" \
            "3 - Buscar produto\n" \
            "4 - Alterar produto\n" \
            "5 - Remover produto\n" \
            "6 - Registrar venda\n" \
            "7 - Relatório\n" \
            "0 - Sair\n" \
            "====================\n" \
            "Resposta: ", 7, 0)

        if resposta == 0:
            limparTela()
            sys.exit()

        elif resposta == 1:
            limparTela()
            cadastrar()

        elif resposta == 2:
            limparTela()
            listar()

        elif resposta == 3:
            limparTela()
            buscaProduto()

        elif resposta == 4:
            limparTela()
            alterar()

if __name__ == "__main__":
    menu()