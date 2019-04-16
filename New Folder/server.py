# TCP Server
# Kelvin Lok
# 15 April 2019

'''code references: 
1)http://books.gigatux.nl/mirror/pythonprogramming/0596000855_python2-CHP-10-SECT-4.html
2)https://www.programcreek.com/python/example/424/os.waitpid
3)https://stackoverflow.com/questions/5106674/error-address-already-in-use-while-binding-socket-with-address-but-the-port-num/41490982

use netstat -ntp to check for time_wait socket
'''
import socket
import sys
import os
import time


ADDR = ''
PORT = 12346


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ADDR,PORT))
    s.listen(5) # Backlog  = 5
    while(1):
        try:
            print '[main] Listening for connections . . .'
            conn, address = s.accept()
            print "[main] New client connected from IP address {} and port number {}".format(*address)
            getrequest = conn.recv(1024).split()
            filename = getrequest[1][1:]
            connectiontype = getrequest[6]
            if connectiontype == 'keep-alive':
                print '[main] Client requests {}, Persistent'.format(filename)
                handle_client_persistent(filename,conn)
            else:
                print '[main] Client requests {}, Non persistent'.format(filename)
                handle_client_nonpersistent(filename,conn)
        except KeyboardInterrupt:
            if conn: conn.close()
            if s: s.close()
            break
        except:
            if conn: conn.close()
            if s: s.close()
            raise
    if s:
        s.close()

def handle_client_persistent(filename, conn):
    f = open(filename,'rb')
    line = f.read(1024)
    while line:
        conn.send(line)
        conn.recv(10)
        line = f.read(1024)
    conn.send(b'end_of_file')
    f.close()
    getrequest = conn.recv(1024)
    while getrequest:
        filename = getrequest.split()[1][1:]
        f = open(filename,'rb')
        line = f.read(1024)
        counter = 0
        while line:
            conn.send(line)
            conn.recv(10)
            counter += 1
            line = f.read(1024)
        conn.send(b'end_of_file')
        print "[persistent] Sent {}, {}".format(counter,filename)
        f.close()
        getrequest = conn.recv(1024)
    print '[persistent] Client has disconnected (Peer disconnect)' #client initiated
    conn.close()
    conn = None
    print '[persistent] Connection socket closed'
    
def handle_client_nonpersistent(filename,conn):
    f = open(filename,'rb')
    line = f.read(1024)
    counter = 0
    while line:
        conn.send(line)
        conn.recv(10)
        counter += 1
        line = f.read(1024)
    conn.send(b'end_of_file')
    print "[nonpersistent] Sent {}, {}".format(counter,filename)
    f.close()
    conn.close() # server initiated
    conn = None
    print '[nonpersistent] Connection socket closed'
    

def time_now():
    return time.ctime(time.time())


if __name__ == '__main__':
    print "Connect to {}:{}".format(ADDR,PORT)
    main()



