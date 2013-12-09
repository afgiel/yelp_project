import json
import os

FILENAME = "yelp_academic_dataset.json"
USER = "user"
REVIEW = "review"
BUSINESS = "business"
USER_FILE = "users.json"
REVIEW_FILE = "review.json"
BUSINESS_FILE = "business.json"

def writeToFile(filename, objs):
	toWriteFile = open(filename, "w")
	for obj in objs:
		toWriteFile.write(obj + "\n")
	toWriteFile.close()


# os.remove(USER_FILE)
# os.remove(REVIEW_FILE)
# os.remove(BUSINESS_FILE)
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