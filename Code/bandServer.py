import socket
import sys
 
stop = 0
        #try:
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', self.port + 1))
s.listen(1)
        #except Exception:
        #    print 'Could not open socket'
            
while True:
    conn, addr = s.accept()
    data = conn.recv(512)
    print data