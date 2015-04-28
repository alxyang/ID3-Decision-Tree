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
	total = float(0)
	# really only need indices 1,2,3 as those are the only labels
	for (features,label) in data:
		count[label] = count[label] + 1
		total = total + 1
	entropy = float(0)
	for c in count:
		if c == 0:
			continue
		prob = c / total
		entropy = entropy + prob * math.log(prob)
	entropy = entropy * -1
	return entropy

load("hw3train.txt", training_set)
load("hw3test.txt", test_set)

sort_test = sorted(training_set, key=lambda tup: tup[0][0])
print calc_entropy([(0,1),(0,2), (0,3)])