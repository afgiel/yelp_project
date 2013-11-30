"""
######################################################################################
TRAIN AND TEST DATA - This file splits a school into train and test data by a given
percentage.
######################################################################################
"""

"""
######################################################################################
	CONSTANTS
######################################################################################
"""
TRAIN_PATH = "../data/train/"
TEST_PATH = "../data/test/"
VAL_PATH = "../data/crossval/"
EDGE_PATH = "../data/edge/"

"""
######################################################################################
	PUBLIC FUNCTIONS
######################################################################################
"""
def generateTrainAndTest(acronym,percentTrain,percentVal,percentTest,verbose):
	reviews = list()
	edgeFile = open(EDGE_PATH + acronym + "_edges.txt")
	for line in edgeFile:
		line = line.split(",")
		reviews.append(tuple(line))
	reviews = sorted(reviews, key=lambda item: item[3])
	if(percentVal > 0.0):
		if(verbose): print "## %s - SPLITTING TRAIN, VALIDATION AND TEST DATA ##\n"%(acronym)
		total = len(reviews)
		splitPoint = int(total*percentTrain)
		train = reviews[:splitPoint]
		testNVal = reviews[splitPoint:]
		if(verbose): print "%s - Train - Split on Date: %s" %(acronym,reviews[splitPoint][3])
		total = len(testNVal)
		splitPoint = int(total*(percentVal)/(percentVal + percentTest))
		validation = testNVal[:splitPoint]
		test = testNVal[splitPoint:]
		if(verbose): print "%s - Validation - Split on Date: %s" %(acronym,testNVal[splitPoint][3])
		if(verbose): print "## %s - WRITING VALIDATION DATA TO FILE ##\n"%(acronym)
		toWrite = open(VAL_PATH + acronym + "_val.txt", "w")
		for line in validation: 
			toAdd = ",".join(line)
			toWrite.write(toAdd)
		toWrite.close()
	else:
		if(verbose): print "## %s - SPLITTING TRAIN AND TEST DATA ##\n"%(acronym)
		total = len(reviews)
		splitPoint = int(total*percentTrain)
		train = reviews[:splitPoint]
		test = reviews[splitPoint:]
		if(verbose): print "%s - Split on Date: %s" %(acronym,reviews[splitPoint][3])
	if(verbose): print "## %s - WRITING TRAIN DATA TO FILE ##\n"%(acronym)
	toWrite = open(TRAIN_PATH + acronym + "_train.txt", "w")
	for line in train: 
		toAdd = ",".join(line)
		toWrite.write(toAdd)
	toWrite.close()
	if(verbose): print "## %s - WRITING TEST DATA TO FILE ##\n"%(acronym)
	toWrite = open(TEST_PATH + acronym + "_test.txt", "w")
	for line in test: 
		toAdd = ",".join(line)
		toWrite.write(toAdd)
	toWrite.close()



