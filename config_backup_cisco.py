import sys
import paramiko 
import os
import time
from tkinter import * # GUI for Python 3
from tkinter import constants, filedialog  #GUI for dialog box Python 3
from datetime import date
from getpass import getpass

#TODO Update default dir for TK open file, Add additions Exceptions, Add CLI checks

os.chdir("Z:\Config BackUp") #Default Dir

today = date.today()
date = today.strftime("%d-%b-%Y")

user = input("Enter username:")
pwd = getpass("Enter password:")

def OpenFile():
       root = Tk()
       root.filename = filedialog.askopenfilename(initialdir = "/",title = "Select Input File",filetypes = (("Text File","*.txt"),("all files","*.*")))
       return root.filename

def connect_ssh(user, pwd, ip):
       
       while True:
              try:
                     ssh = paramiko.SSHClient()
                     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                     ssh.connect(ip, port=22, username=user, password=pwd, timeout=5, look_for_keys=False)
                     break

              except paramiko.ssh_exception.AuthenticationException as e:
                     print(f"Error incorrect username or password {e}")
                     user = input("Enter username:")
                     pwd = getpass("Enter password:")
                     continue
              
              except paramiko.ssh_exception.socket.timeout as e:
                     print(f"connection {e} please check IPaddress {ip} is avaiable")
                     return 0
                     break
       
       return(ssh)

source = OpenFile()

with open(source, "r") as f0:
       for ip in f0.readlines():
              ip = ip.strip()
              ssh = connect_ssh(user, pwd, ip)
              
              if ssh == 0:
                     continue

              terminal = ssh.invoke_shell()
              time.sleep(2)
              terminal.send('term len 0\n')
              time.sleep(1)
              print("Saving Config to device")
              terminal.send('write memory\n')
              time.sleep(2)
              print("Config Saved")
              print(f"backing up config for {ip}")
              terminal.send('sh run\n')
              time.sleep(20)
              output = terminal.recv(999999)
              filename = "%s_%s" % (ip, date) + ".txt"
              with  open(filename, 'a') as backup:
                     backup.write(output.decode("utf-8") )

              print(f"Config saved to {filename} to {os.getcwd()}")
              ssh.close() 