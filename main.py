from flask import Flask
from textblob import TextBlob
from googletrans import Translator

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

# executa a API localhost na orta padrão 5000
app.run(debug=True)

