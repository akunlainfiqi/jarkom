#menyimpan informasi koneksi dan pesan ke sebuah log file
import socket
import sys
import os
from datetime import datetime
server_addr = ('localhost', 5000)

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind(server_addr)
server_socket.listen(5)

if __name__ == "__main__":
    while True:
        try:
            client_socket, client_address = server_socket.accept()
            data= client_socket.recv(1024).decode()
            curtime = datetime.now()
                        
            f = open("./challenge1.log","a")
            print(str(data))
            f.write(str(curtime)+str(client_socket)+ str(client_address)+ ">"+ str(data)+"\n")
            client_socket.close()
            
            f.close()
            

        except KeyboardInterrupt:
            server_socket.close()
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)
            break