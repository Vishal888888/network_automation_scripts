from typing import KeysView
from netmiko import Netmiko, redispatch
from getpass import getpass
from dicfunc import dev_info 
from dicfunc import inpFun
from netmiko.ssh_dispatcher import ConnectHandler
from netmiko.ssh_autodetect import SSHDetect
import time
import os
from netmiko.ssh_exception import AuthenticationException, NetMikoTimeoutException
import re
import sys
from io import StringIO


def sshCon():

    uname= "username"
    uname_input=input("Please enter your username: ")

    #dev_info[uname] = uname_input
    passw= "password"
    # passw_input=input("Please enter your password: ")
    passw_input=getpass()

    dev_info[passw]=passw_input
    config_file='/home/vbisht/.ssh/config'
    ssh_config='ssh_config_file'
    dev_info[ssh_config]=config_file
    use_key=True
    keys='Key_type'
    dev_info[keys]= use_key

    sshCon.jump_host_ip= 'Jumphost_ip'       #Add your Jumphost ip
    sshCon.jump_host_user=uname_input
    sshCon.jump_host_password=passw_input
    sshCon.conf=config_file

    sshCon.router_ip=input("Please enter device ip to login: ")
    # router_ip='10.2.13.5'
    sshCon.router_user= uname_input
    sshCon.router_password=passw_input

    

def funSsh():
    sshCon()    
    try:
        funSsh.net_connect1=Netmiko(device_type='linux_ssh', host=sshCon.jump_host_ip, username=sshCon.jump_host_user, password=sshCon.jump_host_password)
        print(funSsh.net_connect1.find_prompt())
        print("Connected to jump host!!")
        funSsh.net_connect1.write_channel(f"ssh {sshCon.router_user}@{sshCon.router_ip}\n")
        time.sleep(2)
        output=funSsh.net_connect1.read_channel()
        print(output)
        funSsh.net_connect1.write_channel(f"{sshCon.router_password}\n")
        print(funSsh.net_connect1.find_prompt())
    except:
        print("Not connected!!")
    # print(sshCon.router_user)

def configAd():
    funSsh()
    try:
        print("Checking for logs!!")
        cmds=['show log log-id 99', 'show log log-id 99 application ospf']
        redispatch(funSsh.net_connect1, device_type='alcatel_sros')
        for cmd in cmds:
            print(f"\nExecuting the command: {cmd}")
            router_output=funSsh.net_connect1.send_command(cmd)
            filename = input("Please insert the filename you would like to use: ")
            with open(os.path.join(os.getcwd(), filename + ".txt"), 'a') as f:
            # usrInput = input("user input >>> ")
                    usrInput = router_output
                    f.write("%s\n" % usrInput)
        
    except NetMikoTimeoutException:
        print("Something went wrong!! \n Please check the following: \n 1. The ip address entered \n 2. The ip address format \n 3. Connection to company network")
    
    except AuthenticationException:
        print(">>>>>>>>>Authentication Failure!! Please check the username and password entered!!<<<<<<<<<<<<<<< \n")
    
    except Exception as unknown_error:
        print("Something unknown happened! Check for the device logs or consult with the network administrator!")
    # funSsh.net_connect1.write_channel(f"ssh {router_user}@{router_ip}\n")


def serID():
    funSsh()
    try:
        x=input("Please enter the service id: ")
        
        output1=funSsh.net_connect1.send_command('show service id %s base' % (x))
        print(output1)
        # output1=net_connect.send_command('admin display-config')


        filename = input("Insert 'filename.txt' Here >>> ")
        with open(os.path.join(os.getcwd(), filename + ".txt"), 'a') as f:
                                # usrInput = input("user input >>> ")
                                usrInput = output1
                                f.write("%s\n" % usrInput)

        # return filename
        xa= filename + ".txt"
        # print(xa)
    
        f = open(xa, 'r')
        filetext = f.read()
        f.close()

        matches = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", filetext)
        str12=''.join(matches)
        print("Running traceroute for sdp!!")
        while True:
            output_ping=funSsh.net_connect1.send_command('traceroute ' + str12)
            match=re.findall(r"\s{1}\s\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", output_ping)
            str1='\n'.join(match).replace(" ","")   #trace ip list with no white space in a separate file
            # str1.replace(" ","")
            # print(str1.replace(" ",""))
            f=open("traceservice.txt" , "w")
            f.write(str(str1))
            print("Done!")
            print("Next one!! \n") 
            i = input("Enter: ")
            if i.strip() == 'y':
                print("Looping")
                
            if i.strip() == 'n':
                print("Breaking")
                break

        # with open(os.path.join(os.getcwd(), filename + ".txt"), 'a') as f:
        #                         # usrInput = input("user input >>> ")
        #                         usrInput = output_ping
        #                         f.write("%s\n" % usrInput)
        
        # return filename
        funSsh.net_connect1.write_channel(f"ssh {sshCon.router_user}@{str12}\n")
        time.sleep(2)
        output=funSsh.net_connect1.read_channel()
        print(output)
        funSsh.net_connect1.write_channel(f"{sshCon.router_password}\n")
        print(funSsh.net_connect1.find_prompt())

##################Checking for SSH in multiple devices###############################################
        # return filename
        redispatch(funSsh.net_connect1, device_type='alcatel_sros')
        print("Checking ip's in the list")
        f=open('traceservice.txt')
        print("Text file open: Now running for loop!!")
        for ip in f: 
                    # funSsh.net_connect2=Netmiko(device_type='alcatel_sros', host=sshCon.jump_host_ip, username=sshCon.jump_host_user, password=sshCon.jump_host_password, ssh_config_file=sshCon.conf, system_host_keys=True)
                    funSsh.net_connect1.write_channel(f"ssh {sshCon.router_user}@{ip}\n") #SSH KEYS NOT WORKING
                    # funSsh.net_connect1.load_system_host_keys()
                    time.sleep(2)
                    output=funSsh.net_connect1.read_channel()
                    
                    print(output)
                    funSsh.net_connect1.write_channel(f"{sshCon.router_password}\n")
                    print(funSsh.net_connect1.find_prompt())
##############################################################################################################################
    except NetMikoTimeoutException:
        print("Something went wrong!! \n Please check the following: \n 1. The ip address entered \n 2. The ip address format \n 3. Connection to company network")
    
    except AuthenticationException:
        print(">>>>>>>>>Authentication Failure!! Please check the username and password entered!!<<<<<<<<<<<<<<< \n")
    
    # except Exception as unknown_error:
    #     print("Something unknown happened! Check for the device logs or consult with the network administrator!")

############Main script############


if __name__ == '__main__':
    print("Working on it!!")
    #serID()
    print("Please select from the following: \n 1. Logs \n 2. Service configuration and traceroute")
    for ch in range (0,3):
        try:
            usr = int(input("Enter your choice: "))
            if usr == 1:
                    print("****************Running Logs*****************")
                    configAd()
                    break
            if usr == 2:
                    print("****************Gathering Service Information*****************")
                    serID()
                    break
            else:
                print("The option is not available!!")
        except ValueError:
            print("Wrong input!! Please select from the options available!")
        

end= input("Press enter to exit!!")

