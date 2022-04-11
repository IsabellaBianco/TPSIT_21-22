import socket as sck
import time

# ci sono delle variabili che risalgono ad ARPANET
# tipo SOCK_STREAM, SOCK_DGRAM, AF_INET, AF_INET6
# SOCK_STREAM  --> utilizzato per indicare TCP
# SOCK_DGRAM   --> utilizzato per indicare UDP
# AF_INET      --> utilizzato per indicare il protocollo IPv4
# AF_INET6     --> utilizzato per indicare il protocollo IPv6

# Il server inizia ad eseguire sempre per primo
# se io volessi indicare l'indirizzo ip del pc senza però mettere il suo relae indirizzo ip
# utilizzo l'indirizzo ip: 0.0.0.0

LOCAL_HOST = '0.0.0.0'
N_PORTA = 5000

s = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)

s.bind((LOCAL_HOST, N_PORTA))
dictClient = {}

def inviaMessaggioaTutti(msg):
    for _, addr in dictClient.items():
        s.sendto(msg.encode(), addr)

def inviaMessaggio(msg):
    destinatario = msg.split(",")[1].split(":")[1]
    if(destinatario in dictClient.keys()):

        s.sendto(msg.encode(), dictClient[destinatario])
        

def controlloNickname(nickname, addr):
    if(nickname in dictClient.keys()):
        msg = "Il nickname e' gia' presente!"
    else:
         #inviaMessaggioaTutti((f"si è unito alla chat"))
         dictClient[nickname] = addr
         msg = "nickname inserito"
    print(f"client: {dictClient}")
    s.sendto("OK".encode(), addr)

    return msg

def eNickname(msg, addr):
    try:
        print("È un nickname")
        msg = msg.split("Nickname:")[1]
        controlloNickname(msg, addr)
    except:
        print("È un messaggio")
        eMessaggio(msg)

def eMessaggio(msg):
    if((msg.split(",")[1].split(":")[1]) == "tutti"):
        inviaMessaggioaTutti(msg)
    else:
        inviaMessaggio(msg)
    

def get_key(val):
    for key, value in dictClient.items():
         if val == value:
             return key

def main():
    global dictClient
    
    while True:
        messaggio, addr = s.recvfrom(4096)
        print(messaggio.decode())
        msg = eNickname(messaggio.decode(), addr)
            



if __name__ == "__main__":
    main()