from flask import Flask, render_template, request, redirect, url_for
import random
import string
import ipaddress 
import socket as sck
import sqlite3
from datetime import datetime
import pandas as pd
file_servizi = pd.read_csv("/home/isa/Desktop/Isa/Scuola/Quinta/TPSIT/PRATICA/9.Esercitazione_Verifica_2/service-names-port-numbers.csv")
file_servizi = file_servizi[["Port Number","Service Name"]]

PORTA_TROVATA = 0

app = Flask(__name__)
#s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)

token = ''.join(random.choices(string.ascii_uppercase +
                               string.digits, k=15))

@app.route('/', methods=['GET', 'POST'])
def scansione():
    error = None

    if request.method == 'POST':
        indirizzo_ip = request.form['indirizzoIP']
        porta_minima = request.form['portaMinima']
        porta_massima = request.form['portaMassima']

        if controlla_indirizzo_ip(indirizzo_ip) and porta_minima.isdigit() and porta_massima.isdigit():
            prova_connessione(indirizzo_ip, int(porta_minima), int(porta_massima))
            print("-------Scansione terminata----------")
        else:
            error = "Parametri non validi!"
            return render_template('scansione.html', error=error)
        return redirect(url_for('scansione_finita'))
    return render_template('scansione.html', error=error)

@app.route(f'/{token}', methods=['GET', 'POST'])
def scansione_finita():
    return render_template('fine.html')

"""-----------Funzioni--------------"""
def ottieni_nome_servizio(porta):
    s_ritorno = "Nessun servizio"
    try:
        s_ritorno = (file_servizi[file_servizi["Port Number"] == f"{porta}"]["Service Name"].values)[0]
    except:
        pass
    return  s_ritorno

def controlla_indirizzo_ip(indirizzo_ip):
    try:
        ipaddress.ip_address(indirizzo_ip)
        return True
    except ValueError:
        pass
    return False

def prova_connessione(indirizzo_ip, porta_minima, porta_massima):
    con = sqlite3.connect('/home/isa/Desktop/Isa/Scuola/Quinta/TPSIT/PRATICA/9.Esercitazione_Verifica_2/scansione.db')
    #Inserimento del nuovo indirizzo IP se non ?? gi?? presente
    cur = con.cursor()
    cur.execute(f"INSERT OR IGNORE INTO indirizzi (indirizzo_ip)" \
                f"VALUES ('{indirizzo_ip}')")
    con.commit()
    #---------#    

    #-----Ricavo dell'id-------#
    id_indirizzo = cur.execute(f"SELECT id FROM indirizzi WHERE indirizzi.indirizzo_ip = '{indirizzo_ip}'").fetchall()[0][0]
    #-------#

    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    for porta in range(porta_minima,porta_massima):
        #------Inserisco la porta all'interno della tabella servizi----#
        cur.execute(f"INSERT OR IGNORE INTO servizi (porta, nome_servizio)" \
                    f"VALUES ({porta}, '{ottieni_nome_servizio(porta)}')")
        con.commit()
        #-------------#

        stato = "chiusa"
        if s.connect_ex((indirizzo_ip, porta)) == PORTA_TROVATA:
            stato = "aperta"

        cur.execute(f"INSERT INTO scansionati (indirizzo_IP, porta, stato)" \
            f"VALUES ('{id_indirizzo}', {porta}, '{stato}')")
        con.commit()
    cur.close()
"""---------------------------------"""



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

