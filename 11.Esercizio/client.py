import requests


op_scelta = 1

while op_scelta != '0':
    op_scelta = input("Scegliere una delle seguenti opzioni:\n0)Per uscire\n1)Mostra le diverse categorie \n2)Effettua una ricerca per categoria \n3)Ricerca per parola\n")

    if op_scelta == '1':
        ritorno = requests.get("https://api.chucknorris.io/jokes/categories")
        print(eval(ritorno.text))
    elif op_scelta == '2':
        categoria = input("Inserire una categoria: ")
        ritorno = requests.get("https://api.chucknorris.io/jokes/random", params={"category":categoria})
        print(eval(ritorno.text)["value"])
    elif op_scelta == '3':
        parola = input("Inserire la parola: ")
        ritorno = requests.get("https://api.chucknorris.io/jokes/search", params={"query":parola})
        print("Frasi trovate: ")
        for risultato in eval(ritorno.text)["result"]:
            print(f"{risultato['value']}\n\n")
