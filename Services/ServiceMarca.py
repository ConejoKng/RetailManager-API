from flask import request, jsonify
from Globais.globais import abrir_conexao

def jsonMarca(linha):
    marca = {
        "Marca": {
            "id": linha[0],
            "nome": linha[1]
        }
    }
    return marca

def listMarca():
    sqlPadrao =  "SELECT * FROM MARCA"
    parametros = []
    try:
        pagina = int(request.args.get("pagina", "1"))
        limite = int(request.args.get("limite", "10"))
        id_marca = int(request.args.get("id_marca", "0"))
    except ValueError:
        return jsonify({
            "Error": "Tipagem de valores incorreta"
        }), 400

    if pagina <= 0:
        pagina = 1
    if limite <= 0:
        limite = 10
    inicio = ((pagina - 1) * limite) + 1
    fim = inicio + limite - 1

    nome = request.args.get("nome_marca", "")

    conexao = None
    try:
        where_adicionado = False
        conexao, con = abrir_conexao()

        if id_marca != 0:
            sqlPadrao += " WHERE ID = ?"
            parametros.append(id_marca)
            where_adicionado = True

        if nome != "":
            if where_adicionado:
                sqlPadrao += "AND NOME = ?"
                parametros.append(nome)
            else:
                sqlPadrao += " WHERE NOME = ?"
                parametros.append(nome)
                where_adicionado = True

        paginacao = " ORDER BY ID ROWS ? TO ?"

        if len(parametros) == 0:
            con.execute(sqlPadrao + paginacao, (inicio, fim))
            linha = con.fetchall()

            marcas = []
            for i in range(len(linha)):
                marca = jsonMarca(linha[i])
                marcas.append(marca)

            return jsonify({
                "Pagina": pagina,
                "Limite": limite,
                "registros": len(marcas),
                "Dados": marcas
            }), 200

        else:
            parametros.extend([inicio, fim])
            print(sqlPadrao + paginacao, parametros)
            con.execute(sqlPadrao + paginacao, parametros)

            resultado = con.fetchone()

            return ({
                "Marca": {
                    "id_marca": resultado[0],
                    "nome": resultado[1]
                }
            }), 200
        
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({
            "Error": "Erro interno no servidor"
        }), 500   
    finally:
        if conexao:
            conexao.close()

    