from flask import Flask
app=Flask(__name__)

menu="""
<a href="/"><b>Página inicial</b></a> | <a href="/sobre"><b>Sobre</b></a> ! <a href="/contato"><b>Contato</b></a>
<br>
"""

@app.route("/")
def hello_world():
  return menu+"Olá, mundo! Esse é o meu site. (Graziela França)"

@app.route("/sobre")
def sobre():
  return menu+"Aqui vai o conteúdo da página Sobre"

@app.route("/contato")
def contato():
  return menu+"Aqui vai o conteúdo da página Contato"
