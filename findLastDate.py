

lastReviewDict = {}
nextReviewDict = {}
difference = []
trainFile = open("stanfordTrain.txt").readlines()

for line in trainFile:
  lineList = line.split(',')
  if lineList[0] not in lastReviewDict:
    lastReviewDict[lineList[0]] = lineList[3].rstrip()
  elif lastReviewDict[lineList[0]] < lineList[3]:
    lastReviewDict[lineList[0]] = lineList[3].rstrip()

testFile = open("stanfordTest.txt").readlines()

for testLine in testFile:
  lineList = testLine.split(',')
  if lineList[0] in lastReviewDict and lineList[0] not in nextReviewDict:
    nextReviewDict[lineList[0]] = lineList[3].rstrip()
  elif lineList[0] in nextReviewDict and nextReviewDict[lineList[0]] > lineList[3]:
    nextReviewDict[lineList[0]] = lineList[3].rstrip()


for item in nextReviewDict.items():
  d1 = datetime.strptime(item[1], "%Y-%m-%d")
  d2 = datetime.strptime(lastReviewDict[item[0]], "%Y-%m-%d")
  difference.append(abs((d2 - d1).days))

print("Number of people in train: ", len(lastReviewDict))
print("Number of people in test who were also in train: ", len(nextReviewDict))

 
