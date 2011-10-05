import random
import string

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
