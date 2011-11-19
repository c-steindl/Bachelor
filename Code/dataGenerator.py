"""
    Author: Christoph Steindl
    E-Mail: a0706052@unet.univie.ac.at
"""

import random
import string


"""
	Creates some random data in the file <filename>, not containing the const.stop-command.
	The size of the file is defined in while-loop.
"""
filename = "lorem.txt"
 
print "Writing to file: %s" % filename
 
 
file = open(filename, 'w')

s = string.printable
s = s[:90]
print s
i = 0
while i < 20000000:
	file.write(random.choice(s))
	i = i + 1


file.close()
