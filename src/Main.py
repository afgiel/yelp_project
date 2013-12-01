"""
######################################################################################
MAIN - This is the main interface to perform link prediction
######################################################################################
"""

"""
######################################################################################
	PROGRAM PARAMETERS
######################################################################################
"""
# PROGRAM VERBOSITY
VERBOSE = True

# MODULES TO BE RUN
MODULE_GET_EDGES = False
MODULE_SPLIT_DATA = False
MODULE_PROJECTION_GRAPH = False
MODULE_WEIGHTED_PROJECTION_GRAPH = False
MODULE_INTERNAL_LINKS = False
MODULE_LINK_PREDICTION = False
MODULE_EVALUATION = False
MODULE_FIND_THRESHOLD = True

# SCHOOLS TO BE USED
ALL_SCHOOLS = False
SCHOOLS = ['University of Waterloo']

# TRAIN, VALIDATION AND TEST PERCENT
PERCENT_TRAIN = .5
PERCENT_VALIDATION = .1
PERCENT_TEST = .4

# THRESHOLD PARAMETERS
WEIGHT_THRESHOLD = 1
TOTAL_THRESHOLD = 1

"""
######################################################################################
	IMPORTS
######################################################################################
"""
import networkx as nx
from Utils import getSchools
from TrainAndTestDataGen import generateTrainAndTest
from ProjectionGraph import generateProjectionGraph
from WeightInduced import generateWeightedProjectionGraph
from InternalLinks import generateInternalLinks
from LinkPrediction import predictLinks
from SchoolEdges import getReviews
from Evaluation import evaluate
from FindThreshold import findThresholds

"""
######################################################################################
	PROGRAM
######################################################################################
"""
print "#############################################################"
print "## GET SCHOOL DATA ##\n"
schools,school_acronyms = getSchools()
if(VERBOSE):
	for school in schools:
		print school
print "#############################################################\n"

if(MODULE_GET_EDGES):
	print "#############################################################"
	print "## GETTING EDGE DATA ##\n"
	for school in schools:
		if(ALL_SCHOOLS or school in SCHOOLS):
			getReviews(school_acronyms[school],school,VERBOSE)
	print "#############################################################\n"

if(MODULE_SPLIT_DATA):
	print "#############################################################"
	print "## SPLITTING TRAIN AND TEST DATA ##\n"
	for school in schools:
		if(ALL_SCHOOLS or school in SCHOOLS):
			generateTrainAndTest(school_acronyms[school],PERCENT_TRAIN,PERCENT_VALIDATION,PERCENT_TEST,VERBOSE)
	print "#############################################################\n"

if(MODULE_PROJECTION_GRAPH):
	print "#############################################################"
	print "## GENERATING PROJECTION GRAPHS ##\n"
	for school in schools:
		if(ALL_SCHOOLS or school in SCHOOLS):
			generateProjectionGraph(school_acronyms[school],VERBOSE)
	print "#############################################################\n"

if(MODULE_WEIGHTED_PROJECTION_GRAPH):
	print "#############################################################"
	print "## GENERATING WEIGHTED PROJECTION GRAPHS ##\n"
	for school in schools:
		if(ALL_SCHOOLS or school in SCHOOLS):
			generateWeightedProjectionGraph(school_acronyms[school],VERBOSE)
	print "#############################################################\n"

if(MODULE_INTERNAL_LINKS):
	print "#############################################################"
	print "## GENERATING INTERNAL LINKS ##\n"
	for school in schools:
		if(ALL_SCHOOLS or school in SCHOOLS):
			generateInternalLinks(school_acronyms[school],VERBOSE)
	print "#############################################################\n"

if(MODULE_FIND_THRESHOLD):
	print "#############################################################"
	print "## FINDING THRESHOLDS ##\n"
	for school in schools:
		if(ALL_SCHOOLS or school in SCHOOLS):
			findThresholds(school_acronyms[school],VERBOSE)
	print "#############################################################\n"
else:
	if(MODULE_LINK_PREDICTION):
		print "#############################################################"
		print "## PREDICTING LINKS ##\n"
		for school in schools:
			if(ALL_SCHOOLS or school in SCHOOLS):
				predictLinks(school_acronyms[school],VERBOSE,WEIGHT_THRESHOLD,TOTAL_THRESHOLD)
		print "#############################################################\n"
		
	if(MODULE_EVALUATION):
		print "#############################################################"
		print "## EVALUATING ##\n"
		for school in schools:
			if(ALL_SCHOOLS or school in SCHOOLS):
				evaluate(school_acronyms[school],VERBOSE)
		print "#############################################################\n"
