import csv
from jinja2 import Template
import netmiko
from netmiko import ConnectHandler
import serial
import time


# device = {
#         "address": "192.168.0.2",
#         "device_type": 'cisco_ios',
#         "ssh_port": 22,
#         "username": "ben",
#         "password": "Fietsband",
#         "secret": "Fietsband"
#         }

# with ConnectHandler(ip = device["address"],
#                     port = device["ssh_port"],
#                     username = device["username"],
#                     password = device["password"],
#                     device_type = device['device_type'],
#                     secret = device['secret']) as ch:
#                 ch.enable()
#                 output = ch.send_command("show run | inc ip address 192.168.0")
#                 output = output.split(' ')
#                 print(output[3])


open_file = 'Excel/ssh_config.csv'
exemp = {'key' : 'Nigga'}
listz = exemp.values()
ok = list(listz)
with open(open_file, 'a') as a:
        writer = csv.writer(a)
        writer.writerow(ok)               
                       



        