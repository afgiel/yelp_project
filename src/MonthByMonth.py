import OneMonth
from collections import Counter

YEARS = [2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012]
MONTHS = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
WEIGHTS_ACR = ["SW", "JW", "DW", "RSW", "RJW", "RDW", "RLSW"]


THRESH_TRAINING_PATH = "../data/months/threshold_training/"
MONTHS_PATH = "../data/months/"
ACRONYM = "STA"

def writeTrainingtoFile(weightAcr, weightThreshold, recall, precision, year, month):
	print "WRITING RESULTS TO FILE FOR %s %s %s %s MONTH BY MONTH" % (ACRONYM, weightAcr, str(year), month)
	toWrite = (str(year), month, weightThreshold, precision, recall)
	thresholdTrainFile = None
	try: 
		thresholdTrainFile = open(THRESH_TRAINING_PATH + ACRONYM + "_" + weightAcr + "_TRAINING.txt", "a")
	except: 
		thresholdTrainFile = open(THRESH_TRAINING_PATH + ACRONYM + "_" + weightAcr + "_TRAINING.txt", "w")
	thresholdTrainFile.write(str(toWrite) + "\n")
	thresholdTrainFile.close()

def runForThreshold(weightThreshold):

	Precision = dict()
	Recall = dict()

	for trainYearIdx in range(len(YEARS)):
		for trainMonthIdx in range(len(MONTHS)-1):
			testMonthIdx = trainMonthIdx + 1
			trainYear = YEARS[trainYearIdx]
			trainMonth = MONTHS[trainMonthIdx]
			testMonth = MONTHS[testMonthIdx]
			found = 0
			try:
				fileName = (MONTHS_PATH + ACRONYM + "_" + str(trainYear) + "_" + trainMonth + ".txt")
				fileName2 = (MONTHS_PATH + ACRONYM + "_" + str(trainYear) + "_" + testMonth + ".txt")
				f1 = open(fileName)
				f2 = open(fileName2)
				f1.close()
				f2.close()
				found = 1
			except:
				print "NOT FOUND %s %s %s"%(trainYear,trainMonth,testMonth)
			if(found == 1):
				print "FOUND %s %s %s"%(trainYear,trainMonth,testMonth)
				evalStats = OneMonth.testOneMonth(ACRONYM, trainYear, trainMonth, testMonth, weightThreshold)
				for weightAcr in evalStats:
					pre,rec = evalStats[weightAcr]
					Precision[(trainYear,trainMonth,weightAcr)] = pre
					Recall[(trainYear,trainMonth,weightAcr)] = rec

	print Precision

	print "RESULTS FOR %s MONTH BY MONTH" % (ACRONYM)
	for weightAcr in WEIGHTS_ACR:
		for trainYearIdx in range(len(YEARS)):
			for trainMonthIdx in range(len(MONTHS)-1):
				year = YEARS[trainYearIdx]
				month = MONTHS[trainMonthIdx]
				if((year,month,weightAcr) in Precision):
					precision = Precision[(year,month,weightAcr)]
					recall = Recall[(year,month,weightAcr)]
					print "---- %s %s %s ----" % (weightAcr,str(year),month)
					print "R: %f" % recall
					print "P: %f" % precision
					writeTrainingtoFile(weightAcr, weightThreshold, recall, precision, year, month)

weightThresholds = [x*.1 for x in range(1, 6)]
for weightThreshold in weightThresholds:
	print "TRAINING ON WEIGHT THRESHOLD %f" % weightThreshold
	runForThreshold(weightThreshold)

