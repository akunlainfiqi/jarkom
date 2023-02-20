import socket
import sys

server_addr = ('localhost',5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_addr)

while __name__ == "__main__":
    try:
        a = input("msg > ")
        while a.lower().strip != "bye":    
            client_socket.send(a.encode())
            data = client_socket.recv(1024).decode()
            print(str(data))
            a = input("msg > ")

        client_socket.close()

    except KeyboardInterrupt:
        client_socket.close()
        sys.exit(0)