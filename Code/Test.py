"""
    Author: Christoph Steindl
    E-Mail: a0706052@unet.univie.ac.at
"""

import time
import timeit
import socket
import const
import csv
import sys
import os
import platform

"""
    Class Test defines certain functualities and variabls of a test. Each test
    is derived from this class to obtain these functualities.
"""

class Test():
    start = 0
    results = 0
    iter = 5
    const = const.Const()
    path = 0
    s = 0
    serverIP = ''
    port = 0
    init = 0.0
    dur = 0.0
    start = 0.0
    
    try:
        name = str(socket.gethostname() + '(' + socket.gethostbyname(socket.gethostname()) + ')')
        #name = str(socket.gethostname())
    except Exception:
        name = platform.node()
        pass
    
    print name

    # Initiation of the test. Variables are set.
    
    def __init__(self, iter, path, IP, p):
        self.iter = iter    # Number of iterations
        self.path = path    # Path to results/<timestamp>.csv
        self.serverIP = IP  # Host-IP
        self.port = p       # Host-port
        
        # Generation of reults file
        try:
            self.results = csv.writer(open(self.path, 'ab'))
        except Exception:
            print 'Could not open', self.path
            
    # Test connects to Host in order to communicate (recieving the iterations-command, ...)
    # with it.
    def connect(self):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.connect((self.serverIP, self.port))
        except Exception:
            print 'Could not open Socket'
        
    # Closes the connection from above
    def closeConnect(self):
        self.s.close()
        
    # Method to recieve data from Host
    def recieve(self):
        self.connect()
        while True:
            data = self.s.recv(1024)
            data = data.split()
            if data:
                return data
            
    # Calculates the nth number of the Fibonacci-numbers to generate CPU load
    def fib(self, n):
        if n <= 0:
            return 0
        elif n == 1:
            return 1
        else:
            return self.fib(n-1) + self.fib(n-2)
    
    # Opens the file "lorem.txt" and reads it. Afterwards it writes the data
    # to "temp.txt" to generate Disk I/O.        
    def IO(self):
        o = open('lorem.txt', 'r')
        data = o.read()
        i = open('temp.txt', 'w')
        i.write(str(data))
        o.close()
        i.close()
        
    # Opens the file "test.txt" and and seeks for a certain string contained
    # s. Afterwards it writes the search-string with the next 1000000 characters
    # to "temp.txt" to generate Disk I/O.
    def seek(self, s):
        o = open('test.txt', 'r')
        
        # Reads in the file in chunks, in case the data is to huge to manage it
        # at once.
        lastString = ''
        while True:
            currentString = o.read(self.const.chunkSize)
            lastString = lastString + currentString
            index1 = lastString.find(s)
            if index1 > 0:
                index1 = o.tell() + index1 - (2 * self.const.chunkSize)
                break
            else:
                lastString = currentString
                
        # Defines the lower and upper index to write from "test.txt" and sets
        # the upper bound to len(test.txt) in case it is out of bounds.
        i = open('temp.txt', 'w')
        size = os.path.getsize(o.name) - 1
        if (index1 + 1000000) > size:
            index2 = size
        else:
            index2 = index1 + 1000000

        # Writes gathered data to "temp.txt"
        try:
            o.seek(index1)
            while True:
                data = o.read(self.const.chunkSize)
                i.write(str(data))
                if o.tell() > index2:
                    break
        except Exception:
            print 'Could not write to file'
        o.close()
        i.close()
        
    
    # Opens the file "test.txt" and and seeks for a certain position in the file.
    # Afterwards it writes the next 1000000 characters from this position to 
    # "temp.txt" to generate Disk I/O.
    def seekIndex(self, s):
        o = open('test.txt', 'r')             
        i = open('temp.txt', 'w')
        size = os.path.getsize(o.name) - 1
        index1 = int(s)

        # Defines the lower and upper index to write from "test.txt" and sets
        # the upper bound to len(test.txt) in case it is out of bounds.
        if (index1 + 1000000) > size:
            index2 = size
        else:
            index2 = index1 + 1000000

        # Writes gathered data to "temp.txt"
        try:
            o.seek(index1) # Seeks for index received from "Host"
            print o.tell()
            while True:
                data = o.read(self.const.chunkSize)
                i.write(str(data))
                if o.tell() > index2:
                    break
        except Exception:
            print 'Could not write to file'
        o.close()
        i.close()
        

    # This method opens a TCP-connection to <serverIP> on port <port>. It sends a
    # message to this server. Is this message the command to end this iterations
    # it waits until all other "Clients" have finisehd, because in this case the
    # server sends the command for the next iteration.
    def TCP (self, message, serverIP, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect((serverIP, port))
        s.send(message)
        if message == self.const.stop:
            while True:
                data = s.recv(512)
                if data:
                    break
        s.close()
    
    # Writes the first line in the results.csv of the test. Afterwards it sets
    # values to current time or zero.
    def initTest(self, name):
        time.sleep(2)
        self.results.writerow(['NewTest', str(name), self.name])
        
        self.init = time.time()
        self.dur = 0.0
        self.start = 0.0
    
    # Writes the last line in the results.csv of the test.    
    def endTest(self):
        self.results.writerow(['EndTest'])

        
class IOTest(Test):      
    
    # Method to start MatTest called from client.py    
    def startMat(self):
        # Initiation of the Test. Member variables are set.
        self.initTest('Mattest')
        
        while True:
            i = self.recieve()
            if i[0] == self.const.iteration:
                self.start = time.time()
                a = self.fib(35)
                self.dur = time.time() - self.start
                values = [str(i[1]), str(self.dur), str(self.start)]
                print values
                self.results.writerow(values)
            if i[0] == self.const.stop:
                break
            
        self.endTest()

    # Method to start IOTest called from client.py            
    def startIO(self):
        # Initiation of the Test. Member variables are set.
        self.initTest('I-O')
        
        # Receives message from class "Host" and either starts next iteration of the
        # test, or finishes the test. Times of each iteration is logged.
        while True:
            i = self.recieve()
            if i[0] == self.const.iteration:
                j = 0
                self.start = time.time()
                
                # Does 5 times per iteration the IO method and logs the measured values
                # afterwards.
                while j < 5:
                    a = self.IO()
                    j = j + 1
                self.dur = time.time() - self.start
                values = [str(i[1]), str(self.dur), str(self.start)]
                print values
                self.results.writerow(values)
            if i[0] == self.const.stop:
                break
            
        self.endTest()    
        
    # Method to start SeekandWriteTest called from client.py        
    def startSeek(self):
        # Initiation of the Test. Member variables are set.
        self.initTest('SeekAndWrite')

        # Receives message from class "Host" and either starts next iteration of the
        # test, or finishes the test. Times of each iteration is logged.        
        while True:
            i = self.recieve()
            if i[0] == self.const.iteration:
                self.start = time.time()
                
                # Searches for the string received from "Host" and logs the measured
                # values afterwards.
                self.seek(i[2])
                self.dur = time.time() - self.start
                values = [str(i[1]), str(self.dur), str(self.start)]
                print values
                self.results.writerow(values)
            if i[0] == self.const.stop:
                break
            
        self.endTest()
        
    # Method to start SeekIndexTest called from client.py    
    def startSeekIndex(self):
        # Initiation of the Test. Member variables are set.
        self.initTest('SeekIndex')

        # Receives message from class "Host" and either starts next iteration of the
        # test, or finishes the test. Times of each iteration is logged.        
        while True:
            i = self.recieve()
            if i[0] == self.const.iteration:
                self.start = time.time()
                
                # Searches for the position received from "Host" and logs the measured
                # values afterwards.                
                self.seekIndex(i[2])
                self.dur = time.time() - self.start
                values = [str(i[1]), str(self.dur), str(self.start)]
                print values
                self.results.writerow(values)
            if i[0] == self.const.stop:
                break
            
        self.endTest()
            
class NetTest(Test):
    
    # Method to start TCPTest called from client.py    
    def startTCP(self):
        # Initiation of the Test. Member variables are set.
        self.initTest('TCP')
        
        i = 0
        exceptions = 0
        
        # Performs 5000 TCP connects to host and closes the connection afterwards.
        while i < self.iter:
            self.start = time.time()
            j = 0
            while j < 5000:
                try: 
                    self.TCP('test', self.serverIP, self.port)
                except:
                    exceptions = exceptions + 1
                j = j + 1
            self.dur = time.time() - self.start
            values = [str(i), str(self.dur), str(self.start)]
            print values
            self.results.writerow(values)
            i = i + 1
        print 'Exceptions', exceptions
        self.TCP(self.const.stop, self.serverIP, self.port)
        
        self.results.writerow(['EndTest'])