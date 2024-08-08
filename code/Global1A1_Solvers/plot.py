#!/usr/bin/env python
"""This script visualizes solutions to the Traveling Salesman Problem (TSP) using Matplotlib and NetworkX.

It provides functions to plot both the solution to the TSP and the original problem's adjacency matrix. 
The visualizations include node labels, edge weights, and are saved as PNG images.

The script requires NumPy, Matplotlib, and NetworkX to be installed. 

The functions can be used as follows:
1. `plot_solution(n, path, M)` - Plots the TSP solution.
2. `plot_problem(M)` - Plots the problem's adjacency matrix as a graph.
"""

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

__author__ = "Murhaf Alawir, Anas Alatasi"
__copyright__ = "Global1A1"
__credits__ = ["Murhaf Alawir", "Anas Alatasi"]
__license__ = "Apache 2.0"
__version__ = "1.0.0"
__maintainer__ = "Murhaf Alawir"
__email__ = "m.alawir@innopolis.university"
__status__ = "Staging"

def plot_solution(n, path, M):
    """Plots the solution to the Traveling Salesman Problem (TSP).

    Constructs a directed graph from the given path and adjacency matrix, and visualizes it using Matplotlib and NetworkX.
    The graph represents the optimal path found, with edge weights displayed.

    Args:
        n (int): The number of nodes in the graph.
        path (list): The sequence of nodes representing the solution path.
        M (np.array): The adjacency matrix representing the costs between nodes.

    Saves:
        solution.png: A visual representation of the TSP solution with node labels and edge weights.
    """
    adj_matrix = np.zeros((n, n), dtype='int')
    for i in range(len(path) - 1):
        adj_matrix[path[i]][path[i + 1]] = M[path[i]][path[i + 1]]

    G_latest = nx.from_numpy_array(adj_matrix, create_using=nx.DiGraph)
    nodes_pos = nx.kamada_kawai_layout(G_latest)

    scale_factor = 2
    pos_scaled = {
        node: (scale_factor * x if x < 4 else x, scale_factor * y if y < 4 else y)
        for node, (x, y) in nodes_pos.items()
    }
    # Extract edge weights for plotting
    edge_weights = nx.get_edge_attributes(G_latest, 'weight')

    plt.figure(figsize=(10, 10))
    nx.draw(G_latest, pos_scaled, with_labels=True, node_color='skyblue', node_size=2000, edge_color='gray', arrows=True, arrowsize=20)
    nx.draw_networkx_edge_labels(G_latest, pos_scaled, edge_labels=edge_weights, font_color='red')
    plt.title("Solution:")
    plt.savefig('solution.png', format='png', dpi=300)
    plt.show()

def plot_problem(M):
    """Plots the problem's adjacency matrix as a graph.

    Constructs a directed graph from the given adjacency matrix and visualizes it using Matplotlib and NetworkX.
    The graph represents the problem's cost structure with edge weights displayed.

    Args:
        M (np.array): The adjacency matrix representing the costs between nodes.

    Saves:
        problem.png: A visual representation of the problem's graph with node labels and edge weights.
    """
    M0 = np.array(M, dtype='int')
    G_latest = nx.from_numpy_array(M0, create_using=nx.DiGraph)
    nodes_pos = nx.spring_layout(G_latest)

    scale_factor = 3
    pos_scaled = {
        node: (scale_factor * x if x < 4 else x, scale_factor * y if y < 4 else y)
        for node, (x, y) in nodes_pos.items()
    }
    # Extract edge weights for plotting
    edge_weights = nx.get_edge_attributes(G_latest, 'weight')

    plt.figure(figsize=(10, 10))
    nx.draw(G_latest, pos_scaled, with_labels=True, node_color='skyblue', node_size=2000, edge_color='gray', arrows=True, arrowsize=20)
    nx.draw_networkx_edge_labels(G_latest, pos_scaled, edge_labels=edge_weights, font_color='red')
    plt.title("Problem:")
    plt.savefig('problem.png', format='png', dpi=300)
    plt.show()
