
YEARS_PATH = "../data/years/"
EDGES_PATH = "../data/edge/"

ACRONYM = "STA"

def writeOutYearData(acronym, year, yearReviews):
	print year, yearReviews[0]
	yearFile = open(YEARS_PATH + acronym + "_" + str(year) + ".txt", "w")
	for review in yearReviews: 
		toWrite = ",".join(review)
		yearFile.write(toWrite)
	yearFile.close()

def splitByYear(acronym, reviews):
	currYear = None
	currYearData = list()
	for review in reviews:
		date = review[3]
		dateParts = date.split("-")
		year = dateParts[0]
		if year != currYear:
			if currYear != None:
				writeOutYearData(acronym, currYear, currYearData)
			currYear = year
			currYearData[:] = []
		currYearData.append(review)	

def readTrain(acronym):
	reviews = list()
	edgeFile = open(EDGES_PATH + acronym + "_edges.txt")
	for line in edgeFile:
		line = line.split(",")
		reviews.append(tuple(line))
	reviews = sorted(reviews, key=lambda item: item[3])
	return reviews

reviews = readTrain(ACRONYM)
splitByYear(ACRONYM, reviews)