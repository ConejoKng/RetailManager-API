import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from flask import request, jsonify
from Services.ServiceLogin import SECRET_KEY

def verifica_Token():
    # Rotas públicas
    if request.endpoint == "ping" or request.endpoint == "login.rota_login":
        return None

    # Não mandou autorização
    if "Authorization" not in request.headers:
        return jsonify({
                    "Error": "Autorização não informada"
                })

    # Não mandou Token
    if request.headers.get("Authorization") == "":       
         return jsonify({
                    "Error": "Token não informado"
                }), 401

    token = request.headers.get("Authorization") # Recebe o token

    # Remove o Bearer caso ele exista
    if token[:7] == "Bearer ":
        token = token[7:]

    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except ExpiredSignatureError:
        return jsonify({
            "Error": "Token expirado"
        }), 401
    except InvalidTokenError:
        return jsonify({
            "Error": "Token invalido"
        }), 401