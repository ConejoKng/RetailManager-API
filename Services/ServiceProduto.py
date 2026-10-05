from flask import request, jsonify
from Globais.globais import abrir_conexao

def jsonProduto(linha):  
    produto = {
        "Produto": {
            "id": linha[0], 
            "nome": linha[1],
            "estoque": linha[2],
            "valor": linha[3], 
            "nf": linha[5],
            "marca": linha[6]
        }
    }

    return produto

def listProduto():
    sqlPadrao = "SELECT e.ID, e.NOME, e.ESTOQUE, e.VALOR, e.COMISSAO, e.NOTA_FISCAL, m.NOME FROM ESTOQUE e"
    sqlFiltro = ""
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

    try:
        if request.args.get("valor"):
            valor = float(request.args.get("valor"))
        else: 
            valor = 0
        if request.args.get("estoque"):
            estoque = float(request.args.get("estoque"))
        else:
            estoque = 0
    except ValueError:
        return jsonify({
            "Error": "Erro de conversão, estrutura incorreta"
        }), 400

    conexao = None
    try:
        conexao, con = abrir_conexao()

        # Filtro por produto filtro unico
        if request.args.get("id"):
            con.execute(f"{sqlPadrao} INNER JOIN marca m ON m.id = e.id_marca WHERE e.ID = ?", (request.args.get("id"),))

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
            sqlFiltro += " WHERE e.NOME = ?"
            parametros.append(request.args.get("nome").upper())
            where_adicionado = True

        # Filtra por estoque
        if valor:
            if not where_adicionado:
                sqlFiltro += " WHERE e.VALOR = ?"
                where_adicionado = True
            else:
                sqlFiltro += " AND e.VALOR = ?"

            parametros.append(valor)

        # Filtra por estoque
        if estoque:
            if not where_adicionado:
                sqlFiltro += " WHERE e.ESTOQUE = ?"
                where_adicionado = True
            else:
                sqlFiltro += " AND e.ESTOQUE = ?"

            parametros.append(estoque)

        parametros.extend([inicio, fim]) # Adiciona paginação
        innerJoin = " INNER JOIN marca m ON m.id = e.id_marca"
        paginacao = " ORDER BY e.ID ROWS ? TO ?" 

        # Executa a query no banco
        con.execute(sqlPadrao + innerJoin + sqlFiltro + paginacao, parametros)
        # print(sqlPadrao + innerJoin + paginacao, parametros)

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
                "id_marca": "id marca(Int) -> obrigatório",
                "estoque": "estoque(int) -> Obrigatório(Valor opcional)",
                "valor": "valor(float) -> Obrigatório",
                "comissao": "comissao(int) -> Obrigatório",
                "nota_fiscal": "nota_fiscal(String) -> Obrigatório(Valor opcional)"
            }
        }

    # Verifica se todas as chaves obrigatórias existem
    if not all(chave in json for chave in ["nome","estoque", "valor", "comissao", "nota_fiscal", "id_marca"]):
        return jsonify(estruturaJson()), 400

    # Verifica se todos os valores obrigatórios vieram
    if (json["nome"].strip() == "" or 
        (str(json["valor"])).strip() == "" or
        (str(json["comissao"])).strip() == ""or 
        (str(json["id_marca"])).strip() == ""):
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
    id_marca = int(json["id_marca"])

    conexao = None
    try:
        conexao, con = abrir_conexao()

        # Verifica se o produto que está sendo cadastrado existe no banco
        con.execute("SELECT NOME FROM ESTOQUE WHERE NOME = ? AND ID_MARCA = ?", (nome, id_marca))
        resultado = con.fetchone()
        if resultado is not None:
            return jsonify({
                "Error": "Produto com esse nome já cadastrado", 
                "Solucao": "Acesse a rota /v1/produto/alterar para modificar ou /v1/produto/listar para visualizar"
            }), 400

        con.execute("""
                    INSERT INTO ESTOQUE 
                    (NOME, ESTOQUE, VALOR, COMISSAO, NOTA_FISCAL, ID_MARCA) VALUES
                    (?, ?, ?, ?, ?, ?)
                    """, (nome, estoque, valor, comissao, nota_fiscal, id_marca))

        conexao.commit()

        return jsonify({
            "Sucess": "Produto adicionado com sucesso!",
            "produto_cadastrado": {
                "nome": nome,
                "id_marca": id_marca,
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
    try:
        if json.get("todos") == "S":
            todos = True
        else:
            todos = False

        if json.get("id_marca") is None:
            id_marca = 0
        else:
            id_marca = int(json.get("estoque"))

        if json.get("id") is None:
            id = 0
        else:
            id = int(json.get("id"))

        if json.get("nota_fiscal") is None:
            nota_fiscal = ""
        else: 
            str(json.get("nota_fiscal"))

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

        if id_marca != 0:
            con.execute("SELECT * FROM ESTOQUE WHERE id_marca = ?", (id_marca,))
            resultado = con.fetchall()
            if len(resultado) == 0:
                return jsonify({
                    "Error": "Essa marca não existe."
                }), 400
            else:
                con.execute(F"{sqlDelete}WHERE NOME_MARCA = ?", (id_marca,))
                conexao.commit()
                return jsonify({
                    "Sucess": f"todos os produtos da {id_marca} foram apagados."
                }), 200

        if id != 0:
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
                }), 200

        if nota_fiscal != "":
            con.execute("SELECT * FROM ESTOQUE WHERE NOTA_FISCAL = ?", (nota_fiscal,))
            resultado = con.fetchall()
            if resultado is None:
                return jsonify({
                        "Error": "Esse produto não existe"
                    }), 400
            else:
                con.execute(f"{sqlDelete}WHERE NOTA_FISCAL = ?", (nota_fiscal,))
                conexao.commit()
                return jsonify({
                        "Sucess": "Produto deletado com sucesso!"
                    }), 200

    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({
            "Error": "Erro interno no banco"
        })
    finally:
        if conexao:
            conexao.close()