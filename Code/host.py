"""
    Author: Christoph Steindl
    E-Mail: a0706052@unet.univie.ac.at
"""

import socket
import sys
import os
import time
import const
import string
import random
import csv
import results as res
import matplotlib.pyplot as plt

"""
    The class "Host" waits for a certain number <numClients> of "Clients" to connect. 
    Afterwards it performs some tests, which are previously declared in config.csv.
"""
class Host():
    port = 0
    clients = list()
    numClients = 0
    const = const.Const()
    config = list()
    path = str(time.time())
    file = 'results.csv'
    iterations = 0
    
    # Initiates the "Host" and sets and prints the main member variables.
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
        
        # Iteration command is appended to list of commands so the clients knows
        # in each case how many iterations to do.
        self.config.append([self.const.iter, int(iter)])
        
        # The rest of commands are read from "config.csv".
        with open('config.csv', 'rb') as f:
            reader = csv.reader(f)
            for r in reader:
                self.config.append([r[0], r[1]])

    # Opens a TCP connection to each "Client". Blocks until <numClients> clients are
    # connected to the "Host". The connections are saved in <self.clients>.
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
            print 'Attention', msg
    
    # Connects to all "Clients" which send the gathered results. The complete results
    # are saved in <timestamp>/results.csv    
    def dataConnect(self):
        results = open(myServer.path + '/' + myServer.file, 'wb')
        
        # Opens a connection to each "Client".
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
            
        # Receives data from each "Client"
        for x in range(self.numClients):
            data = 0
            c = self.clients[x]
            conn = c[2]
            conn.send(self.const.send)
            while True:
                data = conn.recv(1024)
                print data
                
                if data.find(self.const.stop) >= 0:
                    k = data.find(self.const.stop)
                    if k > 1:
                        data = data[:k]
                        # Writes gathered results.
                        results.write(data)
                    break
                results.write(data)
                
            results.write('\n')
        results.write('finish')
        
        # If all "Clients" sent their informations "Host" sends command to stop in
        # order to proceed to the next command.
        for x in range(self.numClients):
            c = self.clients[x]
            conn = c[2]
            conn.send(self.const.stop)
        
        # Closes file and connection to "Clients".
        results.close()
        self.closeConnect()
    
    # Connects to all "Clients" which send the gathered informations about ther OS. The 
    # complete results are saved in <timestamp>/configuration.txt      
    def configConnect(self):
        config = open(myServer.path + '/configuration.txt', 'wb')
        
        # Opens a connection to each "Client".
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
            
        # Receives data from each "Client"    
        for x in range(self.numClients):
            data = ''
            c = self.clients[x]
            conn = c[2]
            conn.send(self.const.send)
            while True:
                data = conn.recv(1024)
                print data
                if data.find(self.const.stop) >= 0:
                    k = data.find(self.const.stop)
                    data = data[:k]
                    # Writes gathered informations.
                    config.write(data)
                    break
                config.write(data)
                
            config.write('\n')

        # If all "Clients" sent their informations "Host" sends command to stop in
        # order to proceed to the next command.            
        for x in range(self.numClients):
            c = self.clients[x]
            conn = c[2]
            conn.send(self.const.stop)
        
        # Closes file and connection to "Clients".
        config.close()
        self.closeConnect()
        
    # Closes connection opened with method initConnect()
    def closeConnect(self):
        while self.clients:
            client = self.clients.pop()
            client[2].close()
            
    # Sends all "Clients" connected with initConnect() the message <message>
    def sendAll(self, message):
        i = 0
        while i < self.numClients:
            client = self.clients[i]
            client[2].send(message)
            i = i + 1
    
    # Server-behavior for TCPTest.
    def netConnect(self):
        
        # Socket to connect is provided.
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('', self.port))
            s.listen(1)
        except Exception:
            print 'Could not open socket'
        
        stop = 0
        client = list()
        # "Clients" connect to socket and send a test-string. Disconnection afterwards.
        # This action is performed until all "Clients" send stop-command.
        while stop < self.numClients:
            conn, addr = s.accept()
            d = conn.recv(128).split()
            if d[0] == self.const.stop:
                stop = stop + 1
                client.append(conn)
            else:
                conn.close()
            message = myServer.const.stop + ' ' + myServer.const.tcp
            #print message
        while client:
            c = client.pop()
            c.send(message)
        
    # Sends the command for an iteration to "Clients" <self.iterations>-times. If the
    # <data>-parameter is not equal null, the "Host" is performing either a "SeekandWriteTest"
    # or a "SeekIndexTest". In second case the flag <index> has to be true.
    def sendIteration(self, data, index):
        i = 0
        while i < self.iterations:
            self.initConnect()
            
            # Checks which type of iteration to send.
            if data != None:
                if index == True:
                    # "SeekIndexTest" is performed.
                    message = str(self.const.iteration) + ' ' + str(i) + ' ' + str(self.getIndex(data))
                else:
                    # "SeekandWriteTest" is performed.
                    message = str(self.const.iteration) + ' ' + str(i) + ' ' + self.getString(data)
            else:
                # Other Test is performed.
                message = str(self.const.iteration) + ' ' + str(i)
            
            # Sends all "Clients" the command and closes connection.
            self.sendAll(message)
            print message
            self.closeConnect()
            i = i + 1
    
    # After the iterations this method is called to tell the "Clients" that the test is over.        
    def sendFinish(self):
        message = str(self.const.stop) + ' ' + str(1)
        self.initConnect()
        self.sendAll(message)
        self.closeConnect()
        
    # Creates two random indexes from a data file with the maximum range <self.const.chunkSize>
    # for the "SeekandWriteTest".
    def getString(self, data):
        
        size = os.path.getsize(data.name) - 1
        index1 = random.randint(1, size)
        if (index1 + self.const.chunkSize) > size:
            index2 = size
        else:
            index2 = index1 + self.const.chunkSize
        
        print index1, index2
        
        # Gets the data from file between <index1> and <index2>
        return self.getData(data, index1, index2)
    
    # Creates a random index of a file for the "SeekIndexTest".
    def getIndex(self, data):
        
        size = os.path.getsize(data.name) - 1
        index1 = random.randint(1, size)
        
        return index1
    
    # Gathers a string, which contains the characters in <data> between <index1> and <index2>.
    def getData(self, data, index1, index2):
        data.seek(index1)
        string = data.read(index2 - index1)
        return string
        
