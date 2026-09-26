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
    resposta = input(mensagem)
    if resposta.lower() in ["s", "sim"]:
        return True
    else:
        return False

def limparTela():
    os.system('cls')