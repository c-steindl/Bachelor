import socket
import sys
import test
import time
import enum

class Client():
    test = 0
    duration = 0
    port = 0
    s = socket.socket()
    serverIP = ''
    enum = enum.Enum()
    iter = 5
    results = 0
    
    def __init__(self, port, serverIP):
        path = 'results/' + str(time.time()) + '.csv'
        print 'Pfad: ', path
        self.results = open(path, 'w')
        self.port = port
        self.serverIP = serverIP
        
    def __del__(self):
        if self.results != 0:
            self.results.close()

    def connect(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.serverIP, self.port))
        print self.s.getsockname()
        
    def closeConnect(self):
        self.s.close()
        
    def recieve(self):
        data = self.s.recv(1024)
        data = data.split()
        return data

    
def usage():
    print 'USAGE: python client.py <Port to connect> <Server IP>'
	
if __name__ == "__main__":
    if len(sys.argv) == 3:
        myClient = Client(int(sys.argv[1]), sys.argv[2])
        
        myClient.connect()
        d = myClient.recieve()
        if d[0] == myClient.enum.iter:
            myClient.iter = int(d[1])
            print str(myClient.iter) + ' Iterations'
            time.sleep(2)
        
        t = test.IOTest(myClient.iter, myClient.results)
        
        myClient.connect()
        d = myClient.recieve()
        if d[0] == myClient.enum.start:
            t.startMat()
            time.sleep(2)
        
        myClient.connect()
        d = myClient.recieve()
        if d[0] == myClient.enum.start:
            t.startIO()
            time.sleep(2)
            
        t = test.NetTest(myClient.iter, myClient.results)
        
        myClient.connect()
        d = myClient.recieve()
        if d[0] == myClient.enum.start:
            time.sleep(2)
            t.startTCP(myClient.serverIP, myClient.port)
            time.sleep(2)
        
        #myClient.connect()
        #d = myClient.recieve()
        #if d[0] == myClient.enum.start:
        #    t.startTCP()
        #    time.sleep(2)        
            

    else: usage()