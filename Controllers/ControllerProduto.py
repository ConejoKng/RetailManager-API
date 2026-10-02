from flask import Blueprint, request
from Services.ServiceProduto import listProduto as listar_produto
from Services.ServiceProduto import addProduto as Adicionar_produto

produtoList = Blueprint("produto/listar", __name__)
produtoAdd = Blueprint("produto/adicionar", __name__)

@produtoList.route("/produto/listar", methods=["GET"])
def rota_produtoListar():
    return listar_produto()

@produtoAdd.route("/produto/adicionar", methods=["POST"])
def rota_produtoAdd():
    json = request.get_json()
    return Adicionar_produto(json)