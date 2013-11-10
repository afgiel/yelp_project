import networkx as nx

fileName = ("stanfordEdges.txt")
G1 = nx.read_edgelist(fileName, delimiter=',', data=(('rating',int),('date',str)))
