from Middleware.Auth import verifica_Token
from Controllers.ControllerLogin import login
from Controllers.ControllerProduto import produtoList, produtoAdd, produtoDoc, produtoDel
from Controllers.ControllerMarca import listMarca
from Globais.globais import urlPrefix
from flask import Flask, jsonify

app = Flask(__name__)
app.before_request(verifica_Token) # Faz com que toda rota passe pelo token

# Rotas login
app.register_blueprint(login, url_prefix=urlPrefix)

# Rotas produto
app.register_blueprint(produtoDoc, url_prefix=urlPrefix)
app.register_blueprint(produtoList, url_prefix=urlPrefix)
app.register_blueprint(produtoAdd, url_prefix=urlPrefix)
app.register_blueprint(produtoDel, url_prefix=urlPrefix)

# Rotas marca
app.register_blueprint(listMarca, url_prefix=urlPrefix)

# rotas publicas
@app.route("/ping")
def ping():
    return jsonify({
        "secess": "pong"
    }), 200


if __name__ == "__main__":
    app.run(debug=True) 