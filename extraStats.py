#Find num of internal links inside (test intersect train)

testEdges = set()
trainEdges = set()
ilEdges = set()
testUsers = set()
trainUsers = set()
testBusinesses = set()
trainBusinesses = set()

trainAndTestBus = set()
trainAndTestUser = set()

testFile = open("data/test/UWA_test.txt")
trainFile = open("data/train/UWA_train.txt")
ilFile = open("data/internal_links/UWA_il.txt")

def addEdgesToSet(set, file):
  for line in file:
    line = line.split(',')
    set.add((line[0], line[1].rstrip()))

def addUsersToSet(set, file):
  for line in file:
    line = line.split(',')
    set.add(line[0])

def addBusinessesToSet(set, file):
  for line in file:
    line = line.split(',')
    set.add(line[1])

addEdgesToSet(ilEdges, ilFile)
addEdgesToSet(trainEdges, trainFile)

trainFile.seek(0)

addUsersToSet(testUsers, testFile)
addUsersToSet(trainUsers, trainFile)

testFile.seek(0)
trainFile.seek(0)

addBusinessesToSet(testBusinesses, testFile)
addBusinessesToSet(trainBusinesses, trainFile)

trainAndTestBus = testBusinesses.intersection(trainBusinesses)
trainAndTestUser = testUsers.intersection(trainUsers)

testFile.seek(0)

for line in testFile:
  line = line.split(',')
  if line[0] in trainAndTestUser and line[1] in trainAndTestBus:
    testEdges.add((line[0], line[1]))

ilAndTest = testEdges.intersection(ilEdges)
testNotTrain = testEdges.difference(trainEdges)
testAndTrain = testEdges.intersection(trainEdges)

print "Number of users in train: ", len(trainUsers)
print "Number of users in test: ", len(testUsers)
print "Number of users in train and test: ", len(trainAndTestUser)
print "\n"
print "Number of businesses in train: ", len(trainBusinesses)
print "Number of businesses in test: ", len(testBusinesses)
print "Number of businesses in train and test: ", len(trainAndTestBus)
print "\n"
print "Number of edges in test that are not new in any way: ", len(testEdges)
print "Number of edges in test that are not new in any way and are not in train: ", len(testNotTrain)
print "Number of edges in test that are also in train: ", len(testAndTrain)
print "\n"
print "Number of internal links: ", len(ilEdges)
print "Number of edges in test edges that are also internal links: ", len(ilAndTest)
