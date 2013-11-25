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
EDGE_PATH = "../data/edge/"

"""
######################################################################################
	PUBLIC FUNCTIONS
######################################################################################
"""
def generateTrainAndTest(acronym,percent,verbose):
	if(verbose): print "## %s - SPLITTING TRAIN AND TEST DATA ##\n"%(acronym)
	reviews = list()
	edgeFile = open(EDGE_PATH + acronym + "_edges.txt")
	for line in edgeFile:
		line = line.split(",")
		reviews.append(tuple(line))
	reviews = sorted(reviews, key=lambda item: item[3])
	total = len(reviews)
	splitPoint = int(total*percent)
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
	for line in train: 
		toAdd = ",".join(line)
		toWrite.write(toAdd)
	toWrite.close()



