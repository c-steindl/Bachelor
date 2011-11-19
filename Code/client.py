"""
    Author: Christoph Steindl
    E-Mail: a0706052@unet.univie.ac.at
"""

import socket
import sys
import test
import time
import const
import csv
import platform
import os
import userTest


"""
    The class "Client" connects to the "Host" and waits until a command is received.
    This command is executed afterwards.
"""
class Client():
    test = 0
    duration = 0
    port = 0
    s = socket.socket()
    serverIP = ''
    const = const.Const()
    iter = 5
    path = 0
    
    # Initiates the "Client" and sets and prints the main member variables.
    def __init__(self, port, serverIP):
        self.path = 'results/' + str(time.time()) + '.csv'
        print 'Results at:', self.path
        self.port = port
        self.serverIP = serverIP
    
    # Connects to the "Host" via TCP.
    def connect(self):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.connect((self.serverIP, self.port))
        except Exception:
            print 'Could not open Socket'
        #print self.s.getsockname()
    
    # Closes connection opened with method connect().
    def closeConnect(self):
        self.s.close()
        
    # Receives data from "Host" and splits it to get a list of information. This
    # method is used by the main-function and calls after receiving a command the
    # dataHandling()-function.
    def recieve(self):
        self.connect()
        while True:
            data = self.s.recv(1024)
            if data:
                data = data.split()
                print data
                self.dataHandling(data)
                break
    
    # Sends all measured values gathered while performing the tests to the "Host".
    def sendData(self):
        time.sleep(10)
        self.connect()
        while True:
            # If this certain "Client" gets the command to send it's data the csv-file,
            # containing the results is opened and transmitted to "Host".
            data = self.s.recv(1024)
            if data == self.const.send:
                text = open(self.path, 'r').read()
                print text
                print 'sendall_data', self.s.send(text)
                self.s.send(self.const.stop)
            if data == self.const.stop:
                self.closeConnect()
                break
    
    # Sends all gathered configuration data of the operationg system..        
    def sendConfig(self):
        time.sleep(10)
        self.connect()
        while True:
            data = self.s.recv(1024)
            if data == self.const.send:
                # If this certain "Client" gets the command to send it's configuration,
                # system variables are read and transmitted to "Host"
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
                self.s.send(self.const.stop)
            if data == self.const.stop:
                self.closeConnect()
                break
    
    # Main method to assure the correct functionality of the class "Client". This
    # method recieves a command <data> and initiates the correct test or behavior
    # of the "Client"
    def dataHandling(self, data):
        print time.time()
        if data[0] == self.const.iter:
            self.iter = int(data[1])
        elif data[0] == self.const.IO:
            if data[1] == self.const.mat:
                t = test.IOTest(myClient.iter, myClient.path, myClient.serverIP, myClient.port)
                t.startMat()
            if data[1] == self.const.rw:
                t = test.IOTest(myClient.iter, myClient.path, myClient.serverIP, myClient.port)
                t.startIO()
            if data[1] == self.const.seek:
                t = test.IOTest(myClient.iter, myClient.path, myClient.serverIP, myClient.port)
                t.startSeek()
            if data[1] == self.const.seekIndex:
                t = test.IOTest(myClient.iter, myClient.path, myClient.serverIP, myClient.port)
                t.startSeekIndex()
        elif data[0] == self.const.Net:
            if data[1] == self.const.tcp:
                t = test.NetTest(myClient.iter, myClient.path, myClient.serverIP, myClient.port)
                t.startTCP()
        elif data[0] == self.const.User:
            t = userTest.UserTest(myClient.iter, myClient.path, myClient.serverIP, myClient.port)
            t.startUser()
        elif data[0] == self.const.data:
            self.sendData()
        elif data[0] == self.const.config:
            self.sendConfig()
        elif data [0] == self.const.stopClient:
            sys.exit(0)
        self.closeConnect()
        
        time.sleep(2)

# Prints the usage information.    
def usage():
    print 'USAGE: python client.py <Port to connect> <Server IP>'
	
if __name__ == "__main__":
    if len(sys.argv) == 3:
        myClient = Client(int(sys.argv[1]), str(sys.argv[2]))
        
        # Client receives data from host in endless-loop.
        while True:
            myClient.recieve()
        
    else: usage()