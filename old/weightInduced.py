import networkx as nx

PROJ_FILENAME = "waterlooProj.txt"
MAIN_FILENAME = "waterlooTrain.txt"

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

Gproj = nx.read_edgelist(PROJ_FILENAME, delimiter=',')
Gmain = nx.read_edgelist(MAIN_FILENAME, delimiter=',', data=(('rating',int),('date',str)))

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

def getRating(user, business):
	return Gmain[user][business]['rating']

def createRatingSumWeight():
	weights = dict()
	for edge in Gproj.edges():
		total = 0.0
		intersection = intersects[(edge[0],edge[1])]
		for common in intersection:
			user1Rating = getRating(edge[0], common)
			user2Rating = getRating(edge[1], common)
			diff = abs(user1Rating - user2Rating)
			toAdd = float(5-diff)/5
			total += toAdd
		weights[(edge[0],edge[1])] = total
	return weights

def createRatingJaccardWeight():
	weights = dict()
	for edge in Gproj.edges():
		total = 0.0
		intersection = intersects[(edge[0],edge[1])]
		for common in intersection:
			user1Rating = getRating(edge[0], common)
			user2Rating = getRating(edge[1], common)
			diff = abs(user1Rating - user2Rating)
			toAdd = float(5-diff)/5
			total += toAdd
		total = total/len(unions[(edge[0], edge[1])])
		weights[(edge[0],edge[1])] = total
	return weights

def createRatingDeltaWeight():
	weights = dict()
	for edge in Gproj.edges():
		intersection = intersects[(edge[0],edge[1])]
		total = 0.0
		for business in intersection:
			degree = len(Gmain.edges(business))
			base = 2.0/(degree * degree-1)
			user1Rating = getRating(edge[0], business)
			user2Rating = getRating(edge[1], business)
			diff = abs(user1Rating - user2Rating)
			scale = float(5-diff)/5
			total += base*scale
		weights[(edge[0], edge[1])] = total
	return weights	

def createRatingLeastSquareWeight():
	weights = dict()
	for edge in Gproj.edges():
		total = 0.0
		intersection = intersects[(edge[0],edge[1])]
		for common in intersection:
			user1Rating = getRating(edge[0], common)
			user2Rating = getRating(edge[1], common)
			diff = abs(user1Rating - user2Rating)
			toAdd = float(5-diff)/5
			total += pow(toAdd, 2)
		weights[(edge[0],edge[1])] = total
	return weights

def getBusinessNodes(user):
	userSet = set()
	for review in Gmain.edges(user):
		u,b = getUserAndBusiness(review)
		userSet.add(b)
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
	u,b = getUserAndBusiness(edge)
	userNodes.add(u)
	businessNodes.add(b)
print "## CREATED SET OF NODES ##"

intersects = dict()
unions = dict()

print "## COMPUTING INTERSECTION ##"
computeIntersectionAndUnion()

print "## COMPUTING SUM WEIGHT ##"
sumWeights = createSumWeight()
SUM_WEIGHTS_FILE = "waterlooProj-SumWeights.txt"
print "## WRITING SUM WEIGHT ##"
writeToFile(SUM_WEIGHTS_FILE,sumWeights)

print "## COMPUTING JACCARD WEIGHT ##"
jaccardWeights = createJaccardWeight()
JACCARD_WEIGHTS_FILE = "waterlooProj-JaccardWeights.txt"
print "## WRITING JACCARD WEIGHT ##"
writeToFile(JACCARD_WEIGHTS_FILE,jaccardWeights)

print "## COMPUTING DELTA WEIGHT ##"
deltaWeights = createDeltaWeight()
DELTA_WEIGHTS_FILE = "waterlooProj-DeltaWeights.txt"
print "## WRITING DELTA WEIGHT ##"
writeToFile(DELTA_WEIGHTS_FILE,deltaWeights)

print "## COMPUTING RATING SUM WEIGHT ##"
ratingSumWeights = createRatingSumWeight()
RATING_SUM_WEIGHTS_FILE = "waterlooProj-RatingSumWeights.txt"
print "## WRITING RATING SUM WEIGHT ##"
writeToFile(RATING_SUM_WEIGHTS_FILE,ratingSumWeights)

print "## COMPUTING RATING JACCARD WEIGHT ##"
ratingJaccardWeights = createRatingJaccardWeight()
RATING_JACCARD_WEIGHTS_FILE = "waterlooProj-RatingJaccardWeights.txt"
print "## WRITING RATING JACCARD WEIGHT ##"
writeToFile(RATING_JACCARD_WEIGHTS_FILE,ratingJaccardWeights)

print "## COMPUTING RATING DELTA WEIGHT ##"
ratingDeltaWeights = createRatingDeltaWeight()
RATING_DELTA_WEIGHTS_FILE = "waterlooProj-RatingDeltaWeights.txt"
print "## WRITING RATING DELTA WEIGHT ##"
writeToFile(RATING_DELTA_WEIGHTS_FILE,ratingDeltaWeights)

print "## COMPUTING RATING LEAST SQUARE WEIGHT ##"
ratingLeastSquareWeights = createRatingLeastSquareWeight()
RATING_LEAST_SQUARE_WEIGHTS_FILE = "waterlooProj-RatingLeastSquareWeights.txt"
print "## WRITING RATING LEAST SQUARE WEIGHT ##"
writeToFile(RATING_LEAST_SQUARE_WEIGHTS_FILE,ratingLeastSquareWeights)
