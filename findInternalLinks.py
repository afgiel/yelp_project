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

INTERNAL_LINKS_FILE = "internalLinks.txt"

mainFile = ("stanfordEdges.txt")
projFile = ("stanfordProjectionEdges.txt")
G = nx.read_edgelist(mainFile, delimiter=',', data=(('rating',int),('date',str)))
Gproj = nx.read_edgelist(projFile, delimiter=',')
print "## GRAPH CREATED ##"
print "## CREATING SET OF NODES ##"
userNodes = set()
businessNodes = set()
for edge in G.edges():
	userNodes.add(edge[0])
	businessNodes.add(edge[1])
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
				if not Gproj.has_edge(edge[1],userNode):
					internalLink = False
					break
			if internalLink:
				internalLinks.append((userNode,businessNode))

print "## WRITING TO FILE ##"
internalFile = open(INTERNAL_LINKS_FILE, "w")
for link in internalLinks:
	internalFile.write(link[0]+","+link[1]+"\n")
internalFile.close()
					