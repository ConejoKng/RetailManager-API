from flask import Blueprint, request, jsonify
from Services.ServiceProduto import listProduto as listar_produto
from Services.ServiceProduto import addProduto as adicionar_produto
from Services.ServiceProduto import delProduto as deletar_produto
from Globais.globais import urlPrefix

produtoList = Blueprint("produto/listar", __name__)
produtoAdd = Blueprint("produto/adicionar", __name__)
produtoDoc = Blueprint("produto/doc", __name__)
produtoDel = Blueprint("produto/delete", __name__)

@produtoDoc.route("/produto/doc", methods=["GET"])
def rota_docProduto():
    return jsonify({
        "EndPoints_Produtos": {
            "rota": f"{urlPrefix}/produto/listar",
            "GET": {
                "Parametros_de_Query": {
                    "pagina": "int -> caso não enviado padrão: 1",
                    "id": "int -> caso não enviado padrão 1",
                },
            "Filtros": {
                "Parametros_de_Query": {
                    "id": "Filtro unico -> torna apenas um registro, caso enviado ignora todas as outras chaves",
                    "nome": "Filtra por nome do produto",
                    "valor": "Filtra pelo valor do produto",
                    "estoque": "Filtra pelo estoque do produto"
                },
            "Response": {
                "Produto": {
                    "Pagina": "Pagina - Pagina atual",
                    "limite": "Limite - Limite de registros",
                    "Registros": "Registros - Quantidade de registros por pagina",
                    "dados": "Array de produtos com o filtro aplicado"
                }
            }
            }
        },
            "rota": f"{urlPrefix}/produto/adicionar",
            "POST": {
                "Estrutura_JSON": {
                    "nome": "String - Chave(Obrigatório) / Valor(Obrigatório)",
                    "estoque": "Int - Chave(Obrigatório) / Valor(Opcional)",
                    "valor": "Float - Chave(Obrigatório) / Valor(Obrigatório)",
                    "comissao": "int - Chave(Obrigatório) / Valor(Obrigatório)",
                    "nota_fiscal": "String - Chave(Obrigatório) / Valor(Obrigatório)"
                },
            "Response": {
                "Sucess": "Produto adicionado com sucesso!",
                "produto_cadastrado": {
                    "nome": "nome",
                    "estoque": "estoque",
                    "valor": "valor",
                    "nota_fiscal": "nota_fiscal"
                }
            }
            }
        }
    })

@produtoList.route("/produto/listar", methods=["GET"])
def rota_produtoListar():
    return listar_produto()

@produtoAdd.route("/produto/adicionar", methods=["POST"])
def rota_produtoAdd():
    json = request.get_json()
    return adicionar_produto(json)

@produtoDel("/produto/delete", methods=["DELETE"])
def rota_produtoDel():
    json = request.get_json()
    return deletar_produto(json)