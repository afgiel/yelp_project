import json 

REVIEW_FILE = "review.json"
BUSINESS_FILE = "business.json"
STANFORD_FILE = "stanfordEdges.txt"

stanfordBusinesses = set()
stanfordReviews = set()

businessFile = open(BUSINESS_FILE)
for line in businessFile:
	business = json.loads(line)
	if "University of Waterloo" in business['schools']: 
		stanfordBusinesses.add(business['business_id'])

reviewsFile = open(REVIEW_FILE)
for line in reviewsFile:
	review = json.loads(line)
	businessID = review['business_id'] 
	if businessID in stanfordBusinesses:
		reviewerID = review['user_id']
		stars = str(review['stars'])
		date = review['date']
		toAdd = ",".join([reviewerID, businessID, stars, date])
		stanfordReviews.add(toAdd)

print len(stanfordReviews)

"""
stanfordFile = open(STANFORD_FILE, "w")
for sR in stanfordReviews:
	stanfordFile.write(sR + "\n")
stanfordFile.close()
"""