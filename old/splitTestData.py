STANFORD_FILE = "waterlooEdges.txt"
PERCENT_TRAIN = .5
STANFORD_TRAIN = "waterlooTrain.txt" 
STANFORD_TEST = "waterlooTest.txt"

def writeToFile(filename, data):
	toWrite = open(filename, "w")
	for line in data: 
		toAdd = ",".join(line)
		toWrite.write(toAdd)
	toWrite.close()

reviews = list()
stanfordFile = open(STANFORD_FILE)
for line in stanfordFile:
	line = line.split(",")
	reviews.append(tuple(line))

reviews = sorted(reviews, key=lambda item: item[3])
total = len(reviews)
splitPoint = int(total*PERCENT_TRAIN)
train = reviews[:splitPoint]
test = reviews[splitPoint:]
print "Split on Date: %s" % reviews[splitPoint][3]

writeToFile(STANFORD_TRAIN, train)
writeToFile(STANFORD_TEST, test)