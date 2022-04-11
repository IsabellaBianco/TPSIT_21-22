import socket as sck
import time
import sqlite3
import threading as thr

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
N_PORTA = 5001
NUM_MAX_CLIENTI = 15

clients = []

dir_path = "/home/isa/Desktop/Isa/Scuola/Quinta/TPSIT/PRATICA/3.chat_di_gruppo_database_TCP/"


class Client_manager(thr.Thread):
    def __init__(self, connection, address):
        thr.Thread.__init__(self)
        self.connection = connection
        self.address = address
        self.running = True
    
    def run(self):
        while self.running:
            received_msg = self.connection.recv(4096)
            msg = self.eNickname(received_msg.decode(), self.address)

            print(f"{thr.current_thread}>>Messaggio ricevuto da {self.address}: {received_msg.decode()}")


    def inviaMessaggioaTutti(self, msg):
        i=0
        con = sqlite3.connect(f'{dir_path}utenti.db')
        cur = con.cursor()
        for row in cur.execute('SELECT * FROM Utenti_chat ORDER BY Nickname'):
            clients[i].connection.sendall(msg.encode())
            i +=1
        con.close()

    def inviaMessaggio(self, msg, destinatario):
        con = sqlite3.connect(f'{dir_path}utenti.db')
        cur = con.cursor()
        i = 0
        for row in cur.execute('SELECT * FROM Utenti_chat ORDER BY Nickname'):
            if(destinatario == row[0]):
                clients[i].connection.sendall(msg.encode())
                print("Messaggio inviato")
                exit
            i +=1
        con.close()
            
    

    def controlloNickname(self, nickname, addr):
        con = sqlite3.connect(f'{dir_path}utenti.db')
        cur = con.cursor()
        isNew = True
        msg = "Qualcosa e' andato storto! Riprova"
        for row in cur.execute('SELECT * FROM Utenti_chat ORDER BY Nickname'):
            if(nickname == row[0]):
                msg = "Il nickname e' gia' presente!"
                isNew = False
                exit
        if isNew:
            self.inviaMessaggioaTutti((f"Sender:{nickname}, Receveir:all, {nickname} si e' unito alla chat"))
            cur.execute(f"INSERT INTO Utenti_chat VALUES ('{nickname}','{addr[0]}',{addr[1]})")
            con.commit()
            msg = "nickname inserito"
        
        
        #Stampa tutti gli utenti
        for row in cur.execute('SELECT * FROM Utenti_chat ORDER BY Nickname'):
            print(f"{row[0]}: indirizzo IP {row[1]}, porta {row[2]}")

        self.connection.sendall("OK".encode())
        con.close()
        print(f"msg: {msg}")
        return msg
    

    def eNickname(self, msg, addr):
        try:
            print("È un nickname")
            msg = msg.split("Nickname:")[1]
            self.controlloNickname(msg, addr)
        except:
            print("È un messaggio")
            self.eMessaggio(msg)

    def eMessaggio(self, msg):
        if(("all" in msg.split(",")[1])):
            self.inviaMessaggioaTutti(msg)
        else:
            self.inviaMessaggio(msg, msg.split(",")[1].split(":")[1])
    
def main():

    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    s.bind(("0.0.0.0", 5001))

    s.listen(NUM_MAX_CLIENTI)
    while True:
        connection, address = s.accept()
        client = Client_manager(connection, address)
        client.start()
        clients.append(client)
    
    """  while True:
        messaggio, addr = s.recvfrom(4096)
        print(messaggio.decode())
        msg = eNickname(messaggio.decode(), addr)"""
            



if __name__ == "__main__":
    main()

