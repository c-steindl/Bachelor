import socket
import sys

class Host():
    port = 0
    clients = list()
    numClients = 0
    
    def __init__(self, port, numClients):
        self.port = port
        self.numClients = numClients

    def initConnect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('localhost', self.port))
        s.listen(1)
        i = 0
        while i < self.numClients:
            conn, addr = s.accept()
            self.clients.append([i, addr, conn.getsockname()])
            i = i + 1
            print 'Connected by', addr
            conn.close()
        print self.clients

if __name__ == "__main__":
    if len(sys.argv) == 3:
        myServer = Host(long(sys.argv[1]), int(sys.argv[2]))
        myServer.initConnect()
    else: print 'No'