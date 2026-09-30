import configparser
from firebird.driver import connect

def abrir_conexao():
    
    config = configparser.ConfigParser()
    config.read(r"C:/API/fm-api.ini")

    fb = config["FIREBIRD"]
    dsn = f'{fb["host"]}/{fb["port"]}:{fb["caminho"]}'

    conexao = connect(
        dsn,
        user=fb["usuario"],
        password=fb["senha"]
    )

    con = conexao.cursor()

    return conexao, con


