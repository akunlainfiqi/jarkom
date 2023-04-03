import socket
import select
import sys
from threading import Thread
import ftplib


#membuka file config dan menginisiasi koneksi ftp
with open("config.txt") as r:
    a = r.readlines()
    ftpip = a[0].split('\r')[0]
    ftpusername = a[1].split('\r')[0]
    ftppassword = a[2]
    f = ftplib.FTP("localhost")
    f.login("user_1", "abc")
    print("successfull connect ftp")

#menghubungkan ke server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_address = '127.0.0.1'
port = 8081
server.connect((ip_address, port))

def send_msg(sock):
    while True:
        data = sys.stdin.readline()
        #ini nyari caranya sejam sendiri jadi dihilangkan newline dan membaca kata pertama
        datas = data.strip().split(" ")[0]
        #if exit karena kalau di ctrl c di windows tidak bisa keluar dan di wsl tidak bisa connect ftp
        if datas == "exit":
            raise KeyboardInterrupt()
        #if list fitur tambahan list
        elif datas == "LIST":
            print(str(f.nlst()))
        #if pwd fitur tambahan pwd
        elif datas == "PWD":
            x = f.sendcmd(datas)
            print(x)
        #if cd fitur tambahan cd
        elif datas == "CD":
            x = f.cwd(data.strip().split(" ")[1])
            print(x)
        #if mkdir fitur tambahan mkdir
        elif datas == "MKDIR":
            x = f.mkd(data.strip().split(" ")[1])
        #if SENDALL tidak selesai karena tidak cukup waktu
        # elif datas == "SENDALL":
        #     break
        else:
            sock.send(data.encode())
            sys.stdout.write('<You>')
            sys.stdout.write(data)
            sys.stdout.flush()

def recv_msg(sock):
    while True:
        data = sock.recv(2048)
        sys.stdout.write(data.decode())

Thread(target=send_msg, args=(server,)).start()
Thread(target=recv_msg, args=(server,)).start()

#coba-coba mencari cara agar bisa keluar di windows ternyata tidak bisa jadi ya sudahlah
while True:
    try:
        sockets_list = [server]
        read_socket, write_socket, error_socket = select.select(sockets_list, [], [])
        for socks in read_socket:
            if socks == server:
                recv_msg(socks)
            else:
                send_msg(socks)
    except:
        server.close()
        exit(0)