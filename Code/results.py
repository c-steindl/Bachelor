import sys
import csv
import time
import os
import numpy as np
import matplotlib.pyplot as plt

def main(path, file, type):
    currentTest = None
    currentID = None
    ID = 0
    testID = -1
    plots = []
    xValues = []
    yValues = []
    zValues = []
    currentPlot = None
    
    
    with open(path + '/' + file, 'rb') as f:
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
                    if type == 'normal' or type == 'sum':
                        fig = plt.figure()
                        currentPlot = [fig, fig.add_subplot(111), currentTest]
                        currentPlot[1].set_xlabel('Iterations')
                        currentPlot[1].set_ylabel('Time [s]')
                        currentPlot[1].set_title(currentTest)
                        
                        plots.insert(testID, currentPlot)
                    elif type == 'both':
                        fig = plt.figure()
                        currentPlot = [fig, fig.add_subplot(211), currentTest]
                        currentPlot[1].set_xlabel('Iterations')
                        currentPlot[1].set_ylabel('Time [s]')
                        currentPlot[1].set_title(currentTest)
                        
                        currentPlot1 = [fig, fig.add_subplot(212), currentTest]
                        currentPlot1[1].set_xlabel('Iterations')
                        currentPlot1[1].set_ylabel('Time [s]')
                        currentPlot1[1].set_title(currentTest + '_Sum')
                        
                        plots.insert(testID, currentPlot)
            elif r[0] == 'EndTest':
                if ((len(xValues) > 0) and (len(yValues) > 0) and (len(zValues) > 0)):
                    if type == 'normal':
                        addPlot (currentID, currentPlot, xValues, yValues)
                    elif type == 'sum':
                        addPlot (currentID, currentPlot, xValues, zValues)
                    elif type == 'both':
                        addPlot (currentID, currentPlot, xValues, yValues)
                        addPlot (currentID, currentPlot1, xValues, zValues)
                xValues = []
                yValues = []
                zValues = []
            elif r[0] == 'finish':
                time.sleep(2)
            else:
                xValues.append(float(r[0]))
                yValues.append(float(r[1]))
                zValues.append(float(r[2]))
        
        i = 0
        figPath = path + '/' + type + '/'
        os.mkdir(figPath)
        for p in plots:
            currentPlot = p
            fig = p[0]
            fig.savefig(figPath + str(i) + '_' + p[2], dpi=200, orientation='landscape')
            i = i + 1
        plt.legend()
        #plt.show()

def addPlot(machineID, plot, x, y):
    plot[1].plot(x, y, 'o', label=machineID)
    plot[1].legend()
    

def usage():
    print 'USAGE: python results.py <Path to CSV, Filename, Type (normal/sum/both)>'
        
if __name__ == "__main__":
    if len(sys.argv) == 4:
        path = sys.argv[1]
        file = sys.argv[2]
        type = sys.argv[3]
    else: usage()
    main(path, file, path)