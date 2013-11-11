import networkx as nx

PROJ_FILENAME = "stanfordProjectionTrainEdges.txt"
MAIN_FILENAME = "stanfordTrain.txt"

Gproj = nx.read_edgelist(PROJ_FILENAME, delimiter=',')
Gmain = nx.read_edgelist(MAIN_FILENAME, delimiter=',', data=(('rating',int),('date',str)))

# Gmain = nx.Graph()
# Gmain.add_edge('A','i')
# Gmain.add_edge('B','i')
# Gmain.add_edge('B','j')
# Gmain.add_edge('B','k')
# Gmain.add_edge('C','i')
# Gmain.add_edge('C','j')
# Gmain.add_edge('C','l')
# Gmain.add_edge('D','j')
# Gmain.add_edge('D','l')
# Gmain.add_edge('E','k')
# Gmain.add_edge('E','l')

# Gproj = nx.Graph()
# for edge in Gmain.edges():
#        userNode = edge[0]
#        businessNode = edge[1]
#        for edge in Gmain.edges(businessNode):
#                if(edge[1]!=userNode):
#                        Gproj.add_edge(userNode,edge[1])

def createSumWeight():
	weights = dict()
	for edge in Gproj.edges():
		weights[(edge[0],edge[1])] = len(intersects[(edge[0],edge[1])])
	return weights

def createJaccardWeight():
	weights = dict()
	for edge in Gproj.edges():
		weights[(edge[0],edge[1])] = float(len(intersects[(edge[0],edge[1])]))/float(len(unions[(edge[0], edge[1])]))
	return weights

def createDeltaWeight():
	weights = dict()
	for edge in Gproj.edges():
		intersection = intersects[(edge[0],edge[1])]
		total = 0.0
		for business in intersection:
			degree = len(Gmain.edges(business))
			total += 2.0/(degree * degree-1)
		weights[(edge[0], edge[1])] = total
	return weights	

def getBusinessNodes(user):
	userSet = set()
	for review in Gmain.edges(user):
			userSet.add(review[1])
	return userSet

def writeToFile(name,weights):
	weightsFile = open(name,'w')
	for edge in Gproj.edges():
		weightsFile.write(edge[0]+","+edge[1]+","+str(weights[(edge[0],edge[1])]) + "\n")
	weightsFile.close()

def computeIntersectionAndUnion():
	global Gproj, Gmain 
	global intersects
	global unions
	for edge in Gproj.edges():
		user1, user2 = edge
		user1Bus = getBusinessNodes(user1)
		user2Bus = getBusinessNodes(user2)
		intersection = set.intersection(user1Bus, user2Bus)
		union = set.union(user1Bus, user2Bus)
		intersects[(user1, user2)] = intersection
		intersects[(user2, user1)] = intersection
		unions[(user1, user2)] = union
		unions[(user2, user1)] = union

print "## GRAPH CREATED ##"
print "## CREATING SET OF NODES ##"
userNodes = set()
businessNodes = set()
for edge in Gmain.edges():
       userNodes.add(edge[0])
       businessNodes.add(edge[1])
print "## CREATED SET OF NODES ##"

intersects = dict()
unions = dict()

print "## COMPUTING INTERSECTION ##"
computeIntersectionAndUnion()

print "## COMPUTING SUM WEIGHT ##"
sumWeights = createSumWeight()
SUM_WEIGHTS_FILE = "stanfordProjectionTrain-SumWeights.txt"
print "## WRITING SUM WEIGHT ##"
writeToFile(SUM_WEIGHTS_FILE,sumWeights)

print "## COMPUTING JACCARD WEIGHT ##"
jaccardWeights = createJaccardWeight()
JACCARD_WEIGHTS_FILE = "stanfordProjectionTrain-JaccardWeights.txt"
print "## WRITING JACCARD WEIGHT ##"
writeToFile(JACCARD_WEIGHTS_FILE,jaccardWeights)

print "## COMPUTING DELTA WEIGHT ##"
deltaWeights = createDeltaWeight()
DELTA_WEIGHTS_FILE = "stanfordProjectionTrain-DeltaWeights.txt"
print "## WRITING DELTA WEIGHT ##"
writeToFile(DELTA_WEIGHTS_FILE,deltaWeights)

