import ftplib
import zipfile

a = input('username > ')
b = input('password > ')
c = input('ip > ')

if c == "":
    c = "localhost"

f = ftplib.FTP(c)
print(f.getwelcome())
f.login(a,b)

z=1
while z:
    p = input('>>')
    try :
        if p =='exit':
            z=0
            continue
        if p[:4].lower() == 'retr':
            with open(p[5:],"wb") as ft:
                print(p)
                f.retrbinary(p, ft.write)
                continue
        if p[:4].lower() == 'stor':
            with open(p[5:], "rb") as ft:
                res = f.storbinary(p, ft)
                continue
        if p[:4].lower() == 'list':
            print(str(f.nlst()))
            continue
        if p[:7].lower() == 'uptract':

            with zipfile.ZipFile(p[8:],'r') as z:
                for file in z.namelist():
                    if "/" in file:
                        namafolder = file.split('/')[0]
                        f.mkd(namafolder)
                
                    with z.open(file,"r") as ft:
                        print(ft)
                        f.storbinary("STOR "+file,ft)
            continue
        x = f.sendcmd(p)
        print(x)

    except ftplib.all_errors as e:
        print(e)