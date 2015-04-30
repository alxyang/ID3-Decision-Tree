import re
import numpy
import math
import random


class Node:

    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data
        self.threshold_indices = -1
        self.threshold = -1
        self.leaf = True
        self.pure = True
        self.label = -1
        if len(data) > 1:
        	label = data[0][1]
        	for i in range(1, len(data)):
        		if label != data[i][1]:
        			self.pure = False
        if self.pure:
        	self.label = data[0][1]

    def setThresholdIndices(self, index):
    	self.threshold_indices = index

    def setThreshold(self, val):
    	self.threshold = val

    def setLeft(self, elem):
    	self.leaf = False
    	self.left = elem

    def setRight(self, elem):
    	self.leaf = False
    	self.right = elem

    def getThreshold(self):
    	return self.threshold

    def getThresholdIndices(self):
    	return self.threshold_indices

    def getRight(self):
    	return self.right

    def getLeft(self):
    	return self.left

    def getData(self):
    	return self.data

    def getLabel(self):
    	return self.label

    def isLeaf(self):
    	return self.leaf

    def isPure(self):
    	return self.pure

    def getLabelOrThreshold(self):
        if (not self.pure):
            return "threshold: " + str(self.threshold)
        if (self.pure):
            return "label: " + str(self.label)


def load_data(filename):
    data_matrix = []
    f = open(filename, "r")
    for line in f:
		tokens = line.split()
		features = []
		for i in range(0, len(tokens) - 1):
			features.append(float(tokens[i]))
		data = (features, int(tokens[len(tokens) - 1]))
		data_matrix.append(data)
    return data_matrix


# calculates the entropy, given that there are only 3 valid labelings 1,2,3
def calc_entropy(data):
	count = [0,0,0,0]
	total = float(0)
	# really only need indices 1,2,3 as those are the only labels
	for (features, label) in data:
		count[label] = count[label] + 1
		total = total + 1
	entropy = float(0)
	for c in count:
		if c == 0:
			continue
		prob = c / total
		entropy = entropy - prob * math.log(prob)
	return entropy


# split the data into a left(true branch) and right(false branch) given a dataset, threshold, and feature index
def split(dataset, threshold, feature_index):
	left = []
	right = []
	for datapoint in dataset:
		if datapoint[0][feature_index] <= threshold:
			left.append(datapoint)
		else:
			right.append(datapoint)
	return (left,right)

#whats the lowest entropy and threshold I can get given a dataset and a specific feature index
def calc_lowest_entropy(dataset, feature_index):
	sort = sorted(dataset, key=lambda tup: tup[0][feature_index])
	best_entropy = float('inf')
	best_thres = float('inf')
	curr_entropy = float('inf')
	curr_thres = float('inf')

	for i in range(0, len(dataset)):
		if curr_thres == dataset[i][0][feature_index]:
			continue
		curr_thres = dataset[i][0][feature_index]
		(left,right) = split(dataset, curr_thres, feature_index)
		curr_entropy = calc_entropy(left) * float(len(left))/float(len(dataset)) + calc_entropy(right) * float(len(right))/float(len(dataset))
		if curr_entropy < best_entropy:
			best_entropy = curr_entropy
			best_thres = curr_thres
	return (best_entropy, best_thres)


#I want to know what the threshold, and feature index to split by given a dataset
def calc_threshold(dataset):
	best_feature_index = -1
	best_entropy = float('inf')
	best_threshold = float('inf')

	for i in range(0, len(dataset[0][0])):
		(entropy, thres) = calc_lowest_entropy(dataset, i)
		if entropy < best_entropy:
			best_entropy = entropy
			best_feature_index = i
			best_threshold = thres

	return (best_entropy, best_threshold, best_feature_index)

def find_impure_leaf(node):
	if node is None:
		return None
	if not(node.isPure()) and node.isLeaf():
		return node

	lefty = find_impure_leaf(node.getLeft())
	if not(lefty is None):
		return lefty

	righty = find_impure_leaf(node.getRight())
	if not(righty is None):
		return righty

	return None


def ID3(root):

	curr_node = find_impure_leaf(root)
	while not(curr_node is None):
		(entropy, threshold, feature_index) = calc_threshold(curr_node.getData())
		(left, right) = split(curr_node.getData(), threshold, feature_index)

		curr_node.setThreshold(threshold)
		curr_node.setThresholdIndices(feature_index)

		left_node = Node(left)
		right_node = Node(right)
		curr_node.setLeft(left_node)
		curr_node.setRight(right_node)
		curr_node = find_impure_leaf(root)

def calc_error(dataset, root):
	errors = 0
	num_samples = len(dataset)
	for (features, label) in dataset:
		curr_node = root
		while not(curr_node.isPure()):
			threshold = curr_node.getThreshold()
			feature_index = curr_node.getThresholdIndices()
			if features[feature_index] <= threshold:
				curr_node = curr_node.getLeft()
			else:
				curr_node = curr_node.getRight()
		if not(label == curr_node.getLabel()):
			errors = errors + 1
	return float(errors) / float(num_samples)

def print_tree(root):
      thislevel = [root]
      while thislevel:
        nextlevel = list()
        for n in thislevel:
          print n.getLabelOrThreshold(), "training points: " + str(len(n.getData()))
          if n.getLeft():
              nextlevel.append(n.getLeft())
          if n.getRight():
              nextlevel.append(n.getRight())
        print
        thislevel = nextlevel


def main():
    training_set = load_data("hw3train.txt")
    test_set = load_data("hw3test.txt")
    debug_set = load_data("test.txt")
    sort_test = sorted(training_set, key=lambda tup: tup[0][2]) #can you explain how this works?
    root = Node(training_set)
    ID3(root)
    print calc_error(training_set, root)
    print calc_error(test_set, root)
    print_tree(root)


if __name__ == '__main__':
    main()
