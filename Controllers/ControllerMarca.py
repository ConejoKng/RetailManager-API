from flask import Blueprint, request
from Services.ServiceMarca import listMarca as listar_marca

listMarca = Blueprint("marca", __name__)

@listMarca.route("/marca/listar", methods=["GET"])
def rota_marca():
    return listar_marca()