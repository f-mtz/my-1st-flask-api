from flask import Flask, request, jsonify
from textblob import TextBlob
from googletrans import Translator
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


# carregamento dos dados
df = pd.read_csv('casas.csv')

# definindo a ordem de recebimento dos dados
colunas = ['tamanho', 'ano', 'garagem']

# separando variavel dependente e independente
X = df.drop('preco', axis = 1)
y = df['preco']

# separacao treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 42)

# treinamento do modelo
modelo = LinearRegression()
modelo.fit(X_train, y_train)


# cria uma instancia da aplicacao flask
app = Flask(__name__)

# definindo a rota raiz
@app.route('/')
def home():
    return "Minha primeira API."


@app.route('/sentimento/<frase>')
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

