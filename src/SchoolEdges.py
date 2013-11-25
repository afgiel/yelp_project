"""
######################################################################################
SCHOOL EDGES - This file generates an edge file for a given school
######################################################################################
"""

"""
######################################################################################
	IMPORTS
######################################################################################
"""
import json 

"""
######################################################################################
	CONSTANTS
######################################################################################
"""
REVIEWS_FILE = "../data/json/reviews.json"
BUSINESSES_FILE = "../data/json/businesses.json"
EDGES_PATH = "../data/edge/"

"""
######################################################################################
	PUBLIC FUNCTIONS
######################################################################################
"""
def getReviews(acronym,school,verbose):
	if(verbose): print "## %s - GETTING BUSINESSES ##\n"%(acronym)
	businesses = set()
	businessFile = open(BUSINESSES_FILE)
	for line in businessFile:
		business = json.loads(line)
		if school in business['schools']: 
			businesses.add("bb" + business['business_id'])
	
	if(verbose): print "## %s - GETTING REVIEWS ##\n"%(acronym)
	reviews = set()
	reviewsFile = open(REVIEWS_FILE)
	for line in reviewsFile:
		review = json.loads(line)
		businessID = "bb" + review['business_id'] 
		if businessID in businesses:
			reviewerID = "uu" + review['user_id']
			stars = str(review['stars'])
			date = review['date']
			toAdd = ",".join([reviewerID, businessID, stars, date])
			reviews.add(toAdd)

	if(verbose): print "## %s - WRITING REVIEWS ##\n"%(acronym)
	edgeFile = open(EDGES_PATH + acronym + "_edges.txt", "w")
	for review in reviews:
		edgeFile.write(review + "\n")
	edgeFile.close()
