from flask import Flask, jsonify, request
from AbrirConexao import abrir_conexao
import sys

app = Flask(__name__)

@app.route("/ping")
def ping(): 
    return jsonify({
        "secess": "pong"
    }), 200

@app.route("/v1/login",  methods=["GET"])
def login():
    conexao, con = abrir_conexao()
    print("Conectado com sucesso!\n" \
          "rota http://192.168.0.188:5000")
    login = request.get_json()

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
        
        return jsonify({
            "Sucess": "Acesso autorizado!"
        }), 200
    else:
        return jsonify({
            "Error": "Acesso não autorizado"
        }), 401

    

if __name__ == "__main__":
    app.run(debug=True)