"""
######################################################################################
EVALUATION - This file evaluates the predicted links using the test set
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

"""
######################################################################################
	CONSTANTS
######################################################################################
"""
PREDICTED_PATH = "../data/predicted/"
TEST_PATH = "../data/test/"
TRAIN_PATH = "../data/train/"
EVAL_PATH = "../data/evaluation/"
INTERNAL_LINKS_PATH = "../data/internal_links/"

"""
######################################################################################
	PUBLIC FUNCTIONS
######################################################################################
"""
def evaluate(acronym,verbose):
	weights,acronyms = getWeights()
	for weight in weights:
		evaluateWeighted(acronym,acronyms[weight],verbose)
		
"""
######################################################################################
	HELPER FUNCTIONS
######################################################################################
"""
def evaluateWeighted(acronym,acronymw,verbose):
	if(verbose): print "## %s - Weight: %s - CREATING PREDICTED, TRAIN & TEST SETS ##\n"%(acronym,acronymw)
	Gtest = nx.read_edgelist(TEST_PATH + acronym + "_test.txt", delimiter=',', data=(('rating',int),('date',str)))
	Gtrain = nx.read_edgelist(TRAIN_PATH + acronym + "_train.txt", delimiter=',', data=(('rating',int),('date',str)))
	
	predictedLinks = set()
	predictedFile = open(PREDICTED_PATH + acronym + "_" + acronymw + "_predicted.txt")
	for line in predictedFile:
		edge = line.split(',')
		predictedLinks.add((edge[0], edge[1].rstrip()))
	
	if(verbose): print "## %s - Weight: %s - GENERATING TOTAL NUMBER OF USERS AND BUSINESSES ##\n"%(acronym,acronymw)
	trainUsers = set()
	trainBusinesses = set()
	for edge in Gtrain.edges():
		u,b = getUserAndBusiness(edge)
		trainUsers.add(u)
		trainBusinesses.add(b)
	
	testUsers = set()
	testBusinesses = set()
	for edge in Gtest.edges():
		u,b = getUserAndBusiness(edge)
		testUsers.add(u)
		testBusinesses.add(b)
	
	predictedUsers = set()
	predictedBusinesses = set()
	for edge in predictedLinks:
		u,b = getUserAndBusiness(edge)
		predictedUsers.add(u)
		predictedBusinesses.add(b)
	
	if(verbose): print "## %s - Weight: %s - GENERATING OVERLAPPING NUMBER OF USERS AND BUSINESSES ##\n"%(acronym,acronymw)
	numTrainUsersInTest = 0
	for user in trainUsers:
		if(user in testUsers):
			numTrainUsersInTest = numTrainUsersInTest + 1
	
	numTrainBusinessesInTest = 0
	for business in predictedBusinesses:
		if(business in trainBusinesses):
			numTrainBusinessesInTest = numTrainBusinessesInTest + 1
		
	numPredictedUsersInTrain = 0
	for user in predictedUsers:
		if(user in trainUsers):
			numPredictedUsersInTrain = numPredictedUsersInTrain + 1
	
	numPredictedBusinessesInTrain = 0
	for business in predictedBusinesses:
		if(business in trainBusinesses):
			numPredictedBusinessesInTrain = numPredictedBusinessesInTrain + 1
	
	numPredictedUsersInTest = 0
	for user in predictedUsers:
		if(user in testUsers):
			numPredictedUsersInTest = numPredictedUsersInTest + 1
	
	numPredictedBusinessesInTest = 0
	for business in predictedBusinesses:
		if(business in testBusinesses):
			numPredictedBusinessesInTest = numPredictedBusinessesInTest + 1
	
	if(verbose): print "## %s - Weight: %s - GENERATING EDGE DATA ##\n"%(acronym,acronymw)
	numPredictedInTest = 0
	numPredictedNotInTest = 0
	#for edge in predictedLinks:
	#	if(Gtest.has_edge(edge[0],edge[1])):
	#		numPredictedInTest = numPredictedInTest + 1
	#	else:
	#		numPredictedNotInTest = numPredictedNotInTest + 1
			
	numTestInPredicted = 0
	numTestNotInPredicted = 0
	#for edge in Gtest.edges():
	#	u,b = getUserAndBusiness(edge)
	#	found = False
	#	for link in predictedLinks:
	#		if(link[0] == u and link[1] == b):
	#			Found = 1
	#			break
	#	if(found):
	#		numTestInPredicted = numTestInPredicted + 1
	#	else:
	#		numTestNotInPredicted = numTestNotInPredicted + 1
			
	numTestInTrain = 0
	numTestNotInTrain = 0
	#for edge in Gtest.edges():
	#	if(Gtrain.has_edge(edge[0],edge[1])):
	#		numTestInTrain = numTestInTrain + 1
	#	else:
	#		numTestNotInTrain = numTestNotInTrain + 1
	
	if(verbose): print "## %s - Weight: %s - CALCULATING PRECISION AND RECALL ##\n"%(acronym,acronymw)
	allInternalLinks = set()
	internalLinksFile = open(INTERNAL_LINKS_PATH + acronym + "_il.txt")
	for line in internalLinksFile:
		edge = line.split(',')
		allInternalLinks.add((edge[0], edge[1].rstrip()))
	testInternalLinks = set()
	for edge in Gtest.edges(): 
		u,b = getUserAndBusiness(edge)
		if (u, b) in allInternalLinks:
			testInternalLinks.add((u, b))

	if len(predictedLinks) == 0: 
		precision = -1.0
	else:
		precision = float(len(testInternalLinks & predictedLinks))/len(predictedLinks)
	if len(testInternalLinks) == 0:
		recall = -1.0
	else:
		recall = float(len(testInternalLinks & predictedLinks))/len(testInternalLinks)

	if(verbose): print "## %s - Weight: %s - WRITING TO EVALUATION FILE ##\n"%(acronym,acronymw)
	toWrite = "Num Predicted Edges," + str(len(predictedLinks)) + "\n"
	toWrite = toWrite + "Num Predicted Edges In Test," + str(numPredictedInTest) + "\n"
	toWrite = toWrite + "Num Predicted Edges Not In Test," + str(numPredictedNotInTest) + "\n"
	toWrite = toWrite + "Num Test Edges In Predicted," + str(numTestInPredicted) + "\n"
	toWrite = toWrite + "Num Test Edges Not In Predicted," + str(numTestNotInPredicted) + "\n"
	toWrite = toWrite + "Num Test Edges In Train," + str(numTestInTrain) + "\n"
	toWrite = toWrite + "Num Test Edges Not In Train," + str(numTestNotInTrain) + "\n"
	toWrite = toWrite + "Num Train Users," + str(len(trainUsers)) + "\n"
	toWrite = toWrite + "Num Test Users," + str(len(testUsers)) + "\n"
	toWrite = toWrite + "Num Predicted Users," + str(len(predictedUsers)) + "\n"
	toWrite = toWrite + "Num Train Businesses," + str(len(trainBusinesses)) + "\n"
	toWrite = toWrite + "Num Test Businesses," + str(len(testBusinesses)) + "\n"
	toWrite = toWrite + "Num Predicted Businesses," + str(len(predictedBusinesses)) + "\n"
	toWrite = toWrite + "Num Train Users In Test," + str(numTrainUsersInTest) + "\n"
	toWrite = toWrite + "Num Train Businesses In Test," + str(numTrainBusinessesInTest) + "\n"
	toWrite = toWrite + "Num Predicted Users In Train," + str(numPredictedUsersInTrain) + "\n"
	toWrite = toWrite + "Num Predicted Businesses In Train," + str(numPredictedBusinessesInTrain) + "\n"
	toWrite = toWrite + "Num Predicted Users In Test," + str(numPredictedUsersInTest) + "\n"
	toWrite = toWrite + "Num Predicted Businesses In Test," + str(numPredictedBusinessesInTest) + "\n"
	toWrite = toWrite + "Num Test Internal Edges," + str(len(testInternalLinks)) + "\n"
	toWrite = toWrite + "Num Actual Predicted Internal Edges," + str(len(testInternalLinks & predictedLinks)) + "\n"
	toWrite = toWrite + "Precision," + str(precision) + "\n"
	toWrite = toWrite + "Recall," + str(recall) + "\n"

	evalFile = open(EVAL_PATH + acronym + "_" + acronymw + "_eval.txt",'w')
	evalFile.write(toWrite)
	evalFile.close()