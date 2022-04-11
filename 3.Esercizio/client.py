from ctypes import POINTER
import socket as sck
import threading

LOCAL_HOST = '192.168.1.240'
N_PORTA = 5001
nickname = ""

class Receiver(threading.Thread):
    def __init__(self,sock):
        threading.Thread.__init__(self)
        self.sock = sock
        self.running = True
    def run(self):
        while self.running:
            data =  self.sock.recv(4096).decode()
            data = data.split(",")
            ricevente = str(data[0]).split(":")[1]
            msg = data[2]
            print(f"{ricevente}: {msg}") 

def main():
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)

    s.connect((LOCAL_HOST, N_PORTA)) # tupla --> indirizzo ip, porta
    rec = Receiver(s)
    nickname = input('Inserire il nickname: ')
    data = (f"Nickname:{nickname}")
    print(f"messaggio di hello: {data}")
    s.sendall(data.encode())
    data = s.recv(4096)
    data = data.decode()
    print(data)
    if(data != "OK"):
        exit
    rec.start()
    while True:
            data = input("Scrivi messaggio:")
            ricevente = input("A chi lo vuoi inviare: ")
            s.sendall((f"Sender:{nickname},Receveir:{ricevente},{data}").encode())

    
    rec.join()
    
if __name__ == "__main__":
    main()