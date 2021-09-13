#!/usr/bin/env python3

from netmiko import Netmiko
from getpass import getpass
from dicfunc import dev_info 
from dicfunc import inpFun
import re
import os
from netmiko.ssh_exception import AuthenticationException, NetMikoTimeoutException

def serID():
    inpFun()
    net_connect=Netmiko(**dev_info)
    x=input("Please enter the service id: ")
    net_connect=Netmiko(**dev_info)
    
    output1=net_connect.send_command('show service id %s base' % (x))
    # output1=net_connect.send_command('admin display-config')
    net_connect=Netmiko(**dev_info)


    filename = input("Insert 'filename.txt' Here >>> ")
    with open(os.path.join(os.getcwd(), filename + ".txt"), 'a') as f:
                            # usrInput = input("user input >>> ")
                            usrInput = output1
                            f.write("%s\n" % usrInput)

    # return filename
    xa= filename + ".txt"
    # print(xa)
    print("Running traceroute for sdp!!")
    f = open(xa, 'r')
    filetext = f.read()
    f.close()

    matches = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", filetext)
    str1=''.join(matches)

    output_ping=net_connect.send_command('traceroute ' + str1)
    #filename_trace = input("Insert traceroute test file name here >>> ")
    with open(os.path.join(os.getcwd(), filename + ".txt"), 'a') as f:
                            # usrInput = input("user input >>> ")
                            usrInput = output_ping
                            f.write("%s\n" % usrInput)
    
    return filename



def configAd():
    inpFun()
    try:
        net_connect=Netmiko(**dev_info)
        print("Saving config to the file!!")
        output1=net_connect.send_command('show log log-id 99')
        filename = input("Please insert the filename you would like to use: ")
        with open(os.path.join(os.getcwd(), filename + ".txt"), 'a') as f:
                                # usrInput = input("user input >>> ")
                                usrInput = output1
                                f.write("%s\n" % usrInput)

        return filename
    except NetMikoTimeoutException:
        print("Something went wrong!! \n Please check the following: \n 1. The ip address entered \n 2. The ip address format \n 3. Connection to Vertel network")
    
    except AuthenticationException:
        print(">>>>>>>>>Authentication Failure!! Please check the username and password entered!!<<<<<<<<<<<<<<< \n")
    
    except Exception as unknown_error:
        print("Something unknown happened! Check for the device logs or consult with the network administrator!")


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