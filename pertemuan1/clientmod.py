import socket
import sys

ip = input("ip>")
port = input(" port> ")
server_addr = ('localhost',5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_addr)

while __name__ == "__main__":
    try:
        a = input("msg > ")
        while a.lower().strip != "bye":  
            if a.lower().split()[0] == "/sendfile":
                filename = data.split()[0]
                client_socket.send(data.split()[1])
                data = client_socket.recv(1024).decode()
                f = open("./"+filename,'rb')
                client_socket.send(f.read())
                continue
            client_socket.send(a.encode())
            data = client_socket.recv(8388608).decode()
            print(str(data))
            a = input("msg > ")

        client_socket.close()

    except KeyboardInterrupt:
        client_socket.close()
        sys.exit(0)