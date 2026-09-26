from Globais import limparTela, produtos, tratarErroPergunta, pesquisaSimNao
from motor.listar import listar

def buscaProduto():
    if pesquisaSimNao("Deseja listar todos antes de buscar?(S/N)?: "):
        limparTela()
        listar(True)
    primeiraVez = True
    while True:
        if primeiraVez:
            perguntaProduto = tratarErroPergunta("Deseja buscar por:\n" \
                                                "1 - Nome\n" \
                                                "2 - Estoque\n" \
                                                "3 - Valor\n" \
                                                "Resposta: ", 3, 1)
            limparTela()
            match perguntaProduto:
                case 1:
                    while True:
                        nome = input("Digite o nome do produto: ")
                        if nome == "":
                            print("O nome não pode ser vazio!")
                        else: break
                    for produto in produtos:
                        if produto["nome"].lower() == nome.lower():
                            print("==========")
                            print(f"Nome - {produto['nome']}")
                            print(f"Quantiade - {produto['quantidade']}")
                            print(f"Valor - {produto['valor']:.2f}R$")
                            print("==========")
                    input("Digite enter para continuar...")
                    primeiraVez = False
                    limparTela()
        else:
            if pesquisaSimNao("Deseja pesquisar mais?(S/N): "):
                primeiraVez = True
                continue
            else:
                limparTela()
                break

