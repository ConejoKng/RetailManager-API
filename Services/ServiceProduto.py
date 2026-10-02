from flask import request, jsonify
from Globais.globais import abrir_conexao

def jsonProduto(linha):
    produto = {
        "Produto": {
            "id": linha[0], 
            "nome": linha[1],
            "estoque": linha[2],
            "valor": linha[3], 
            "nf": linha[5]
        }
    }

    return produto

def listProduto():
    sqlPadrao = "SELECT ID, NOME, ESTOQUE, VALOR, COMISSAO, NOTA_FISCAL FROM ESTOQUE"
    try:
        pagina = int(request.args.get("pagina", "1"))
        limite = int(request.args.get("limite", "10"))
    except ValueError:
        return jsonify({
            "Error": "Paginação e limite devem ser numeros inteiros!"
        }), 400

    if pagina <= 0:
        pagina = 1
    if limite <= 0:
        limite = 10
    inicio = ((pagina - 1) * limite) + 1
    fim = inicio + limite - 1

    conexao = None
    try:
        conexao, con = abrir_conexao()
        # Filtro por produto filtro unico
        if request.args.get("id"):
            con.execute(f"{sqlPadrao}  WHERE ID = ?", (request.args.get("id"),))

            linha = con.fetchone()

            if linha is None:
                return jsonify({
                    "Error": "Produto não encontrado!"
                }), 404
            
            
            return jsonify(jsonProduto(linha))

        where_adicionado = False
        parametros = []

        # Filtro por nome
        if request.args.get("nome"):
            sqlPadrao += " WHERE NOME = ?"
            parametros.append(request.args.get("nome"))
            where_adicionado = True

        # Filtra por estoque
        if request.args.get("valor"):
            if not where_adicionado:
                sqlPadrao += " WHERE VALOR = ?"
                where_adicionado = True
            else:
                sqlPadrao += " AND VALOR = ?"

            parametros.append(request.args.get("valor"))

        # Filtra por estoque
        if request.args.get("estoque"):
            if not where_adicionado:
                sqlPadrao += " WHERE ESTOQUE = ?"
                where_adicionado = True
            else:
                sqlPadrao += " AND ESTOQUE = ?"

            parametros.append(request.args.get("estoque"))

        parametros.extend([inicio, fim]) # Adiciona paginação
        paginacao = " ORDER BY ID ROWS ? TO ?" 

        # Executa a query no banco
        con.execute(sqlPadrao + paginacao, parametros)

        linha = con.fetchall()

        if len(linha) == 0:
            
            return jsonify({
                "Error": "Produto não encontrado"
            }), 404

        produtos = []
        for i in range(len(linha)):
            produto = jsonProduto(linha[i])
            produtos.append(produto)

        return jsonify({
            "Pagina": pagina,
            "Limite": limite,
            "registros": len(produtos),
            "dados": produtos
            })
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({
            "Error": "Erro interno no servidor"
        }), 500
    finally:
        # Fecha Conexão com o banco 
        if conexao:
            conexao.close()

def addProduto(json):
    def estruturaJson():
        return {
            "Error": "Estrutura Json incorreta",
            "Estrutura correta": {
                "nome": "nome -> Obrigatório",
                "estoque": "estoque(int) -> Obrigatório(Valor opcional)",
                "valor": "valor(float) -> Obrigatório",
                "comissao": "comissao(int) -> Obrigatório",
                "nota_fiscal": "nota_fiscal -> Obrigatório(Valor opcional)"
            }
        }

    # Verifica se todas as chaves obrigatórias existem
    if not all(chave in json for chave in ["nome","estoque", "valor", "comissao", "nota_fiscal"]):
        return jsonify(estruturaJson()), 400

    # Verifica se todos os valores obrigatórios vieram
    if (json["nome"].strip() == "" or 
        (str(json["valor"])).strip() == "" or
        (str(json["comissao"])).strip() == ""):
        return jsonify(estruturaJson()), 400

    # Se a nota fiscal vier vazia ela recebe none
    if str(json["nota_fiscal"]).strip() == "":
        nota_fiscal = None
    else:
        nota_fiscal = json["nota_fiscal"]

    try:
        if str(json["estoque"]).strip() == "":
            estoque = 0
        else:
            estoque = int(json.get("estoque"))
        valor = float(json.get("valor"))
        comissao = int(json.get("comissao"))
    except (ValueError, TypeError):
        return jsonify({
            "Error": "tipos invalidos",
            "Tipos_corretos": {
                "valor": "Float",
                "estoque": "Int",
                "comissao": "Int"
            }
        }), 400

    conexao = None
    try:
        conexao, con = abrir_conexao()

        con.execute("""
                    INSERT INTO ESTOQUE 
                    (NOME, ESTOQUE, VALOR, COMISSAO, NOTA_FISCAL) VALUES
                    (?, ?, ?, ?, ?)
                    """, (json["nome"], estoque, valor, comissao, nota_fiscal))

        conexao.commit()

        return jsonify({
            "Sucess": "produto adicionado com sucesso!",
            "produto_cadastrado": {
                "nome": json['nome'],
                "estoque": estoque,
                "valor": valor,
                "nota_fiscal": nota_fiscal
            }
        })

    # Captura erro de conexão com o banco
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify ({
            "Error": "Erro interno no banco"
        }), 500
    finally:
        if conexao:
            conexao.close()