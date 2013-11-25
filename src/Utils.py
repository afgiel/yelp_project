"""
######################################################################################
UTILITIES - This file has global utilities
######################################################################################
"""

"""
######################################################################################
	IMPORTS
######################################################################################
"""
import networkx as nx

"""
######################################################################################
	CONSTANTS
######################################################################################
"""
SCHOOLS_FILE = "../data/global/schools.txt"
WEIGHTS_FILE = "../data/global/weights.txt"

"""
######################################################################################
	PUBLIC FUNCTIONS
######################################################################################
"""
def getSchools():
	acronyms = dict()
	schools = set()
	schoolFile = open(SCHOOLS_FILE)
	for line in schoolFile:
		s,a = line.split(',')
		s = s.rstrip()
		a = a.rstrip()
		acronyms[s] = a
		schools.add(s)
	schools = sorted(schools)
	return schools,acronyms
	
def getWeights():
	acronyms = dict()
	weights = set()
	weightFile = open(WEIGHTS_FILE)
	for line in weightFile:
		w,a = line.split(',')
		w = w.rstrip()
		a = a.rstrip()
		acronyms[w] = a
		weights.add(w)
	weights = sorted(weights)
	return weights,acronyms
	
def getUserAndBusiness(edge):
	userNode = "test"
	businessNode = "test"
	if(edge[0].startswith("uu")):
		userNode = edge[0]
	if(edge[0].startswith("bb")):
		businessNode = edge[0]
	if(edge[1].startswith("uu")):
		userNode = edge[1]
	if(edge[1].startswith("bb")):
		businessNode = edge[1]
	if(userNode == "test" or businessNode == "test"):
		print "## ERROR IN GRAPH!!! ##\n\n"
	return userNode,businessNode
	
def generateSmallGraph():
	G = nx.Graph()
	G.add_edge('uuA','bbi')
	G.add_edge('uuB','bbi')
	G.add_edge('uuB','bbj')
	G.add_edge('uuB','bbk')
	G.add_edge('uuC','bbi')
	G.add_edge('uuC','bbj')
	G.add_edge('uuC','bbl')
	G.add_edge('uuD','bbj')
	G.add_edge('uuD','bbl')
	G.add_edge('uuE','bbk')
	G.add_edge('uuE','bbl')
	return G