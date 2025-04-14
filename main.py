from flask import Flask

# cria uma instancia da aplicacao flask
app = Flask('meu_app')

# definindo a rota raiz
@app.route('/')
def home():
    return "Minha primeira API."

# executa a API localhost na orta padrão 5000
app.run()

