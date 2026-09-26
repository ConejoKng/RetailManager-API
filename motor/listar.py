from Globais import produtos, tratarErroInt, limparTela

def listar(busca = False):
    if not busca:
        forProdutos()
        while True:
            pergunta = input("Deseja detalhar algum produto?(S/N): ")
            if pergunta.lower() in ["s", "sim"]:
                while True:
                    perguntaProd = tratarErroInt("Qual produto deseja detalhar?: ")
                    if perguntaProd > len(produtos) or perguntaProd < 1:
                        print("Esse produto não existe!")
                    else:
                        limparTela()
                        break

                print("===========")
                print(f"Produto - [{perguntaProd}]")
                print(f"Nome - {produtos[perguntaProd - 1]['nome']}")
                print(f"Estoque - {produtos[perguntaProd - 1]['quantidade']}")
                print(f"Valor - {produtos[perguntaProd - 1]['valor']:.2f}")
                print("===========")

                perguntaMaisAlgum = input("Mais algum?(S/N): ")
                if perguntaMaisAlgum.lower() in ["s", "sim"]:
                    continue
                else:
                    limparTela()
                    break
            else:
                break

    else:
        return forProdutos()

def forProdutos():
    if len(produtos) == 0:
        print("Não a produtos para listar!")
    else:
        for i in range(len(produtos)):
            print(f"{i + 1} - {produtos[i]['nome']}")
            print("==========")