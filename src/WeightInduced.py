"""
######################################################################################
WEIGHTED INDUCED - This file creates a projection graph with each of the weight induced
ratings.
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
WEIGHT_PATH = "../data/weighted_projection_graph/"

"""
######################################################################################
	GLOBALS
######################################################################################
"""
Gproj = None
Gmain = None
intersects = dict()
unions = dict()

"""
######################################################################################
	PUBLIC FUNCTIONS
######################################################################################
"""
def generateWeightedProjectionGraph(acronym,verbose):
	global Gproj,Gmain
	Gproj = nx.read_edgelist(PROJ_PATH + acronym + "_proj.txt", delimiter=',')
	Gmain = nx.read_edgelist(TRAIN_PATH + acronym + "_train.txt", delimiter=',', data=(('rating',int),('date',str)))
	if(verbose): print "## %s - GRAPHS CREATED ##\n"%(acronym)

	weights,acronyms = getWeights()

	if(verbose): print "## %s - CREATING SET OF NODES ##\n"%(acronym)
	userNodes = set()
	businessNodes = set()
	for edge in Gmain.edges():
		u,b = getUserAndBusiness(edge)
		userNodes.add(u)
		businessNodes.add(b)
	if(verbose): print "## %s - CREATED SET OF NODES ##\n"%(acronym)

	if(verbose): print "## %s - COMPUTING INTERSECTION ##\n"%(acronym)
	computeIntersectionAndUnion()

	for weight in weights:
		if(verbose): print "## %s - COMPUTING %s ##\n"%(acronym,weight)
		if(weight == "SUM WEIGHT"): ratings = createSumWeight()
		if(weight == "JACCARD WEIGHT"): ratings = createJaccardWeight()
		if(weight == "DELTA WEIGHT"): ratings = createDeltaWeight()
		if(weight == "RATING SUM WEIGHT"): ratings = createRatingSumWeight()
		if(weight == "RATING JACCARD WEIGHT"): ratings = createRatingJaccardWeight()
		if(weight == "RATING DELTA WEIGHT"): ratings = createRatingDeltaWeight()
		if(weight == "RATING LEAST SQUARE WEIGHT"): ratings = createRatingLeastSquareWeight()
		if(verbose): print "## %s - WRITING %s ##\n"%(acronym,weight)
		writeToFile(WEIGHT_PATH + acronym + "_" + acronyms[weight] + "_proj.txt",ratings)
		
"""
######################################################################################
	HELPER FUNCTIONS
######################################################################################
"""
def createSumWeight():
	weights = dict()
	for edge in Gproj.edges():
		weights[(edge[0],edge[1])] = len(intersects[(edge[0],edge[1])])
	return weights

def createJaccardWeight():
	weights = dict()
	for edge in Gproj.edges():
		weights[(edge[0],edge[1])] = float(len(intersects[(edge[0],edge[1])]))/float(len(unions[(edge[0], edge[1])]))
	return weights

def createDeltaWeight():
	weights = dict()
	for edge in Gproj.edges():
		intersection = intersects[(edge[0],edge[1])]
		total = 0.0
		for business in intersection:
			degree = len(Gmain.edges(business))
			total += 2.0/(degree * degree-1)
		weights[(edge[0], edge[1])] = total
	return weights	

def getRating(user, business):
	return Gmain[user][business]['rating']

def createRatingSumWeight():
	weights = dict()
	for edge in Gproj.edges():
		total = 0.0
		intersection = intersects[(edge[0],edge[1])]
		for common in intersection:
			user1Rating = getRating(edge[0], common)
			user2Rating = getRating(edge[1], common)
			diff = abs(user1Rating - user2Rating)
			toAdd = float(5-diff)/5
			total += toAdd
		weights[(edge[0],edge[1])] = total
	return weights

def createRatingJaccardWeight():
	weights = dict()
	for edge in Gproj.edges():
		total = 0.0
		intersection = intersects[(edge[0],edge[1])]
		for common in intersection:
			user1Rating = getRating(edge[0], common)
			user2Rating = getRating(edge[1], common)
			diff = abs(user1Rating - user2Rating)
			toAdd = float(5-diff)/5
			total += toAdd
		total = total/len(unions[(edge[0], edge[1])])
		weights[(edge[0],edge[1])] = total
	return weights

def createRatingDeltaWeight():
	weights = dict()
	for edge in Gproj.edges():
		intersection = intersects[(edge[0],edge[1])]
		total = 0.0
		for business in intersection:
			degree = len(Gmain.edges(business))
			base = 2.0/(degree * degree-1)
			user1Rating = getRating(edge[0], business)
			user2Rating = getRating(edge[1], business)
			diff = abs(user1Rating - user2Rating)
			scale = float(5-diff)/5
			total += base*scale
		weights[(edge[0], edge[1])] = total
	return weights	

def createRatingLeastSquareWeight():
	weights = dict()
	for edge in Gproj.edges():
		total = 0.0
		intersection = intersects[(edge[0],edge[1])]
		for common in intersection:
			user1Rating = getRating(edge[0], common)
			user2Rating = getRating(edge[1], common)
			diff = abs(user1Rating - user2Rating)
			toAdd = float(5-diff)/5
			total += pow(toAdd, 2)
		weights[(edge[0],edge[1])] = total
	return weights

def getBusinessNodes(user):
	userSet = set()
	for edge in Gmain.edges(user):
		u,b = getUserAndBusiness(edge)
		userSet.add(b)
	return userSet

def writeToFile(name,weights):
	weightsFile = open(name,'w')
	for edge in Gproj.edges():
		weightsFile.write(edge[0]+","+edge[1]+","+str(weights[(edge[0],edge[1])]) + "\n")
	weightsFile.close()

def computeIntersectionAndUnion():
	global Gproj, Gmain 
	global intersects
	global unions
	for edge in Gproj.edges():
		user1, user2 = edge
		user1Bus = getBusinessNodes(user1)
		user2Bus = getBusinessNodes(user2)
		intersection = set.intersection(user1Bus, user2Bus)
		union = set.union(user1Bus, user2Bus)
		intersects[(user1, user2)] = intersection
		intersects[(user2, user1)] = intersection
		unions[(user1, user2)] = union
		unions[(user2, user1)] = union
