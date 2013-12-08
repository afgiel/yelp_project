import networkx as nx
import Utils as util

MONTHS_PATH = "../data/months/"
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

def generateWeightedProjectionGraph(acronym, year, month, Gmain, Gproj, userNodes, businessNodes):
	print "## %s %s %s - CREATING WEIGHTS ##\n"%(acronym, str(year), month)
	intersects, unions = computeIntersectionAndUnion(Gmain, Gproj)
	weights = dict()
	for weightAcr in WEIGHTS_ACR:
		print "## %s %s %s - WEIGHTING BY %s ##\n"%(acronym, str(year), month, weightAcr)
		weights[weightAcr] = getWeightings(weightAcr, Gmain, Gproj, unions, intersects)
	return weights
"""
##############
INTERNAL LINKS
##############
"""

def generateInternalLinks(acronym, year, month, Gmain, Gproj, userNodes, businessNodes):
	print "## %s %s %s - FINDING INTERNAL LINKS ##\n"%(acronym, str(year), month)	
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
	print "## %s %s %s - FOUND %d INTERNAL LINKS ##\n"%(acronym, str(year), month,len(internalLinks))
	return internalLinks

"""
##############
GRAPH CREATION
##############
"""

def createMain(acronym, year, month):
	print "## %s %s %s - CREATING GRAPH ##\n"%(acronym, str(year), month)
	fileName = (MONTHS_PATH + acronym + "_" + str(year) + "_" + month + ".txt")
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

def createProjection(acronym, year, month, Gmain, userNodes, businessNodes):
	print "## %s %s %s - CREATING PROJECTION GRAPH ##\n"%(acronym, str(year), month)
	Gproj = nx.Graph()
	for edge in Gmain.edges():
		userNode, businessNode = util.getUserAndBusiness(edge)
		for edge2 in Gmain.edges(businessNode):
			u, b = util.getUserAndBusiness(edge2)
			if(u!=userNode):
				Gproj.add_edge(userNode,u)
	print "## %s %s %s - PROJECTION GRAPH EDGES = %d ##\n"%(acronym, str(year), month, Gproj.number_of_edges())
	return Gproj

"""
##############
PREDICTION
##############
"""

def predictLinks(acronym, year, month, Gproj, Gmain, userNodes, businessNodes, allWeights, internalLinks, weightThreshold):
	print "## %s %s %s - MAKING PREDICTIONS ##\n"%(acronym, str(year), month)
	predicted = dict()
	for weightAcr in allWeights:
		print "## %s %s %s - PREDICTING FOR %s ##\n"%(acronym, str(year), month, weightAcr)
		weight = allWeights[weightAcr]
		predicted[weightAcr] = predictLinkForWeight(acronym, year, month, weightThreshold, Gproj, Gmain, weight, userNodes, businessNodes, internalLinks)
	return predicted

def getWeight(weighting, user1, user2):
		if (user1, user2) in weighting:
			return weighting[(user1, user2)]
		else:
			return weighting[(user2, user1)]

def predictLinkForWeight(acronym, year, month, weightThreshold, Gproj, Gmain, weighting, userNodes, businessNodes, internalLinks):
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
	TintP = len(overlap)
	T = len(testInternalLinks)
	P = len(predicted)
	if P != 0:
		precision = float(TintP)/P
	else: 
		precision = -1.0
	if T != 0:
		recall = float(TintP)/T
	else: 
		recall = -1.0
	return precision,recall


def evaluate(acronym, year, trainMonth, testMonth, predictedByWeight, internalLinks):
	Gtest = createMain(acronym, year, testMonth)
	evalStats = dict()
	for weightAcr in predictedByWeight:
		print "## %s %s %s - EVALUATING FOR %s ##\n"%(acronym, str(year),trainMonth, weightAcr)
		pre, rec = evaluateWeighted(Gtest, predictedByWeight[weightAcr], internalLinks)
		evalStats[weightAcr] = (pre, rec)
	return evalStats

"""
##############
MAIN METHODS
##############
"""
	
def testOneMonth(acronym, year, trainMonth, testMonth, weightThreshold):
	Gmain = createMain(acronym, year, trainMonth)
	userNodes, businessNodes = getUsersAndBusinesses(Gmain)
	Gproj = createProjection(acronym, year, trainMonth, Gmain, userNodes, businessNodes)
	allWeights = generateWeightedProjectionGraph(acronym, year, trainMonth, Gmain, Gproj, userNodes, businessNodes)
	internalLinks = generateInternalLinks(acronym, year, trainMonth, Gmain, Gproj, userNodes, businessNodes)
	predictedByWeight = predictLinks(acronym, year, trainMonth, Gproj, Gmain, userNodes, businessNodes, allWeights, internalLinks, weightThreshold)
	evalStats = evaluate(acronym, year, trainMonth, testMonth, predictedByWeight, internalLinks)
	return evalStats

