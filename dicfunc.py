from netmiko import Netmiko
from getpass import getpass

dev_info={}

def inpFun():   
    device_os='alcatel_sros'
    type='device_type'
    dev_info[type]=device_os

    #Adding ssh config file
    config_file='/home/vbisht/.ssh/config'
    ssh_config='ssh_config_file'
    dev_info[ssh_config]=config_file

    ip="ip"
    ip_add=input("Please enter the ip for the device: ")
    dev_info[ip]=ip_add

    # uname= input("Please enter your username: \n")
    uname= "username"
    uname_input=input("Please enter your username: ")

    dev_info[uname] = uname_input
    passw= "password"
    # passw_input=input("Please enter your password: ")
    passw_input=getpass()

    dev_info[passw]=passw_input

