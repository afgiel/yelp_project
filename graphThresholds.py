import matplotlib.pyplot as plt

THRESHOLD_PATH = "data/threshold_training/"
acronym = "STA"
algos = ["DW", "JW", "RDW", "RJW", "SW", "RSW", "RLSW"]
algoNames = ["Delta", "Jaccard", "Delta with ratings", "Jaccard with ratings", "Sum", "Sum with ratings", "Least Squares Ratings"]
colors = ["b-", "g-", "y-", "r-", "c-", "m-", "k-"]
precisionsList = []
recallsList = []
thresholds = []

for x in range(1, 51):
  thresholds.append(x/10.0)

def findPrecision(allLines):
  precisionList = []
  for line in allLines:
    if float(line[2]) != -1:
      precisionList.append(float(line[2]))
  return precisionList

def findRecall(allLines):
  recallList = []
  for line in allLines:
    recallList.append(float(line[3]))
  return recallList

def addAll(algos, precisionsList, recallsList):
  for algo in algos:
    addAlgo(algo, precisionsList, recallsList)

def addAlgo(algo, precisionsList, recallsList):
  file = open(THRESHOLD_PATH + acronym + "_" + algo + "_thresh_train.txt")
  allLines = []
  for line in file:
    line = line.rstrip()
    line = line.split(',')
    allLines.append(line) 
  precisions = findPrecision(allLines)
  recalls = findRecall(allLines)
  precisionsList.append(precisions)
  recallsList.append(recalls)

def plotThresholds(thresholds, yList, colors, algos):
  for x in range (0, 7):
    numElems = len(yList[x])
    plt.plot(thresholds[:numElems], yList[x], colors[x], label=algos[x])

addAll(algos, precisionsList, recallsList)
plotThresholds(thresholds, precisionsList, colors, algoNames)
plt.title("Precisions at various thresholds for each method")
plt.xlabel("Thresholds")
plt.ylabel("Precisions")

#legend = plt.legend(loc='upper right', shadow=True)

#plt.show()
#plotThresholds(thresholds, recallsList, colors, algoNames)
#plt.title("Recalls at various thresholds for each method")
#plt.xlabel("Thresholds")
#plt.ylabel("Recalls")
legend = plt.legend(loc='upper left', shadow=True)
plt.show()

