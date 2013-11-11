import networkx as nx

fileName = ("stanfordEdges.txt")
G = nx.read_edgelist(fileName, delimiter=',', data=(('rating',int),('date',str)))

"""
G = nx.Graph()
G.add_edge('A','i')
G.add_edge('B','i')
G.add_edge('B','j')
G.add_edge('B','k')
G.add_edge('C','i')
G.add_edge('C','j')
G.add_edge('C','k')
G.add_edge('D','j')
G.add_edge('D','l')
G.add_edge('E','k')
G.add_edge('E','l')
"""

Gproj = nx.Graph()
for edge in G.edges():
	userNode = edge[0]
	businessNode = edge[1]
	for edge in G.edges(businessNode):
		if(edge[1]!=userNode):
			print userNode
			print edge[1]
			Gproj.add_edge(userNode,edge[1])
	