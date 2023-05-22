import smtplib
import time
import email
import imaplib
import zipfile
import os
import shutil

SRC_EMAIL =""
SRC_PASS = ""

run = True


mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(SRC_EMAIL,SRC_PASS)
mail.select('INBOX')

while run:
    try:
        command = input("Masukkan prompt >> ")
        cmd = command.split()[0]
        if command.split()[0] == "findmail":
            key = command.split()[1]
            n = int(command.split()[2])
            currenttime = time.time()
            type,data = mail.search(None,f'(SUBJECT "{key}")')
            c = 1;
            foldername = SRC_EMAIL.split(".")[0]+str(currenttime).split(".")[0].strip()
            os.makedirs(foldername, exist_ok=True)
            for i in reversed(data[0].split()):
                if c > n:
                    break
                typ, dat = mail.fetch(i,'(RFC822)')
                msg = email.message_from_bytes(dat[0][1])
                filename = "".join(x for x in str(msg["subject"]) if x.isalnum())+".txt"
                if msg.get_content_maintype() == 'multipart':
                    for part in msg.walk():
                        if part.get_content_maintype() == 'multipart':
                            continue
                        if part.get('Content-Disposition') is None:
                            continue

                        # Save the attachment
                        filename = part.get_filename()
                        if filename:
                            attachment_path = os.path.join(foldername, filename)
                            with open(attachment_path, 'wb') as file:
                                file.write(part.get_payload(decode=True))
                            print(f"Saved attachment: {filename}")

                print(filename)
                fpath = os.path.join(foldername,filename)
                f = open(fpath,"w")
                f.write(str(msg))
                f.close()
                c+=1
            
            zipname = foldername+".zip"
            with zipfile.ZipFile(zipname,'w') as zf:
                for r,d,f in os.walk(foldername):
                    for file in f:
                        fpath = os.path.join(r,file)
                        zf.write(fpath, file)
            
            shutil.rmtree(foldername)
            print('hehe')
        if command.split()[0] == "downmail":
            currenttime = time.time()
            n = int(command.split()[1])
            type,data = mail.search(None,'ALL')
            c = 1;
            foldername = SRC_EMAIL.split(".")[0]+str(currenttime).split(".")[0]
            os.makedirs(foldername, exist_ok=True)
            for i in reversed(data[0].split()):
                if c > n:
                    break
                typ, dat = mail.fetch(i,'(RFC822)')
                msg = email.message_from_bytes(dat[0][1])
                filename = "".join(x for x in str(msg["subject"]) if x.isalnum())+".txt"
                if msg.get_content_maintype() == 'multipart':
                    for part in msg.walk():
                        if part.get_content_maintype() == 'multipart':
                            continue
                        if part.get('Content-Disposition') is None:
                            continue

                        # Save the attachment
                        filename = part.get_filename()
                        if filename:
                            attachment_path = os.path.join(foldername, filename)
                            with open(attachment_path, 'wb') as file:
                                file.write(part.get_payload(decode=True))
                            print(f"Saved attachment: {filename}")
                fpath = os.path.join(foldername,filename)
                f = open(fpath,"w")
                f.write(str(msg))
                f.close()
                c+=1
            
            zipname = foldername+".zip"
            with zipfile.ZipFile(zipname,'w') as zf:
                for r,d,f in os.walk(foldername):
                    for file in f:
                        fpath = os.path.join(r,file)
                        zf.write(fpath, file)
            
            shutil.rmtree(foldername)
            print('hehe')
        if cmd == "exit":
            run = False
    except Exception as e:
        print(e)