from flask import Flask
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

csrf = CSRFProtect(app) 

@app.route("/")
def pagina_inicial():
    return "Demo Petrobras CI/CD Hoffmann"

 


if __name__ == '__main__':
    app.run()