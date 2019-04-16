# Server Single/ Multi-client
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


ADDR = ''
PORT = 12346

activeChildren = [] #list of pid of active children
def close_children():
    '''
    Reaps any child processes using os.wait(pid, options)
    
    Setting argument pid 0 kills all child processes that are
    part of the caller's process group.
    
    Setting argument options to os.WNOHANG will make the 
    function non-blocking.
    '''
    while activeChildren:
        try:
            pid,status = os.waitpid(0, os.WNOHANG)
        except:
            print "Failed to kill pid: {}".format(pid)
            pass
        if not pid: break
        #print "pid: {} exited with status {}".format(pid,status)
        activeChildren.remove(pid)

def main_multiclient():
    ''' 
    Multi-client server using os.fork()
    The main listening loop is handled by the parent process 
    and the client connection is handled by the child
    process. 
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ADDR,PORT))
    s.listen(5) # Backlog  = 5
    while(1):
        try:
            close_children()
            conn, address = s.accept()
            print "[Parent] New client connected from IP address {} and port number {}".format(*address)
            #print "[Parent {}] before forking".format(os.getpid())
            pid = os.fork()
            if pid == 0:    # if children process
                            # handle request and close connection
                s.close()   # close listen port in child
                s = None
                print '[Child {}] Connection with {}:{} started'.format(os.getpid(),*address)
                handle_client_file(conn,address)
                print '[Child {}] Connection with {}:{} closed'.format(os.getpid(),*address)
                break
            else:               # if parent process
                                # keep listening for next connection
                conn.close()    # Remove reference to connection/ Decrement reference count, otherwise child's connection will stay alive due to ghost reference
                conn = None
                print "[Parent {}] New child pid = {}".format(os.getpid(),pid)
                activeChildren.append(pid)
                
        except KeyboardInterrupt:
            if conn:
                conn.close()
                print "[process {}] conn closed".format(os.getpid())
            break
        except:
            if conn: conn.close()
            if s: s.close()
            print "[process {}] error raised".format(os.getpid())
            raise
    if s:
        s.close()
        print "[process {}] listen closed".format(os.getpid())
    print '[process {}] terminated'.format(os.getpid())


          
def handle_client_file(conn,address):
    '''
    Client connect handler, run by the child process.
    Checks the connection type from the GET Request and 
    carries out either persistent or non persistent
    HTTP connection.
    
    Once connection is finished the connection socket is closed, 
    the function returns and the child process is terminated.
    '''
    getrequest = conn.recv(1024)
    if not (getrequest):
        # Peer has disconnected
        # Base case for recursive call
        conn.close()
        return
    getrequest = getrequest.split()
    filename = getrequest[1][1:] 
    connectiontype = getrequest[6] 
    if connectiontype == 'keep-alive':
        f = open(filename,'rb')
        line = f.read(1024)
        counter = 0
        while line:
            conn.send(line)
            conn.recv(10)
            counter += 1
            line = f.read(1024)
        conn.send(b'end_of_file')
        print "[persistent] Sent {} packets, {}".format(counter,filename)
        f.close()
        #print "Done"
        handle_client_file(conn,address) # recursive call - base case when connectiontype = closed
        conn.close()
        conn = None
    else:
        f = open(filename,'rb')
        line = f.read(1024)
        counter = 0
        while line:
            conn.send(line)
            conn.recv(10)
            counter += 1
            line = f.read(1024)
        conn.send(b'end_of_file')
        print "[nonpersistent] Sent {} packets, {}".format(counter,filename)
        f.close()
        conn.close() # close connection to let client know the transfer is complete
        conn = None
    
    #os._exit(0)
        


def main_singleclient():
    ''' 
    Single-client server.
    
    Only 1 client can be served at a time.The 
    server is blocked until the existing client
    connection is completed. 
    '''
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
                print '[persistent] Connection with {}:{} closed'.format(*address)
            else:
                print '[main] Client requests {}, Non persistent'.format(filename)
                handle_client_nonpersistent(filename,conn)
                print '[nonpersistent] Connection with {}:{} closed'.format(*address)
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
    '''
    <do-while structure>
    do: send data
    while: recv data != None
    
    Outer while loop is for receiving GET requests. Connection
    remains open until no more requests are received. Then the 
    connection will close and the function returns to main 
    application loop to listen for new clients.
    
    Inner while loop is for reading the file, sending the file and
    receiving the acknowledge from client.
    '''
    f = open(filename,'rb')
    line = f.read(1024)
    counter = 0
    while line:
        conn.send(line)
        conn.recv(10)
        counter += 1
        line = f.read(1024)
    conn.send(b'end_of_file')
    print "[persistent] Sent {} packets, {}".format(counter,filename)
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
        print "[persistent] Sent {} packets, {}".format(counter,filename)
        f.close()
        getrequest = conn.recv(1024) 
    #print '[persistent] Client has disconnected (Peer disconnect)' #client initiated
    conn.close()
    conn = None
    
def handle_client_nonpersistent(filename,conn):
    '''
    Reads the file, sends the file and receives acknowledge.
    Closes connection after 1 complete file is sent.
    '''
    f = open(filename,'rb')
    line = f.read(1024)
    counter = 0
    while line:
        conn.send(line)
        conn.recv(10)
        counter += 1
        line = f.read(1024)
    conn.send(b'end_of_file')
    print "[nonpersistent] Sent {} packets, {}".format(counter,filename)
    f.close()
    conn.close() # server initiated
    conn = None
    


if __name__ == '__main__':
    if len(sys.argv)!= 3:
        print "Too few arguments"
        print "Usage: <Mode> <Port number>"
        print "Mode: 1 for Single-client, 2 for Multi-client"
        print "E.g: $ python server.py 1 55055 "
        sys.exit(0)
    PORT = int(sys.argv[2])
    print "Started on port {}".format(PORT)
    if sys.argv[1] == '1':
        print "Running single client mode"
        main_singleclient()
    else:
        print "Running multi-client mode"
        main_multiclient()



