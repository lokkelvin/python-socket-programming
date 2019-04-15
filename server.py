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

activeChildren = [] #list of pid of active children
def close_children():
    '''os.waitpid(pid, options)

Wait for completion of a child process given by process id pid, and return a tuple containing its process id and exit status indication (encoded as for wait()). The semantics of the call are affected by the value of the integer options, which should be 0 for normal operation.

If pid is greater than 0, waitpid() requests status information for that specific process. If pid is 0, the request is for the status of any child in the process group of the current process. If pid is -1, the request pertains to any child of the current process. If pid is less than -1, status is requested for any process in the process group -pid (the absolute value of pid).

An OSError is raised with the value of errno when the syscall returns -1.'''
    while activeChildren:
        try:
            pid,status = os.waitpid(0, os.WNOHANG)
        except:
            print "Failed to kill pid: {}".format(pid)
        if not pid: break
        print "pid: {} exited with status {}".format(pid,status)
        activeChildren.remove(pid)


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ADDR,PORT))
    s.listen(5) # Backlog  = 5
    #conn is a new socket object usable to send and receive data on the connection, and address is the address bound to the socket on the other end of the connection
    # address = tuple of addr and port. Use *arg to unpack tuple.
    while(1):
        try:
            close_children()
            conn, address = s.accept()
            print "[Parent] New client connected from IP address {} and port number {}".format(*address)
            print "[Parent {}] before forking".format(os.getpid())
            pid = os.fork()
            if pid == 0: # if children process
                # handle request and close connection
                #handle_client_echo(conn,address)
                s.close() # close listen port in child
                s = None
                handle_client_file(conn,address)
                break
            else: # if parent process
                # keep listening for next connection
                conn.close() # Remove reference to connection/ Decrement reference count, otherwise child's connection will stay alive due to ghost reference
                conn = None
                print "[Parent {}] New child pid = {}".format(os.getpid(),pid)
                activeChildren.append(pid)
                
        except KeyboardInterrupt:
            if conn:
                conn.close()
                print "[process {}] conn closed".format(os.getpid())
            break
    if s:
        s.close()
    print "[parent {}] listen closed".format(os.getpid())

            
def handle_client_file(conn,address):
    print "[child {}] Closed listen".format(os.getpid())
    #time.sleep(2) # simulated 2 second delay
    
    getrequest = conn.recv(1024) #e.g of getrequest is 'GET /a.jpg HTTP/1.1\r\nHost: 127.0.0.1:12345\r\nConnection: keep-alive\r\n\n'
    gr = getrequest.split("\n")
    for i in gr:
        print i
    filename = getrequest.split()[1][1:] #e.g. 'a.jpg'
    connectiontype = getrequest.split()[6] #e.g. 'keep-alive' or 'closed'
    if connectiontype == 'keep-alive':
        f = open(filename,'rb')
        line = f.read(1024)
        counter = 0
        while line:
            conn.send(line)
            counter += 1
            #print "Sent {} ".format(counter), repr(line)
            line = f.read(1024)
        conn.send(b'end_of_file')
        print "Sent {}, {}, {}".format(counter,filename, connectiontype)
        f.close()
        print "Done"
        handle_client_file(conn,address) # recursive call - base case when connectiontype = closed
        conn.close()
    else:
        
        f = open(filename,'rb')
        line = f.read(1024)
        counter = 0
        while line:
            conn.send(line)
            counter += 1
            #print "Sent {} ".format(counter), repr(line)
            line = f.read(1024)
        print "Sent {}, {}, {}".format(counter,filename, connectiontype)
        f.close()
        print "Done"
        conn.close() # close connection to let client know the transfer is complete
        conn = None
        print "[child {}] Closed accept".format(os.getpid())
        #os._exit(0)
        
def handle_client_echo(conn,address):
    time.sleep(2) # simulated 2 second delay
    while True:
        data = conn.recv(1024)
        if not data: break
        print "[Received {} bytes from {}:{}]".format(len(data), *address)
        conn.send('[{}]: {}'.format(time_now(),data))
        print "[Sent message: {} to {}:{}]".format(data,*address)
    print "[Client {}:{} disconnected]".format(*address)
    conn.close()
    os._exit(0)

def time_now():
    return time.ctime(time.time())


if __name__ == '__main__':
    main()



