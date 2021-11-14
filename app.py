from flask import Flask

app = Flask(__name__)

@app.route("/")
def pagina_inicial():
    return "Tudo funcionando perfeitamente!!"

if __name__ == '__main__':
    app.run()