import networkx as nx

"""
G = nx.Graph()
G.add_edge('A','i')
G.add_edge('B','i')
G.add_edge('B','j')
G.add_edge('B','k')
G.add_edge('C','i')
G.add_edge('C','j')
G.add_edge('C','l')
G.add_edge('D','j')
G.add_edge('D','l')
G.add_edge('E','k')
G.add_edge('E','l')

Gproj = nx.Graph()
for edge in G.edges():
	userNode = edge[0]
	businessNode = edge[1]
	for edge in G.edges(businessNode):
		if(edge[1]!=userNode):
			Gproj.add_edge(userNode,edge[1])
"""

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
		print "ERROR IN GRAPH"
	return userNode,businessNode

INTERNAL_LINKS_FILE = "waterlooIL.txt"

mainFile = ("waterlooTrain.txt")
projFile = ("waterlooProj.txt")
G = nx.read_edgelist(mainFile, delimiter=',', data=(('rating',int),('date',str)))
Gproj = nx.read_edgelist(projFile, delimiter=',')
print "## GRAPH CREATED ##"
print "## CREATING SET OF NODES ##"
userNodes = set()
businessNodes = set()
for edge in G.edges():
	u,b = getUserAndBusiness(edge)
	userNodes.add(u)
	businessNodes.add(b)
print "## CREATED SET OF NODES ##"

print "## FINDING INTERNAL LINKS ##"
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

print "## WRITING TO FILE ##"
internalFile = open(INTERNAL_LINKS_FILE, "w")
for link in internalLinks:
	internalFile.write(link[0]+","+link[1]+"\n")
internalFile.close()
					