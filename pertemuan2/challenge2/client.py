import socket
import sys

server_addr = ('127.0.0.1', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_addr)

sys.stdout.write('>> ')

try:
    while True:
        message = str(input())
        with open(message) as f:
            lines = f.readlines()
            for line in lines:
                client_socket.send(line.encode())
                sys.stdout.write(client_socket.recv(1024).decode())
            f.close()
        sys.stdout.write('>> ')
except KeyboardInterrupt:
    client_socket.close()
    sys.exit(0)