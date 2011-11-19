"""
    Author: Christoph Steindl
    E-Mail: a0706052@unet.univie.ac.at
"""

import test as T
import time

"""
    Sample UserTest class. This class can be overridden by user to define an own test.
    Methods and member variables are derived from class "Test" in test.py.
"""
class UserTest(T.Test):
    
    # Method to start user-defined test from client.py
    def startUser(self):
        # Initiation of the Test. Member variables are set.
        self.initTest('UserTest')
        
        # Receives message from class "Host" and either starts next iteration of the
        # test, or finishes the test. Times of each iteration is logged.
        while True:
            i = self.recieve()
            if i[0] == self.const.iteration:
                self.start = time.time()
                
                print 'UserTest' # Has to be changed to more useful function
                
                # Logs and prints the measured values.
                self.dur = time.time() - self.start
                values = [str(i[1]), str(self.dur), str(self.start)]
                print values
                self.results.writerow(values)
            if i[0] == self.const.stop:
                break
            
        # Ends this test
        self.endTest()