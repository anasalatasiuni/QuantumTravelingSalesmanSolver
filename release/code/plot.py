import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

latest_adj_matrix = np.array(
[[0, 0, 1, 0, 0, 0, 0, 0,],
 [0, 0, 0, 0, 1, 0, 0, 0,],
 [0, 0, 0, 1, 0, 0, 0, 0,],
 [0, 0, 0, 0, 0, 0, 1, 0,],
 [0, 0, 0, 0, 0, 1, 0, 0,],
 [1, 0, 0, 0, 0, 0, 0, 0,],
 [0, 1, 0, 0, 0, 0, 0, 0,],
 [0, 0, 0, 0, 0, 0, 0, 1,],])

# Create a directed graph from the latest adjacency matrix
G_latest = nx.from_numpy_array(latest_adj_matrix, create_using=nx.DiGraph)

# Draw the graph
plt.figure(figsize=(8, 8))
pos = nx.spring_layout(G_latest)
nx.draw(G_latest, pos, with_labels=True, node_color='lightblue', node_size=2000, edge_color='gray', arrowsize=20)
plt.title("Graph Representation from Latest Adjacency Matrix")
plt.show()