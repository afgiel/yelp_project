"""
######################################################################################
CUMULATIVE RATING PREDICTION EVALUATION- This file evaluates the rating prediction for
all the universities.
######################################################################################
"""

"""
######################################################################################
	IMPORTS
######################################################################################
"""
from Utils import getSchools
import matplotlib.pyplot as plt

"""
######################################################################################
	CONSTANTS
######################################################################################
"""
RATING_EVALUATED_PATH = "../data/rating_evaluated/"

"""
######################################################################################
	CODE
######################################################################################
"""
schools,acronyms = getSchools()

diffRatings = {}
diffRatings[0] = 0
diffRatings[1] = 0
diffRatings[2] = 0
diffRatings[3] = 0
diffRatings[4] = 0
diffRatings[5] = 0
for acronym in acronyms:
	predictedFile = open(RATING_EVALUATED_PATH + acronyms[acronym] + "_rating_eval.txt", "r")
	for line in predictedFile:
		r,n = line.split(",")
		rn = int(r)
		nn = int(n)
		diffRatings[rn] = diffRatings[rn] + nn

xaxis = []
yaxis = []
for x in diffRatings:
	xaxis.append(x)
	yaxis.append(diffRatings[x])

print diffRatings
sum = sum(yaxis)
prob = []
for x in diffRatings:
	prob.append((float(diffRatings[x])*100)/sum)

print prob

plt.figure(1)
ax = plt.subplot(111)
plt.ylabel('Number of Links')
plt.xlabel('Difference in Rating of Predicted and Actual Test Links')
plt.title('Distibution of difference in rating between predicted and actual test links')
ax.plot(xaxis,prob,marker = 'o',linestyle = '--')
plt.show()