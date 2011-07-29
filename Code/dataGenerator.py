import random
import string

filename = "test.txt"
 
print "Writing to file: %s" % filename
 
 
file = open(filename, 'w')

s = string.printable
s = s[:94]
print s
i = 0
while i < 1000:
	file.write(random.choice(s))
	i = i + 1


file.close()
