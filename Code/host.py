import socket
import sys
import time
import enum
import string
import results as res
import matplotlib.pyplot as plt

class Host():
    port = 0
    clients = list()
    numClients = 0
    iter = 5
    enum = enum.Enum()
    config = list()
    
    def __init__(self, port, numClients, iter):
        print socket.gethostbyname(socket.gethostname())
        self.port = port
        self.numClients = numClients

        self.config.append([self.enum.iter, int(iter)])
        self.config.append([self.enum.IO, self.enum.mat])
        self.config.append([self.enum.IO, self.enum.rw])
        self.config.append([self.enum.Net, self.enum.tcp])
        #self.config.append([self.enum.Net, self.enum.band])
        self.config.append([self.enum.data, 0])
        self.config.append([self.enum.stopClient, 0])

    def initConnect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', self.port))
        s.listen(1)
        i = 0
        while i < self.numClients:
            conn, addr = s.accept()
            i = i + 1
            client = [i, addr, conn]
            self.clients.append(client)
        #print 'connected clients', self.clients
        
    def dataConnect(self):
        results = open('results.csv', 'wb')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', self.port))
        s.listen(1)
        i = 0
        while i < self.numClients:
            conn, addr = s.accept()
            i = i + 1
            client = [i, addr, conn]
            self.clients.append(client)
        for x in range(self.numClients):
            data = 0
            c = self.clients[x]
            conn = c[2]
            conn.send('send')
            while True:
                if data  == self.enum.stop:
                    break
                data = conn.recv(1024)
                print data
                results.write(data)
                
            results.write('\n')
        #print 'connected clients', self.clients
        results.close()
        self.closeConnect()
        
    def closeConnect(self):
        while self.clients:
            client = self.clients.pop()
            client[2].close()
            
    def sendAll(self, message):
        i = 0
        while i < self.numClients:
            client = self.clients[i]
            client[2].send(message)
            i = i + 1

    def netConnect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', self.port))
        s.listen(1)
        stop = 0
        client = list()
        while stop < self.numClients:
            conn, addr = s.accept()
            d = conn.recv(128).split()
            if d[0] == self.enum.stop:
                stop = stop + 1
                client.append(conn)
            else:
                conn.close()
        message = myServer.enum.stop + ' ' + myServer.enum.tcp
        print message
        while client:
            c = client.pop()
            c.send(message)
            
    def bandConnect(self):
        stop = 1
        client = list()
        self.initConnect()
        while stop < self.numClients:
            for i in range(len(self.clients)):
                data = self.clients[i][2].recv(128)
                #print data
                d = string.find(data, self.enum.stop)
                if d > 0:
                    stop = stop + 1
                    client.append(self.clients[i][2])
                    print 'increment', stop, self.numClients
        print 'outof'
        message = myServer.enum.stop + ' ' + myServer.enum.band
        
        print client
        while client:
            c = client.pop()
            c.send(message)
            print message
        self.closeConnect()
        
        
def usage():
    print 'USAGE: python host.py <Port to listen> <Number of clients> <Number of iterations>'

if __name__ == "__main__":
    if len(sys.argv) == 4:
        myServer = Host(int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]))
        
        while myServer.config:
            myServer.initConnect()
            d = myServer.config.pop(0)
            message = str(d[0]) + ' ' + str(d[1])
            myServer.sendAll(message)
            print message
            myServer.closeConnect()
            if d == [myServer.enum.Net, myServer.enum.tcp]:
                myServer.netConnect()
            if d == [myServer.enum.Net, myServer.enum.band]:
                myServer.bandConnect()
            if d == [myServer.enum.data, 0]:
                myServer.dataConnect()
        
        res.main('results.csv')
        
        
    else: usage()