from Globais import produtos, tratarErroInt, tratarErroValor, limparTela
import time

def cadastrar():
    while True:
        perguntaQuant = tratarErroInt("Quantos produtos você quer cadastrar?: ")
        for i in range(perguntaQuant):
            nomeProduto = input("Digite o nome do produto: ")
            quantidade = tratarErroInt("Digite a quantidade: ")
            valor = tratarErroValor("Digite o valor: ")

            produto = {
                "nome": nomeProduto,
                "quantidade": quantidade,
                "valor": valor
            }

            produtos.append(produto)
            print(f"Produto cadastrado!\n" \
                  f"Nome: {nomeProduto}\n" \
                  f"Valor: {valor:.2f}R$")
            
            time.sleep(2)
            limparTela()

        perguntaNova = input("Deseja Adicionar mais?(S/N): ")
        if perguntaNova.lower() in ["s", "sim"]:
            continue
        else:
            print("Produtos cadastrados com sucesso!")
            input("Aperte enter para continuar...")
            limparTela()
            break