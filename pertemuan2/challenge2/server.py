import socket
import select
import sys

server_addr = ('127.0.0.1', 5000)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_addr)
server_socket.listen(5)

input_socket = [server_socket]

def isPalindrome(s):
    if s == s[::-1]:
        return "yes"
    return "no"

try:
    while True:
        read_ready, write_ready, exception = select.select(input_socket, [], [])

        for sock in read_ready:
            if sock == server_socket:
                client_socket, client_addr = server_socket.accept()
                input_socket.append(client_socket)
            else:
                data = sock.recv(1024).decode()
                res = str(data).strip() + "-" + isPalindrome(str(data).strip())            
                f = open('result.txt','a')
                f.write(res+"\n")
                f.close()
                print(sock.getpeername(), str(res))
                if str(data):
                    sock.send(res.encode())
                else:
                    sock.close()
                    input_socket.remove(sock)

except KeyboardInterrupt:
    server_socket.close()
    sys.exit(0)