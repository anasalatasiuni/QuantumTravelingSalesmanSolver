#!/usr/bin/env python
"""This program uses D-Wave's quantum annealing technology to solve the Traveling Salesman Problem (TSP).

The algorithm formulates the TSP as a Quadratic Unconstrained Binary Optimization (QUBO) problem 
and solves it using a hybrid quantum-classical solver. The output includes the path and cost of 
the solution found.

The program takes two inputs:
1. A file containing the pairwise costs as an adjacency matrix.
2. The output file where the solution (path and cost) will be written.

The program can be run like this:
$ python tsp_dwave.py problem.txt solution.txt
"""

from dwave_networkx import traveling_salesperson_qubo
import networkx as nx
from dwave.system import LeapHybridSampler
import sys
import numpy as np

__author__ = "Murhaf Alawir, Anas Alatasi"
__copyright__ = "Global1A1"
__credits__ = ["Murhaf Alawir, Anas Alatasi"]
__license__ = "Apache 2.0"
__version__ = "1.0.0"
__maintainer__ = "Murhaf Alawir"
__email__ = "m.alawir@innopolis.university"
__status__ = "Staging"


def score(M, X):
    """Calculates the total cost and path of a given solution.

    Args:
        M (np.array): The matrix of pairwise costs.
        X (np.array): The binary matrix representing the solution path.

    Returns:
        tuple: Total cost and the path as a list of nodes.
    """
    n, _ = M.shape
    cost = 0
    path = []

    # Find the first node in the path (assuming the path starts from node 0)
    current_node = 0

    for j in range(n):
        for i in range(n):
            if not X[i , j]:
                continue
            next_node = i
            path.append(next_node)
            cost += M[current_node, next_node]
            current_node = next_node

    # Add the cost to return to the starting node
    cost += M[current_node, path[0]]
    path.append(path[0])  # Completing the cycle by returning to the start

    return cost, path

def is_valid_solution(X):
    """Checks if a given solution is valid.

    A valid solution has exactly one outgoing edge from each node.

    Args:
        X (np.array): The binary matrix representing the solution path.

    Returns:
        bool: True if the solution is valid, False otherwise.
    """
    n, _ = X.shape
    for i in range(n):
        count = 0
        for j in range(n):
            if X[i, j] == 1:
                count += 1
        if count != 1:
            return False
    return True

def build_solution(sample, n):
    """Builds the solution matrix from the raw sample output.

    Args:
        sample (dict): The raw sample output from the QUBO solver.
        n (int): The dimension of the solution matrix.

    Returns:
        np.array: The binary matrix representing the solution path.
    """
    X = np.zeros((n, n))
    i = 0
    j = 0
    for x in sample:
        X[i, j] = x
        j += 1
        if j == n:
            j = 0
            i += 1
    return X

if __name__ == "__main__":
    in_file = sys.argv[1]
    out_file = sys.argv[2]
    num_samples = 1000

    # Load the cost matrix
    M0 = np.loadtxt(in_file)
    M = np.loadtxt(in_file)

    # Symmetrize the matrix
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            M[i, j] += M0[j, i]

    # Create a graph from the adjacency matrix
    G = nx.from_numpy_array(M)

    # Formulate the QUBO problem for TSP
    new_q = traveling_salesperson_qubo(G)

    # Solve the QUBO problem using the Leap Hybrid Sampler
    sampler = LeapHybridSampler()
    sampleset = sampler.sample_qubo(new_q, time_limit=3)

    # Extract the first solution
    first = sampleset.first

    # Problem ID for tracking
    problem_id = sampleset.info['problem_id']

    # Build the solution matrix
    e = first.sample.values()
    n = M.shape[0]
    X = build_solution(e, n)

    # Validate and score the solution
    if is_valid_solution(X):
        cost, path = score(M, X)
        with open(out_file, 'w') as f:
            f.write(f"{X}\n")
            f.write(f"Score: {cost}\n")
            f.write(f"Path: {path}\n")
