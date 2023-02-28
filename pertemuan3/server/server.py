import select
import socket
import sys
import threading

threads = []
class Server:
    def __init__(self):
        self.host = 'localhost'
        self.port = 5008
        self.backlog = 5
        self.size = 1024
        self.server = None

    def open_socket(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host,self.port))
        self.server.listen(5)

    def run(self):
        self.open_socket()
        input = [self.server]
        running = 1
        while running:
            inputready,outputready,exceptready = select.select(input,[],[])

            for s in inputready:
                if s == self.server:
                    # handle the server socket
                    c = Client(self.server.accept())
                    c.start()
                    threads.append(c)
                    
                    print(threads)
                elif s == sys.stdin:
                    print("hai")
                    
                    print(s)
                    # handle standard input
                    junk = sys.stdin.readline()
                    running = 0
                print(1)
            print(input)
	 # close all threads
        self.server.close()
        for c in threads:
            print(c)
            c.join()

class Client(threading.Thread):
    def __init__(self, (client, address)):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.size = 1024

    def run(self):
        running = 1
        while running:
            data = self.client.recv(self.size)
            print ('recv: ' + str(self.address) + str(data) + str(threads))
            for c in threads:
                print(c)
                c.send("tes")

            if data:
                self.client.sendall((str(data)+"response\n").encode())
            else:
                self.client.close()
                running = 0
    def send(self, message):
        data = self.client.send("tes".encode())

if __name__ == "__main__":
    s = Server()
    s.run()
