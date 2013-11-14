import networkx as nx 
from networkx.algorithms import bipartite
import collections
import matplotlib.pyplot as plt
import math 

ALL_EDGES = "allEdges.txt"
ALL_STATS_FILE = "allStats.txt"

print "## MAKING GRAPH ##"
G = nx.read_edgelist(ALL_EDGES, delimiter=',', data=(('rating',int),('date',str)), create_using=nx.DiGraph())
print "## GRAPH MADE ##"

stats = dict()

print "## COMPUTING STATS ##"
stats["Number of Edges: "]= G.size()
stats["Number of Nodes: "] = len(G)
# stats["Clustering Coefficient: "] = nx.bipartite.average_clustering(G) 
stats["Number of Strongly Connected Components: "] = nx.number_strongly_connected_components(G)
stats["Number of Weakly Connected Components: "] = nx.number_weakly_connected_components(G)

userDegreeDist = collections.Counter()
businessDegreeDist = collections.Counter()
rawDegrees = list()

numBusiness = 0
numUser = 0

print "## COMPUTING DEGREE DIST ##"
for node in G: 
	outDegree = G.out_degree(node)
	if outDegree != 0: 
		numUser += 1
		userDegreeDist[outDegree] += 1
		rawDegrees.append(outDegree)
	else: 
		numBusiness += 1
		inDegree = G.in_degree(node)
		businessDegreeDist[inDegree] += 1
		rawDegrees.append(inDegree)

plt.loglog(userDegreeDist.keys(), userDegreeDist.values(), marker='o', linestyle = 'None')
plt.show()

plt.loglog(businessDegreeDist.keys(), businessDegreeDist.values(), marker='o', linestyle = 'None')
plt.show()

stats["Number of Businesses: "] = numBusiness
stats["Number of Users: "] = numUser

print "## ESTIMATING ALPHA VIA MLE ##"
n = len(rawDegrees)
xMin = 1
totalSum = 0.0
for i in range(n):
	di = rawDegrees[i]
	if di > 1:
		toAdd = (math.log((di)/xMin))
		totalSum += toAdd
alpha = 1 + n*(1.0/totalSum)
stats["Alpha : "] = alpha

print "## WRITING STATS ##"
statsFile = open(ALL_STATS_FILE, "w")
for stat, value in stats.items():
	toWrite = stat + str(value)
	statsFile.write(toWrite + "\n")
statsFile.close()