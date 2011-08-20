import time
import timeit
import socket
import enum
import csv
import sys

class Test():
    start = 0
    results = 0
    iter = 5
    enum = enum.Enum()
    path = 0
    
    name = str(socket.gethostname() + '(' + socket.gethostbyname(socket.gethostname()) + ')')
    
    def __init__(self, iter, path):
        self.iter = iter
        self.path = path
        try:
            self.results = csv.writer(open(self.path, 'ab'))
        except Exception:
            print 'Could not open', self.path 
    
    def fib(self, n):
        if n <= 0:
            return 0
        elif n == 1:
            return 1
        else:
            return self.fib(n-1) + self.fib(n-2)
        
class IOTest(Test):
    
    def startMat(self):
        self.results.writerow(['NewTest', 'Mattest', self.name])
        
        
        i = 0
        init = time.time()
        dur = 0.0
        #sys.setrecursionlimit(1500)
        start = 0.0
        dur = 0.0
        while i < self.iter:
            start = time.time()
            a = self.fib(25)
            dur = time.time() - start
            values = [str(i), str(dur), str(time.time()-init)]
            print values
            self.results.writerow(values)
            i = i + 1
        self.results.writerow(['EndTest'])
            
    def startIO(self):
        self.results.writerow(['NewTest', 'I-O', self.name])

        
        j = 0
        init = time.time()
        start = 0.0
        dur = 0.0
        while j < self.iter:
            start = time.time()
            k = 0
            while k < 5:
                o = open('lorem.txt', 'r')
                data = o.read()
                i = open('temp.txt', 'w')
                i.write(str(data))
                o.close()
                i.close()
                k = k + 1
            dur = time.time() - start
            values = [str(j), str(dur), str(time.time()-init)]
            print values
            self.results.writerow(values)
            j = j + 1
        
        self.results.writerow(['EndTest'])
        
    def startSeek(self):
        self.results.writerow(['NewTest', 'SeekAndWrite', self.name])

        
        j = 0
        init = time.time()
        start = 0.0
        dur = 0.0
        while j < self.iter:
            start = time.time()
            k = 0
            while k < 10: 
                o = open('data.txt', 'r')
                data = o.read()
                o = open('string.txt', 'r')
                s = o.read()
                index = data.find(s)
                i = open('temp.txt', 'w')
                i.write(str(data[index:index+10000]))
                o.close()
                i.close()
                k = k + 1
            dur = time.time() - start
            values = [str(j), str(dur), str(time.time()-init)]
            self.results.writerow(values)
            j = j + 1
        
        self.results.writerow(['EndTest'])
            
class NetTest(Test):
    
    def startTCP(self, serverIP, port):
        self.results.writerow(['NewTest', 'TCP', self.name])
        
        
        init = time.time()
        exceptions = 0
        i = 0
        start = 0.0
        dur = 0.0
        while i < self.iter:
            start = time.time()
            j = 0
            while j < 50:
                try: 
                    self.TCP('test', serverIP, port)
                except:
                    exceptions = exceptions + 1
                j = j + 1
            dur = time.time() - start
            values = [str(i), str(dur), str(time.time()-init)]
            print values
            self.results.writerow(values)
            i = i + 1
        print 'Exceptions', exceptions
        self.TCP(self.enum.stop, serverIP, port)
        
        self.results.writerow(['EndTest'])
        
    def startBand(self, serverIP, port):
        self.results.writerow(['NewTest', 'Band', self.name])
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect((serverIP, port))
        
        
        s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s1.connect((serverIP, port + 1))
        
        j = 0
        init = time.time()
        start = 0.0
        dur = 0.0
        o = open('lorem.txt', 'r')
        data = o.read()
        while j < self.iter:
            start = time.time()
            k = 0
            while k < 5:
                s1.send(data)
                print 'iter'
                k = k + 1
            dur = time.time() - start
            values = [str(j), str(dur), str(time.time()-init)]
            print values
            self.results.writerow(values)
            j = j + 1
            o.close()
        
        time.sleep(2)
        s1.send('stop')
        print 'yes'
        while True:
            print 'yes1'
            d = s.recv(512)
            print d
            if d:
                break
        
        self.results.writerow(['EndTest'])
        
        
    def TCP (self, message, serverIP, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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

        
