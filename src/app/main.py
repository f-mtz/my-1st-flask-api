from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
from textblob import TextBlob
from googletrans import Translator
from sklearn.linear_model import LinearRegression
import pickle
import os
from dotenv import load_dotenv


load_dotenv()  # Carrega o .env automaticamente

# Usando modelo serializado
colunas = ['tamanho', 'ano', 'garagem']
modelo = pickle.load(open('models/modelo.sav', 'rb'))

# cria uma instancia da aplicacao flask
app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = os.getenv('BASIC_AUTH_USERNAME') # os.environ.get('BASIC_AUTH_USERNAME')
app.config['BASIC_AUTH_PASSWORD'] = os.getenv('BASIC_AUTH_PASSWORD') # os.environ.get('BASIC_AUTH_PASSWORD')


print(os.getenv('BASIC_AUTH_USERNAME'))
print(os.getenv('BASIC_AUTH_PASSWORD'))

basic_auth = BasicAuth(app)

# definindo a rota raiz
@app.route('/')
def home():
    return "Minha primeira API no Docker."


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


@app.route('/sentimento2/', methods=['POST'])
@basic_auth.required
def sentimento2():
    try:
        # Recebe o JSON do payload
        data = request.get_json()
        
        if not data or 'frase' not in data:
            return jsonify({"erro": "Payload inválido. Envie {'frase': 'texto'}"}), 400
        
        frase = data['frase']
        
        # Tradução
        tradutor = Translator()
        traducao = tradutor.translate(frase, src='pt', dest='en')
        frase_english = traducao.text
        
        # Análise de sentimento
        tb_en = TextBlob(frase_english)
        polaridade = tb_en.sentiment.polarity
        
        # Resposta de sucesso
        return jsonify({
            "frase_original": frase,
            "frase_traduzida": frase_english,
            "polaridade": polaridade,
            "status": "sucesso"
        })
        
    except Exception as e:
        # Captura qualquer erro inesperado
        return jsonify({
            "erro": str(e),
            "status": "falha"
        }), 500

@app.route('/cotacao/', methods=['POST'])
@basic_auth.required
def cotacao():
    dados = request.get_json() # recendo dados do payload json
    dados_input = [dados[col] for col in colunas] # criando lista dos dados na ordem que o modelo de regressão espera receber
    preco = modelo.predict([dados_input])
    formatted_prediction = "R$ {:,.2f}".format(preco[0]).replace(",", "X").replace(".", ",").replace("X", ".")

    return jsonify(preco=formatted_prediction) # str(formatted_prediction)




# executa a API localhost na porta padrão 5000
app.run(debug=True, host='0.0.0.0')