# Prints the usage information.        
def usage():
    print 'USAGE: python host.py <Port to listen> <Number of clients> <Number of iterations>'

if __name__ == "__main__":
    if len(sys.argv) == 4:
        myServer = Host(int(sys.argv[1]), int(sys.argv[2]), long(sys.argv[3]))

        while myServer.config:
            # Pops a command and sends it to all "Clients". Afterwards the "Host" sends the
            # command for iteration.
            data = None
            d = myServer.config.pop(0)
            
            if d[0] != myServer.const.plot:
                myServer.initConnect()
            
            message = str(d[0]) + ' ' + str(d[1])
            
            if d[0] != myServer.const.plot:
                myServer.sendAll(message)
                print message
                myServer.closeConnect()

            if d == [myServer.const.IO, myServer.const.mat]:
                myServer.sendIteration(data, False)
                myServer.sendFinish()
            if d == [myServer.const.IO, myServer.const.rw]:
                myServer.sendIteration(data, False)
                myServer.sendFinish()
            if d == [myServer.const.IO, myServer.const.seek]:
                data = open('test.txt', 'r')

                myServer.sendIteration(data, False)
                myServer.sendFinish()
                
                data.close()
            if d == [myServer.const.IO, myServer.const.seekIndex]:
                data = open('test.txt', 'r')

                myServer.sendIteration(data, True)
                myServer.sendFinish()
                
                data.close()
            if d == [myServer.const.Net, myServer.const.tcp]:
                myServer.netConnect()
            if d[0] == myServer.const.User:
                myServer.sendIteration(data, False)
                myServer.sendFinish()
            if d[0] == myServer.const.data:
                myServer.dataConnect()
            if d[0] == myServer.const.config:
                myServer.configConnect()
            
            # Plays an acoustical signal to announce the end of all tests.
            if d[0] == myServer.const.stopClient:
                for i in range(5):
                    print chr(7)
                    time.sleep(2)
        
            # Plot of the results is initiated.
            if d[0] == myServer.const.plot:
                print message
                res.main(myServer.path, myServer.file, str(d[1]))
        
        
    else: usage()
