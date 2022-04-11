from flask import Flask, render_template, request, redirect, url_for, make_response
import random
import string
import sqlite3
from datetime import datetime
from sympy import *

x, y, z = symbols("x y z")

PATH = "/home/isa/Desktop/Isa/Scuola/Quinta/TPSIT/PRATICA/12.Esercitazione/"
app = Flask(__name__)

token = ''.join(random.choices(string.ascii_uppercase +
                               string.digits, k=15))

def validate(username, password):
    completion = False
    con = sqlite3.connect(f"{PATH}integrali.db")
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
            resp = make_response(redirect(url_for('ottieniIntegrale')))
            resp.set_cookie('username', username)
            return resp
    return render_template('login.html', error=error)


@app.route(f'/{token}', methods=['GET', 'POST'])
def ottieniIntegrale():
    if request.method == 'POST':
        utente = request.cookies.get('username')
        if request.form['calcola'] == "calcola_integrale_definito":
            soluzione = calcolaIntegrale(request.form['int_definito'], utente, True, estremo_sup=request.form['estremo_maggiore'], estremo_inf=request.form['estremo_minore'])
        elif request.form['calcola'] == "calcola_integrale_indefinito":
            soluzione = calcolaIntegrale(request.form['int_indefinito'], utente, False)
        return render_template("index.html", soluzione=soluzione) 
    return render_template("index.html")
        
def calcolaIntegrale(funzione, id_utente, eDefinito, estremo_sup=0, estremo_inf=0):
    data = datetime.now().strftime('%d/%m/%Y')
    ora = datetime.now().strftime('%H:%M:%S')

    try:
        if eDefinito:
            soluzione = str(integrate(eval(funzione), (x, estremo_inf, estremo_sup)))
        else: soluzione = str(integrate(eval(funzione), x))
    except:
        return "Errore nel calcolo"
    
    #Memorizzazione nel database
    con = sqlite3.connect(f"{PATH}integrali.db")
    cur = con.cursor()

    if eDefinito:
        cur.execute(f"INSERT INTO integrali (integrale, e_inf, e_sup, soluzione, data, ora)" \
        f"VALUES ('{funzione}', '{estremo_inf}', '{estremo_sup}', '{soluzione}', '{data}', '{ora}')")
    else:
        cur.execute(f"INSERT INTO integrali (integrale, soluzione, data, ora)" \
        f"VALUES ('{funzione}', '{soluzione}', '{data}', '{ora}')")
    con.commit()

    id_integrale = cur.execute(f"SELECT id_integrale FROM integrali WHERE data='{data}' and ora='{ora}'").fetchall()[0][0]
    cur.execute(f"INSERT INTO calcoli (id_utente, id_integrale) VALUES ('{id_utente}', {id_integrale})")
    con.commit()
    cur.close()
    return f"Soluzione: {soluzione}"



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')