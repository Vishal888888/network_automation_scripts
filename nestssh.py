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

def sshCon():

    uname= "username"
    uname_input=input("Please enter your username: ")

    #dev_info[uname] = uname_input
    passw= "password"
    # passw_input=input("Please enter your password: ")
    passw_input=getpass()

    dev_info[passw]=passw_input

    sshCon.jump_host_ip= '172.16.2.2'       #Add your Jumphost ip
    sshCon.jump_host_user=uname_input
    sshCon.jump_host_password=passw_input

    sshCon.router_ip=input("Please enter device ip to login: ")
    # router_ip='10.2.13.5'
    sshCon.router_user= uname_input
    sshCon.router_password=passw_input

    # router_ip1='10.6.0.5'
    # router_user1='vbisht'
    # router_password1='Vertel112021??'

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
        # print("Checking nested ssh")
        # router_ip1=input("Please enter the device ip: ")
        # #router_ip1='10.6.0.5'
        # funSsh.net_connect1.write_channel(f"ssh {sshCon.router_user}@{router_ip1}\n")
        # time.sleep(2)
        # output=funSsh.net_connect1.read_channel()
        # print(output)
        # funSsh.net_connect1.write_channel(f"{sshCon.router_password}\n")
        # print(funSsh.net_connect1.find_prompt())
        # if 'password' in output:
        #     print("Got it!")
        #     funSsh.net_connect1.write_channel(f"{sshCon.router_password}\n")
        #     time.sleep(2)
        #     print("\n Destin dev prompt")
        #     print(funSsh.net_connect1.find_prompt())

        #     cmds=['show port description', 'show service service-using epipe']
        #     redispatch(funSsh.net_connect1, device_type='alcatel_sros')
        # for cmd in cmds:
        #     print(f"\nExecuting the command: {cmd}")
        #     router_output=funSsh.net_connect1.send_command(cmd)
        #     print(router_output)

        # funSsh.net_connect1.write_channel(f"ssh {sshCon.router_user1}@{sshCon.router_ip1}\n")
        # time.sleep(2)
        # output=funSsh.net_connect1.read_channel()
        # print(output)
        # funSsh.net_connect1.write_channel(f"{sshCon.router_password1}\n")
        # print(funSsh.net_connect1.find_prompt())
        # redispatch(funSsh.net_connect1, device_type='alcatel_sros')
        # out1=funSsh.net_connect1.send_command('admin display-config')
        # print(out1)
       
        # output1=funSsh.net_connect1.send_command('show log log-id 99')
        # print("Saving config to the file!!")
        # filename = input("Please insert the filename you would like to use: ")
        # with open(os.path.join(os.getcwd(), filename + ".txt"), 'a') as f:
        #                         # usrInput = input("user input >>> ")
        #                         usrInput = output1
        #                         f.write("%s\n" % usrInput)

        # return filename 
    except NetMikoTimeoutException:
        print("Something went wrong!! \n Please check the following: \n 1. The ip address entered \n 2. The ip address format \n 3. Connection to Vertel network")
    
    except AuthenticationException:
        print(">>>>>>>>>Authentication Failure!! Please check the username and password entered!!<<<<<<<<<<<<<<< \n")
    
    except Exception as unknown_error:
        print("Something unknown happened! Check for the device logs or consult with the network administrator!")
    # funSsh.net_connect1.write_channel(f"ssh {router_user}@{router_ip}\n")

# def tracSsh():
#     funSsh()
#     funSsh.net_connect1.write_channel(f"ssh {sshCon.router_user}@{router_ip1}\n")  #Need to change the ip part
#     output_ping=funSsh.net_connect1.send_command('traceroute 10.10.0.15')
#     match=re.findall(r"\s{1}\s\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", output_ping)
#     str1=''.join(match)
#     print(str1)

def serID():
    funSsh()
    try:
        x=input("Please enter the service id: ")
        
        output1=funSsh.net_connect1.send_command('show service id %s base' % (x))
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
        return filename
    except NetMikoTimeoutException:
        print("Something went wrong!! \n Please check the following: \n 1. The ip address entered \n 2. The ip address format \n 3. Connection to Vertel network")
    
    except AuthenticationException:
        print(">>>>>>>>>Authentication Failure!! Please check the username and password entered!!<<<<<<<<<<<<<<< \n")
    
    except Exception as unknown_error:
        print("Something unknown happened! Check for the device logs or consult with the network administrator!")

############Main script############
'''   
    funSsh.net_connect1.write_channel(f"ssh {router_user}@{router_ip}\n")
    time.sleep(2)
    output=funSsh.net_connect1.read_channel()
    print(output)
    funSsh.net_connect1.write_channel(f"{router_password}\n")
    print(funSsh.net_connect1.find_prompt())
    print("Checking nested ssh")
    funSsh.net_connect1.write_channel(f"ssh {router_user1}@{router_ip1}\n")
    time.sleep(2)
    output=funSsh.net_connect1.read_channel()
    print(output)
    funSsh.net_connect1.write_channel(f"{router_password1}\n")
    print(funSsh.net_connect1.find_prompt())
    redispatch(funSsh.net_connect1, device_type='alcatel_sros')
    out1=funSsh.net_connect1.send_command('admin display-config')
    print(out1)
'''

    # if 'password' in output:
    #     print("Got it!")
    #     funSsh.net_connect1.write_channel(f"{router_password}\n")
    #     time.sleep(2)
    #     print("\n Destin dev prompt")
    #     print(funSsh.net_connect1.find_prompt())

    #     cmds=['show port description', 'show service service-using epipe']
    #     redispatch(funSsh.net_connect1, device_type='alcatel_sros')
    #     for cmd in cmds:
    #         print(f"\nExecuting the command: {cmd}")
    #         router_output=funSsh.net_connect1.send_command(cmd)
    #         print(router_output)

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

