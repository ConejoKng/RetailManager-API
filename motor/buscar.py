from Globais import limparTela, produtos, tratarErroPergunta, pesquisaSimNao, tratarErroValor, tratarErroInt, mostrarProduto
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
                                                "2 - Estoque acabando\n" \
                                                "3 - Valor\n" \
                                                "4 - Voltar\n" \
                                                "Resposta: ", 4, 1)
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
                            mostrarProduto(produto)

                    input("Digite enter para continuar...")
                    primeiraVez = False
                    limparTela()

                case 2:
                    for produto in produtos:
                        if produto["quantidade"] < 5:
                            mostrarProduto(produto)

                    input("Digite enter para continuar...")
                    limparTela()

                case 3:
                    limparTela()
                    valor = tratarErroValor("Digite o valor a ser pesquisado: ")
                    opcao = tratarErroInt("1 - Pesquisar por valor especifico\n" \
                                          "2 - Pesquisar por valor menor que\n" \
                                          "3 - Pesquisar por valor maior que\n" \
                                          "Resposta: ")
                                          
                    for produto in produtos:
                        match opcao:
                            case 1: 
                                encontrou = produto["valor"] == valor
                            case 2:
                                encontrou = produto["valor"] < valor
                            case 3:
                                encontrou = produto["valor"] > valor
                        if encontrou:
                            mostrarProduto(produto)

                        input("Digite enter para continuar...")
                        limparTela()
                case 4: 
                    break
        else:
            if pesquisaSimNao("Deseja pesquisar mais?(S/N): "):
                primeiraVez = True
                continue
            else:
                limparTela()
                break
