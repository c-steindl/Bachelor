import socket
import sys
import test
import time
import enum
import csv

class Client():
    test = 0
    duration = 0
    port = 0
    s = socket.socket()
    serverIP = ''
    enum = enum.Enum()
    iter = 5
    path = 0
    
    def __init__(self, port, serverIP):
        self.path = 'results/' + str(time.time()) + '.csv'
        print 'Results at:', self.path
        self.port = port
        self.serverIP = serverIP

    def connect(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.serverIP, self.port))
        #print self.s.getsockname()
        
    def closeConnect(self):
        self.s.close()
        
    def recieve(self):
        self.connect()
        while True:
            data = self.s.recv(1024)
            if data:
                data = data.split()
                print data
                self.dataHandling(data)
                break
            
    def sendData(self):
        time.sleep(10)
        self.connect()
        while True:
            data = self.s.recv(1024)
            if data:
                text = open(self.path, 'r').read()
                print text
                print 'sendall', self.s.send(text)
                self.s.send(self.enum.stop)
                self.closeConnect()
                break

    def dataHandling(self, data):
        print time.time()
        if data[0] == self.enum.iter:
            self.iter = int(data[1])
        elif data[0] == self.enum.IO:
            if data[1] == self.enum.mat:
                t = test.IOTest(myClient.iter, myClient.path)
                t.startMat()
            if data[1] == self.enum.rw:
                t = test.IOTest(myClient.iter, myClient.path)
                t.startIO()
        elif data[0] == self.enum.Net:
            if data[1] == self.enum.tcp:
                t = test.NetTest(myClient.iter, myClient.path)
                t.startTCP(myClient.serverIP, myClient.port)
            if data[1] == self.enum.band:
                t = test.NetTest(myClient.iter, myClient.path)
                t.startBand(myClient.serverIP, myClient.port)
        elif data[0] == self.enum.data:
            self.sendData()
        elif data [0] == self.enum.stopClient:
            sys.exit(0)
        self.closeConnect()
        
        time.sleep(2)

    
def usage():
    print 'USAGE: python client.py <Port to connect> <Server IP>'
	
if __name__ == "__main__":
    if len(sys.argv) == 3:
        myClient = Client(int(sys.argv[1]), str(sys.argv[2]))
        
        while True:
            myClient.recieve()
        
    else: usage()