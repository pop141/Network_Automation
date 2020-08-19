import paramiko
import os
import time
from datetime import date
from getpass import getpass
import tempfile


class Connect:
    def __init__(self):
        self._default_save = r"Z:\Config BackUp" if os.path.exists(r"Z:\Config BackUp") else tempfile.gettempdir()
        self.today = date.today()
        self.date = self.today.strftime("%d-%b-%Y")
        self.file_name = ''

    @property
    def default_save(self):
        return self._default_save

    @default_save.setter
    def default_save(self, value):
        if os.path.exists(value):
            self._default_save = value
        else:
            raise ValueError('Path not found')

    def connect_ssh(self, user, pwd, ip):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, port=22, username=user, password=pwd, timeout=5, look_for_keys=False)
        except paramiko.ssh_exception.AuthenticationException as e:
            raise ValueError(f"Error incorrect username or password {e}")
        except paramiko.ssh_exception.socket.timeout as e:
            raise ValueError(f"connection {e} please check IPaddress {ip} is avaiable")
        return ssh

    def save_config(self, filename, user, pwd):
        with open(filename, "r") as f0:
            for ip in f0.readlines():
                ip = ip.strip()
                ssh = self.connect_ssh(user, pwd, ip)

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
                file_name = "%s_%s" % (ip, date) + ".txt"

                with open(file_name, 'a') as backup:
                    backup.write(output.decode("utf-8"))

                print(f"Config saved to {file_name} to {os.getcwd()}")
                ssh.close()
