"""
######################################################################################
LINK PREDICTION - This file predicts links based on internal links, projection graph
for a given school.
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
PROJ_PATH = "../data/weighted_projection_graph/"
TRAIN_PATH = "../data/train/"
IL_PATH = "../data/internal_links/"
PREDICTED_PATH = "../data/predicted/"

"""
######################################################################################
	GLOBALS
######################################################################################
"""
Gproj = None

"""
######################################################################################
	PUBLIC FUNCTIONS
######################################################################################
"""
def predictLinks(acronym,verbose,weightThresh,totalThresh):
	weights,acronyms = getWeights()
	for weight in weights:
		predictLinksWeighted(acronym,acronyms[weight],verbose,weightThresh,totalThresh)
		
"""
######################################################################################
	HELPER FUNCTIONS
######################################################################################
"""
def predictLinksWeighted(acronym,acronymw,verbose,weightThresh,totalThresh):
	global Gproj
	Gproj = nx.read_edgelist(PROJ_PATH + acronym + "_" + acronymw + "_proj.txt", delimiter=',', data=(('rating',float),))
	Gmain = nx.read_edgelist(TRAIN_PATH + acronym + "_train.txt", delimiter=',', data=(('rating',int),('date',str)))
	if(verbose): print "## %s - Weight: %s - GRAPHS CREATED ##"%(acronym,acronymw)

	numOverThreshold = dict()
	internalLinks = open(IL_PATH + acronym + "_il.txt")
	nodes = Gmain.nodes()

	if(verbose): print "## %s - Weight: %s - CREATING SET OF NODES ##\n"%(acronym,acronymw)
	userNodes = set()
	businessNodes = set()
	for edge in Gmain.edges():
		u,b = getUserAndBusiness(edge)
		userNodes.add(u)
		businessNodes.add(b)
	if(verbose): print "## %s - Weight: %s - CREATED SET OF NODES ##\n"%(acronym,acronymw)

	if(verbose): print "## %s - Weight: %s - GENERATING POSSIBLE LINKS ##\n"%(acronym,acronymw)
	countX = 0
	#totalX = len(internalLinks)
	#print "Total=%d"%totalX
	for line in internalLinks:
		countX = countX + 1;
		if(countX%100 == 0):
			print "Completed %d"%countX
		internalLink = line.split(',')
		userNode = internalLink[0]
		businessNode = internalLink[1].rstrip()
		total = 0
		for edge in Gmain.edges(businessNode):
			if edge[1] != userNode:
				weight = getWeight(userNode, edge[1])
				if weight > weightThresh:
					total += 1
		numOverThreshold[(userNode, businessNode)] = total
	if(verbose): print "## %s - Weight: %s - GENERATED POSSIBLE LINKS ##\n"%(acronym,acronymw)

	if(verbose): print "## %s - Weight: %s - PREDICTING LINKS ##\n"%(acronym,acronymw)
	predicted = set()
	for key, value in numOverThreshold.items():
		if value >= totalThresh:
			predicted.add(key)

	if(verbose): print "## %s - Weight: %s - WRITING TO PREDICTED FILE ##\n"%(acronym,acronymw)
	predictedFile = open(PREDICTED_PATH + acronym + "_" + acronymw + "_predicted.txt", "w")
	for item in predicted:
		predictedFile.write(item[0]+ "," + item[1] + "\n")
	predictedFile.close()

def getWeight(user1, user2):
		return Gproj[user1][user2]['rating']