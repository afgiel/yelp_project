"""
######################################################################################
FIND THRESHOPLD - This file tests multiple thresholds for weights and writes them out
######################################################################################
"""

"""
######################################################################################
	IMPORTS
######################################################################################
"""
import networkx as nx
from Utils import getUserAndBusiness
from Utils import getWeights
from Evaluation import evaluate
from LinkPrediction import predictLinks

"""
######################################################################################
	CONSTANTS
######################################################################################
"""
PRECISION = "Precision"
RECALL = "Recall"
THRESHOLD_TRAINING_PATH = "../data/threshold_training/"
EVAL_PATH = "../data/evaluation/"

"""
######################################################################################
	PUBLIC FUNCTIONS
######################################################################################
"""
def findThresholds(acronym, verbose):
	tryThresholds(acronym, verbose)

		
"""
######################################################################################
	HELPER FUNCTIONS
######################################################################################
"""

def tryThresholds(acronym, verbose):
	precisionDict = dict()
	recallDict = dict()
	weightThresholds = [x*.1 for x in range(1, 30)]
	totalThresholds = [1, 2, 3]
	for weightThreshold in weightThresholds:
		for totalThreshold in totalThresholds:
			predictLinks(acronym,verbose,weightThreshold,1)
			evaluate(acronym,verbose)
			weights,acronyms = getWeights()
			for weight in weights:
				if acronyms[weight] not in precisionDict: precisionDict[acronyms[weight]] = dict()
				if acronyms[weight] not in recallDict: recallDict[acronyms[weight]] = dict()
				evalFile = open(EVAL_PATH + acronym + "_" + acronyms[weight] + "_eval.txt")
				for line in evalFile:
					stat, val = line.split(",")
					if stat == PRECISION:
						precisionDict[acronyms[weight]][(weightThreshold,totalThreshold)] = float(val)
					if stat == RECALL:
						recallDict[acronyms[weight]][(weightThreshold,totalThreshold)] = float(val)

	weights,acronyms = getWeights()
	for weight in weights:
		if(verbose): print "## %s - Weight: %s - WRITING TO THRESHOLD TRAINING FILE ##\n"%(acronym,acronyms[weight])
		thresholdTrain = open(THRESHOLD_TRAINING_PATH + acronym + "_" + acronyms[weight] + "_thresh_train.txt", "w")
		toWrite = ""
		for weightThreshold in weightThresholds:
			for totalThreshold in totalThresholds:
				thresholds = (weightThreshold, totalThreshold)
				precision = precisionDict[acronyms[weight]][thresholds]
				recall = recallDict[acronyms[weight]][thresholds]
				toWrite += str(thresholds[0]) + "," + str(thresholds[1]) + "," + str(precision) + "," + str(recall) + "\n"
		thresholdTrain.write(toWrite)




