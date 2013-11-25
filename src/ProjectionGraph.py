"""
######################################################################################
PROJECTION GRAPH - This file creates a projection graph
######################################################################################
"""

"""
######################################################################################
	IMPORTS
######################################################################################
"""
import networkx as nx
from Utils import getUserAndBusiness

"""
######################################################################################
	CONSTANTS
######################################################################################
"""
PROJ_PATH = "../data/projection_graph/"
TRAIN_PATH = "../data/train/"

"""
######################################################################################
	PUBLIC FUNCTIONS
######################################################################################
"""
def generateProjectionGraph(acronym,verbose):
	fileName = (TRAIN_PATH + acronym + "_train.txt")
	G = nx.read_edgelist(fileName, delimiter=',', data=(('rating',int),('date',str)))
	if(verbose): print "## %s - GRAPH CREATED ##\n"%(acronym)
	
	userNodes = set()
	businessNodes = set()
	for edge in G.edges():
		userNode, businessNode = getUserAndBusiness(edge)
		userNodes.add(userNode)
		businessNodes.add(businessNode)

	if(verbose): print "## %s - CREATING PROJECTION GRAPH ##\n"%(acronym)
	Gproj = nx.Graph()
	for edge in G.edges():
		userNode, businessNode = getUserAndBusiness(edge)
		for edge2 in G.edges(businessNode):
			u, b = getUserAndBusiness(edge2)
			if(u!=userNode):
				Gproj.add_edge(userNode,u)
	if(verbose): print "## %s - CREATED PROJECTION GRAPH ##\n"%(acronym)
		
	if(verbose): print "## %s - WRITING PROJECTION GRAPH TO FILE ##\n"%(acronym)
	projFile = open(PROJ_PATH + acronym + "_proj.txt", "w")
	for edge in Gproj.edges():
		projFile.write(edge[0]+","+edge[1]+"\n")
	projFile.close()