from Globais.globais import abrir_conexao
import jwt
from flask import Flask, jsonify, request
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

def login(login):
    conexao, con = abrir_conexao()

    if login["user"].strip() == "" or login["password"].strip() == "":
        conexao.close()
        return jsonify({
            "Error": "Acesso não autorizado"
        })

    con.execute("SELECT * FROM usuario WHERE login = ? and senha = ?", (login["user"], login["password"]))

    resultado = con.fetchall()

    conexao.close()
    
    if resultado:
        agora = datetime.now(timezone.utc)
        token = jwt.encode({"user": login["user"], "exp": agora + timedelta(hours=1)}, SECRET_KEY, algorithm="HS256")
        print(f"Login efetuado com sucesso! Usuario: {login["user"]}")
        return jsonify({
            "Sucess": "Acesso autorizado!",
            "token": token
        }), 200
    else:
        return jsonify({
            "Error": "Acesso não autorizado"
        }), 401