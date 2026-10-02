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
                "nome": "nome(String) -> Obrigatório",
                "estoque": "estoque(int) -> Obrigatório(Valor opcional)",
                "valor": "valor(float) -> Obrigatório",
                "comissao": "comissao(int) -> Obrigatório",
                "nota_fiscal": "nota_fiscal(String) -> Obrigatório(Valor opcional)"
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
        nota_fiscal = str(json["nota_fiscal"])

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

    nome = str(json["nome"]).strip().upper()

    conexao = None
    try:
        conexao, con = abrir_conexao()

        # Verifica se o produto que está sendo cadastrado existe no banco
        con.execute("SELECT NOME FROM ESTOQUE WHERE NOME = ?", (nome, ))
        resultado = con.fetchone()
        if resultado is not None:
            return jsonify({
                "Error": "Produto com esse nome já cadastrado", 
                "Solucao": "Acesse a rota /v1/produto/alterar para modificar ou /v1/produto/listar para visualizar"
            }), 400

        con.execute("""
                    INSERT INTO ESTOQUE 
                    (NOME, ESTOQUE, VALOR, COMISSAO, NOTA_FISCAL) VALUES
                    (?, ?, ?, ?, ?)
                    """, (nome, estoque, valor, comissao, nota_fiscal))

        conexao.commit()

        return jsonify({
            "Sucess": "Produto adicionado com sucesso!",
            "produto_cadastrado": {
                "nome": nome,
                "estoque": estoque,
                "valor": valor,
                "nota_fiscal": nota_fiscal
            }
        }), 201

    # Captura erro de conexão com o banco
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify ({
            "Error": "Erro interno no banco"
        }), 500
    finally:
        if conexao:
            conexao.close()

def delProduto(json):
    if not all(chave in json for chave in ["todos_marca", "id", "nome_marca", "nota_fiscal"]):
        return jsonify({
            "Error": "Estrutura json incorreta",
            "Estrutura_correta": {
                "todos": "boolean -> True(apaga todos os produtos) / False(ignora a chave)",
                "todos_marca": "string -> Insira a marca e todos os produtos dessa marca serão apagados",
                "id": "int -> Apaga um produto por ID especifico",
                "nota_fiscal": "Apaga todos os produtos que pertencem a essa nota"
            }
        }), 400
    try:
        todos = json.get("todos") is True
        todos_marca = str(json["todos_marca"])
        id = int(json["id"])
        nota_fiscal = str(json["nota_fiscal"])
    except (TypeError, ValueError):
        return jsonify({
            "Error": "Tipagens incorretas"
        }), 400

    conexao = None
    try:
        sqlDelete = "DELETE FROM ESTOQUE "
        conexao, con = abrir_conexao()

        if todos:
            con.execute(sqlDelete)
            conexao.commit()
            return jsonify({
                "Sucess": "Todos os produtos foram apagados."
            }), 200

        if todos_marca.strip() != "":
            con.execute("SELECT * FROM ESTOQUE WHERE NOME_MARCA = ?", (todos_marca,))
            resultado = con.fetchall()
            if len(resultado) == 0:
                return jsonify({
                    "Error": "Essa marca não existe."
                }), 400
            else:
                con.execute(F"{sqlDelete}WHERE NOME_MARCA = ?", (todos_marca,))
                conexao.commit()
                return jsonify({
                    "Sucess": f"todos os produtos da {todos_marca} foram apagados."
                }), 200

        if str(id) == "":
            con.execute("SELECT ID FROM ESTOQUE WHERE ID = ?", (id,))
            resultado = con.fetchone()
            if resultado is None:
                return jsonify({
                    "Error": "Esse produto não existe"
                }), 400
            else:
                con.execute(F"{sqlDelete}WHERE ID = ?", (id,)) 
                conexao.commit()
                return jsonify({
                    "Sucess": "Produto deletado com sucesso!"
                })

    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({
            "Error": "Erro interno no banco"
        })
    finally:
        if conexao:
            conexao.close()