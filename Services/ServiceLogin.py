from AbrirConexao import abrir_conexao
import jwt
from flask import Flask, jsonify, request
from datetime import datetime, timedelta, timezone
from Globais.globais import SECRET_KEY

def login(login):
    conexao, con = abrir_conexao()
    user = login["user"]
    password = login["password"]

    if password.strip() == "" or user.strip() == "":
        conexao.close()
        return jsonify({
            "Error": "Acesso não autorizado"
        })

    con.execute("SELECT * FROM usuario WHERE login = ? and senha = ?", (user, password))

    resultado = con.fetchall()

    conexao.close()
    
    if resultado:
        agora = datetime.now(timezone.utc)
        token = jwt.encode({"user": user, "exp": agora + timedelta(hours=1)}, SECRET_KEY, algorithm="HS256")
        return jsonify({
            "Sucess": "Acesso autorizado!",
            "token": token
        }), 200
    else:
        return jsonify({
            "Error": "Acesso não autorizado"
        }), 401