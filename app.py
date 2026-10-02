from Middleware.Auth import verifica_Token
from Controllers.ControllerLogin import login
from Controllers.ControllerProduto import produtoList, produtoAdd
from flask import Flask, jsonify

app = Flask(__name__)

# Rotas login
app.register_blueprint(login, url_prefix="/v1")

# Rotas produto
app.register_blueprint(produtoList, url_prefix="/v1")
app.register_blueprint(produtoAdd, url_prefix="/v1")


app.before_request(verifica_Token)

@app.route("/ping")
def ping():
    return jsonify({
        "secess": "pong"
    }), 200


if __name__ == "__main__":
    app.run(debug=True) 