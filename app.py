from Middleware.Auth import verifica_Token
from Controllers.ControllerLogin import login
from flask import Flask, jsonify

app = Flask(__name__)

app.register_blueprint(login, url_prefix="/v1")

app.before_request(verifica_Token)

@app.route("/ping")
def ping():
    return jsonify({
        "secess": "pong"
    }), 200


if __name__ == "__main__":
    app.run(debug=True) 