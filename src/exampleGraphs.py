import networkx as nx 
import matplotlib.pyplot as plt 

B = ["Pizza Place", "Steak Restaurant", "Ice Cream Parlor", "Sushi Restaurant", "Burger Joint"]
U = ["Sally", "Sid", "Kelly", "Andrew"]

G = nx.Graph()
G.add_nodes_from(B)
G.add_nodes_from(U)

G.add_edge(U[0], B[2])
G.add_edge(U[0], B[3])
G.add_edge(U[0], B[4])

G.add_edge(U[1], B[1])
G.add_edge(U[1], B[3])

G.add_edge(U[2], B[1])
G.add_edge(U[2], B[3])

G.add_edge(U[3], B[0])

pos = dict()
for i in range(len(B)):
	pos[B[i]] = (i*2, 5)
for i in range(len(U)):
	pos[U[i]] = ((i+1)*(8.0/5), 0)

nx.draw(G, pos)
plt.show()

Gproj = nx.Graph()
Gproj.add_nodes_from(U)
for u in U:
	for v in U:
		if v != u:
			Gproj.add_edge(u, v)

nx.draw(Gproj)
plt.show()
