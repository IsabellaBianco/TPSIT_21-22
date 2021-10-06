import socket as sck
import time
import sqlite3

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

con = sqlite3.connect('/home/isa/Desktop/Isa/Scuola/Quinta/TPSIT/PRATICA/2.chat_di_gruppo_databse/utenti.db')
cur = con.cursor()
s = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)

s.bind((LOCAL_HOST, N_PORTA))

def inviaMessaggioaTutti(msg):
    for row in cur.execute('SELECT * FROM Utenti_chat ORDER BY Nickname'):
        s.sendto(msg.encode(), (row[1], row[2]))

def inviaMessaggio(msg):
    destinatario = msg.split(",")[1].split(":")[1]

    for row in cur.execute('SELECT * FROM Utenti_chat ORDER BY Nickname'):
        if(destinatario == row[0]):
             s.sendto(msg.encode(), (row[1], row[2]))
        

def controlloNickname(nickname, addr):
    isNew = True
    for row in cur.execute('SELECT * FROM Utenti_chat ORDER BY Nickname'):
        if(nickname == row[0]):
            msg = "Il nickname e' gia' presente!"
            isNew = False
            exit
    if isNew:
         #inviaMessaggioaTutti((f"si è unito alla chat"))
         cur.execute(f"INSERT INTO Utenti_chat VALUES ('{nickname}','{addr[0]}',{addr[1]})")
         con.commit()
         msg = "nickname inserito"
    
    #Stampa tutti gli utenti
    for row in cur.execute('SELECT * FROM Utenti_chat ORDER BY Nickname'):
        print(f"{row[0]}: indirizzo IP {row[1]}, porta {row[2]}")

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
    
def main():
    
    while True:
        messaggio, addr = s.recvfrom(4096)
        print(messaggio.decode())
        msg = eNickname(messaggio.decode(), addr)
            



if __name__ == "__main__":
    main()

"""
_____________CODICE PER ITERARE:____________
con = sqlite.connect("percorso/nome_database")
cur = con.cursor()
for row in cur.execute("SELECT * FROM utenti"):
    print(row)
con.close()
_____________________________________________
"""