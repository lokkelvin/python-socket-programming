#https://stackoverflow.com/questions/10091271/how-can-i-implement-a-simple-web-server-using-python-without-using-any-libraries
import socket
def createServer():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try :
        serversocket.bind(('localhost',12345))
        serversocket.listen(5)
        while(1):
            (clientsocket, address) = serversocket.accept()

            rd = clientsocket.recv(5000)
            pieces = rd.split("\n")
            repr(rd)
            for i in pieces:
              print i

            data = "HTTP/1.1 200 OK\r\n"
            data += "Content-Type: text/html; charset=utf-8\r\n"
            data += "\r\n"
            data += "<html><body>Hello World</body></html>\r\n\r\n"
            clientsocket.sendall(data.encode())
            print "Done"
            clientsocket.shutdown(socket.SHUT_WR)

    except KeyboardInterrupt :
        print("\nShutting down...\n");
    except Exception as exc :
        print("Error:\n");
        print(exc)

    serversocket.close()

print('Access http://localhost:12345')
createServer()
