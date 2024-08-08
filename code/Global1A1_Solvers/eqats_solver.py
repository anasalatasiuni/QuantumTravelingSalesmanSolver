#!/usr/bin/env python
"""This program solves the Traveling Salesman Problem (TSP) using D-Wave's quantum annealing and hybrid quantum-classical solvers.

The algorithm formulates the TSP as a Quadratic Unconstrained Binary Optimization (QUBO) problem. 
It can be solved using either a quantum annealer or a hybrid quantum-classical approach. The solution 
includes the optimal path, energy, and other relevant metrics.

The program takes two inputs:
1. A file containing the pairwise costs as an adjacency matrix.
2. The output file where the solution (path, cost, energy) will be written.

The program can be run like this:
$ python tsp_dwave.py problem.txt solution.txt
"""

import sys
from dwave.system.composites import EmbeddingComposite
from dwave.system import DWaveSampler, LeapHybridSampler
import dwave.inspector
import numpy as np
from plot import plot_problem, plot_solution

__author__ = "Murhaf Alawir, Anas Alatasi, Hadi Salloum"
__copyright__ = "Global1A1"
__credits__ = ["Murhaf Alawir, Anas Alatasi, Hadi Salloum"]
__license__ = "Apache 2.0"
__version__ = "1.0.0"
__maintainer__ = "Murhaf Alawir"
__email__ = "m.alawir@innopolis.university"
__status__ = "Staging"

# Input and output file arguments
in_file = sys.argv[1]
out_file = sys.argv[2]
num_samples = 1000

# Load the cost matrix and symmetrize it
M0 = np.loadtxt(in_file)
M = np.loadtxt(in_file)
for i in range(M.shape[0]):
    for j in range(M.shape[1]):
        M[i, j] += M0[j, i]

# Lambda is a scaling factor for the QUBO matrix
_lambda = np.max(np.abs(M)) * 2

def build_objective_matrix():
    """Builds the QUBO objective matrix for the TSP problem.
    
    Constructs the QUBO matrix that represents the TSP as a quadratic optimization problem,
    incorporating penalties for invalid solutions and costs for edges between cities.
    
    Returns:
        np.array: The QUBO matrix used for solving the TSP.
    """
    n, _ = M.shape
    n = n - 1
    m = int(n * n)
    Q = np.zeros((m, m))

    for i in range(m):
        Q[i, i] = 2 * -_lambda
        city_i = i // n + 1
        pos_i = i % n

        if pos_i == 0 or pos_i == n - 1:
            Q[i, i] += M[city_i, 0]

        k = i + 1
        while k % n != 0:
            Q[i, k] = 2 * _lambda
            if pos_i == 0 or pos_i == n - 1:
                Q[i, k] += M[city_i, 0]
            k += 1

    for i in range(m):
        for j in range(i + 1, m):
            city_i = i // n + 1
            pos_i = i % n
            city_j = j // n + 1
            pos_j = j % n

            if city_i == city_j:
                continue
            elif pos_i == pos_j - 1 or pos_i == pos_j + 1:
                Q[i, j] = M[city_i, city_j]
            elif pos_i == pos_j:
                Q[i, j] = 2 * _lambda

    return Q

Q = build_objective_matrix()

def is_valid_solution(X):
    """Checks if a given solution matrix is valid for TSP.
    
    Verifies that each city in the solution matrix is visited exactly once and each row 
    of the matrix contains exactly one '1', indicating that each city has exactly one outgoing edge.
    
    Args:
        X (np.array): The binary matrix representing the solution path.
    
    Returns:
        bool: True if the solution matrix is valid, False otherwise.
    """
    n, _ = X.shape
    for i in range(n):
        if np.sum(X[i, :]) != 1:
            return False
    return True

def build_solution(sample):
    """Builds the solution matrix from a QUBO sample.
    
    Converts a binary sample obtained from the QUBO solver into a solution matrix representing 
    the order of the Traveling Salesman Problem (TSP).
    
    Args:
        sample (list): The binary sample obtained from the QUBO solver.
    
    Returns:
        np.array: The solution matrix of size n*n 
        where each 'X[i][j]=1' indicates city i is visited at time j.
    """
    n, _ = M.shape
    m = len(sample)
    assert m == int((n - 1) * (n - 1))
    X = np.zeros((n, n))
    k = 0
    X[0, 0] = 1
    for i in range(1, n):
        for j in range(1, n):
            X[i, j] = sample[k]
            k += 1
    return X

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


def qbu_solve(best_energy):
    """Solves the QUBO problem using D-Wave's quantum annealer.
    
    Uses D-Wave's quantum annealing solver to sample solutions from the QUBO problem, 
    evaluates their validity, and updates the best solution found so far. The result is 
    written to an output file if a better solution is found.
    
    Args:
        best_energy (float): The best energy (cost) found so far.
    
    Returns:
        float: The updated best energy after solving.
    """
    plot_problem(M)
    sampler = EmbeddingComposite(DWaveSampler())
    sampleset = sampler.sample_qubo(Q, num_reads=num_samples)
    dwave.inspector.show(sampleset)
    problem_id = sampleset.info['problem_id']

    for e in sampleset.data(sorted_by='energy'):
        sample = e.sample
        energy = e.energy

        if best_energy <= energy:
            return best_energy

        X = build_solution(sample)
        if is_valid_solution(X):
            best_energy = energy
            cost, path = score(M, X)
            plot_solution(M.shape[0], path, M)
            with open(out_file, 'w') as f:
                f.write(f"Problem Id: {problem_id}\n")
                f.write(f"Solution:\n{X}\n")
                f.write(f"Score: {cost}\n")
                f.write(f"{sample}\n")
                f.write(f"Energy: {energy}\n")
                f.write(f"Chain break fraction: {e.chain_break_fraction}\n")
            break

    return best_energy

def hybrid_solve(best_energy):
    """Solves the QUBO problem using D-Wave's hybrid quantum-classical solver.
    
    Uses D-Wave's hybrid quantum-classical solver to sample solutions from the QUBO problem, 
    evaluates their validity, and updates the best solution found so far. Additionally, plots 
    the problem and solution, and writes the results to an output file.
    
    Args:
        best_energy (float): The best energy (cost) found so far.
    
    Returns:
        float: The updated best energy after solving.
    """
    plot_problem(M)
    sampler = LeapHybridSampler()
    sampleset = sampler.sample_qubo(Q, time_limit=3)
    problem_id = sampleset.info['problem_id']

    for e in sampleset.data(sorted_by='energy'):
        sample = e.sample
        energy = e.energy

        if best_energy <= energy:
            return best_energy

        X = build_solution(sample)
        if is_valid_solution(X):
            best_energy = energy
            cost, path = score(M, X)
            plot_solution(M.shape[0], path, M)
            with open(out_file, 'w') as f:
                f.write(f"Problem Id: {problem_id}\n")
                f.write(f"Solution:\n{X}\n")
                f.write(f"Score: {cost}\n")
                f.write(f"{sample}\n")
                f.write(f"Energy: {energy}\n")
            break

    return best_energy

best_energy = 1e9
for _ in range(1):
    best_energy = hybrid_solve(best_energy)
