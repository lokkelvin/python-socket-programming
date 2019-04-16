# TCP Client Non-Persistent
# Kelvin Lok
# 15 April 2019

''' code references
1)http://code.activestate.com/recipes/408859/
'''
import socket
import sys
import time

ADDR = '127.0.0.1'
PORT = 12346

def get_request(filename, persistent = False):
    data = 'GET /{} HTTP/1.1\r\n'.format(filename)
    data += 'Host: {}:{}\r\n'.format(ADDR,PORT)
    data += 'Connection: {}\r\n\n'.format(['closed','keep-alive'][persistent])
    return data

def main():
    
    t1 = time.time()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ADDR,PORT))
    #print "[client] Requesting a.jpg"
    s.sendall(get_request('a.jpg'))
    recv_file(s,'received.jpg')
    #print "[client] Received a.jpg"
    s.close()
    
    t2 = time.time()
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ADDR,PORT))
    #print "[client] Requesting b.mp3"
    s.sendall(get_request('b.mp3'))
    recv_file(s,'received.mp3')
    #print "[client] Received b.mp3"
    s.close()
    
    t3 = time.time()
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ADDR,PORT))
    #print "[client] Requesting c.txt"
    s.sendall(get_request('c.txt'))
    recv_file(s, 'received.txt')
    #print "[client] Received c.txt"
    s.close()
    
    t4 = time.time()

    print "[client] Connection closed\n"
    print "a.jpg: {:.6f} ms".format((t2-t1)/10e-3)
    print "b.mp3: {:.6f} ms".format((t3-t2)/10e-3)
    print "c.txt: {:.6f} ms".format((t4-t3)/10e-3)
    
  
def echo(s):
    s.sendall(b'Hello World\n')
    data = s.recv(1024)
    #print 'Received', repr(data)


def recv_file(s,filename):
    endmarker = 'end_of_file'
    with open(filename,'wb') as f:
        counter = 0
        while True:
            data = s.recv(1024)
            if not data: break
            if endmarker in data: 
                loc = data.find(endmarker)
                ##print "End of file"
                ##print "[{} with endmarker]".format(counter), repr(data)
                ##print "[{} without endmarker]".format(counter), repr(data[:loc])
                f.write(data[:loc])
                break
            counter += 1
            #print "Received {} :".format(counter)#, repr(data)
            f.write(data)
    f.close()


if __name__ == '__main__':
    main()
