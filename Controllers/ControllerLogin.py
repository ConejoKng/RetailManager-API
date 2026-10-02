from flask import Blueprint, request
from Services.ServiceLogin import login as service_login

login = Blueprint("login", __name__)

@login.route("/login", methods=["GET"])
def rota_login():
    loginUser = request.get_json()
    print(f"Tentativa de Login usuario: {loginUser['user']}")

    return service_login(loginUser)
