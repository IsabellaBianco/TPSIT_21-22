from flask import jsonify, request
import flask
import sqlite3
from pathlib import Path
import pandas as pd

app = flask.Flask(__name__)
app.config["DEBUG"] = True

dir_path = str(Path(__file__).parent.resolve())

books = [
    {'id':0,
    'title': 'Il nome della Rosa',
    'author': 'Umberto Eco',
    'year_published': '1980'},
    {'id':1,
    'title': 'Il problema dei tre corpi',
    'author': 'Liu Cixin',
    'year_published': '2008'},
    {'id':2,
    'title': 'Fondazione',
    'author': 'Isaac Asimov',
    'year_published': '1951'}
]



@app.route('/', methods=['GET'])
def home():
    return "<h1>Biblioteca online</h1><p>Prototipo di web API</p>"

@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    con = sqlite3.connect(f"{dir_path}/libri.db")
    cur = con.cursor()
    libri = cur.execute(f"SELECT * FROM libri").fetchall()
    con.close()
    return jsonify(libri)

@app.route('/api/v1/resources/books', methods=['GET'])
def api_id():
    if 'id' in request.args:
        con = sqlite3.connect(f"{dir_path}/libri.db")
        cur = con.cursor()
        results = cur.execute(f"SELECT * FROM libri WHERE id = {request.args['id']}").fetchall()
        con.close()

        return jsonify(results)
    
    elif 'title' in request.args:
        con = sqlite3.connect(f"{dir_path}/libri.db")
        cur = con.cursor()
        results = cur.execute(f"SELECT * FROM libri WHERE titolo = '{request.args['title']}'").fetchall()
        con.close()
        return jsonify(results)

    else: return "Error: No id or name field provided."

    



app.run()

