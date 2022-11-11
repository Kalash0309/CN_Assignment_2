import socket
import os
import time
from encryption import *
 
header_size = 2048
port = 6100
host = "10.0.0.1"
address = (host, port)
format = 'utf-8'
disconnect = "disconnect"
directory = '/home/kali/Desktop'
connection = True
shift = 4

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

# Command Handling from client side for different commands as per user input
def DWD_cmd(cmd,client,encryption_type):
   exist = encryption_func(client.recv(header_size).decode(format),encryption_type,False)
   if exist == '0':
       print("File Doesn't Exist")
       return
   with open(os.path.join(directory, cmd[4:len(cmd)-1]), 'wb') as newFile:
       while True:
           data = client.recv(header_size)
           if not data:
               break

           data_decoded = data.decode(format)
           data_decrypted = encryption_func(data_decoded,encryption_type,False)
           newFile.write(data_decrypted.encode(format))
       newFile.close()
   print("File Downloaded!")
 
def UPD_cmd(cmd,client,encryption_type):
   filename = cmd[4:len(cmd)-1]
 
   with open(filename, "rb") as sendFile:
       while True:
           data = sendFile.read(header_size)
           if not data:
               break
           data_decoded = data.decode(format)
           data_encrypted = encryption_func(data_decoded,encryption_type,True)
           client.sendall(data_encrypted.encode(format))
       sendFile.close()
   client.close()
   print("File Uploaded")
 
# Handling Client as per the commands received
def handle_command(cmd, client, encryption_type):
   
   cmd_length = len(cmd)
   send_length = str(cmd_length).encode(format)
   send_length += b' ' * (header_size - len(send_length))
 
   if cmd[0:4].lower() == "dwd<" and cmd[len(cmd)-1] == ">":
       start = time.process_time()
       client.send(encryption_func(send_length.decode(),encryption_type,True).encode(format))
       client.send(encryption_func(cmd,encryption_type,True).encode(format))
       DWD_cmd(cmd,client,encryption_type)
       print("Runtime for this command: ", time.process_time() - start)
       main()
 
   elif cmd[0:4].lower() == "upd<" and cmd[len(cmd)-1] == ">":
       start = time.process_time()
       client.send(encryption_func(send_length.decode(),encryption_type,True).encode(format))
       client.send(encryption_func(cmd,encryption_type,True).encode(format))
       UPD_cmd(cmd,client,encryption_type)
       print("Runtime for this command: ", time.process_time() - start)
       main()
      
   else:
       start = time.process_time()
       client.send(encryption_func(send_length.decode(),encryption_type,True).encode(format))
       client.send(encryption_func(cmd,encryption_type,True).encode(format))
       print(encryption_func(client.recv(header_size).decode(format),encryption_type,False))
       print("Runtime for this command: ", time.process_time() - start)

# Main function that stasrts the client
def main():
   client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   client.connect(address)
   encryption_type = input("Choose Encryption Type(1,2 or 3): 1) Plain Text 2) Substitute Cipher 3) Transpose Cipher: ")
   client.send(encryption_type.encode(format))
   while True:
       command_input = input("Enter Command: ")
       cmd = command_input
       handle_command(command_input, client,encryption_type)
       if cmd == disconnect:
           break
       
main()
