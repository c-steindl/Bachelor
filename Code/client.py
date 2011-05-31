# Echo client program
import socket

HOST = '127.0.0.1'    # The remote host
PORT = 50007              # The same port as used by the server
i = 0
while i < 2:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    print s.getsockname()
    #s.send(b'Hello, world')
    #data = s.recv(1024)
    s.close()
    #print('Received', repr(data))
    i = i + 1