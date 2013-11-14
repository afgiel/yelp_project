import networkx as nx 

INTERNAL_LINKS_FILE = "internalLinksTrain.txt"
PROJ_FILENAME = "stanfordProjectionTrain-SumWeights.txt"
MAIN_FILENAME = "stanfordTrain.txt"
PREDICTED_FILE = "stanfordPredicted.txt"

WEIGHT_THRESHOLD = 1
TOTAL_THRESHOLD = 1

Gproj = nx.read_edgelist(PROJ_FILENAME, delimiter=',', data=(('rating',float),))
Gmain = nx.read_edgelist(MAIN_FILENAME, delimiter=',', data=(('rating',int),('date',str)))
print "## CREATED GRAPHS ##"
# Gmain = nx.Graph()
# Gmain.add_edge('A','i', rating = 1)
# Gmain.add_edge('B','i', rating = 2)
# Gmain.add_edge('B','j', rating = 1)
# Gmain.add_edge('B','k', rating = 3)
# Gmain.add_edge('C','i', rating = 5)
# Gmain.add_edge('C','j', rating = 4)
# Gmain.add_edge('C','l', rating = 5)
# Gmain.add_edge('D','j', rating = 1)
# Gmain.add_edge('D','l', rating = 4)
# Gmain.add_edge('E','k', rating = 3)
# Gmain.add_edge('E','l', rating = 2)

def getWeight(user1, user2):
	return Gproj[user1][user2]['rating']

numOverThreshold = dict()
internalLinks = open(INTERNAL_LINKS_FILE)
# internalLinks = open("testInternalLinks.txt")
print "## OPENED GRAPHS ##"
nodes = Gmain.nodes()

userNodes = set()
businessNodes = set()
for edge in Gmain.edges():
	userNodes.add(edge[0])
	businessNodes.add(edge[1])


for line in internalLinks:
	internalLink = line.split(',')
	userNode = internalLink[0]
	businessNode = internalLink[1].rstrip()
	total = 0
	for edge in Gmain.edges(businessNode):
		if edge[1] != userNode:
			weight = getWeight(userNode, edge[1])
			if weight > WEIGHT_THRESHOLD:
				total += 1
	numOverThreshold[(userNode, businessNode)] = total

predicted = set()
for key, value in numOverThreshold.items():
	if value >= TOTAL_THRESHOLD:
		predicted.add(key)

predictedFile = open(PREDICTED_FILE, "w")
for item in predicted:
	predictedFile.write(item[0]+ "," + item[1] + "\n")
predictedFile.close()
