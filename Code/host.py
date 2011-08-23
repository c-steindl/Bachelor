import socket
import sys
import os
import time
import enum
import string
import results as res
import matplotlib.pyplot as plt

class Host():
    port = 0
    clients = list()
    numClients = 0
    enum = enum.Enum()
    config = list()
    path = str(time.time())
    file = 'results.csv'
    iterations = 0
    
    def __init__(self, port, numClients, iter):
        print 'IP:', socket.gethostbyname(socket.gethostname())
        self.port = port
        print 'Port:', self.port
        os.mkdir(self.path)
        print 'Results at:', self.path + '/'
        self.numClients = numClients
        print 'Number of Clients:', self.numClients
        self.iterations = iter
        print 'Number of Iterations:', self.iterations

        #self.config.append([self.enum.iter, int(iter)])
        self.config.append([self.enum.IO, self.enum.mat])
        #self.config.append([self.enum.IO, self.enum.rw])
        #self.config.append([self.enum.IO, self.enum.seek])
        #self.config.append([self.enum.Net, self.enum.tcp])
        #self.config.append([self.enum.Net, self.enum.band])
        self.config.append([self.enum.data, 0])
        self.config.append([self.enum.config, 0])
        self.config.append([self.enum.stopClient, 1])
        #self.config.append([self.enum.plot, 1])

    def initConnect(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('', self.port))
            s.listen(1)
            i = 0
            while i < self.numClients:
                conn, addr = s.accept()
                i = i + 1
                client = [i, addr, conn]
                self.clients.append(client)
                #print 'connected clients', self.clients
        except Exception as msg:
            print 'Achtung', msg
        
    def dataConnect(self):
        results = open(myServer.path + '/' + myServer.file, 'wb')
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('', self.port))
            s.listen(1)
        except Exception:
            print 'Could not open socket'
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
        
    def configConnect(self):
        config = open(myServer.path + '/config.txt', 'wb')
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('', self.port))
            s.listen(1)
        except Exception:
            print 'Could not open socket'
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
                config.write(data)
                
            config.write('\n')
        #print 'connected clients', self.clients
        config.close()
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
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('', self.port))
            s.listen(1)
        except Exception:
            print 'Could not open socket'
        stop = 0
        client = list()
        while stop < self.numClients:
            conn, addr = s.accept()
            d = conn.recv(128).split()
            #print d
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
        self.initConnect()
        
        stop = 0
        #try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', self.port + 1))
        s.listen(1)
        #except Exception:
        #    print 'Could not open socket'
        
        lastData = ''
        currentData = ''
        #nextData = ''
        conn, addr = s.accept()
        while True:
            lastData = currentData
            currentData = conn.recv(512)
            data = lastData + currentData
            print 'yes', data.find('stop'), lastData, currentData, data
            if data.find('stop') >= 0:
                stop = stop + 1
            if stop == self.numClients:
                break
            print data
            
        self.sendAll('end_bandwidth')
        self.closeConnect()
        
    def sendIteration(self):
        i = 0
        while i < self.iterations:
            message = str(self.enum.iteration) + ' ' + str(i)
            self.initConnect()
            self.sendAll(message)
            print message
            self.closeConnect()
            i = i + 1
            
    def sendFinish(self):
        message = str(self.enum.stop) + ' ' + str(1)
        self.initConnect()
        self.sendAll(message)
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
            #if d == [myServer.enum.IO, myServer.enum.mat]:
            if d == [myServer.enum.Net, myServer.enum.tcp]:
                myServer.netConnect()
            if d == [myServer.enum.Net, myServer.enum.band]:
                myServer.bandConnect()
            if d == [myServer.enum.data, 0]:
                myServer.dataConnect()
            if d == [myServer.enum.config, 0]:
                myServer.configConnect()
            
            if d[0] == myServer.enum.IO or d[0] == myServer.enum.Net:    
                myServer.sendIteration()
                myServer.sendFinish()
        
            if d[0] == myServer.enum.plot:
                res.main(myServer.path, myServer.file, 'normal')
                res.main(myServer.path, myServer.file, 'sum')
                res.main(myServer.path, myServer.file, 'both')
        
        
    else: usage()