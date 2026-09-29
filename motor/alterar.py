from Globais import produtos, tratarErroPergunta, pesquisaSimNao, mostrarProduto, limparTela, tratarErroInt, tratarErroValor
from motor.listar import forProdutos
from motor.listar import listar
import time

def alterar():
    parar = False
    while True:
        if not parar:
            if pesquisaSimNao("Deseja listar os produtos antes de alterar?(S/N): "):
                listar(True)

            nome = input("Digite qual produto deseja alterar ou apenas digite enter para sair: ")
            if nome.strip() == "":
                limparTela()
                break
            for produto in produtos:
                if produto["nome"].lower() == nome.lower():
                    encontrou = produto
                    mostrarProduto(produto)

            opcao = tratarErroPergunta("Oque deseja alterar?\n" \
                                    "1 - Alterar Nome\n" \
                                    "2 - Alterar estoque\n" \
                                    "3 - Alterar valor\n" \
                                    "4 - Alterar varios produtos\n"
                                    "Resposta: ", 4, 1)
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
                    if mensagens(encontrou):
                        continue
                    else:
                        parar = True
                        break

                case 2:
                    while True:
                        estoque = tratarErroInt("Qual o novo estoque?: ")
                        encontrou["quantidade"] = estoque
                        if mensagens(encontrou):
                            continue
                        else: 
                            parar = True
                            break

                case 3:
                    while True:
                        valor = tratarErroValor("Qual o novo valor?: ")
                        encontrou["valor"] = valor
                        if mensagens(encontrou):
                            continue
                        else: 
                            parar = True
                            break 

                case 4:
                    while True:
                        pergunta = tratarErroInt("Quantos produtos você quer alterar?: ")
                        perguntaAlterar = tratarErroPergunta(f"Oque você quer alterar desses {pergunta} produtos?\n" \
                                                            "1 - Aumentar estoque\n" \
                                                            "2 - Aumentar valor\n" \
                                                            "0 - Cancelar"
                                                            "Resposta: ", 2, 0)

                        match perguntaAlterar:
                            case 1:
                                while True:
                                    produtoList = []
                                    for i in range(pergunta):
                                        produtoList.append(tratarErroInt(f"Digite o produto {i + 1}: "))

                                    perguntaQuant = tratarErroPergunta(f"Oque você deseja fazer?\n" \
                                                                    "1 - Aumentar estoque em %\n" \
                                                                    "2 - Aumentar estoque em numeros inteiros\n" \
                                                                    "3 - Aumentar estoque 1 por 1\n"
                                                                    "0 - Cancelar\n"
                                                                    "Resposta: ", 3, 0)

                                    match perguntaQuant:
                                        case 1:
                                            porcentagem = tratarErroInt("Quantos % você deseja que aumente?: ")
                                            for produto in produtos:
                                                produto["quantidade"] += produto["quantidade"] * porcentagem / 100



        else: 
            limparTela()
            break



def mensagens(encontrou):
    print("Estoque alterado com sucesso!")
    mostrarProduto(encontrou)
    time.sleep(2)
    limparTela()
    if pesquisaSimNao("Deseja continuar?(S/N): "):
        return True
    else:
        return False

