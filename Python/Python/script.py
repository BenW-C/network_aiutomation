import csv
from jinja2 import Template
import netmiko
from netmiko import ConnectHandler
import serial
import time

def main():
    source_file = "Excel/basic_config.csv"
    interface_template_file = "Jinja Files/basic_config.j2"
    interface_config = ''
    with open(interface_template_file) as f:
        interface_template = Template(f.read(), keep_trailing_newline=True)
    
        device = {
                "address": "192.168.0.2",
                "device_type": 'cisco_ios',
                "ssh_port": 22,
                "username": "ben",
                "password": "Fietsband3808",
                "secret": "Fietsband3808"
                }
    try:
        with ConnectHandler(ip = device["address"],
                            port = device["ssh_port"],
                            username = device["username"],
                            password = device["password"],
                            device_type = device['device_type'],
                            secret = device['secret']) as ch:
            ch.enable()
            config_set = interface_config.split('\n')
            output = ch.send_config_set(config_set)
            print(output)
            ch.disconnect()
    
    except netmiko.ssh_exception.SSHException:
        print('SSH Not enabled')
        zero_touch()

    def config_vlans():
        with open(source_file) as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Switch'] != '':                     
                    hostname = row['Switch']
                else:
                    hostname = row['Router']
                interface_config += interface_template.render(
                    interface = row['Interface'],
                    hostname = hostname,
                    vlan = row['VLAN'],
                    purpose = row['Purpose']    
                )

    def config_etherchannel():
        pass
    def config_hsrp():
        pass

    def print_menu():
        print('Config Menu')
        print('     [1] VLANS')
        print('     [2] Etherchannel')
        print('     [3] HSRP')

        user_input = input('Pick your weapon: ')
        if user_input > '3':
            print_menu()
        else:
            if user_input == '1':
                config_vlans()
            if user_input == '2':
                config_etherchannel()
            if user_input == '3':
                config_hsrp()
    print_menu()

#### CONFIGURE SSH ZERO TOUCH ####
def zero_touch():
    ssh_config = "Excel/ssh_config.csv"
    ssh_template_file = "Jinja Files/ssh_config.j2"
    ssh_vars = ''

    with open(ssh_template_file) as f:
           ssh_template = Template(f.read(), keep_trailing_newline=True)

    with open(ssh_config) as f:
        reader = csv.DictReader(f)
        for row in reader:
            ssh_vars += ssh_template.render(
            username = row['Username'],
            password = row['Password'],
            domain = row['Domain'],
            modulus = row['Modulus'],
            supported = row['Supported'],
            login = row['Login'],
            hostname = row['Hostname'],
            management = row['Management'],
            address = row['Address'],
            mask = row['Mask'],
            secret = row['Secret'],
            )
    test = ssh_vars.split('\n ')

    with serial.Serial() as ser:
        ser.baudrate = 9600
        ser.port = 'COM3'
        ser.open()
        for cmd in test:
            ser.write(bytes(cmd, encoding="ascii"))
            main()              
main()

