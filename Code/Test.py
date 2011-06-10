import time
import timeit
import socket
import enum
import csv

class Test():
    start = 0
    results = 0
    iter = 5
    enum = enum.Enum()
    path = 0
    
    def __init__(self, iter, path):
        self.iter = iter
        self.path = path
        self.results = csv.writer(open(self.path, 'ab')) 
    
    def fib(self, n):
        if n <= 0:
            return 0
        elif n == 1:
            return 1
        else:
            return self.fib(n-1) + self.fib(n-2)
        
class IOTest(Test):
    
    def startMat(self):
        self.results.writerow([self.enum.IO])
        self.results.writerow(['Mattest'])
        self.results.writerow([str(socket.gethostname())])
        
        i = 0
        init = time.time()
        while i < self.iter:
            start = time.time()
            a = self.fib(30)
            dur = time.time() - start
            values = [str(i), str(dur), str(time.time()-init)]
            #print values
            self.results.writerow(values)
            i = i + 1
            
    def startIO(self):
        self.results.writerow([self.enum.IO])
        self.results.writerow(['I/O'])
        self.results.writerow([str(socket.gethostname())])
        
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
            values = [str(j), str(dur), str(time.time()-init)]
            #print values
            self.results.writerow(values)
            j = j + 1
            
class NetTest(Test):
    
    def startTCP(self, serverIP, port):
        self.results.writerow([self.enum.Net])
        self.results.writerow(['TCP'])
        self.results.writerow([str(socket.gethostname())])
        
        init = time.time()
        exceptions = 0
        i = 0
        while i < self.iter:
            start = time.time()
            j = 0
            while j < 10:
                try: 
                    self.TCP('test', serverIP, port)
                except:
                    exceptions = exceptions + 1
                j = j + 1
            dur = time.time() - start
            values = [str(i), str(dur), str(time.time()-init)]
            #print values
            self.results.writerow(values)
            i = i + 1
        print 'Exceptions', exceptions
        self.TCP(self.enum.stop, serverIP, port)
        
    def startBand(self, serverIP, port):
        self.results.writerow([self.enum.Net])
        self.results.writerow(['Band'])
        self.results.writerow([str(socket.gethostname())])
        
        bytes = 0
        o = open('lorem.txt', 'r')
        data = o.read()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((serverIP, port))
        init = time.time()
        exceptions = 0
        i = 0
        while i < self.iter:
            start = time.time()
            j = 0
            while j < 25:
                try: 
                    bytes += self.transmit(data, s)
                except:
                    exceptions = exceptions + 1
                j = j + 1
            dur = time.time() - start
            values = [str(bytes), str(dur), str(time.time()-init)]
            #print values
            self.results.writerow(values)
            i = i + 1
        print 'Exceptions', exceptions
        time.sleep(2)
        self.transmit(' ' + self.enum.stop, s)
        print 'sendstop'
        while True:
            data = s.recv(512)
            print data
            if data:
                break
        print 'stop'
        
        
    def TCP (self, message, serverIP, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((serverIP, port))
        s.send(message)
        if message == self.enum.stop:
            while True:
                data = s.recv(512)
                if data:
                    break
        s.close()
    
    def transmit(self, data, socket):
        size = socket.send(data)
        return size

        