"""
######################################################################################
RATING PREDICTION - This file predicts ratings based on predicted links and the 
projection graph.
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
PROJ_PATH = "../data/projection_graph/"
TRAIN_PATH = "../data/train/"
TEST_PATH = "../data/test/"
INTERNAL_PATH = "../data/internal_links/"
RATING_PREDICTED_PATH = "../data/rating_predicted/"
RATING_EVALUATED_PATH = "../data/rating_evaluated/"

"""
######################################################################################
	GLOBALS
######################################################################################
"""
Gproj = None
Gmain = None
Gtest = None
intersects = {}

"""
######################################################################################
	PUBLIC FUNCTIONS
######################################################################################
"""
def predictRatings(acronym,verbose):
	global Gproj, Gmain, Gtest
	Gproj = nx.read_edgelist(PROJ_PATH + acronym + "_proj.txt", delimiter=',')
	Gmain = nx.read_edgelist(TRAIN_PATH + acronym + "_train.txt", delimiter=',', data=(('rating',int),('date',str)))
	if(verbose): print "## %s - GRAPHS CREATED ##\n"%(acronym)
	
	if(verbose): print "## %s - CREATING INTERSECTION ##\n"%(acronym)
	computeIntersectionAndUnion()

	internalLinks = set()
	internalFile = open(INTERNAL_PATH + acronym + "_il.txt")
	for line in internalFile:
		edge = line.split(',')
		internalLinks.add((edge[0], edge[1].rstrip()))
	internalFile.close()

	if(verbose): print "## %s - PREDICTING RATINGS ##"%(acronym)
	ratingInternalLinks = []
	countX = 0
	totalX = len(internalLinks)
	print "Total=%d"%totalX
	for link in internalLinks:
		countX = countX + 1;
		if(countX%100 == 0):
			print "Completed %d"%countX
		user = link[0]
		business = link[1]
		neighbor_users = Gproj.neighbors(user)
		ratings = []
		for neighbor in neighbor_users:
			r = getRating(neighbor, business)
			if(r != 0):
				intersection = intersects[(user,neighbor)]
				total = 0
				for common in intersection:
					user1Rating = getRating(user, common)
					user2Rating = getRating(neighbor, common)
					diff = user1Rating - user2Rating
					total += diff
				weight = float(total)/len(intersection)
				ratings.append(r + weight)
		newRating = sum(ratings)/len(ratings)
		if(newRating > 5.0):
			newRating = 5.0
		if(newRating < 1.0):
			newRating = 1.0
		newRating = int(round(newRating))
		ratingInternalLinks.append((link[0],link[1],newRating))

	if(verbose): print "## %s - WRITING TO RATING PREDICTED FILE ##\n"%(acronym)
	predictedFile = open(RATING_PREDICTED_PATH + acronym + "_rating_predicted.txt", "w")
	for item in ratingInternalLinks:
		predictedFile.write(item[0]+ "," + item[1] + "," + str(item[2]) + "\n")
	predictedFile.close()
	
	Gtest = nx.read_edgelist(TEST_PATH + acronym + "_test.txt", delimiter=',', data=(('rating',int),('date',str)))
	testInternalLinks = set()
	for edge in Gtest.edges(): 
		u,b = getUserAndBusiness(edge)
		if (u, b) in internalLinks:
			testInternalLinks.add((u, b))
	
	diffRatings = {}
	diffRatings[0] = 0
	diffRatings[1] = 0
	diffRatings[2] = 0
	diffRatings[3] = 0
	diffRatings[4] = 0
	diffRatings[5] = 0
	for link in ratingInternalLinks:
		user = link[0]
		business = link[1]
		rating = link[2]
		if((user,business) in testInternalLinks):
			testRating = getTestRating(user,business)
			if(testRating == 0):
				print "ERROR"
				continue
			diff = abs(testRating - rating)
			diffRatings[diff] = diffRatings[diff] + 1
	
	if(verbose): print "## %s - WRITING TO RATING EVALUATED FILE ##\n"%(acronym)
	predictedFile = open(RATING_EVALUATED_PATH + acronym + "_rating_eval.txt", "w")
	for item in diffRatings:
		predictedFile.write(str(item)+ "," + str(diffRatings[item]) + "\n")
	predictedFile.close()

"""
######################################################################################
	HELPER FUNCTIONS
######################################################################################
"""
		
def getRating(user, business):
	try:
		return Gmain[user][business]['rating']
	except:
		return 0
		
def getTestRating(user, business):
	try:
		return Gtest[user][business]['rating']
	except:
		return 0
	
def computeIntersectionAndUnion():
	global Gproj, Gmain 
	global intersects
	for edge in Gproj.edges():
		user1, user2 = edge
		user1Bus = getBusinessNodes(user1)
		user2Bus = getBusinessNodes(user2)
		intersection = set.intersection(user1Bus, user2Bus)
		intersects[(user1, user2)] = intersection
		intersects[(user2, user1)] = intersection
		
def getBusinessNodes(user):
	userSet = set()
	for edge in Gmain.edges(user):
		u,b = getUserAndBusiness(edge)
		userSet.add(b)
	return userSet