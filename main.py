from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
from textblob import TextBlob
from googletrans import Translator
from sklearn.linear_model import LinearRegression
import pickle

# Usando modelo serializado
colunas = ['tamanho', 'ano', 'garagem']
modelo = pickle.load(open('modelo.sav', 'rb'))

# cria uma instancia da aplicacao flask
app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'admin'

basic_auth = BasicAuth(app)

# definindo a rota raiz
@app.route('/')
def home():
    return "Minha primeira API."


@app.route('/sentimento/<frase>')
@basic_auth.required
def sentimento(frase):
    tradutor = Translator()
    traducao = tradutor.translate(frase, src='pt', dest='en')
    print(traducao)
    frase_english = traducao.text
    tb_en = TextBlob(frase_english)
    polaridade = tb_en.sentiment.polarity
    return "polaridade: {}".format(polaridade)



@app.route('/cotacao/', methods=['POST'])
def cotacao():
    dados = request.get_json() # recendo dados do payload json
    dados_input = [dados[col] for col in colunas] # criando lista dos dados na ordem que o modelo de regressão espera receber
    preco = modelo.predict([dados_input])
    formatted_prediction = "R$ {:,.2f}".format(preco[0]).replace(",", "X").replace(".", ",").replace("X", ".")

    return jsonify(preco=formatted_prediction) # str(formatted_prediction)




# executa a API localhost na orta padrão 5000
app.run(debug=True)

