from flask import Blueprint
from Services.ServiceProduto import listProduto as listar_produto

produtoList = Blueprint("produto/listar", __name__)

@produtoList.route("/produto/listar", methods=["GET"])
def rota_produtoListar():
    return listar_produto()