import networkx as nx
import Utils as util

YEARS_PATH = "../data/years/"
# WEIGHT_THRESHOLD = 1
TOTAL_THRESHOLD = 1
WEIGHTS_ACR = ["SW", "JW", "DW", "RSW", "RJW", "RDW", "RLSW"]

"""
##############
HELPERS
##############
"""

def getBusinessNodes(Gmain, user):
	userSet = set()
	for edge in Gmain.edges(user):
		u,b = util.getUserAndBusiness(edge)
		userSet.add(b)
	return userSet

def computeIntersectionAndUnion(Gmain, Gproj):
	intersects = dict()
	unions = dict()
	for edge in Gproj.edges():
		user1, user2 = edge
		user1Bus = getBusinessNodes(Gmain, user1)
		user2Bus = getBusinessNodes(Gmain, user2)
		intersection = set.intersection(user1Bus, user2Bus)
		union = set.union(user1Bus, user2Bus)
		intersects[(user1, user2)] = intersection
		intersects[(user2, user1)] = intersection
		unions[(user1, user2)] = union
		unions[(user2, user1)] = union
	return intersects, unions

"""
##############
WEIGHTS 
##############
"""
def createSumWeight(Gproj, intersects):
	weights = dict()
	for edge in Gproj.edges():
		weights[(edge[0],edge[1])] = len(intersects[(edge[0],edge[1])])
	return weights

def createJaccardWeight(Gproj, intersects, unions):
	weights = dict()
	for edge in Gproj.edges():
		weights[(edge[0],edge[1])] = float(len(intersects[(edge[0],edge[1])]))/float(len(unions[(edge[0], edge[1])]))
	return weights

def createDeltaWeight(Gproj, Gmain, intersects):
	weights = dict()
	for edge in Gproj.edges():
		intersection = intersects[(edge[0],edge[1])]
		total = 0.0
		for business in intersection:
			degree = len(Gmain.edges(business))
			total += 2.0/(degree * degree-1)
		weights[(edge[0], edge[1])] = total
	return weights	

def getRating(Gmain, user, business):
	return Gmain[user][business]['rating']

def createRatingSumWeight(Gproj, Gmain, intersects):
	weights = dict()
	for edge in Gproj.edges():
		total = 0.0
		intersection = intersects[(edge[0],edge[1])]
		for common in intersection:
			user1Rating = getRating(Gmain, edge[0], common)
			user2Rating = getRating(Gmain, edge[1], common)
			diff = abs(user1Rating - user2Rating)
			toAdd = float(5-diff)#/5
			total += toAdd
		weights[(edge[0],edge[1])] = total
	return weights

def createRatingJaccardWeight(Gproj, Gmain, intersects, unions):
	weights = dict()
	for edge in Gproj.edges():
		total = 0.0
		intersection = intersects[(edge[0],edge[1])]
		for common in intersection:
			user1Rating = getRating(Gmain, edge[0], common)
			user2Rating = getRating(Gmain, edge[1], common)
			diff = abs(user1Rating - user2Rating)
			toAdd = float(5-diff)#/5
			total += toAdd
		total = total/len(unions[(edge[0], edge[1])])
		weights[(edge[0],edge[1])] = total
	return weights

def createRatingDeltaWeight(Gproj, Gmain, intersects):
	weights = dict()
	for edge in Gproj.edges():
		intersection = intersects[(edge[0],edge[1])]
		total = 0.0
		for business in intersection:
			degree = len(Gmain.edges(business))
			base = 2.0/(degree * degree-1)
			user1Rating = getRating(Gmain, edge[0], business)
			user2Rating = getRating(Gmain, edge[1], business)
			diff = abs(user1Rating - user2Rating)
			scale = float(5-diff)#/5
			total += base*scale
		weights[(edge[0], edge[1])] = total
	return weights	

def createRatingLeastSquareWeight(Gproj, Gmain, intersects):
	weights = dict()
	for edge in Gproj.edges():
		total = 0.0
		intersection = intersects[(edge[0],edge[1])]
		for common in intersection:
			user1Rating = getRating(Gmain, edge[0], common)
			user2Rating = getRating(Gmain, edge[1], common)
			diff = abs(user1Rating - user2Rating)
			toAdd = float(5-diff)#/5
			total += pow(toAdd, 2)
		weights[(edge[0],edge[1])] = total
	return weights

def getWeightings(weightAcr, Gmain, Gproj, unions, intersects):
	if weightAcr == "SW":
		return createSumWeight(Gproj, intersects)
	if weightAcr == "JW":
		return createJaccardWeight(Gproj, intersects, unions)
	if weightAcr == "DW":
		return createDeltaWeight(Gproj, Gmain, intersects)
	if weightAcr == "RSW":
		return createRatingSumWeight(Gproj, Gmain, intersects)
	if weightAcr == "RJW":
		return createRatingJaccardWeight(Gproj, Gmain, intersects, unions)
	if weightAcr == "RDW":
		return createRatingDeltaWeight(Gproj, Gmain, intersects)
	if weightAcr == "RLSW":
		return createRatingLeastSquareWeight(Gproj, Gmain, intersects)

def generateWeightedProjectionGraph(acronym, year, Gmain, Gproj, userNodes, businessNodes):
	print "## %s %s - CREATING WEIGHTS ##\n"%(acronym, str(year))
	intersects, unions = computeIntersectionAndUnion(Gmain, Gproj)
	weights = dict()
	for weightAcr in WEIGHTS_ACR:
		print "## %s %s - WEIGHTING BY %s ##\n"%(acronym, str(year), weightAcr)
		weights[weightAcr] = getWeightings(weightAcr, Gmain, Gproj, unions, intersects)
	return weights
