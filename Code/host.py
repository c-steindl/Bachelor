import socket
import sys
import time
import enum

class Host():
    port = 0
    clients = list()
    numClients = 0
    iter = 5
    enum = enum.Enum()
    
    def __init__(self, port, numClients, iter):
        self.port = port
        self.numClients = numClients
        self.iter = int(iter)

    def initConnect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('localhost', self.port))
        s.listen(1)
        i = 0
        while i < self.numClients:
            conn, addr = s.accept()
            i = i + 1
            client = [i, addr, conn]
            self.clients.insert(i, client)
        print 'connected clients', self.clients
        
    def closeConnect(self):
        i = 0
        while i < self.numClients:
            client = self.clients.pop(i)
            client[2].close()
            i = i + 1
            
    def sendAll(self, message):
        self.initConnect()
        i = 0
        while i < self.numClients:
            client = self.clients[i]
            client[2].send(message)
            i = i + 1
        self.closeConnect()
    
    def recv(self, sockets):
        test = list()
        i = 0
        while i < selfnumClients:
            socket
            test.insert (i, True)
            i = i + 1
        
        i = 0
        while test == True:
            while i < self.numClients:
                socket[i].recv(1024)
                if data != self.enum.end:
                    socket[i].send(self.enum.done)
                i = i + 1 
    
    def recvConnect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('localhost', self.port))
        s.listen(1)
        sockets = list()
        i = 0
        while i < self.numClients:
            conn, addr = s.accept()
            i = i + 1
            client = [i, addr, conn]
            self.clients.insert(i, client)
            sockets.insert(i, conn)
        print 'connected clients', self.clients

    def netConnect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('localhost', self.port))
        s.listen(1)
        stop = 0
        while stop < self.numClients:
            conn, addr = s.accept()
            d = conn.recv(128).split()
            if d[0] == self.enum.stop:
                stop = stop + 1
                client = [stop, addr, conn]
                self.clients.insert(stop, client)

def usage():
    print 'USAGE: python host.py <Port to listen> <Number of clients> <Number of iterations>'

if __name__ == "__main__":
    if len(sys.argv) == 4:
        myServer = Host(int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]))
        
        message = myServer.enum.iter + ' ' + str(myServer.iter)
        myServer.sendAll(message)
        
        message = myServer.enum.start
        myServer.sendAll(message)
        myServer.sendAll(message)
        
        myServer.sendAll(message)
        myServer.netConnect()
        myServer.closeConnect()
        

        
        
        
        
        
    else: usage()