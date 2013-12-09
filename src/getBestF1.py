

FIFTY_SPLIT_THRESHOLD_PATH = "../data/threshold_training/"

WEIGHTS_ACR = ["SW", "JW", "DW", "RSW", "RJW", "RDW", "RLSW"]

SCHOOL_ACR = ["COR", "PRC", "UMC", "UIC", "CMU"]

def getF1(precision, recall):
	numer = 2 * precision * recall
	denom = precision + recall
	return numer/denom if denom != 0 else -1.0

def getBestForWeight(weightAcr, schoolAcr):
	resultFile = open(FIFTY_SPLIT_THRESHOLD_PATH + schoolAcr + "_" + weightAcr + "_" + "thresh_train.txt")
	highF1 = 0.0
	highPrecision = 0.0
	highRecall = 0.0
	choiceThreshold = None
	for line in resultFile:
		tau, T, precision, recall = line.split(",")
		if precision != "-1.0" and recall != "-1.0":			
			F1 = getF1(float(precision), float(recall))
			if F1 > highF1:
				highF1 = F1
				choiceThreshold = tau
				highPrecision = float(precision)
				highRecall = float(recall)
	return choiceThreshold, highF1, highPrecision, highRecall


def writeToFileForSchool(results, schoolAcr):
	fileToWrite = open(FIFTY_SPLIT_THRESHOLD_PATH + "BEST_" + schoolAcr + ".txt", "w+")
	fileToWrite.write("Weight, Tau, F1, P, R\n")
	for line in results:
		toWrite = str(line[0]) + "," + str(line[1]) + "," + str(line[2]) + "," + str(line[3]) + "," + str(line[4]) + "\n"
		fileToWrite.write(toWrite)
	fileToWrite.close()

for schoolAcr in SCHOOL_ACR:
	results = []
	for weightAcr in WEIGHTS_ACR:
		tau, F1, precision, recall = getBestForWeight(weightAcr, schoolAcr)
		results.append((weightAcr, tau, F1, precision, recall))
	writeToFileForSchool(results, schoolAcr)

