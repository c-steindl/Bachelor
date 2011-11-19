"""
    Author: Christoph Steindl
    E-Mail: a0706052@unet.univie.ac.at
"""

import sys
import csv
import time
import numpy as np
import matplotlib.pyplot as plt

"""
    Method to create plots out of collected data. This script is called by the class
    "Host".
"""
def main(p, f, type):
    print 'Parameters:', p, f, type
    currentTest = None
    currentID = None
    ID = 0
    testID = -1
    plots = []
    xValues = []
    yValues = []
    currentPlot = None
    path = str(p) + '/' + str(f)
    
    # Opens the file "result.csv"
    with open(path, 'rb') as f:
        reader = csv.reader(f)
        
        # Reads each line and decides what to do.
        for r in reader:
            #print r
            
            # No data --> pass
            if len(r) == 0 or r[0] == '' or r[0] == '\n':
                pass
            # "NewTest" --> either create a whole new list with test-values or add 
            # a data-line of another "Client" to an existing list.
            elif r[0] == 'NewTest':
                currentTest = r[1]
                testID = testID + 1
                if currentID != r[2]:
                    ID = ID + 1
                    testID = 0
                currentID = r [2]
                if len(plots) >= (testID + 1):
                    currentPlot = plots[testID]
                else:
                    # Create new plot and set title of the axis.
                    fig = plt.figure()
                    if type == 'hist':
                        plt.xlabel('Time [s]')
                        plt.ylabel('Frequency of occurrence')
                    else:
                        plt.xlabel('Iterations')
                        plt.ylabel('Time [s]')
                    plt.legend()
                    currentPlot = [fig, fig.add_subplot(111), currentTest]
                    plots.insert(testID, currentPlot)
            elif r[0] == 'EndTest':
                if ((len(xValues) > 0) and (len(yValues) > 0)):
                    # Add data-line to the right plot
                    addPlot (currentID, currentPlot, xValues, yValues, p, type)
                xValues = []
                yValues = []
            elif r[0] == 'finish':
                time.sleep(2)
            else:
                # Gets the values and saves them.
                xValues.append(float(r[0]))
                yValues.append(float(r[1]))
        
        if type != 'stats':
            # Shows and saves all plots.
            for pl in plots:
                currentPlot = pl
                fig = pl[0]
                fig.suptitle(pl[2] + ' (' + type + ')', fontsize=12)
                fig.savefig(p + '/' + type + '_' + pl[2])
            plt.legend()
            plt.show()

# Adds data-line to plot and respects the type of the plot.
def addPlot(machineID, plot, x, y, p, type):
    if type == 'scatter':
        print 'yes'
        # Scatter plot of all single values.
        plot[1].plot(x, y, 'o', label=machineID)
    elif type == 'sum':
        # Cumulative scatter plot of all values.
        i = 0
        sum = 0
        currentY = y
        while i < len(currentY):
            sum = sum + currentY[i]
            currentY[i] = sum
            i = i + 1
        plot[1].plot(x, currentY, 'o', label=machineID)
    elif type == 'stats':
        # No plot is generated. Only a file with some statistical data.
        stats = csv.writer(open(p + '/stats.csv', 'a'))
        stats.writerow(['start', plot[2], str(machineID)])
        stats.writerow(['Mean-Value', str(np.mean(y))])
        stats.writerow(['Variance', str(np.var(y))])
        stats.writerow(['Std_Variation', str(np.sqrt(np.var(y)))])
        stats.writerow(['Maximum', str(np.max(y))])
        stats.writerow(['Minimum', str(np.min(y))])
        stats.writerow(['Sum', str(np.sum(y))])
        stats.writerow(['end', str(machineID)])
        stats.writerow('')
    elif type == 'hist':
        # Histogram plot of all single values.
        plot[1].hist(y, 100, alpha=0.75)
    elif type == 'scatter90':
        # Scatter plot of the values between 1.05*min and 0.95*max.
        currentY = y
        lowerBound = 1.05 * np.min(y)
        upperBound = 0.95 * np.max(y)
        
        i = 0
        while i < len(currentY):
            if currentY[i] < lowerBound or currentY[i] > upperBound:
                currentY[i] = None
            i = i + 1
        plot[1].plot(x, currentY, 'o', label=machineID)
        
    
# Prints the usage information. 
def usage():
    print 'USAGE: python results.py <Path to CSV> <Filename> <Type of plot (scatter, sum, stats, hist, scatter90)>'
        
if __name__ == "__main__":
    path = 'results.csv'
    if len(sys.argv) == 4:
        path = str(sys.argv[1])
        file = str(sys.argv[2])
        type = str(sys.argv[3])
        main(path, file, type)
    else: usage()