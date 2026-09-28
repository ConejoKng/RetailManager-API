from Globais import produtos, tratarErroPergunta, pesquisaSimNao, mostrarProduto, limparTela
from listar import listar
import time

def alterar():
    if pesquisaSimNao("Deseja listar os produtos antes de alterar?(S/N): "):
        listar(True)

    nome = input("Digite qual produto deseja alterar: ")
    for produto in produtos:
        if produto["nome"].lower() == nome.lower():
            encontrou = produto
            mostrarProduto(produto)

    opcao = tratarErroPergunta("Oque deseja alterar?\n" \
                               "1 - Alterar Nome\n" \
                               "2 - Alterar estoque\n" \
                               "3 - Alterar valor\n" \
                               "Resposta: ")
    limparTela()
    match opcao:
        case 1: 
            while True:
                nome = input("Digite o novo nome do produto: ")
                if nome == "":
                    print("O nome n pode ser vazio!")
                else: 
                    break
            encontrou["nome"] = nome
            print("Produto alterado com sucesso!")
            time.sleep(2)
            limparTela()


