import socket as sck
import time
import threading

# ci sono delle variabili che risalgono ad ARPANET
# tipo SOCK_STREAM, SOCK_DGRAM, AF_INET, AF_INET6
# SOCK_STREAM  --> utilizzato per indicare TCP
# SOCK_DGRAM   --> utilizzato per indicare UDP
# AF_INET      --> utilizzato per indicare il protocollo IPv4
# AF_INET6     --> utilizzato per indicare il protocollo IPv6

# la porta del server la decido io mentre la porta del client la decide il SO

LOCAL_HOST = '192.168.1.240'
N_PORTA = 5000
nickname = ""

s = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)


class Receiver(threading.Thread):
    def __init__(self,sock):
        threading.Thread.__init__(self)
        self.sock = sock
        self.running = True
    def run(self):
        while self.running:
            data, _ = self.sock.recvfrom(4096)
            data = data.decode().split(",")
            ricevente = str(data[0]).split(":")[1]
            msg = str(data[2])
            print(f"{ricevente}: {msg}") 
def main():
    receiver = Receiver(s)
    try:
        nickname = input('Inserire il nickname: ')
        data = (f"Nickname:{nickname}")
        print(f"messaggio di hello: {data}")
        s.sendto(data.encode(), (LOCAL_HOST, N_PORTA))
        data, addr = s.recvfrom(4096)
        data = data.decode()
        print(data)
        if(data != "OK"):
            exit
        receiver.start()
        while True:
             data = input("Scrivi messaggio:")
             ricevente = input("A chi lo vuoi inviare: ")
             s.sendto((f"Sender:{nickname},Receveir:{ricevente},{data}").encode(), (LOCAL_HOST, N_PORTA))
    except:
        sck.close()

if __name__ == "__main__":
    main()


"""
Da modificare 
INVIO UN MESSAGGIO: "Sender:{nickname_mittente}, Receveir:{nickname ricevente}, msg"
"""