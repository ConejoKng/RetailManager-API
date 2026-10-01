from flask import Blueprint, request
from Services.ServiceLogin import login as service_login

login = Blueprint("login", __name__)

@login.route("/login", methods=["GET"])
def rota_login():
    print("Conectado com sucesso!\n" \
              "rota http://127.0.0.1:5000/login")
    loginUser = request.get_json()

    return service_login(loginUser)
