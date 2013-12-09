
THRESH_TRAIN_PATH = "../data/threshold_training/"

SCHOOL_ACR = ["COR", "PRC", "UMC", "UIC", "CMU"]

def getBestforSchool(schoolAcr):
	best = []
	bestFile = open(THRESH_TRAIN_PATH + "BEST_" + schoolAcr +".txt")
	next(bestFile)
	for line in bestFile:
		weight, tau, F1, P, R = line.split(",")
		best.append((weight, tau, F1, P, R))
	return best

def getF1(precision, recall):
	numer = 2 * precision * recall
	denom = precision + recall
	return numer/denom if denom != 0 else -1.0

def getSTAforbest(best):
	STAforBest = []
	for line in best:
		weight, tau, F1, P, R = line
		weightFile = open(THRESH_TRAIN_PATH + "STA_" + weight + "_thresh_train.txt")
		for line in weightFile:
			lineData = line.split(",")
			if lineData[0] == tau:
				precision = float(lineData[2])
				recall = float(lineData[3])
				STAforBest.append((weight, tau, getF1(precision, recall), precision, recall))
	return STAforBest

def writeOutResults(bestForSTA, schoolAcr):
	fileToWrite = open(THRESH_TRAIN_PATH + "STA_CV_" + schoolAcr + ".txt", "w+")
	fileToWrite.write("Weight, Tau, F1, P, R\n")
	for line in bestForSTA:
		print line
		toWrite = str(line[0]) + "," + str(line[1]) + "," + str(line[2]) + "," + str(line[3]) + "," + str(line[4]) + "\n"
		fileToWrite.write(toWrite)
	fileToWrite.close()

for schoolAcr in SCHOOL_ACR:
	bestForSchool = getBestforSchool(schoolAcr)
	bestForSTA = getSTAforbest(bestForSchool)
	writeOutResults(bestForSTA, schoolAcr)