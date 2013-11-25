"""
######################################################################################
GENERATE JSON DATA - This file breaks the yelp data into users, businesses and reviews
######################################################################################
"""

"""
######################################################################################
	IMPORTS
######################################################################################
"""
import json
import os

"""
######################################################################################
	CONSTANTS
######################################################################################
"""
FILENAME = "../data/json/yelp_academic_dataset.json"
USER_FILE = "../data/json/users.json"
REVIEW_FILE = "../data/json/reviews.json"
BUSINESS_FILE = "../data/json/businesses.json"
USER = "user"
REVIEW = "review"
BUSINESS = "business"

"""
######################################################################################
	HELPER FUNCTIONS
######################################################################################
"""
def writeToFile(filename, objs):
	toWriteFile = open(filename, "w")
	for obj in objs:
		toWriteFile.write(obj + "\n")
	toWriteFile.close()

"""
######################################################################################
	PROGRAM
######################################################################################
"""
users = set()
reviews = set()
businesses = set()
dataset = open(FILENAME)
print "running through data"
for line in dataset:
	obj = json.loads(line)
	if obj['type'] == USER:
		users.add(json.dumps(obj))
	elif obj['type'] == REVIEW:
		reviews.add(json.dumps(obj))
	elif obj['type'] == BUSINESS:
		businesses.add(json.dumps(obj))

print "writing data"
writeToFile(USER_FILE, users)
writeToFile(REVIEW_FILE, reviews)
writeToFile(BUSINESS_FILE, businesses)