import networkx as nx 
from networkx.algorithms import bipartite

STANFORD_EDGES = "stanfordEdges.txt"
STANFORD_STATS_FILE = "stanfordStats.txt"

print "## MAKING GRAPH ##"
G = nx.read_edgelist(STANFORD_EDGES, delimiter=',', data=(('rating',int),('date',str)), create_using=nx.DiGraph())
print "## GRAPH MADE ##"

stats = dict()

print "## COMPUTING STATS ##"
stats["Number of Edges: "]= G.size()
stats["Number of Nodes: "] = len(G)
stats["Clustering Coefficient: "] = nx.bipartite.average_clustering(G) 
stats["Number of Strongly Connected Components: "] = nx.number_strongly_connected_components(G)
stats["Number of Weakly Connected Components: "] = nx.number_weakly_connected_components(G)

print "## WRITING STATS ##"
statsFile = open(STANFORD_STATS_FILE, "w")
for stat, value in stats.items():
	toWrite = stat + str(value)
	statsFile.write(toWrite + "\n")
statsFile.close()