import networkx as nx
from datetime import datetime
import matplotlib as plt
from collections import Counter

userAndReviews = {}
userAndTimeBetweenReviews = {}
userAndAverageTimeBetweenReviews = {}
stanfordData = open("stanfordEdges.txt").readlines()

for line in stanfordData:
  line = line.split(',')
  line[3] = datetime.strptime(line[3].rstrip(), "%Y-%m-%d") 
  if line[0] in userAndReviews:
    userAndReviews[line[0]].append(line[3])
  else:
    userAndReviews[line[0]] = [line[3]]

for item in userAndReviews.items():
  dateDifferenceList = []
  item[1].sort()
  if len(item[1]) > 1:
    for x in range(0, len(item[1]) - 1):
      dateDifferenceList.append(abs((item[1][x] - item[1][x+1]).days))
  else:
    #this means the user only made one review, so wait time is 0
    dateDifferenceList.append(0) 
  userAndTimeBetweenReviews[item[0]] = dateDifferenceList
  userAndAverageTimeBetweenReviews[item[0]] = sum(dateDifferenceList)/len(dateDifferenceList)

#averageWaitTimes includes 0's. A value of 0 means that the user only made one review
averageWaitTimes = userAndAverageTimeBetweenReviews.values()

#we omit 0's in averageNonZeroWaitTimes
averageNonZeroWaitTimes = [x for x in averageWaitTimes if x != 0]

#average wait time
averageWaitTime = sum(averageNonZeroWaitTimes)/len(averageNonZeroWaitTimes)

averageCounter = Counter(averageNonZeroWaitTimes)
xlist = averageCounter.keys()
ylist = averageCounter.values()
plt.plot(xlist, ylist, 'ro')
plt.title("Frequency of Average Wait Time Between Reviews") 
