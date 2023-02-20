#menyimpan informasi koneksi dan pesan ke sebuah log file
import socket
import sys
import os
from datetime import datetime
server_addr = ('localhost', 5000)

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind(server_addr)
server_socket.listen(5)
client_socket, client_address = server_socket.accept()

if __name__ == "__main__":
    try:
        while True:            
            data = client_socket.recv(8388608).decode()
            if data.lower().strip() == "asklog":
                print("asklog")
                f = open("./challenge1.log","r")
                strck = f.read()
                client_socket.send(strck.encode())
                f.close()
                continue
            if data.lower().split()[0] == "/sendfile":
                ack = "ok"
                client_socket.send(ack.encode())
                f = open("file/"+data.split[1])
                client_socket.recv(8388608)
                f.write()
                f.write()
                continue
            if data.lower().strip() != "bye":
                curtime = datetime.now()                
                f = open("./challenge1.log","a")
                print(str(data))
                f.write(str(curtime)+str(client_socket)+ str(client_address)+ ">"+ str(data)+"\n")
                ack = str(curtime)+str(client_address)+str(data)+"\n"
                client_socket.send(ack.encode())
                f.close()
            else:
                client_socket.close()
            

    except KeyboardInterrupt:
        server_socket.close()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)