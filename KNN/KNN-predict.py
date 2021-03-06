import ConfigParser
import requests
import json
from datetime import datetime, timedelta
import numpy as np
from operator import itemgetter
import time 

#parameters
instr = "EUR_USD"
base_units = 1000
historyX = [] #dimension: 49510x48
historyY = [] #dimension: 49510

testX = []
testY = []

kval = 9 

def getHistoryNodes():
    # get history data from file
    # 50 candle prices in one node (25min), 1000 nodes in history(17day)
    with open("history-overlap-49510-nodes-2016dec.txt", "r") as f:
        next(f) #skip first line ( time )
        for line in f: #49510 lines
            data = line.split()
            node = []
            for number in data: #49 numbers
                node.append(float(number))
            historyX.append(node[0:-1])
            historyY.append(node[-1])

def getTestingNodes():
    # get history data from file
    # 50 candle prices in one node (25min), 1000 nodes in history(17day)
    with open("history-overlap-49510-nodes-2017jan.txt", "r") as f:
    #with open("history-overlap-49510-nodes-2016dec.txt", "r") as f:
        print "Use Different Data"
        next(f) #skip first line ( time )
        for line in f: #49510 lines
            data = line.split()
            node = []
            for number in data: #49 numbers
                node.append(float(number))
            testX.append(node[0:-1])
            testY.append(node[-1])

def distance( node1, node2 ):
    euclidean = np.linalg.norm( np.array(node1)[0:-1] - np.array(node2)[0:-1] ) #-1: drop the last element of one node
    return euclidean

def predictChange():
    # use KNN-like mmethod to predict if the price will rise/drop
    # use data 2016dec(49510nodes, 49 nums/node), to predict data 2017jan
    # Y = { True(rise), False(drop) }
    correct = 0
    error = 0
    
    testLength = len(testY)
    historyLength = len(historyY)

    numTestNodes = 10
    print "number of Testing Nodes: ", numTestNodes
    
    #for t in range(testLength):
    for t in range(numTestNodes):
        # calculate the distance between history-nodes and current-node
        # choose the k closest nodes to vote
        distances = []
        for h in range(historyLength):
            distances.append( ( h, distance(testX[t], historyX[h]) ) )
            #(index, distance)
        distances.sort(key=itemgetter(1)) #sort by distance

        rise = 0
        drop = 0
        # Vote for the answer by k neighbors
        for neighbor in distances[0:kval]:
            if( historyY[ neighbor[0] ] > 0 ):
                rise = rise + 1
            else:
                drop = drop + 1
        predict = (rise > drop) # True=>rise, False=>drop

        #check if predicted y == real testing y?
        if predict == (testY[t] > 0):
            correct = correct + 1
            #print "correct, ", predict
        else:
            error = error + 1
            #print "error, ", predict
    
    print "Correct Prediction: ", correct
    print "Error Prediction: ", error
    print "Correctness: ", correct / float(correct+error)
    

if __name__ == "__main__":
    print "K = ", kval
    getHistoryNodes()
    getTestingNodes()
    print "Prepare for Data...finished"

    predictChange()

    #getCurNode()