"""
##############
INTERNAL LINKS
##############
"""

def generateInternalLinks(acronym, year, Gmain, Gproj, userNodes, businessNodes):
	print "## %s %s - FINDING INTERNAL LINKS ##\n"%(acronym, str(year))	
	internalLinks = []
	count = 0
	total = len(userNodes)
	for userNode in userNodes:
		count = count + 1;
		for businessNode in businessNodes:
			if not Gmain.has_edge(userNode,businessNode):
				internalLink = True
				for edge in Gmain.edges(businessNode):
					u,b = util.getUserAndBusiness(edge)
					if not Gproj.has_edge(u,userNode):
						internalLink = False
						break
				if internalLink:
					internalLinks.append((userNode,businessNode))
	return internalLinks

"""
##############
GRAPH CREATION
##############
"""

def createMain(acronym, year):
	print "## %s %s - CREATING GRAPH ##\n"%(acronym, str(year))
	fileName = (YEARS_PATH + acronym + "_" + str(year) + ".txt")
	G = nx.read_edgelist(fileName, delimiter=',', data=(('rating',int),('date',str)))
	return G

def getUsersAndBusinesses(G):
	userNodes = set()
	businessNodes = set()
	for edge in G.edges():
		userNode, businessNode = util.getUserAndBusiness(edge)
		userNodes.add(userNode)
		businessNodes.add(businessNode)
	return userNodes, businessNodes

def createProjection(acronym, year, Gmain, userNodes, businessNodes):
	print "## %s %s - CREATING PROJECTION GRAPH ##\n"%(acronym, str(year))
	Gproj = nx.Graph()
	for edge in Gmain.edges():
		userNode, businessNode = util.getUserAndBusiness(edge)
		for edge2 in Gmain.edges(businessNode):
			u, b = util.getUserAndBusiness(edge2)
			if(u!=userNode):
				Gproj.add_edge(userNode,u)
	return Gproj

"""
##############
PREDICTION
##############
"""

def predictLinks(acronym, year, Gproj, Gmain, userNodes, businessNodes, allWeights, internalLinks, weightThreshold):
	print "## %s %s - MAKING PREDICTIONS ##\n"%(acronym, str(year))
	predicted = dict()
	for weightAcr in allWeights:
		print "## %s %s - PREDICTING FOR %s ##\n"%(acronym, str(year), weightAcr)
		weight = allWeights[weightAcr]
		predicted[weightAcr] = predictLinkForWeight(acronym, year, weightThreshold, Gproj, Gmain, weight, userNodes, businessNodes, internalLinks)
	return predicted

def getWeight(weighting, user1, user2):
		if (user1, user2) in weighting:
			return weighting[(user1, user2)]
		else:
			return weighting[(user2, user1)]

def predictLinkForWeight(acronym, year, weightThreshold, Gproj, Gmain, weighting, userNodes, businessNodes, internalLinks):
	numOverThreshold = dict()
	countX = 0
	for internalLink in internalLinks:
		countX = countX + 1;
		userNode = internalLink[0]
		businessNode = internalLink[1].rstrip()
		total = 0
		for edge in Gmain.edges(businessNode):
			if edge[1] != userNode:
				weight = getWeight(weighting, userNode, edge[1])
				if weight >= weightThreshold:
					total += 1
		numOverThreshold[(userNode, businessNode)] = total
	predicted = set()
	for key, value in numOverThreshold.items():
		if value >= TOTAL_THRESHOLD:
			predicted.add(key)
	return predicted

"""
##############
EVALUATION
##############
"""
def evaluateWeighted(Gtest, predicted, internalLinks):
	testUser, testBusinesses = getUsersAndBusinesses(Gtest)
	predictedUsers = set()
	predictedBusinesses = set()
	for edge in predicted:
		u,b = util.getUserAndBusiness(edge)
		predictedUsers.add(u)
		predictedBusinesses.add(b)
	testInternalLinks = set()
	for edge in Gtest.edges(): 
		u,b = util.getUserAndBusiness(edge)
		if (u, b) in internalLinks:
			testInternalLinks.add((u, b))
	overlap = testInternalLinks & predicted
	return len(overlap), len(testInternalLinks), len(predicted)


def evaluate(acronym, year, testYear, predictedByWeight, internalLinks):
	Gtest = createMain(acronym, testYear)
	evalStats = dict()
	for weightAcr in predictedByWeight:
		print "## %s %s - EVALUATING FOR %s ##\n"%(acronym, str(year), weightAcr)
		TintP, T, P = evaluateWeighted(Gtest, predictedByWeight[weightAcr], internalLinks)
		evalStats[weightAcr] = (TintP, T, P)
	return evalStats

"""
##############
MAIN METHODS
##############
"""
	
def testOneYear(acronym, year, testYear, weightThreshold):
	Gmain = createMain(acronym, year)
	userNodes, businessNodes = getUsersAndBusinesses(Gmain)
	Gproj = createProjection(acronym, year, Gmain, userNodes, businessNodes)
	allWeights = generateWeightedProjectionGraph(acronym, year, Gmain, Gproj, userNodes, businessNodes)
	internalLinks = generateInternalLinks(acronym, year, Gmain, Gproj, userNodes, businessNodes)
	predictedByWeight = predictLinks(acronym, year, Gproj, Gmain, userNodes, businessNodes, allWeights, internalLinks, weightThreshold)
	evalStats = evaluate(acronym, year, testYear, predictedByWeight, internalLinks)
	return evalStats

