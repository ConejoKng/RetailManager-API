from flask import Blueprint
from Services.ServiceProdutoList import listProduto as listar_produto

produtoList = Blueprint("produto/listar", __name__)

@produtoList.route("/produto/listar", methods=["GET"])
def rota_produtoListar():
    return listar_produto()