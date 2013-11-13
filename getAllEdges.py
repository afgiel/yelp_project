import json 

REVIEW_FILE = "review.json"
EDGES_FILE = "allEdges.txt"

edges = set()

print "## GETTING INFO FOR EDGES ##"
reviewsFile = open(REVIEW_FILE)
for line in reviewsFile:
	review = json.loads(line)
	businessID = review['business_id'] 
	reviewerID = review['user_id']
	stars = str(review['stars'])
	date = review['date']
	toAdd = ",".join([reviewerID, businessID, stars, date])
	edges.add(toAdd)

print "## WRITING OUT ALL EDGES ##"
edgesFile = open(EDGES_FILE, "w")
for edge in edges:
	edgesFile.write(edge + "\n")
edgesFile.close()