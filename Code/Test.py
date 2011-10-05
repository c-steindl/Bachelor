import time
import timeit
import socket
import enum
import csv
import sys
import os

class Test():
    start = 0
    results = 0
    iter = 5
    enum = enum.Enum()
    path = 0
    s = 0
    serverIP = ''
    port = 0
    
    #name = str(socket.gethostname() + '(' + socket.gethostbyname(socket.gethostname()) + ')')
    name = str(socket.gethostname())
    
    def __init__(self, iter, path, IP, p):
        self.iter = iter
        self.path = path
        self.serverIP = IP
        self.port = p
        try:
            self.results = csv.writer(open(self.path, 'ab'))
        except Exception:
            print 'Could not open', self.path
            
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
            data = data.split()
            if data:
                return data
            
    
    def fib(self, n):
        if n <= 0:
            return 0
        elif n == 1:
            return 1
        else:
            return self.fib(n-1) + self.fib(n-2)
        
    def IO(self):
        o = open('lorem.txt', 'r')
        data = o.read()
        i = open('temp.txt', 'w')
        i.write(str(data))
        o.close()
        i.close()
        
    def seek(self, s):
        o = open('/home/bachelor/Code/test.txt', 'r')
        #o = open('lorem.txt', 'r')
        
        lastString = ''
        while True:
            currentString = o.read(self.enum.chunkSize)
            lastString = lastString + currentString
            index1 = lastString.find(s)
            if index1 > 0:
                index1 = o.tell() + index1 - (2 * self.enum.chunkSize)
                break
            else:
                lastString = currentString
                
        i = open('temp.txt', 'w')
        size = os.path.getsize(o.name) - 1
        if (index1 + 1000000) > size:
            index2 = size
        else:
            index2 = index1 + 1000000

        try:
            o.seek(index1)
            while True:
                data = o.read(self.enum.chunkSize)
                i.write(str(data))
                if o.tell() > index2:
                    break
        except Exception:
            print 'Could not write to file'
        o.close()
        i.close()
        
class IOTest(Test):      
        
    def startMat(self):
        time.sleep(2)
        self.results.writerow(['NewTest', 'Mattest', self.name])
        
        init = time.time()
        dur = 0.0
        #sys.setrecursionlimit(1500)
        start = 0.0
        dur = 0.0
        
        while True:
            i = self.recieve()
            if i[0] == self.enum.iteration:
                start = time.time()
                a = self.fib(35)
                dur = time.time() - start
                values = [str(i[1]), str(dur), str(start)]
                print values
                self.results.writerow(values)
            if i[0] == self.enum.stop:
                break
            
        self.results.writerow(['EndTest'])

            
    def startIO(self):
        time.sleep(2)
        self.results.writerow(['NewTest', 'I-O', self.name])

        init = time.time()
        dur = 0.0
        start = 0.0
        dur = 0.0
        
        while True:
            i = self.recieve()
            if i[0] == self.enum.iteration:
                j = 0
                start = time.time()
                while j < 5:
                    a = self.IO()
                    j = j + 1
                dur = time.time() - start
                values = [str(i[1]), str(dur), str(start)]
                print values
                self.results.writerow(values)
            if i[0] == self.enum.stop:
                break
            
        self.results.writerow(['EndTest'])
        
        
        
        
    def startSeek(self):
        time.sleep(2)
        self.results.writerow(['NewTest', 'SeekAndWrite', self.name])

        init = time.time()
        dur = 0.0
        start = 0.0
        dur = 0.0
        
        while True:
            i = self.recieve()
            if i[0] == self.enum.iteration:
                start = time.time()
                self.seek(i[2])
                dur = time.time() - start
                values = [str(i[1]), str(dur), str(start)]
                print values
                self.results.writerow(values)
            if i[0] == self.enum.stop:
                break
            
        self.results.writerow(['EndTest'])
            
class NetTest(Test):
    
    def startTCP(self):
        self.results.writerow(['NewTest', 'TCP', self.name])
        
        
        init = time.time()
        exceptions = 0
        i = 0
        start = 0.0
        dur = 0.0
        while i < self.iter:
            start = time.time()
            j = 0
            while j < 5000:
                try: 
                    self.TCP('test', self.serverIP, self.port)
                except:
                    exceptions = exceptions + 1
                j = j + 1
            dur = time.time() - start
            values = [str(i), str(dur), str(start)]
            print values
            self.results.writerow(values)
            i = i + 1
        print 'Exceptions', exceptions
        self.TCP(self.enum.stop, self.serverIP, self.port)
        
        self.results.writerow(['EndTest'])
        
    def startBand(self):
        self.results.writerow(['NewTest', 'Band', self.name])
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect((self.serverIP, self.port))
        
        
        s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s1.connect((self.serverIP, self.port + 1))
        
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
            values = [str(j), str(dur), str(start)]
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

        
