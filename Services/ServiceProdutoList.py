from flask import Flask, request, jsonify
from Globais.globais import abrir_conexao

def listProduto():
    conexao, con = abrir_conexao()

    sqlPadrao = "SELECT * FROM ESTOQUE WHERE "

    try:
        pagina = request.args.get("pagina", "1")
        limite = request.args.get("limite", "10")
    except ValueError:
        return jsonify({
            "Error": "Paginação e limite devem ser numeros inteiros!"
        }), 400
 
    if request.args.get("id"):
        con.execute(f"{sqlPadrao}ID = ?", request.args.get("id"))

        linha = con.fetchone()

        if linha is None:
            con.close()
            return jsonify({
                "Error": "Produto não encontrado!"
            })

        produto = {
            "Produto": {
                "id": linha[0], 
                "nome": linha[1],
                "estoque": linha[2],
                "valor": linha[3], 
                "nf": linha[5]
            }
        }

        con.close()
        return jsonify(produto)

