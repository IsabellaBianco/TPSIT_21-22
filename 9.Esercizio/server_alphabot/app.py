from flask import Flask, render_template, request, redirect, url_for, make_response
from Alphabot import AlphaBot
import random
import string
import sqlite3
from datetime import datetime

NON_FARE_NIENTE = "q:0"
PATH = "./"
app = Flask(__name__)
alphabot = AlphaBot()

comandi_consentiti = {"w": alphabot.avanti, "s": alphabot.indietro, "a": alphabot.sinistra
   , "d": alphabot.destra, "q": alphabot.fermo}

token = ''.join(random.choices(string.ascii_uppercase +
                               string.digits, k=15))

def validate(username, password):
    completion = False
    con = sqlite3.connect(f"{PATH}alphabot.db")
    # with sqlite3.connect('static/db.db') as con:
    cur = con.cursor()
    cur.execute("SELECT * FROM utenti")
    rows = cur.fetchall()
    for row in rows:
        dbUser = row[0]
        dbPass = row[1]
        if dbUser == username:
            completion = check_password(dbPass, password)
    con.close()
    return completion


def check_password(hashed_password, user_password):
    return hashed_password == user_password


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        completion = validate(username, password)
        if completion == False:
            error = 'Invalid Credentials. Please try again.'
        else:
            memorizza_nuovo_accesso(username)
            resp = make_response(redirect(url_for('controllaAlphaboz')))
            resp.set_cookie('username', username)
            return resp
    return render_template('login.html', error=error)


@app.route(f'/{token}', methods=['GET', 'POST'])
def controllaAlphaboz():
    if request.method == 'POST':
        utente = request.cookies.get('username')
        comando_ricevuto = "q"
        if request.form.get('avanti') == 'avanti':
            comando_ricevuto = "w"
            print("l'Alphabot va avanti")
        elif request.form.get('indietro') == 'indietro':
            comando_ricevuto = "s"
            print("l'Alphabot va indietro")
        elif request.form.get('sinistra') == 'sinistra':
            comando_ricevuto = "a"
            print("l'Alphabot va sinistra")
        elif request.form.get('destra') == 'destra':
            comando_ricevuto = "d"
            print("l'Alphabot va destra")
        elif request.form.get('fermo') == 'fermo':
            print("l'Alphabot è fermo")
        else:
            print(request.form['altro_comando'])
            comando_ricevuto= request.form['altro_comando']
        memorizza_azione(comando_ricevuto, utente)
        eseguiMovimento(comando_ricevuto)
    elif request.method == 'GET':
        return render_template('index.html')

    return render_template("index.html")

"""Questa funzione memorizza il login al database dell'utente"""
def memorizza_nuovo_accesso(utente):
    now_date = datetime.now().strftime("%d/%m/%Y")
    now_time = datetime.now().strftime("%H:%M:%S")
    con = sqlite3.connect(f"{PATH}alphabot.db")
    cur = con.cursor()
    cur.execute(f"INSERT INTO accessi (utente, data, ora)" \
         f"VALUES ('{utente}', '{now_date}', '{now_time}')")
    con.commit()
    cur.close()
"""-----------------------------------------------------------"""
"""Questa funzione memorizza le azioni"""
def memorizza_azione(azione, utente):
    now_date = datetime.now().strftime("%d/%m/%Y")
    now_time = datetime.now().strftime("%H:%M:%S")
    con = sqlite3.connect(f"{PATH}alphabot.db")
    cur = con.cursor()
    cur.execute(f"INSERT INTO registro (utente, azione, data, ora)" \
                f"VALUES ('{utente}', '{azione}', '{now_date}', '{now_time}')")
    con.commit()
    cur.close()
"""-----------------------------------------------------------"""
"""Cerca se il messaggio che ha inviato il client è il nome di una sequenza,
        nel caso contrario invia un messaggio di errore e non fa niente"""

def trovaSequenza(nome_movimento):
    # apre la connessione con il database e crea il cursore
    con = sqlite3.connect(f"{PATH}alphabot.db")
    cur = con.cursor()
    # verifica che il movimento sia all'interno del database
    for row in cur.execute('SELECT * FROM movimenti'):
        if nome_movimento == row[0]:
            con.close()
            return row[1]
    print("Il comando non è valido!")
    con.close()
    return NON_FARE_NIENTE

"""--------------------------------------------------------------------"""

"""Esegue la lista di comandi"""

def eseguiComando(comando_da_eseguire):
    lista_comandi = comando_da_eseguire.split(",")
    for comando in lista_comandi:
        comandi_consentiti[comando.split(":")[0]](float(comando.split(":")[1]))

"""--------------------------------------------------------------------"""

"""Verifica se il movimento è 'diretto' o se è il nome di una sequenza"""

def eseguiMovimento(nome_movimento):
    if nome_movimento in comandi_consentiti:
        comandi_consentiti[nome_movimento]()
    else:
        eseguiComando(trovaSequenza(nome_movimento))

"""--------------------------------------------------------------------"""

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')