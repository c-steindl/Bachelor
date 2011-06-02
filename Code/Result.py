import socket

HOST = '74.125.77.99'
PORT = 80      
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send('Hello, world')
#data = s.recv(1024)
s.close()
print 'Received', 'data'
