import re
import numpy
import math
import random

training_set = []
test_set = []

def load(fn, ds):
	f = open(fn, "r")
	for line in f:
		tokens = line.split()
		features = []
		for i in range(0, len(tokens) - 1):
			features.append(float(tokens[i]))
		data = (features, int(tokens[len(tokens) - 1]))
		ds.append(data)

load("hw3train.txt", training_set)
load("hw3test.txt", test_set)

print training_set[0]