import time
import socket

class Enum():
    dur = 'duration'
    start = 'start'
    end = 'finish'
    IO = 'IOTest'
    Net = 'NetworkTest'

class Test():
    start = 0
    results = 0
    iter = 5
    enum = Enum()
    
    def __init__(self):
        path = 'results/' + str(time.time()) + '.csv'
        print 'Pfad: ', path
        self.results = open(path, 'w') 
    
    def fib(self, n):
        if n <= 0:
            return 0
        elif n == 1:
            return 1
        else:
            return self.fib(n-1) + self.fib(n-2)
        
class IOTest(Test):
    def __del__(self):
        if self.results != 0:
            self.results.close()
    
    def startMat(self):
        self.results.write(self.enum.IO)
        self.results.write('\n')
        self.results.write('Mattest')
        self.results.write('\n')
        self.results.write(str(socket.gethostbyname(socket.gethostname())))
        self.results.write('\n')
        
        i = 0
        while i < self.iter:
            start = time.time()
            a = self.fib(30)
            dur = time.time() - start
            values = str(i) + ';' + str(dur)
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
            values = str(j) + ';' + str(dur)
            print values
            self.results.write(values)
            self.results.write('\n')
            j = j + 1
            
class NetTest(Test):
    def startBand(self):
        self.results.write(self.enum.IO)
        self.results.write('\n')
        self.results.write('Bandwitdh')
        self.results.write('\n')
        self.results.write(str(socket.gethostbyname(socket.gethostname())))
        self.results.write('\n')
        
#    def startTCP(self):