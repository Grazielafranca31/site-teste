import datetime
import os
import gspread
import requests
from flask import Flask, request
from oauth2client.service_account import ServiceAccountCredentials
from tchan import ChannelScraper


TELEGRAM_API_KEY=os.environ['TELEGRAM_API_KEY']
TELEGRAM_ADMIN_ID=os.environ['TELEGRAM_ADMIN_ID']
GOOGLE_SHEETS_CREDENTIALS=os.environ['GOOGLE_SHEETS_CREDENTIALS']
GOOGLE_SHEETS_CREDENTIALS=os.environ['GOOGLE_SHEETS_CREDENTIALS']
with open('credenciais.json', mode='w') as arquivo:
  arquivo.write(GOOGLE_SHEETS_CREDENTIALS)
conta=ServiceAccountCredentials.from_json_keyfile_name('credenciais.json')
api = gspread.authorize(conta) # sheets.new
planilha = api.open_by_key("1ZDyxhXlCtCjMbyKvYmMt_8jAKN5JSoZ7x3MqlnoyzAM")
sheet = planilha.worksheet("Sheet1")
app = Flask(__name__)


def ultimas_promocoes():
  scraper = ChannelScraper()
  contador = 0
  resultado = []
  for message in scraper.messages("promocoeseachadinhos"):
    contador += 1
    texto = message.text.strip().splitlines()[0]
    resultado.append(f"{message.created_at} {texto}")
    if contador == 10:
      return resultado

    
menu = """
<a href="/">Página inicial</a> | <a href="/promocoes">PROMOÇÕES</a> | <a href="/sobre">Sobre</a> | <a href="/contato">Contato</a>
<br>
"""

@app.route("/")
def index():
  return menu + "Olá, mundo! Esse é meu site. (Graziela França)"

@app.route("/sobre")
def sobre():
  return menu + "Aqui vai o conteúdo da página Sobre"

@app.route("/contato")
def contato():
  return menu + "Aqui vai o conteúdo da página Contato"


@app.route("/promocoes")
def promocoes():
  conteudo = menu + """
  Encontrei as seguintes promoções no <a href="https://t.me/promocoeseachadinhos">@promocoeseachadinhos</a>:
  <br>
  <ul>
  """
  for promocao in ultimas_promocoes():
    conteudo += f"<li>{promocao}</li>"
  return conteudo + "</ul>"


@app.route("/promocoes2")
def promocoes2():
  conteudo = menu + """
  Encontrei as seguintes promoções no <a href="https://t.me/promocoeseachadinhos">@promocoeseachadinhos</a>:
  <br>
  <ul>
  """
  scraper = ChannelScraper()
  contador = 0
  for message in scraper.messages("promocoeseachadinhos"):
    contador += 1
    texto = message.text.strip().splitlines()[0]
    conteudo += f"<li>{message.created_at} {texto}</li>"
    if contador == 10:
      break
  return conteudo + "</ul>"

@app.route("/dedoduro")
def dedoduro():
  mensagem = {"chat_id": TELEGRAM_ADMIN_ID, "text": "Alguém acessou a página dedo duro!"}
  resposta=requests.post(f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage", data=mensagem)
  return f"Mensagem enviada. Resposta ({resposta.status_code}): {resposta.text}"

@app.route("/dedoduro2")
def dedoduro2():
  sheet.append_row(["Graziela", "França", "a partir do Flask"])
  return "Planilha escrita"

@app.route("/telegram-bot", methods=["POST"])
def telegram_bot():
    update = request.json
    if "text" not in update["message"]:
        return "Não é um texto!"  # Retorna imediatamente se não for um texto

    message = update["message"]["text"]
    chat_id = update["message"]["chat"]["id"]
    datahora = str(datetime.datetime.fromtimestamp(update["message"]["date"]))

    if "username" in update["message"]["from"]:
        username = update["message"]["from"]["username"]
    else:
        username = "[não definido]"

    print(f"[{datahora}] Nova mensagem de {first_name} @{username} ({chat_id}): {message}")
    mensagens.append([datahora, "recebida", username, first_name, chat_id, message])

    # Define qual será a resposta e envia
    if message.lower().strip() == "olá, tatu" or message.lower().strip() == "ola, tatu":
        texto_resposta = "Olá! Se quer receber as notícias de sites independentes do Nordeste me envie seu e-mail, por favor"
    else:
        texto_resposta = "Não entendi! Se quiser ter acesso às matérias de sites indepentes do Nordeste, envie seu e-mail, por favor "

    nova_mensagem = {"chat_id": chat_id, "text": texto_resposta}
    requests.post(f"https://api.telegram.org./bot{token}/sendMessage", data=nova_mensagem)
    mensagens.append([datahora, "enviada", username, first_name, chat_id, texto_resposta])

    requests.post(f"https://api.telegram.org./bot{TELEGRAM_API_KEY}/sendMessage", data=nova_mensagem)
    return "ok"

  
