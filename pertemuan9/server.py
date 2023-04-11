import socket
import select
import sys
import os
import time
import textwrap

server_addr = ('127.0.0.1',80)
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 100)
server_sock.bind(server_addr)
server_sock.listen(1000)

input_socket = [server_sock]

def generate_headers(response_code,content_length):
        header = ''
        if response_code == 200:
            header += 'HTTP/1.1 200 OK\r\n'
        elif response_code == 404:
            header += 'HTTP/1.1 404 Not Found\r\n'

        time_now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        header += 'Date: {now}\r\n'.format(now=time_now)
        header += 'Server: Simple-Python-Server\r\n'
        header += 'Content-Length:'+str(content_length)+'\r\n\r\n'
        # header += 'Connection: close\r\n\r\n' # Signal that connection will be closed after completing the request
        return header

def return_list_html(arr:list,d:str):
    html = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Document</title>
            </head>
            <body>
                <h1>List of files</h1>
                <ul>
            """
    if d != ".":
        html += f"""
                <a href="../">..</a></br>
                """
    else:
        d = ""
    for i in arr:
        if os.path.isdir(d+i):
            html += f"""
                    <a href="{i+'/'}">{i}</a></br>
                    """
        else :
            html += f"""
                    <a href="{i}" download>{i}</a></br>
                    """
        
    html += f"""
                </ul>
            </body>
            </html>
            """
    return html

def list_files(d:str):
    arr = os.listdir(d)
    response_data = ''
    f = open('list.html', 'w')
    html = return_list_html(arr,d)
    f.write(textwrap.dedent(html))
    f.close()

    g = open('list.html', 'r')
    response_data = g.read()
    g.close()
    content_length = len(response_data)
    response_header = 'HTTP/1.1 200 OK \r\n Content-Type: text/html; charset=UTF-8\r\nContent-Length:'+str(content_length)+'\r\n\r\n'
    return response_header, response_data
try :
    while True :
        read_r, write_r, exception = select.select(input_socket, [],[],0)
        for sock in read_r:
            if sock == server_sock:
                client_sock, client_addr = server_sock.accept()
                input_socket.append(client_sock)
            else :
                data = sock.recv(4096).decode()

                if not data: break
                print(data)

                request_header = data.split("\r\n")
                request_file = request_header[0].split()[1]
                print(request_header)

                if request_file == "/":
                    is_exists = os.path.exists("index.html")
                    if is_exists:
                        f = open("index.html",'r')
                        response_data = f.read()
                        f.close()

                        content_length = len(response_data)
                        response_header = 'HTTP/1.1 200 OK \r\n Content-Type: text/html; charset=UTF-8\r\nContent-Length:'+str(content_length)+'\r\n\r\n'
                    else :
                        response_header, response_data = list_files(".")
                else:
                    is_exists = os.path.exists(request_file[1:])
                    if is_exists == False:
                        response_data = '<html><body><center><h1>Error 404: File not found</h1></center><p>Head back to <a href="/">dry land</a>.</p></body></html>'
                        response_header = generate_headers(404,len(response_data))
                    else:
                        if os.path.isdir(request_file[1:]):
                            response_header, response_data = list_files(request_file[1:])
                        else:
                            g = open(request_file[1:])
                            response_data = g.read()
                            g.close()
                            content_length = len(response_data)
                            response_header = 'HTTP/1.1 200 OK \r\n Content-Type: text/html; charset=UTF-8\r\nContent-Length:'+str(content_length)+'\r\n\r\n'
                sock.send((response_header + response_data).encode())

except KeyboardInterrupt:
    server_sock.close()
    sys.exit(0)