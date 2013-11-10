import json

FILENAME = "yelp_academic_dataset.json"
USER = "user"
REVIEW = "review"
BUSINESS = "business"
USER_FILE = "users.json"
REVIEW_FILE = "review.json"
BUSINESS_FILE = "business.json"

def writeToFile(filename, objs):
	toWriteFile = open(filename)
	for obj in objs:
		toWriteFile.write(obj + "\n")
	toWriteFile.close()

users = set()
reviews = set()
businesses = set()
dataset = open(FILENAME)
for line in dataset:
	obj = dict(line)
	if obj['type'] == USER:
		users.add(json.dumps(obj))
	elif obj['type'] == REVIEW:
		reviews.add(json.dumps(obj))
	else obj['type'] == BUSINESS:
		businesses.add(json.dumps(obj))

writeToFile(USER_FILE, users)
writeToFile(REVIEW_FILE, reviews)
writeToFile(BUSINESS_FILE, businesses)