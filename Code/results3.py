import sys
import csv
import time
import numpy as np
import matplotlib.pyplot as plt

def main(p):
    currentTest = None
    currentID = None
    ID = 0
    testID = -1
    plots = []
    xValues = []
    yValues = []
    currentPlot = None
    
    
    with open(p, 'rb') as f:
        reader = csv.reader(f)
        for r in reader:
            if r[0] == 'NewTest':
                currentTest = r[1]
                testID = testID + 1
                if currentID != r[2]:
                    ID = ID + 1
                    testID = 0
                currentID = r [2]
                if len(plots) >= (testID + 1):
                    currentPlot = plots[testID]
                else:
                    fig = plt.figure()
                    currentPlot = [fig, fig.add_subplot(111), currentTest]
                    plots.insert(testID, currentPlot)
            elif r[0] == 'EndTest':
                if ((len(xValues) > 0) and (len(yValues) > 0)):
                    print
                    addPlot (currentID, currentPlot, xValues, yValues)
                plt.legend()
                xValues = []
                yValues = []
            elif r[0] == 'finish':
                time.sleep(2)
            else:
                xValues.append(float(r[0]))
                yValues.append(float(r[1]))
        print plots
        
        for p in plots:
            currentPlot = p
            fig = p[0]
            print fig
            fig.savefig(p[2] + '_hist')
            #p[0].savefig(p[2])
        #plt.legend()
        plt.show()

def addPlot(machineID, plot, x, y):
    plot[1].hist(y, 200, alpha=0.75)
    

def usage():
    print 'USAGE: python results.py <Path to CSV>'
        
if __name__ == "__main__":
	path = 'results.csv'
	if len(sys.argv) == 2:
		path = sys.argv[1]
	#else: usage()
	main(path)