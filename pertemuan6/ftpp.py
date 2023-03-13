from ftplib import FTP

f= FTP('localhost')
print('Welcome: '+ f.getwelcome())

f.login('fiqi')
print(f.pwd)
names = f.nlst()
print(str(names))
f.quit()