
STANFORD_PREDICTED_FILE = "stanfordPredicted.txt"
STANFORD_TEST_FILE = "stanfordTest.txt"

predicted = set()
actual = set()

print "## READING IN PREDICTED ##"
predictedFile = open(STANFORD_PREDICTED_FILE)
for line in predictedFile:
	edge = line.split(',')
	predicted.add((edge[0], edge[1]))

print "## READING IN ACTUAL ##"
testFile = open(STANFORD_TEST_FILE)
for line in testFile:
	edge = line.split(',')
	actual.add((edge[0], edge[1]))

numberWrong = predicted - actual
numberRight = predicted & actual
print "NUMBER GUESSED: %d" % len(predicted)
print "NUMBER RIGHT: %d" % numberRight
print "NUMBER WRONG: %d" % numberWrong
