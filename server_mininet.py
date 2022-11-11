import socket
import os
from encryption import *
 
header_size = 2048
port = 6100
host = "10.0.0.1"
address = (host, port)
format = 'utf-8'
disconnect = "disconnect"
directory = '/home/kali/Desktop'
shift = 4
 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(address)
 
# Main function that implements encryption-decryption based on user input
def encryption_func(text, encryption_type, encrypt):
    if encryption_type == '1':
        return text
    elif encryption_type == '2' and encrypt:
        return caesar_encrypt(text,shift)
    elif encryption_type == '2' and not encrypt:
        return caesar_decrypt(text,shift)
    elif encryption_type == '3':
        return transpose_encrypt(text)
    else:
        return text

# Command Handling from server side for different commands as per user input
def CWD(conn,encryption_type):
   conn.send(encryption_func(f"The current directory path is: {os.getcwd()}",encryption_type,True).encode(format))
 
def LS(conn,encryption_type):
   dir_list = os.listdir(os.getcwd())
   conn.send(encryption_func(f"The current directory contains: {dir_list}",encryption_type,True).encode(format))
 
def CD(conn,cmd,encryption_type):
   path = cmd[3:len(cmd)-1]
   os.chdir(path)
   conn.send(encryption_func("Directory Changed!",encryption_type,True).encode(format))
 
def DWD(conn,cmd,encryption_type):
   filename = cmd[4:len(cmd)-1]
   exist = '1'
   if not os.path.isfile(filename):
       exist = '0'
   conn.send(encryption_func(exist,encryption_type,True).encode(format))
   if exist == '1':
       with open(filename, 'rb') as reqFile:
           while True:
               data = reqFile.read(header_size)
               if not data:
                   break

               data_decoded = data.decode(format)
               data_encrypted = encryption_func(data_decoded,encryption_type,True)
               conn.sendall(data_encrypted.encode(format))
           reqFile.close()
       conn.close()
 
def UPD(conn,cmd,encryption_type):
   filename = cmd[4:len(cmd)-1]
   filename = os.path.basename(filename)
 
   with open(os.path.join(directory, filename), 'wb') as newFile:
       while True:
           data = conn.recv(header_size)
           if not data:
               break
           data_decoded = data.decode(format)
           data_decrypted = encryption_func(data_decoded,encryption_type,False)
           newFile.write(data_decrypted.encode(format))
       newFile.close()
 
# Handling Client as per the commands received
def handle_client(conn, addr):
   print(f"[NEW CONNECTION] {addr} connected.")
   encryption_type = conn.recv(header_size).decode(format)
   connected = True
   while connected:
       
       cmd_len = encryption_func(conn.recv(header_size).decode(format),encryption_type,False)
       if cmd_len:
           cmd_len = int(cmd_len)
           cmd = encryption_func(conn.recv(cmd_len).decode(format),encryption_type,False)

           # Handling Different Commands

           if cmd.lower() == "cwd":
               CWD(conn,encryption_type)
          
           elif cmd.lower() == "ls":
               LS(conn,encryption_type)
 
           elif cmd[0:3].lower() == "cd<" and cmd[len(cmd)-1] == ">":
               CD(conn,cmd,encryption_type)
 
           elif cmd[0:4].lower() == "dwd<" and cmd[len(cmd)-1] == ">":
               DWD(conn,cmd,encryption_type)
               connected = False
 
           elif cmd[0:4].lower() == "upd<" and cmd[len(cmd)-1] == ">":
               UPD(conn,cmd,encryption_type)
               connected = False
 
           elif cmd == disconnect:
               conn.send(encryption_func(f"Connection Disconnected!",encryption_type,True).encode(format))
               connected = False

           else:
               conn.send(encryption_func("ERROR! Wrong Command",encryption_type,True).encode(format))
 
   conn.close()
 
# Main function that starts the server
def start_server():
   server.listen()
   print(f"[LISTENING] The server {host} is listening")
   while True:
       conn, addr = server.accept()
       handle_client(conn, addr)
 
 
print("[STARTING] server is starting...")
start_server()
