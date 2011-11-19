"""
    Author: Christoph Steindl
    E-Mail: a0706052@unet.univie.ac.at
"""

import string

"""
    Simple class, which only contains constants. These constants act like a dictionary
    for class "Host" and class "Client". 
"""
class Const():
    dur = 'duration'
    start = 'startTest'
    stop = string.printable[90]
    end = 'EndTest'
    IO = 'IOTest'
    Net = 'NetworkTest'
    User = 'UserTest'
    iter = 'NumberOfIterations'
    tcp = 'TCPTest'
    mat = 'MatTest'
    rw = 'RWTest'
    seek = 'SeekAndWrite'
    seekIndex = 'SeekIndex'
    stopClient = 'SystemExit'
    data = 'sendData'
    config = 'sendConfig'
    iteration = 'Iteration'
    plot = 'plotResults'
    send = 'startSending'
    chunkSize = 4096