import time
import timeit
import socket
import enum

class Test():
    start = 0
    results = 0
    iter = 5
    enum = enum.Enum()
    
    def __init__(self, iter, results):
        self.results = results
        self.iter = iter 
    
    def fib(self, n):
        if n <= 0:
            return 0
        elif n == 1:
            return 1
        else:
            return self.fib(n-1) + self.fib(n-2)
        
class IOTest(Test):
    
    def startMat(self):
        self.results.write(self.enum.IO)
        self.results.write('\n')
        self.results.write('Mattest')
        self.results.write('\n')
        self.results.write(str(socket.gethostbyname(socket.gethostname())))
        self.results.write('\n')
        
        i = 0
        init = time.time()
        while i < self.iter:
            start = time.time()
            a = self.fib(30)
            dur = time.time() - start
            values = str(i) + ';' + str(dur) + ';' + str(time.time()-init)
            print values
            self.results.write(values)
            self.results.write('\n')
            i = i + 1
            
    def startIO(self):
        self.results.write(self.enum.IO)
        self.results.write('\n')
        self.results.write('I/O')
        self.results.write('\n')
        self.results.write(str(socket.gethostbyname(socket.gethostname())))
        self.results.write('\n')
        
        j = 0
        init = time.time()
        while j < self.iter:
            start = time.time()
            k = 0
            while k < 100: 
                o = open('lorem.txt', 'r')
                data = o.read()
                i = open('temp.txt', 'w')
                i.write(str(data))
                o.close()
                i.close()
                k = k + 1
            dur = time.time() - start
            values = str(j) + ';' + str(dur) + ';' + str(time.time()-init)
            print values
            self.results.write(values)
            self.results.write('\n')
            j = j + 1
            
class NetTest(Test):
    
    def startTCP(self, serverIP, port):
        self.results.write(self.enum.IO)
        self.results.write('\n')
        self.results.write('TCP')
        self.results.write('\n')
        self.results.write(str(socket.gethostbyname(socket.gethostname())))
        self.results.write('\n')
        
        init = time.time()
        i = 0
        while i < self.iter:
            start = time.time()
            j = 0
            while j < 100:
                self.TCP('test', serverIP, port)
                j = j + 1
            dur = time.time() - start
            values = str(i) + ';' + str(dur) + ';' + str(time.time()-init)
            print values
            self.results.write(values)
            self.results.write('\n')
            i = i + 1
        self.TCP(self.enum.stop, serverIP, port)
        
        
    def TCP (self, message, serverIP, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((serverIP, port))
        s.send(message)

        