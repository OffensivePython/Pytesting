#!/usr/bin/env python3
#=========================================================#
# [+] Title: FTP Anonymous Login Scanner v0.1             #
# [+] Script: AnonFTP.py                                  #
# [+] Blog: pytesting.blogspot.com                        #
#=========================================================#

import os
import time
import datetime
import socket
import random
import threading
from optparse import OptionParser


def AnonLogin(address, logfile, verbose):
    global counter
    """ Anonymous Authentication Process """
    ftp=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        ftp.connect((address, 21));
        banner=ftp.recv(45)
        ftp.recv(1024) # receive the rest of the banner
        banner.replace("\r\n", ' ')
        ftp.send("USER anonymous\r\n")
        ftp.recv(1024)
        ftp.send("PASS anon@\r\n")
        response=ftp.recv(1024)

        try:
            if response.index("230")!=-1:
                status="Success"
        except ValueError:
            status="Failure"
        log=" # %-15s # %-45s # %-7s #"%(address, banner, status)
        if logfile:
            logfile.write(log+"\n")
        if verbose:
            print(log)
        elif status=="Success":
            print(log)
        counter-=1
    except socket.error:
        pass
    ftp.close()
    return

def randomHost():
    """ Generates a random IP address """
    host=str(random.randint(0,255))
    host+="."+str(random.randint(0,255))
    host+="."+str(random.randint(0,255))
    host+="."+str(random.randint(0,255))
    return host

def main():
    global counter
    
    parser=OptionParser()
    parser.add_option("-n", dest="nhost", type="int",\
                      help="Number of hosts", metavar="nHost")
    parser.add_option("-o", "--output", dest="oFile", type="string",\
                      help="File to save logs", metavar="FILE")
    parser.add_option("-v", "--verbose", dest="verbose", default=False,\
                      action="store_true",\
                      help="Logs everything")
    parser.add_option("-t", "--timeout", dest="timeout", type="float",\
                      help="Timeout in seconds")
    parser.add_option("-m", "--maxthread", dest="max", type="int",\
                      help="Maximum thread number")

    (options, args)= parser.parse_args()
    if options.nhost==None or options.nhost<1 or options.max<1:
        parser.print_help()
        os._exit(1)
    else:
        counter=options.nhost

    log="[#]=========================================================================[#]\n"
    log+=" #       Host      #                    Banner                     #  Login  #\n"
    log+="[#]=========================================================================[#]"
    
    if options.oFile!=None:
        logFile=open(options.oFile, "a")
        ctime=str(datetime.datetime.now()) # returns "yy-mm-dd hh:mm:ss.xx
        ctime=ctime[:ctime.index(".")]
        logFile.write("\nScan time: %s\n"%ctime)
        logFile.write(log+"\n")
    else:
        logFile=None
        
    verbose=options.verbose
    tmax=options.max

    nthreads=threading.activeCount() # get initial number of running threads
    socket.setdefaulttimeout(options.timeout)
    print(log)
    while counter>0:
        address=randomHost()
        try:
            while threading.activeCount()>tmax:
                time.sleep(10)
            t=threading.Thread(target=AnonLogin, args=(address, logFile, verbose))
            t.start()
        except:
            pass

    while threading.activeCount()>nthreads: # if number of running threads less than initial number
        time.sleep(10)                      # then, there are few threads still running

    log="[#]=========================================================================[#]"
    print(log)
    if logFile:
        logFile.write(log+"\n")
        logFile.close()

if __name__=="__main__":
    main()
