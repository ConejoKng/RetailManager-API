import configparser
from firebird.driver import connect

urlPrefix = "/v1"   

def abrir_conexao():
    
    config = configparser.ConfigParser()
    config.read(r"C:/API/fm-api.ini")

    fb = config["FIREBIRD"]
    dsn = f'{fb["host"]}/{fb["port"]}:{fb["caminho"]}'

    conexao = connect(
        dsn,
        user=fb["usuario"],
        password=fb["senha"],
        charset="UTF8"
    )

    con = conexao.cursor()

    return conexao, con
