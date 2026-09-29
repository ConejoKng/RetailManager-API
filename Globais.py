import os

#Variaveis globais
produtos = [{
    "nome": "arroz",
    "quantidade": 8,
    "valor": 15
},
{
    "nome": "feijão",
    "quantidade": 10,
    "valor": 8.99
},
{
    "nome": "Miojo",
    "quantidade": 4,
    "valor": 4   
},
{
    "nome": "Farinha",
    "quantidade": 2,
    "valor": 2.00
}
]
vendas = []

#Funções globais 
def tratarErroInt(mensagem):
    while True:
        try:
            valor = int(input(mensagem))
            return valor
        except ValueError:
            print("Use apenas numeros!")

def tratarErroPergunta(pergunta, maximo, minimo):
    while True:
        valor = (tratarErroInt(pergunta))
        if valor >= minimo and valor <= maximo:
            return valor
        else:
            print("Opção invalida!")

def tratarErroValor(mensagem):
    while True:
        try:
            valor = float(input(mensagem))
            return valor
        except ValueError:
            print("Digite apenas numeros!")

def pesquisaSimNao(mensagem):
    while True:
        resposta = input(mensagem)
        if resposta.lower() in ["s", "sim"]:
            return True
        elif resposta.lower() in ["n", "não", "nao"] or resposta == "":
            return False
        else:
            print("resposta invalida!")

def limparTela():
    os.system('cls')

def mostrarProduto(produto, nome = "nome", quantidade = "quantidade", valor = "valor"):
    print("==========")
    print(f"Nome - {produto[nome]}")
    print(f"Estoque - {produto[quantidade]}")
    print(f"Valor - {produto[valor]}")
    print("==========") 