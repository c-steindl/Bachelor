import socket
import sys
import test
import time

class Enum():
    dur = 'duration'
    start = 'start'
    end = 'finish'
    IO = 'IOTest'
    Net = 'NetworkTest'

class Client():
    test = 0
    duration = 0
    port = 0
    s = socket.socket()
    serverIP = ''
    enum = Enum()
    
    def __init__(self, port, serverIP):
        self.port = port
        self.serverIP = serverIP

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
        test = test.IOTest()
        
        myClient.connect()
        d = myClient.recieve()
        if d[0] == myClient.enum.start:
            test.startMat()
            time.sleep(2)
        
        myClient.connect()
        d = myClient.recieve()
        if d[0] == myClient.enum.start:
            test.startIO()
            time.sleep(2)
            
        #test = test.NetTest()
        
        #myClient.connect()
        #d = myClient.recieve()
        #if d[0] == myClient.enum.start:
        #    test.startBand()
        #    time.sleep(2)
        
        #myClient.connect()
        #d = myClient.recieve()
        #if d[0] == myClient.enum.start:
        #    test.startTCP()
        #    time.sleep(2)        
            

    else: usage()