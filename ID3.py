import re
import numpy
import math
import random

training_set = []
test_set = []

class Node:
    def __init__(self,data):
        self.left = None
        self.right = None
        self.data = data
        self.threshold_indices = -1
        self.threshold = -1

    def setThresholdIndices(self, index):
    	self.threshold_indices = index
    def setThreshold(self, val):
    	self.threshold = val
    def setLeft(self, elem):
    	self.left = elem
    def setright(self, elem):
    	self.right = elem
    def getRight(self):
    	return self.right
    def getLeft(self):
    	return self.left
    def getData(self):
    	return self.data



def load(fn, ds):
	f = open(fn, "r")
	for line in f:
		tokens = line.split()
		features = []
		for i in range(0, len(tokens) - 1):
			features.append(float(tokens[i]))
		data = (features, int(tokens[len(tokens) - 1]))
		ds.append(data)

def calc_entropy(data):
	count = [0,0,0,0] 
	# really only need indices 1,2,3 as those are the only labels

load("hw3train.txt", training_set)
load("hw3test.txt", test_set)

sort_test = sorted(training_set, key=lambda tup: tup[0][0])
root = Node(training_set)
print root.getData()