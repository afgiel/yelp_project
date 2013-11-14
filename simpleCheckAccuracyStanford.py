import networkx as nx 

STANFORD_PREDICTED_FILE = "waterlooIL.txt"
STANFORD_TEST_FILE = "waterlooTest.txt"
STANFORD_TRAIN_FILE = "waterlooTrain.txt"

predicted = set()
actual = set()

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

Gactual = nx.read_edgelist(STANFORD_TEST_FILE, delimiter=',', data=(('rating',int),('date',str)))
Gtrain = nx.read_edgelist(STANFORD_TRAIN_FILE, delimiter=',', data=(('rating',int),('date',str)))

print "## READING IN PREDICTED ##"
predictedFile = open(STANFORD_PREDICTED_FILE)
for line in predictedFile:
	edge = line.split(',')
	predicted.add((edge[0], edge[1].rstrip()))

print "## READING IN ACTUAL ##"
testFile = open(STANFORD_TEST_FILE)
for line in testFile:
	edge = line.split(',')
	actual.add((edge[0], edge[1].rstrip()))
	
actualusers = set()
actualbusi = set()
for a in actual:
	actualusers.add(a[0])
	actualbusi.add(a[1])

pusers = set()
pbusi = set()
for a in predicted:
	pusers.add(a[0])
	pbusi.add(a[1])
	
cu = 0
cb = 0
for p in pusers:
	if(p in actualusers):
		cu = cu + 1
for p in pbusi:
	if(p in actualbusi):
		cb = cb + 1
print "NUMBER of pred USERS in actual: %d" % cu
print "NUMBER of pred BUSIN in actual: %d" % cb
print "NUMBER of actual users: %d" % len(actualusers)
print "NUMBER of actual busi: %d" % len(actualbusi)
print "NUMBER of pred users: %d" % len(pusers)
print "NUMBER of pred busi: %d" % len(pbusi)

num_edges = 0
for edge in Gactual.edges():
	u,b = getUserAndBusiness(edge)
	if(u in pusers and b in pbusi and (not Gtrain.has_edge(b,u))):
		num_edges = num_edges + 1

print "NUMBER of edges between old users and businesses: %d" % num_edges


numberWrong = predicted - actual
numberRight = predicted & actual
print "NUMBER GUESSED: %d" % len(predicted)
print "NUMBER RIGHT: %d" % len(numberRight)
print "NUMBER WRONG: %d" % len(numberWrong)
