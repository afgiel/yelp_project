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
"""

PROJ_FILE = "stanfordProjectionTrainEdges.txt"

fileName = ("stanfordTrain.txt")
G = nx.read_edgelist(fileName, delimiter=',', data=(('rating',int),('date',str)))
print "## GRAPH CREATED ##"

print "## CREATING PROJECTION GRAPH ##"
Gproj = nx.Graph()
for edge in G.edges():
	userNode = edge[0]
	businessNode = edge[1]
	for edge in G.edges(businessNode):
		if(edge[1]!=userNode):
			Gproj.add_edge(userNode,edge[1])
print "## CREATED PROJECTION GRAPH ##"

print "## WRITING TO FILE ##"
projFile = open(PROJ_FILE, "w")
for edge in Gproj.edges():
	projFile.write(edge[0]+","+edge[1]+"\n")
projFile.close()
					