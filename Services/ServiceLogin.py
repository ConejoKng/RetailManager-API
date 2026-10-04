from Globais.globais import abrir_conexao
import jwt
from flask import Flask, jsonify, request
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

def login(login):
    if login["user"].strip() == "" or login["password"].strip() == "":
        return jsonify({
            "Error": "Acesso não autorizado"
        })

    loginAgora = False
    conexao = None
    try:
        conexao, con = abrir_conexao()
        con.execute("SELECT ID, LOGIN, SENHA FROM usuario WHERE login = ? and senha = ?", (login["user"], login["password"]))

        resultado = con.fetchone()
        
        if resultado:
            agora_utc = datetime.now(timezone.utc)
            agora_br = datetime.now(ZoneInfo("America/Sao_Paulo"))
            token = jwt.encode({"user": login["user"], "exp": agora_utc + timedelta(hours=1)}, SECRET_KEY, algorithm="HS256")
            id_user = resultado[0]
            loginAgora = True
            print(f"Login efetuado com sucesso! Usuario: {login['user']}")
            return jsonify({
                "Sucess": "Acesso autorizado!",
                "token": token
            }), 200
        else:
            return jsonify({
                "Error": "Acesso não autorizado"
            }), 401
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({
            "Error": "Erro interno no servidor"
        })
    finally:
        if loginAgora:
            con.execute("INSERT INTO LOGINS (ID_USUARIO, DATA_HORA) VALUES (?, ?)", (id_user, agora_br))
            conexao.commit()
            print("Acesso gravado")
        if conexao:
            conexao.close()