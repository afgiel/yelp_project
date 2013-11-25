"""
######################################################################################
INTERNAL LINKS - This file generates all possible internal links for a school
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
IL_PATH = "../data/internal_links/"

"""
######################################################################################
	PUBLIC FUNCTIONS
######################################################################################
"""
def generateInternalLinks(acronym,verbose):
	G = nx.read_edgelist(TRAIN_PATH + acronym + "_train.txt", delimiter=',', data=(('rating',int),('date',str)))
	Gproj = nx.read_edgelist(PROJ_PATH + acronym + "_proj.txt", delimiter=',')
	if(verbose): print "## %s - GRAPHS CREATED ##\n"%(acronym)
	
	if(verbose): print "## %s - CREATING SET OF NODES ##\n"%(acronym)
	userNodes = set()
	businessNodes = set()
	for edge in G.edges():
		u,b = getUserAndBusiness(edge)
		userNodes.add(u)
		businessNodes.add(b)
	if(verbose): print "## %s - CREATED SET OF NODES ##\n"%(acronym)

	if(verbose): print "## %s - FINDING INTERNAL LINKS ##"%(acronym)
	internalLinks = []
	count = 0
	total = len(userNodes)
	print "Total=%d"%total
	for userNode in userNodes:
		count = count + 1;
		if(count%100 == 0):
			print "Completed %d"%count
		for businessNode in businessNodes:
			if not G.has_edge(userNode,businessNode):
				internalLink = True
				for edge in G.edges(businessNode):
					u,b = getUserAndBusiness(edge)
					if not Gproj.has_edge(u,userNode):
						internalLink = False
						break
				if internalLink:
					internalLinks.append((userNode,businessNode))

	if(verbose): print "## %s - WRITING TO INTERNAL LINKS FILE ##\n"%(acronym)
	internalFile = open(IL_PATH + acronym + "_il.txt", "w")
	for link in internalLinks:
		internalFile.write(link[0]+","+link[1]+"\n")
	internalFile.close()
					