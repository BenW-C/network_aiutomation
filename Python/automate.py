from termcolor import cprint
import getpass
import csv
from jinja2 import Template
import netmiko
from netmiko import ConnectHandler
import serial
import time

### Voeg alle parameters toe aan interactief stuk zodat params met ssh jinja file matchen ##
## insert new script for this part
device = {
        "address": None,
        "device_type": 'cisco_ios',
        "ssh_port": 22,
        "username": None,
        "password": None,
        "secret": None,
         }

def main():
    print('Configure SSH from scratch? [1]')
    print('SSH is already configured and set up [2]')
    config_ssh = input('Select an option: ')

    if config_ssh == '1':
        ssh_config_params()
    if config_ssh == '2':
        make_ssh_connection()
    else:
        print('please select an option [1] or [2]')
        time.sleep(2)
        main()

## Create New Excel File ##
def ssh_config_params():
    attempts = 0
    max_attempts = 3
    if device['address'] == None and device['username'] == None:
        mgmt_address = input('Insert management addres: ')
        device.update( {'address' : mgmt_address})
        username = input('Insert username: ')
        device.update( {'username' : username})

    if device['password'] == None:
        password = getpass.getpass('Insert ssh password: ')
        verify_password = getpass.getpass('Verify ssh password: ')
        while verify_password != password:
            attempts += 1
            if attempts == 3:
                ssh_config_params()
            else:
                cprint(f"Passwords do not match! Attempts left: {max_attempts - attempts}", 'red')
                verify_password = getpass.getpass('Verify ssh password: ')
        device.update( {'password' : password})

    if device['secret'] == None:
        secret = getpass.getpass('Insert priviliged EXEC password: ')
        verify_secret = getpass.getpass('Verify priviliged EXEC password: ')
        while verify_secret != secret:
            attempts += 1
            if attempts == 3:
                ssh_config_params()
            else:
                cprint(f'Secrets do not match! Attempts left: {max_attempts - attempts}', 'red')
                verify_secret = getpass.getpass('Verify priviliged EXEC password: ')
        device.update( {'secret' : secret})
        ## Write to excel file for later use of params ##
        open_file = 'Excel/ssh_config.csv'
        device_list = device.values()
        with open(open_file, 'a') as a:
            writer = csv.writer(a)
            writer.writerow(device_list)
        cprint(f"SSH is now available through interface {device['address']}", 'red')
        ## Call function for further configuration ##    


## In case Excel File is already Created ##
def make_ssh_connection():
    ssh_template_file = "Jinja Files/ssh_config.j2"
    ssh_config = "Excel/ssh_config.csv"
    ssh_vars = ''
    with open(ssh_template_file) as f:
        ssh_template = Template(f.read(), keep_trailing_newline=True)

    try:
        with ConnectHandler(ip = device["address"],
                            port = device["ssh_port"],
                            username = device["username"],
                            password = device["password"],
                            device_type = device['device_type'],
                            secret = device['secret']) as ch:
            ch.enable()
            config_set = ssh_vars.split('\n')
            output = ch.send_config_set(config_set)
            print(output)
            ch.disconnect()
        
    except netmiko.ssh_exception.SSHException:
        cprint('SSH Not enabled', 'red')
        configure_ssh = input('Enter SSH configuration mode? [y/n]: ')
        if configure_ssh.lower() == 'y':
            ssh_config_params()
        else:
            print('Exiting script')
    with open(ssh_config) as f:
        reader = csv.DictReader(f)
        for row in reader:
            ssh_vars += ssh_template.render(        ## Pas aan naar gewenste config
            username = row['Username'],
            password = row['Password'],
            domain = row['Domain'],
            modulus = row['Modulus'],
            supported = row['Supported'],
            login = row['Login'],
            hostname = row['Hostname'],
            management = row['Management'],
            address = device['address'],
            mask = row['Mask'],
            secret = device['secret'],
            )
    ssh_params_list = ssh_vars.split('\n ')
    with serial.Serial() as ser:
        ser.baudrate = 9600
        ser.port = 'COM3'
        ser.open()
        for cmd in ssh_params_list:
            ser.write(bytes(cmd, encoding="ascii"))   

main()

