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

PROJ_FILE = "waterlooProj.txt"

fileName = ("waterlooTrain.txt")
G = nx.read_edgelist(fileName, delimiter=',', data=(('rating',int),('date',str)))
print "## GRAPH CREATED ##"

userNodes = set()
businessNodes = set()
for edge in G.edges():
	userNode, businessNode = getUserAndBusiness(edge)
	userNodes.add(userNode)
	businessNodes.add(businessNode)

"""
print len(userNodes & businessNodes)
	
print len(userNodes)
print len(businessNodes)
cu = 0
cb = 0
cub = 0
cbu = 0
for edge in G.edges():
	u = edge[0]
	b = edge[1]
	if(u not in userNodes):
		cu = cu + 1
	if(b not in businessNodes):
		cb = cb + 1
	if(u in businessNodes):
		cub = cub + 1
	if(b in userNodes):
		cbu = cbu + 1

print "Review source not in user: %d"%cu
print "Review dest not in business: %d"%cb
print "Review source in business: %d"%cub
print "Review dest in user: %d"%cbu
"""

print "## CREATING PROJECTION GRAPH ##"
Gproj = nx.Graph()
for edge in G.edges():
	userNode, businessNode = getUserAndBusiness(edge)
	for edge2 in G.edges(businessNode):
		u, b = getUserAndBusiness(edge2)
		if(u!=userNode):
			Gproj.add_edge(userNode,u)
print "## CREATED PROJECTION GRAPH ##"
"""
print len(Gproj.nodes())
print len(Gproj.edges())
"""

for edge in Gproj.edges():
	u1 = edge[0]
	u2 = edge[1]
	

print "## WRITING TO FILE ##"
projFile = open(PROJ_FILE, "w")
for edge in Gproj.edges():
	projFile.write(edge[0]+","+edge[1]+"\n")
projFile.close()
					