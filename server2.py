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
            conn, address = s.accept()
            print "New client connected from IP address {} and port number {}".format(*address)
            #handle_client_file(conn,address)
            getrequest = conn.recv(1024).split()
            filename = getrequest[1][1:]
            connectiontype = getrequest[6]
            if connectiontype == 'keep-alive':
                f = open('a.jpg','rb')
                line = f.read(1024)
                while line:
                    conn.send(line)
                    line = f.read(1024)
                conn.send(b'end_of_file')
                f.close()
                x=conn.recv(1024)
                f = open('b.mp3','rb')
                line = f.read(1024)
                while line:
                    conn.send(line)
                    line = f.read(1024)
                conn.send(b'end_of_file')
                f.close()
                x=conn.recv(1024)
                f = open('c.txt','rb')
                line = f.read(1024)
                while line:
                    conn.send(line)
                    line = f.read(1024)
                conn.send(b'end_of_file')
                f.close()
                conn.close()
                conn = None
            else:
                f = open(filename,'rb')
                line = f.read(1024)
                counter = 0
                while line:
                    conn.send(line)
                    counter += 1
                    line = f.read(1024)
                conn.send(b'end_of_file')
                print "Sent {}, {}, {}".format(counter,filename, connectiontype)
                f.close()
                conn.close() # close connection to let client know the transfer is complete
                conn = None
            
        except:
            if conn:
                conn.close()
            s.close()
            break
    if s:
        s.close()

            
def handle_client_file(conn,address):
    getrequest = conn.recv(1024).split() #e.g of getrequest is 'GET /a.jpg HTTP/1.1\r\nHost: 127.0.0.1:12345\r\nConnection: keep-alive\r\n\n'
    filename = getrequest[1][1:] #e.g. 'a.jpg'
    connectiontype = getrequest[6] #e.g. 'keep-alive' or 'closed'
    if connectiontype == 'keep-alive2':
        f = open(filename,'rb')
        line = f.read(1024)
        counter = 0
        while line:
            conn.send(line)
            counter += 1
            line = f.read(1024)
        conn.send(b'end_of_file')
        print "Sent {}, {}".format(counter,filename)
        f.close()
        
        
        getrequest = conn.recv(1024).split()
        filename = getrequest[1][1:] #e.g. 'a.jpg'
        f = open(filename,'rb')
        line = f.read(1024)
        counter = 0
        while line:
            conn.send(line)
            counter += 1
            line = f.read(1024)
        conn.send(b'end_of_file')
        print "Sent {}, {}".format(counter,filename)
        f.close()
        
        
        getrequest = conn.recv(1024).split()
        filename = getrequest[1][1:] #e.g. 'a.jpg'
        f = open(filename,'rb')
        line = f.read(1024)
        counter = 0
        while line:
            conn.send(line)
            counter += 1
            line = f.read(1024)
        conn.send(b'end_of_file')
        print "Sent {}, {}".format(counter,filename)
        f.close()
        conn.close()
    elif connectiontype == 'keep-alive':
        f = open('a.jpg','rb')
        line = f.read(1024)
        while line:
            conn.send(line)
            line = f.read(1024)
        conn.send(b'end_of_file')
        f.close()
        x=conn.recv(1024)
        f = open('b.mp3','rb')
        line = f.read(1024)
        while line:
            conn.send(line)
            line = f.read(1024)
        conn.send(b'end_of_file')
        f.close()
        x=conn.recv(1024)
        f = open('c.txt','rb')
        line = f.read(1024)
        while line:
            conn.send(line)
            line = f.read(1024)
        conn.send(b'end_of_file')
        f.close()
        conn.close()
        conn = None
    else:
        f = open(filename,'rb')
        line = f.read(1024)
        counter = 0
        while line:
            conn.send(line)
            counter += 1
            line = f.read(1024)
        conn.send(b'end_of_file')
        print "Sent {}, {}, {}".format(counter,filename, connectiontype)
        f.close()
        conn.close() # close connection to let client know the transfer is complete
        conn = None

        
def handle_client_echo(conn,address):
    time.sleep(2) # simulated 2 second delay
    while True:
        data = conn.recv(1024)
        if not data: break
        #print "[Received {} bytes from {}:{}]".format(len(data), *address)
        conn.send('[{}]: {}'.format(time_now(),data))
        #print "[Sent message: {} to {}:{}]".format(data,*address)
    #print "[Client {}:{} disconnected]".format(*address)
    conn.close()
    os._exit(0)

def time_now():
    return time.ctime(time.time())


if __name__ == '__main__':
    main()



