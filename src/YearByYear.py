import OneYear 
from collections import Counter

YEARS = [2005, 2006, 2007, 2008, 2009, 2010, 2011]


THRESH_TRAINING_PATH = "../data/years/threshold_training/"
ACRONYM = "STA"

def writeTrainingtoFile(weightAcr, weightThreshold, recall, precision):
	print "WRITING RESULTS TO FILE FOR %s %s YEAR BY YEAR" % (ACRONYM, weightAcr)
	toWrite = (weightThreshold, precision, recall)
	thresholdTrainFile = open(THRESH_TRAINING_PATH + ACRONYM + "_" + weightAcr + "_TRAINING.txt", "a")
	thresholdTrainFile.write(str(toWrite))
	thresholdTrainFile.close()

def runForThreshold(weightThreshold):

	TintPCount = Counter()
	TCount = Counter()
	PCount = Counter()

	for trainYearIdx in range(len(YEARS)-1):
		testYearIdx = trainYearIdx + 1
		trainYear = YEARS[trainYearIdx]
		testYear = YEARS[testYearIdx]
		evalStats = OneYear.testOneYear(ACRONYM, trainYear, testYear, weightThreshold)
		for weightAcr in evalStats:
			TintP, T, P = evalStats[weightAcr]
			TintPCount[weightAcr] += TintP 
			TCount[weightAcr] += T
			PCount[weightAcr] += P

	print "RESULTS FOR %s YEAR BY YEAR" % (ACRONYM)
	for weightAcr in TintPCount:
		TintP = TintPCount[weightAcr]
		T = TCount[weightAcr]
		P = PCount[weightAcr]
		if P != 0:
			precision = float(TintP)/P
		else: 
			precision = -1.0
		if T != 0:
			recall = float(TintP)/T
		else: 
			recall = -1.0
		print "---- %s ----" % (weightAcr)
		print "R: %f" % recall
		print "P: %f" % precision
		writeTrainingtoFile(weightAcr, weightThreshold, recall, precision)

weightThresholds = [x*.1 for x in range(1, 6)]
for weightThreshold in weightThresholds:
	print "TRAINING ON WEIGHT THRESHOLD %f" % weightThreshold
	runForThreshold(weightThreshold)

