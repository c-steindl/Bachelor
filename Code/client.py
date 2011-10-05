import socket
import sys
import test
import time
import enum
import csv
import platform
import os

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
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.connect((self.serverIP, self.port))
        except Exception:
            print 'Could not open Socket'
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
                print 'sendall_data', self.s.send(text)
                self.s.send(self.enum.stop)
                self.closeConnect()
                break
            
    def sendConfig(self):
        time.sleep(10)
        self.connect()
        while True:
            data = self.s.recv(1024)
            if data:
                text = ''
                text = text + 'newVM \n'
                text = text + (str(socket.gethostname() + '(' + socket.gethostbyname(socket.gethostname()) + ')') + '\n')
                text = text + platform.machine() +'\n'
                text = text + platform.node() +'\n'
                text = text + platform.processor() +'\n'
                text = text + platform.system() +'\n'
                
                try:
                    text = text + os.popen('cat /proc/meminfo').read() +'\n'
                    text = text + os.popen('cat /proc/cpuinfo').read() +'\n'
                except Exception:
                    print 'No Unix System'
                    pass
                
                try:
                    text = text + os.popen('systeminfo').read() +'\n'
                except Exception:
                    print 'No Windows System'
                    pass
                
                text = text + '---------------------------\n'
                print 'sendall_config', self.s.send(text)
                self.s.send(self.enum.stop)
                self.closeConnect()
                break

    def dataHandling(self, data):
        print time.time()
        if data[0] == self.enum.iter:
            self.iter = int(data[1])
        elif data[0] == self.enum.IO:
            if data[1] == self.enum.mat:
                t = test.IOTest(myClient.iter, myClient.path, myClient.serverIP, myClient.port)
                t.startMat()
            if data[1] == self.enum.rw:
                t = test.IOTest(myClient.iter, myClient.path, myClient.serverIP, myClient.port)
                t.startIO()
            if data[1] == self.enum.seek:
                t = test.IOTest(myClient.iter, myClient.path, myClient.serverIP, myClient.port)
                t.startSeek()
        elif data[0] == self.enum.Net:
            if data[1] == self.enum.tcp:
                t = test.NetTest(myClient.iter, myClient.path, myClient.serverIP, myClient.port)
                t.startTCP()
            if data[1] == self.enum.band:
                t = test.NetTest(myClient.iter, myClient.path, myClient.serverIP, myClient.port)
                t.startBand()
        elif data[0] == self.enum.data:
            self.sendData()
        elif data[0] == self.enum.config:
            self.sendConfig()
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